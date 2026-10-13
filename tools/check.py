#!/usr/bin/env python3
"""Structure check for a Zettelkasten-Hub bundle. Standard library only.

Usage:
  python tools/check.py BUNDLE_DIR [--example]   check the notes of one bundle
  python tools/check.py --i18n [REPO_DIR]        repo check: German translations of system documents,
                                                 agents, their skills and their tool adapters

Output: one finding per line, "path:line: LEVEL message". Exit code 1 if any ERROR.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("check_config.json")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
WIKI_RE = re.compile(r"\[\[[^\]]+\]\]")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
SOURCE_NAME_RE = re.compile(r"^[a-z0-9-]+-\d{4}-[a-z0-9-]+\.md$")
LOC_RE = re.compile(r"\bLoc\.\s?\d|\bS\.\s?\d")
PUBLIC_VALUES = {"öffentlich", "public"}
THOUGHT_TYPES = {"gedanke", "thought"}
RAW_IDEA_SECTIONS = {"rohidee", "raw idea"}
BUNDLE_FOLDERS = {"00_Inbox", "10_Concepts", "20_Frameworks", "30_Syntheses", "40_Sources",
                  "50_Open-Questions", "70_Tools", "95_System"}
AGENT_FIELDS = ("type", "name", "description", "phase", "skills", "reads", "writes")
AGENT_SECTIONS = ("Role", "Goal and when to use", "Reads", "Writes", "Skills",
                  "Phase rules", "Handoff", "Final check")
ADAPTERS = ((".github/agents", "{}.agent.md"), (".claude/agents", "{}.md"))


def load_config():
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"note_folders": ["10_Concepts", "40_Sources", "70_Tools"],
                "example_open_links": [], "i18n_required": []}


def parse_frontmatter(lines):
    """Return (dict, index of first body line). Empty dict if no frontmatter."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    data = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return data, i + 1
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", lines[i])
        if m:
            value = re.sub(r"\s+#.*$", "", m.group(2)).strip()
            data[m.group(1)] = value
    return {}, 0


class Report:
    def __init__(self):
        self.items = []

    def add(self, path, line, level, msg):
        self.items.append((str(path), line, level, msg))

    @property
    def errors(self):
        return [i for i in self.items if i[2] == "ERROR"]

    def print(self):
        for path, line, level, msg in self.items:
            loc = f"{path}:{line}" if line else str(path)
            print(f"{loc}: {level} {msg}")


RESERVED = {"index.md", "log.md"}  # OKF reserved file names: not concept documents


def note_files(bundle, config):
    for folder in config["note_folders"]:
        base = bundle / folder
        if base.is_dir():
            yield from sorted(base.rglob("*.md"))


def check_okf_conformance(bundle, config, report):
    """OKF v0.2 section 11: every non-reserved .md has frontmatter with a non-empty `type`."""
    notes = set(note_files(bundle, config))
    for path in sorted(bundle.rglob("*.md")):
        if path.name in RESERVED or path in notes:
            continue  # notes get the same check in check_note
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8").splitlines())
        if not fm.get("type"):
            report.add(path.relative_to(bundle), 1, "ERROR",
                       "missing frontmatter with non-empty `type:` (OKF conformance)")


def check_note(path, bundle, report, config, example):
    rel = path.relative_to(bundle)
    lines = path.read_text(encoding="utf-8").splitlines()
    fm, body_start = parse_frontmatter(lines)
    ntype = fm.get("type", "")

    if not ntype:
        report.add(rel, 1, "ERROR", "missing `type:` in frontmatter")
    if not NAME_RE.match(path.name):
        report.add(rel, 0, "ERROR", "file name must be lowercase-with-hyphens.md without umlauts")
    elif ntype == "Source" and not SOURCE_NAME_RE.match(path.name):
        report.add(rel, 0, "WARN", "source note name should be lastname-year-shorttitle.md")
    if not any(re.search(r"review[- ]status", l, re.I) for l in lines):
        report.add(rel, 0, "ERROR", "missing review status")

    section = ""
    open_allowed = set(config.get("example_open_links", []))
    for n, line in enumerate(lines, 1):
        if n <= body_start:
            continue
        if line.startswith("#"):
            section = line.lstrip("#").strip().lower()
        if WIKI_RE.search(line):
            report.add(rel, n, "ERROR", "wikilink; use [Title](/folder/file.md)")
        for _, target in LINK_RE.findall(line):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            target_path = target.split("#")[0]
            if not target_path.startswith("/"):
                report.add(rel, n, "ERROR", f"link `{target}` is not bundle-relative (start with /)")
                continue
            if not target_path.endswith(".md") or ".." in target_path.split("/"):
                report.add(rel, n, "ERROR", f"link `{target}` is not a bundle note path")
                continue
            if (bundle / target_path.lstrip("/")).is_file():
                continue
            stem = Path(target_path).stem
            if example and stem not in open_allowed:
                report.add(rel, n, "ERROR", f"link to `{target}` leaves the example (not in allowed open links)")
            elif not example:
                report.add(rel, n, "WARN", f"open link: `{target}` does not exist yet")
        if example:
            raw_idea = ntype.lower() in THOUGHT_TYPES and section in RAW_IDEA_SECTIONS
            if line.lstrip().startswith(">") and not raw_idea:
                report.add(rel, n, "ERROR", "blockquote in example (only the raw-idea section of thought notes may quote)")
            if LOC_RE.search(line):
                report.add(rel, n, "ERROR", "location/page reference (Loc./S.) in example")
    if example and fm.get("visibility", "").lower() not in PUBLIC_VALUES:
        report.add(rel, 1, "ERROR", "example notes need `visibility: öffentlich` (or public)")


def check_bundle(bundle, example, report):
    config = load_config()
    if not bundle.is_dir():
        report.add(bundle, 0, "ERROR", "bundle directory not found")
        return
    for path in note_files(bundle, config):
        check_note(path, bundle, report, config, example)
    check_okf_conformance(bundle, config, report)


def check_i18n(repo, report):
    config = load_config()
    de_files = [p for p in repo.rglob("*.md")
                if ("de" in p.relative_to(repo).parts[:1] or p.name.endswith(".de.md"))
                and "_input" not in p.relative_to(repo).parts]
    translated = set()
    for p in sorted(de_files):
        rel = p.relative_to(repo)
        fm, _ = parse_frontmatter(p.read_text(encoding="utf-8").splitlines())
        src = fm.get("translation_of")
        if not src:
            report.add(rel, 1, "ERROR", "German file needs `translation_of:` in its header")
            continue
        translated.add(src)
        if not (repo / src).is_file():
            report.add(rel, 1, "ERROR", f"translation_of target `{src}` does not exist")
    for req in config.get("i18n_required", []):
        if (repo / req).is_file() and req not in translated:
            report.add(req, 0, "ERROR", "no German translation (expected a file with translation_of: " + req + ")")
    check_agents(repo, report)


def as_list(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [v.strip() for v in value[1:-1].split(",") if v.strip()]
    return [value] if value else []


def check_agents(repo, report):
    """Agents in agents/: frontmatter, sections, skills, write scope, and one adapter per tool."""
    agent_dir = repo / "agents"
    if not agent_dir.is_dir():
        return
    names, used_skills = set(), set()
    for path in sorted(agent_dir.glob("*.md")):
        rel = path.relative_to(repo).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        fm, _ = parse_frontmatter(lines)
        for field in AGENT_FIELDS:
            if field not in fm or (field != "writes" and not fm[field]):
                report.add(rel, 1, "ERROR", f"agent frontmatter needs `{field}:`")
        if fm.get("type") and fm["type"] != "Agent":
            report.add(rel, 1, "ERROR", "agent `type:` must be Agent")
        name = fm.get("name", "")
        if name and name != path.stem:
            report.add(rel, 1, "ERROR", f"agent `name: {name}` must match the file name")
        names.add(path.stem)
        if fm.get("phase") and not re.fullmatch(r"[1-5]", fm["phase"]):
            report.add(rel, 1, "ERROR", "agent `phase:` must be a number from 1 to 5")
        for skill in as_list(fm.get("skills", "")):
            used_skills.add(skill)
            if not (repo / "skills" / skill / "SKILL.md").is_file():
                report.add(rel, 1, "ERROR", f"skill `{skill}` not found (skills/{skill}/SKILL.md)")
        for folder in as_list(fm.get("writes", "")):
            if folder not in BUNDLE_FOLDERS:
                report.add(rel, 1, "ERROR", f"`writes:` folder `{folder}` is not a bundle folder")
        headings = {l[3:].strip() for l in lines if l.startswith("## ")}
        for title in AGENT_SECTIONS:
            if title not in headings:
                report.add(rel, 0, "ERROR", f"agent section `## {title}` missing")
    for folder, pattern in ADAPTERS:
        for name in sorted(names):
            if not (repo / folder / pattern.format(name)).is_file():
                report.add(f"{folder}/{pattern.format(name)}", 0, "ERROR",
                           f"adapter missing for agent `{name}`")
        base = repo / folder
        suffix = pattern.format("")
        for path in sorted(base.glob("*.md")) if base.is_dir() else []:
            stem = path.name[: -len(suffix)] if path.name.endswith(suffix) else path.stem
            if stem not in names:
                report.add(f"{folder}/{path.name}", 0, "ERROR", "adapter without an agent in agents/")
    skills_dir = repo / "skills"
    for path in sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []:
        if path.parent.name not in used_skills:
            report.add(path.relative_to(repo).as_posix(), 0, "WARN", "skill is not used by any agent")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None, help="bundle directory (or repo directory with --i18n)")
    ap.add_argument("--example", action="store_true", help="publishing rules for example bundles")
    ap.add_argument("--i18n", action="store_true", help="repo check: German translations, agents, skills, adapters")
    args = ap.parse_args(argv)
    report = Report()
    if args.i18n:
        check_i18n(Path(args.path or "."), report)
    else:
        if not args.path:
            ap.error("BUNDLE_DIR is required")
        check_bundle(Path(args.path), args.example, report)
    report.print()
    n_err, n_warn = len(report.errors), len(report.items) - len(report.errors)
    print(f"{n_err} error(s), {n_warn} warning(s)")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
