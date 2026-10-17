#!/usr/bin/env python3
"""Convert wikilinks [[target]] to standard bundle-relative Markdown links. Standard library only.

Usage:
  python tools/migrate_links.py BUNDLE_DIR                 dry run: report only, nothing is written
  python tools/migrate_links.py BUNDLE_DIR --apply         write the changes
  python tools/migrate_links.py BUNDLE_DIR --report FILE   also write the full report as Markdown

A wikilink [[target]], [[target|label]] or [[target#anchor]] becomes [Title](/folder/target.md).
Title is the first "# " heading of the target note. The target is found by file name, by a
slugified spelling (umlauts ae/oe/ue, lowercase, hyphens) or by `aliases:`.
Not changed, only reported: links to notes that do not exist yet, and names that match several notes.
With --missing-to FOLDER, links to missing notes become [name](/FOLDER/name.md): allowed as a to-do list.
Wikilinks inside fenced code blocks and inline code are left alone.
--apply refuses to run on a git working tree with uncommitted changes (use --allow-dirty to override).
"""
import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402  (reuses folder list and frontmatter parser)

WIKI = re.compile(r"(?<!!)\[\[([^\]|#]+?)(?:#([^\]|]*))?(?:\|([^\]]*))?\]\]")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
UMLAUTS = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss"})


def slug(text):
    text = text.translate(UMLAUTS).lower()
    text = re.sub(r"\.md$", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_aliases(lines):
    """Aliases from frontmatter: inline list [a, b] or a block list under `aliases:`."""
    if not lines or lines[0].strip() != "---":
        return []
    out, in_block = [], False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^aliases:\s*(.*)$", line)
        if m:
            value = m.group(1).strip()
            in_block = not value
            if value.startswith("["):
                out += [a.strip().strip("'\"") for a in value.strip("[]").split(",") if a.strip()]
            elif value:
                out.append(value.strip("'\""))
            continue
        if in_block:
            item = re.match(r"^\s*-\s+(.*)$", line)
            if item:
                out.append(item.group(1).strip().strip("'\""))
            elif line.strip():
                in_block = False
    return out


def title_of(lines, fallback):
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_index(bundle, folders):
    """Return (by_key, titles): key (stem or slug or alias slug) -> set of rel paths; rel path -> title."""
    by_key = defaultdict(set)
    titles = {}
    for folder in folders:
        base = bundle / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = "/" + path.relative_to(bundle).as_posix()
            lines = path.read_text(encoding="utf-8").splitlines()
            titles[rel] = title_of(lines, path.stem)
            by_key[path.stem].add(rel)
            by_key[slug(path.stem)].add(rel)
            for alias in parse_aliases(lines):
                by_key[slug(alias)].add(rel)
    return by_key, titles


def resolve(target, by_key):
    """Return ('ok', rel) | ('missing', None) | ('ambiguous', [rels])."""
    name = target.strip()
    name = name.rsplit("/", 1)[-1]  # [[folder/name]] -> name
    for key in (name, re.sub(r"\.md$", "", name), slug(name)):
        hits = by_key.get(key)
        if hits:
            return ("ok", next(iter(hits))) if len(hits) == 1 else ("ambiguous", sorted(hits))
    return "missing", None


def convert_text(text, rel_file, by_key, titles, stats, missing_to=None):
    """Convert wikilinks in text. Returns new text. Updates stats."""
    out, in_fence = [], False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            in_fence = not in_fence
        if in_fence or "[[" not in line:
            out.append(line)
            continue
        # mask inline code so its wikilinks survive
        masks = []

        def mask(m):
            masks.append(m.group(0))
            return f"\x00{len(masks) - 1}\x00"

        masked = INLINE_CODE.sub(mask, line)

        def repl(m):
            target, _anchor, label = m.group(1), m.group(2), m.group(3)
            status, hit = resolve(target, by_key)
            if status == "ok":
                stats["converted"] += 1
                title = titles.get(hit) or label or target
                return f"[{title}]({hit})"
            if status == "ambiguous":
                stats["ambiguous"][target.strip()] = hit
                stats["ambiguous_at"].append((rel_file, n, target.strip()))
                return m.group(0)
            stats["missing"][target.strip()] += 1
            stats["missing_at"].append((rel_file, n, target.strip()))
            if missing_to:
                name = target.strip()
                stats["to_do"] += 1
                return f"[{label or name}](/{missing_to.strip('/')}/{slug(name)}.md)"
            return m.group(0)

        new = WIKI.sub(repl, masked)
        new = re.sub(r"\x00(\d+)\x00", lambda m: masks[int(m.group(1))], new)
        out.append(new)
    return "\n".join(out)


def git_dirty(bundle):
    try:
        res = subprocess.run(["git", "-C", str(bundle), "status", "--porcelain"],
                             capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return False  # not a git repo: nothing to protect
    return bool(res.stdout.strip())


def run(bundle, apply=False, missing_to=None, folders=None):
    config = check.load_config()
    folders = folders or config["note_folders"]
    by_key, titles = build_index(bundle, folders)
    stats = {"converted": 0, "to_do": 0, "missing": Counter(), "ambiguous": {},
             "missing_at": [], "ambiguous_at": [], "files": 0}
    changed = []
    for folder in folders:
        base = bundle / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            old = path.read_text(encoding="utf-8")
            if "[[" not in old:
                continue
            rel = path.relative_to(bundle).as_posix()
            new = convert_text(old, rel, by_key, titles, stats, missing_to)
            if new != old:
                changed.append((path, new))
    stats["files"] = len(changed)
    if apply:
        for path, new in changed:
            path.write_text(new, encoding="utf-8")
    return stats


def render(stats, applied):
    lines = ["# Link migration " + ("(applied)" if applied else "(dry run, nothing written)"), "",
             f"- Files affected: {stats['files']}",
             f"- Links converted: {stats['converted']}",
             f"- Links to missing notes turned into to-do links: {stats['to_do']}",
             f"- Links to missing notes, left as wikilinks: {sum(stats['missing'].values()) - stats['to_do']}"
             f" ({len(stats['missing'])} distinct names)",
             f"- Ambiguous names (left unchanged): {len(stats['ambiguous'])}", ""]
    if stats["ambiguous"]:
        lines += ["## Ambiguous", ""]
        for name, hits in sorted(stats["ambiguous"].items()):
            lines.append(f"- `{name}` matches: " + ", ".join(hits))
        lines.append("")
    if stats["missing"]:
        lines += ["## Missing targets (most referenced first)", ""]
        for name, count in stats["missing"].most_common():
            lines.append(f"- `{name}` ({count}x)")
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundle", help="bundle directory")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--allow-dirty", action="store_true", help="allow --apply with uncommitted git changes")
    ap.add_argument("--missing-to", metavar="FOLDER", help="turn links to missing notes into to-do links in FOLDER")
    ap.add_argument("--report", metavar="FILE", help="write the full report as Markdown")
    args = ap.parse_args(argv)
    bundle = Path(args.bundle).resolve()
    if not bundle.is_dir():
        print(f"not a directory: {bundle}", file=sys.stderr)
        return 2
    if args.apply and not args.allow_dirty and git_dirty(bundle):
        print("refusing to --apply: uncommitted changes in the bundle. Commit first (or --allow-dirty).",
              file=sys.stderr)
        return 2
    stats = run(bundle, args.apply, args.missing_to)
    report = render(stats, args.apply)
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
    print(report if not args.report else "\n".join(report.split("\n")[:9]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
