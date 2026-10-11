#!/usr/bin/env python3
"""Bundle rules, one procedure and chosen notes into one file (pack.md) for chat tools
without file access. Standard library only; no AI involved.

Usage:
  python tools/pack.py BUNDLE_DIR -k addition bias --skill answer
  python tools/pack.py BUNDLE_DIR -f 10_Concepts/a.md 40_Sources/b.md --skill answer -o pack.md

Notes are chosen by keyword score (title counts triple) or by explicit file list.
Notes are copied verbatim; nothing is shortened or rephrased.
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LIMIT = 30000
NOTE_FOLDERS = ("10_Concepts", "40_Sources", "70_Tools", "00_Inbox")

PREAMBLE = """# Knowledge pack

You are working with the rules, one procedure and a selection of notes below. Follow the rules in AGENTS.md.
Answer only from the notes in this pack. Name the note path for every statement (for example `/10_Concepts/x.md`).
If the notes do not cover something, say «not in the notes». Do not present general knowledge as a finding.
"""


def read(path):
    return Path(path).read_text(encoding="utf-8")


def candidates(bundle):
    for folder in NOTE_FOLDERS:
        base = bundle / folder
        if base.is_dir():
            yield from sorted(base.rglob("*.md"))


def score(text, terms):
    low = text.lower()
    title = next((l for l in text.splitlines() if l.startswith("# ")), "").lower()
    return sum(low.count(t) + 2 * title.count(t) for t in terms)


def select(bundle, keywords, files, max_notes):
    if files:
        chosen = []
        for f in files:
            p = (bundle / f.lstrip("/"))
            if not p.is_file():
                raise SystemExit(f"error: note not found: {f}")
            chosen.append(p)
        return chosen
    terms = [t.lower() for k in keywords for t in re.split(r"\W+", k) if len(t) >= 3]
    if not terms:
        raise SystemExit("error: give keywords (-k) or files (-f)")
    scored = [(score(read(p), terms), p) for p in candidates(bundle)]
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda s: (-s[0], str(s[1])))
    return [p for _, p in scored[:max_notes]]


def build(bundle, notes, skill):
    parts = [PREAMBLE, "\n## Rules (AGENTS.md)\n\n", read(REPO / "AGENTS.md")]
    perspective = bundle / "perspective.md"
    if perspective.is_file():
        parts += ["\n\n## Perspective of this bundle\n\n", read(perspective)]
    if skill:
        sk = REPO / "skills" / skill / "SKILL.md"
        if not sk.is_file():
            raise SystemExit(f"error: skill not found: {skill}")
        parts += [f"\n\n## Procedure: {skill}\n\n", read(sk)]
    parts.append("\n\n## Notes\n")
    for p in notes:
        rel = "/" + p.relative_to(bundle).as_posix()
        parts += [f"\n### {rel}\n\n", read(p).rstrip(), "\n"]
    return "".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundle", help="bundle directory")
    ap.add_argument("-k", "--keywords", nargs="*", default=[], help="keywords or a question")
    ap.add_argument("-f", "--files", nargs="*", default=[], help="notes relative to the bundle")
    ap.add_argument("-s", "--skill", default=None, help="procedure to include (e.g. answer)")
    ap.add_argument("-n", "--max-notes", type=int, default=6)
    ap.add_argument("-o", "--out", default="pack.md")
    args = ap.parse_args(argv)
    bundle = Path(args.bundle)
    if not bundle.is_dir():
        raise SystemExit(f"error: bundle not found: {bundle}")
    notes = select(bundle, args.keywords, args.files, args.max_notes)
    if not notes:
        raise SystemExit("error: no note matches the keywords")
    text = build(bundle, notes, args.skill)
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
