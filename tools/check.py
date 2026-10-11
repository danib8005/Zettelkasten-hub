#!/usr/bin/env python3
"""Structure check for a Zettelkasten-Hub bundle. Standard library only.

Usage:
  python tools/check.py BUNDLE_DIR [--example]   check the notes of one bundle
  python tools/check.py --i18n [REPO_DIR]        check German translations of system documents

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


def note_files(bundle, config):
    for folder in config["note_folders"]:
        base = bundle / folder
        if base.is_dir():
            yield from sorted(base.rglob("*.md"))


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
            if line.lstrip().startswith(">") and not (ntype == "Gedanke" and section == "rohidee"):
                report.add(rel, n, "ERROR", "blockquote in example (only the Rohidee section of thought notes may quote)")
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None, help="bundle directory (or repo directory with --i18n)")
    ap.add_argument("--example", action="store_true", help="publishing rules for example bundles")
    ap.add_argument("--i18n", action="store_true", help="check German translations of system documents")
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
