#!/usr/bin/env python3
"""Bundle rules, one agent (or one procedure) and chosen notes into one file (pack.md) for chat
tools without file access. Standard library only; no AI involved.

Usage:
  python tools/pack.py BUNDLE_DIR -k addition bias --agent answer
  python tools/pack.py BUNDLE_DIR -k addition bias --skill answer-from-notes
  python tools/pack.py BUNDLE_DIR -f 10_Concepts/a.md 40_Sources/b.md --skill answer-from-notes -o pack.md

With --agent the file holds: rules (AGENTS.md) → agent file → its skills → perspective → notes →
the agent's final check again at the end. Notes are then chosen only from the agent's `reads:` folders.
Notes are chosen by keyword score (title counts triple) or by explicit file list.
By default notes are copied verbatim. Optional mechanical reductions, never rephrasing:
  --visibility team public   only notes with these visibility values (default: public only;
                             a note without `visibility:` counts as private)
  --include-private          also pack private notes (you take responsibility for the upload)
  --strip-quotes             drop blockquote lines and parenthetical Loc./S. references
  --sections "Core idea" ... keep only the title and the listed `##` sections
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LIMIT = 30000
NOTE_FOLDERS = ("10_Concepts", "40_Sources", "70_Tools", "00_Inbox")

PREAMBLE = """# Knowledge pack

You are working with the rules, one agent or procedure and a selection of notes below. Follow the rules in AGENTS.md.
Answer only from the notes in this pack. Name the note path for every statement (for example `/10_Concepts/x.md`).
If the notes do not cover something, say «not in the notes». Do not present general knowledge as a finding.
"""


def read(path):
    return Path(path).read_text(encoding="utf-8")


def frontmatter(text):
    """Simple `key: value` frontmatter; `[a, b]` values become lists."""
    lines = text.splitlines()
    data = {}
    if not lines or lines[0].strip() != "---":
        return data
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if m:
            value = m.group(2)
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
            data[m.group(1)] = value
    return data


def section(text, title):
    """The `## title` section of a Markdown text, heading included; empty if missing."""
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip().lower() == title.lower()
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def load_agent(name):
    path = REPO / "agents" / f"{name}.md"
    if not path.is_file():
        raise SystemExit(f"error: agent not found: {name}")
    text = read(path)
    fm = frontmatter(text)
    skills = fm.get("skills") or []
    folders = [r for r in fm.get("reads") or [] if not r.endswith(".md")]
    return text, (skills if isinstance(skills, list) else [skills]), folders


VISIBILITY_ALIASES = {"öffentlich": "public", "privat": "private"}
LOC_PAREN_RE = re.compile(r"\s*\([^()]*\b(?:Loc\.|S\.)\s?\d[^()]*\)")


def visibility_of(text):
    """`visibility:` value from the frontmatter, normalised; private if missing."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            m = re.match(r"^visibility:\s*([^\s#]+)", line)
            if m:
                v = m.group(1).lower()
                return VISIBILITY_ALIASES.get(v, v)
    return "private"


def strip_quotes(text):
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith(">"):
            continue
        out.append(LOC_PAREN_RE.sub("", line))
    return "\n".join(out)


def keep_sections(text, wanted):
    """Keep the frontmatter-free title line and the listed `##` sections (case-insensitive)."""
    wanted = {w.lower() for w in wanted}
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]
    out, keep = [], False
    for line in lines:
        if line.startswith("# "):
            out.append(line)
        elif line.startswith("## "):
            keep = line[3:].strip().lower() in wanted
            if keep:
                out.append(line)
        elif keep:
            out.append(line)
    return "\n".join(out)


def candidates(bundle, folders=NOTE_FOLDERS):
    for folder in folders:
        base = bundle / folder
        if base.is_dir():
            yield from sorted(base.rglob("*.md"))


def score(text, terms):
    low = text.lower()
    title = next((l for l in text.splitlines() if l.startswith("# ")), "").lower()
    return sum(low.count(t) + 2 * title.count(t) for t in terms)


def allowed(path, visibilities):
    return visibilities is None or visibility_of(read(path)) in visibilities


def select(bundle, keywords, files, max_notes, visibilities=None, folders=NOTE_FOLDERS):
    if files:
        chosen = []
        for f in files:
            p = (bundle / f.lstrip("/"))
            if not p.is_file():
                raise SystemExit(f"error: note not found: {f}")
            if not allowed(p, visibilities):
                raise SystemExit(f"error: {f} is not {'/'.join(sorted(visibilities))}; "
                                 "set its visibility or pass --include-private")
            chosen.append(p)
        return chosen
    terms = [t.lower() for k in keywords for t in re.split(r"\W+", k) if len(t) >= 3]
    if not terms:
        raise SystemExit("error: give keywords (-k) or files (-f)")
    scored = [(score(read(p), terms), p) for p in candidates(bundle, folders) if allowed(p, visibilities)]
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda s: (-s[0], str(s[1])))
    return [p for _, p in scored[:max_notes]]


def render_note(path, strip, sections):
    text = read(path)
    if sections:
        text = keep_sections(text, sections)
    if strip:
        text = strip_quotes(text)
    return text


def skill_text(name):
    sk = REPO / "skills" / name / "SKILL.md"
    if not sk.is_file():
        raise SystemExit(f"error: skill not found: {name}")
    return read(sk)


def build(bundle, notes, skill=None, strip=False, sections=None, agent=None):
    parts = [PREAMBLE, "\n## Rules (AGENTS.md)\n\n", read(REPO / "AGENTS.md")]
    final_check = ""
    if agent:
        text, skills, _ = load_agent(agent)
        parts += [f"\n\n## Agent: {agent}\n\n", text]
        for name in skills:
            parts += [f"\n\n## Procedure: {name}\n\n", skill_text(name)]
        final_check = section(text, "Final check")
    perspective = bundle / "perspective.md"
    if perspective.is_file():
        parts += ["\n\n## Perspective of this bundle\n\n", read(perspective)]
    if skill:
        parts += [f"\n\n## Procedure: {skill}\n\n", skill_text(skill)]
    parts.append("\n\n## Notes\n")
    for p in notes:
        rel = "/" + p.relative_to(bundle).as_posix()
        parts += [f"\n### {rel}\n\n", render_note(p, strip, sections).rstrip(), "\n"]
    if final_check:
        parts += [f"\n\n## Before you answer: final check of agent {agent}\n\n",
                  final_check.split("\n", 1)[-1].strip(), "\n"]
    return "".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundle", help="bundle directory")
    ap.add_argument("-k", "--keywords", nargs="*", default=[], help="keywords or a question")
    ap.add_argument("-f", "--files", nargs="*", default=[], help="notes relative to the bundle")
    who = ap.add_mutually_exclusive_group()
    who.add_argument("-a", "--agent", default=None, help="agent to include with its skills (e.g. answer)")
    who.add_argument("-s", "--skill", default=None, help="single procedure to include (e.g. answer-from-notes)")
    ap.add_argument("-n", "--max-notes", type=int, default=6)
    ap.add_argument("--visibility", nargs="*", default=["public"], help="allowed visibility values (default: public)")
    ap.add_argument("--include-private", action="store_true", help="do not filter by visibility")
    ap.add_argument("--strip-quotes", action="store_true", help="drop blockquotes and Loc./S. references")
    ap.add_argument("--sections", nargs="*", default=None, help="keep only these ## sections")
    ap.add_argument("-o", "--out", default="pack.md")
    args = ap.parse_args(argv)
    bundle = Path(args.bundle)
    if not bundle.is_dir():
        raise SystemExit(f"error: bundle not found: {bundle}")
    vis = None if args.include_private else {VISIBILITY_ALIASES.get(v.lower(), v.lower()) for v in args.visibility}
    folders = load_agent(args.agent)[2] if args.agent else NOTE_FOLDERS
    notes = select(bundle, args.keywords, args.files, args.max_notes, vis, folders)
    if not notes:
        raise SystemExit("error: no note matches the keywords (and the visibility filter)")
    text = build(bundle, notes, args.skill, args.strip_quotes, args.sections, args.agent)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"{args.out}: {len(text)} characters, {len(notes)} note(s)")
    for p in notes:
        print("  /" + p.relative_to(bundle).as_posix())
    if len(text) > LIMIT:
        print(f"WARNING: {len(text)} characters exceeds {LIMIT}; many chat tools truncate or reject this. "
              "Use fewer notes (-n) or a more specific query.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
