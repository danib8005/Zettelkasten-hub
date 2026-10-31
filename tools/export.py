#!/usr/bin/env python3
"""Make a filtered, generated copy of a bundle for another device or tool (standard library only; no AI).

Usage:
  python tools/export.py BUNDLE_DIR PROFILE.md -o OUT_DIR [--dry-run] [--strip-quotes]

The profile is a Markdown file with frontmatter (keys are plain `key: value`, lists as `[a, b]`):
  name:         short name of the target, e.g. work
  audience:     who may read the copy: owner (only you, on your own device) | team | public. Required.
                Verbatim book quotes only go into an owner copy; for team or public, strip-quotes must be true.
  folders:      note folders to take from; the visibility rule applies to them
  visibility:   values allowed in `visibility:` (default: public; `private` is ignored); a note without the key is private
  include:      paths or globs you approve by name (a folder name or `65_Consulting/x/**`);
                they need no `visibility:`, but a note marked private is still never exported
  exclude:      paths or globs that are never exported (they win over everything else)
  strip-quotes: true drops blockquote lines and Loc./S. references
  leak-terms:   file in the bundle with names that must not appear in the copy (a table with a
                column headed "Name", or one term per line); the file itself is never exported

Rules that no profile can change: `visibility: private` is never exported, nor are `.git`,
`90_Originals`, `99_Raw-Data`, any `reflexion` folder or the leak-terms file. Only `.md` files are copied,
verbatim (except with strip-quotes). If a leak term is found, nothing is written and the exit code is 1.
Links to notes that are not exported stay as they are: they become open links in the copy.
The copy is generated: OUT_DIR gets an `EXPORT.md` listing its files. Running the export again replaces the
copy and removes files that are no longer approved. Changes made in the copy are not carried back; hand
them to the bundle through its inbox.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pack  # noqa: E402

NEVER_DIRS = {".git", "90_Originals", "99_Raw-Data", "reflexion"}
MANIFEST = "EXPORT.md"
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)\s#]+\.md)(?:#[^)]*)?\)")


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value] if value else []


def glob_regex(pattern):
    pattern = pattern.strip().lstrip("/")
    if pattern.endswith("/"):
        pattern += "**"
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
        elif pattern[i] == "*":
            out += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(pattern[i])
            i += 1
    return re.compile(out + r"(/.*)?$")


def matches(rel, patterns):
    return any(glob_regex(p).match(rel) for p in patterns)


def load_profile(path):
    fm = pack.frontmatter(pack.read(path))
    profile = {
        "name": fm.get("name", Path(path).stem),
        "folders": as_list(fm.get("folders")),
        "visibility": [v for v in (pack.VISIBILITY_ALIASES.get(v.lower(), v.lower()) for v in as_list(fm.get("visibility")))
                       if v != "private"] or ["public"],
        "include": as_list(fm.get("include")),
        "exclude": as_list(fm.get("exclude")),
        "audience": str(fm.get("audience", "")).lower(),
        "strip_quotes": str(fm.get("strip-quotes", "false")).lower() == "true",
        "leak_terms": fm.get("leak-terms", ""),
    }
    if profile["audience"] not in ("owner", "team", "public"):
        raise SystemExit("profile needs `audience:` owner | team | public (who may read the copy)")
    if not profile["folders"] and not profile["include"]:
        raise SystemExit("profile has neither `folders:` nor `include:`: nothing would be exported")
    return profile


def load_terms(bundle, rel):
    """Names to look for: the 'Name' column of a table, or one term per line."""
    if not rel:
        return []
    path = bundle / rel
    if not path.is_file():
        raise SystemExit(f"leak-terms file not found: {rel}")
    lines = pack.read(path).splitlines()
    terms, col = [], None
    for line in lines:
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if col is None:
                for i, c in enumerate(cells):
                    if "name" in c.lower():
                        col = i
                        break
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            if col is not None and col < len(cells) and cells[col]:
                terms.append(cells[col])
        elif col is None:
            t = re.sub(r"^[-*]\s*", "", line.strip())
            if t and not t.startswith(("#", "---", "type:", "name:")):
                terms.append(t)
    return sorted({t for t in terms if len(t) >= 3})


def decide(bundle, profile, leak_rel):
    """Return (selected {rel: text}, skipped [(rel, reason)])."""
    selected, skipped = {}, []
    for path in sorted(bundle.rglob("*.md")):
        rel = path.relative_to(bundle).as_posix()
        parts = set(path.relative_to(bundle).parts[:-1])
        in_scope = matches(rel, profile["folders"]) or matches(rel, profile["include"])
        if not in_scope:
            continue
        if parts & NEVER_DIRS or rel == leak_rel:
            skipped.append((rel, "never exported"))
            continue
        if matches(rel, profile["exclude"]):
            skipped.append((rel, "excluded by profile"))
            continue
        text = pack.read(path)
        marked = "visibility" in pack.frontmatter(text)
        vis = pack.visibility_of(text)
        if marked and vis == "private":
            skipped.append((rel, "private"))
            continue
        if not matches(rel, profile["include"]):  # approved by name needs no visibility
            if not marked:
                skipped.append((rel, "no visibility"))
                continue
            if vis not in profile["visibility"]:
                skipped.append((rel, f"visibility {vis}"))
                continue
        selected[rel] = pack.strip_quotes(text) + "\n" if profile["strip_quotes"] else text
    return selected, skipped


def leak_check(selected, terms):
    hits = []
    for rel, text in selected.items():
        for term in terms:
            if re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.IGNORECASE):
                hits.append((rel, term))
    return hits


def open_links(selected):
    exported = {"/" + r for r in selected}
    return sum(1 for text in selected.values() for m in LINK_RE.finditer(text) if m.group(1) not in exported)


def previous_files(out):
    manifest = out / MANIFEST
    if not manifest.is_file():
        return None
    return set(re.findall(r"^- `([^`]+\.md)`", pack.read(manifest), re.MULTILINE))


def write_copy(out, selected, profile, skipped, n_open):
    old = previous_files(out)
    if out.exists() and any(out.iterdir()) and old is None:
        raise SystemExit(f"{out} is not empty and holds no {MANIFEST}: refusing to write into it")
    out.mkdir(parents=True, exist_ok=True)
    for rel in sorted((old or set()) - set(selected)):
        target = out / rel
        if target.is_file():
            target.unlink()
            for parent in target.parents:
                if parent == out or any(parent.iterdir()):
                    break
                parent.rmdir()
    for rel, text in selected.items():
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    reasons = {}
    for _, why in skipped:
        reasons[why] = reasons.get(why, 0) + 1
    lines = ["---", "type: System", "---", f"# Export: {profile['name']}", "",
             f"Generated copy, {datetime.date.today().isoformat()}. Do not edit here: changes go back through the inbox of the bundle.",
             f"Audience: {profile['audience']}" + (" — for the owner only, on their own device; do not share, upload to a shared space or sync to a shared folder" if profile["audience"] == "owner" else ""),
             f"Files: {len(selected)} · open links to notes that are not in this copy: {n_open}",
             "Not exported: " + (", ".join(f"{n}× {why}" for why, n in sorted(reasons.items())) or "nothing"), "", "## Files"]
    lines += [f"- `{rel}`" for rel in sorted(selected)]
    (out / MANIFEST).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundle")
    ap.add_argument("profile")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--dry-run", action="store_true", help="decide and check, write nothing")
    ap.add_argument("--strip-quotes", action="store_true", help="also drop blockquotes and Loc./S. references")
    args = ap.parse_args(argv)
    bundle, out = Path(args.bundle).resolve(), Path(args.out).resolve()
    profile = load_profile(args.profile)
    if args.strip_quotes:
        profile["strip_quotes"] = True
    if profile["audience"] != "owner" and not profile["strip_quotes"]:
        raise SystemExit("audience is not owner: verbatim book quotes must not leave; set `strip-quotes: true`")
    if out == bundle or bundle in out.parents:
        raise SystemExit("OUT_DIR must be outside the bundle")
    terms = load_terms(bundle, profile["leak_terms"])
    selected, skipped = decide(bundle, profile, profile["leak_terms"])
    hits = leak_check(selected, terms)
    if hits:
        for rel, term in hits:
            print(f"LEAK  {rel}: «{term}»")
        print(f"{len(hits)} leak(s): nothing written")
        return 1
    n_open = open_links(selected)
    for rel, why in skipped:
        print(f"skip  {rel}  ({why})")
    if not args.dry_run:
        write_copy(out, selected, profile, skipped, n_open)
    print(f"{'would export' if args.dry_run else 'exported'} {len(selected)} file(s), skipped {len(skipped)}, "
          f"{n_open} link(s) now open, leak check on {len(terms)} term(s): clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
