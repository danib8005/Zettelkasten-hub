#!/usr/bin/env python3
"""Build a thematic catalog of source notes from a manifest. Standard library only; no AI.

Usage:
  python tools/catalog.py BUNDLE_DIR MANIFEST.md -o OUT_DIR [--strip-quotes] [--include-private]

Manifest (Markdown): `# Title` (optional), one `## Group` per output file, then one note
per list item, either a path relative to the bundle root or a bare file name in 40_Sources:
    ## Product and design
    - perri-2018-escaping-build-trap
    - 40_Sources/torres-2021-continuous-discovery.md
    Optional line under a group heading (plain text): the group's one-sentence scope.

Per note the catalog copies, verbatim: title, bibliographic reference, core-thesis section
(including its quote with location, unless --strip-quotes) and the tag line. Nothing is
rephrased. Every entry names the note path, so an answer can cite it.
Notes without `visibility: public|team` are skipped unless --include-private is given
(the default is the safe one for public bundles; for your own private copy pass the flag).
One file per group: catalog-<slug>.md, plus catalog-index.md. Warns above 30,000 characters.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack import visibility_of, strip_quotes  # noqa: E402

LIMIT = 30000
THESIS = ("Kernthese", "Core thesis", "Core idea")
BIBLIO = ("Bibliographische Information", "Bibliographic information", "Reference")


def slug(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "group"


def parse_manifest(text):
    title, groups = "Catalog", []
    for line in text.splitlines():
        if line.startswith("# ") and not groups:
            title = line[2:].strip()
        elif line.startswith("## "):
            groups.append({"name": line[3:].strip(), "scope": "", "items": []})
        elif groups and re.match(r"^\s*[-*]\s+\S", line):
            groups[-1]["items"].append(re.sub(r"^\s*[-*]\s+", "", line).split("#")[0].strip())
        elif groups and line.strip() and not groups[-1]["items"] and not groups[-1]["scope"]:
            groups[-1]["scope"] = line.strip()
    return title, groups


def resolve(bundle, item):
    p = Path(item)
    cands = [bundle / p, bundle / (str(p) + ".md"), bundle / "40_Sources" / p, bundle / "40_Sources" / (p.name + ("" if p.suffix == ".md" else ".md"))]
    return next((c for c in cands if c.is_file()), None)


def section(text, names):
    """Body of the first `## name` section, up to the next `## ` or `---` rule."""
    lines, out, on = text.splitlines(), [], False
    for line in lines:
        if line.startswith("## "):
            if on:
                break
            on = line[3:].strip() in names
            continue
        if on:
            if line.strip() == "---":
                break
            out.append(line)
    return "\n".join(out).strip()


def tag_line(text):
    m = re.search(r"^\W*\**Tags:?\**\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def entry(bundle, path, strip):
    text = path.read_text(encoding="utf-8")
    h1 = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), path.stem)
    ref = section(text, BIBLIO)
    ref = "\n".join(l for l in ref.splitlines() if l.strip() and not re.match(r"^\**(Format|Highlights|Kindle)", l.strip("* ")))
    ref = re.sub(r"^\*\*Vollständige Referenz:\*\*\s*", "", ref).strip()
    thesis = section(text, THESIS)
    if strip:
        thesis = strip_quotes(thesis).strip()
    rel = "/" + path.relative_to(bundle).as_posix()
    parts = ["### " + h1, f"Note: `{rel}`"]
    if ref:
        parts.append(ref)
    parts.append("**Kernthese / core thesis:** " + thesis if thesis else "_(no core-thesis section in this note)_")
    t = tag_line(text)
    if t:
        parts.append("Tags: " + t)
    return "\n\n".join(parts), h1, rel


def build(bundle, manifest_text, strip=False, include_private=False):
    title, groups = parse_manifest(manifest_text)
    files, warnings = {}, []
    index = [f"# {title}", "", "Catalog of source notes, generated from the bundle (verbatim extracts, no rephrasing).", ""]
    for g in groups:
        body, names = [], []
        for item in g["items"]:
            p = resolve(bundle, item)
            if p is None:
                warnings.append(f"not found: {item}")
                continue
            if not include_private and visibility_of(p.read_text(encoding="utf-8")) == "private":
                warnings.append(f"skipped (private): {item}")
                continue
            e, h1, rel = entry(bundle, p, strip)
            body.append(e)
            names.append(h1)
        fname = f"catalog-{slug(g['name'])}.md"
        head = f"# {title}: {g['name']}\n\n" + (g["scope"] + "\n\n" if g["scope"] else "")
        head += "Use: each entry gives reference, core thesis and note path. Cite the note path for every statement; if a topic is not covered here, say «not in the notes».\n\n"
        content = head + "\n\n---\n\n".join(body) + "\n"
        files[fname] = content
        if len(content) > LIMIT:
            warnings.append(f"{fname}: {len(content)} characters (> {LIMIT}); split the group")
        index.append(f"## {g['name']} ({len(body)})")
        if g["scope"]:
            index.append(g["scope"])
        index += [f"- {n}" for n in names] + [""]
    files["catalog-index.md"] = "\n".join(index)
    return files, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundle")
    ap.add_argument("manifest")
    ap.add_argument("-o", "--out", default="catalog")
    ap.add_argument("--strip-quotes", action="store_true")
    ap.add_argument("--include-private", action="store_true")
    a = ap.parse_args(argv)
    bundle = Path(a.bundle).resolve()
    files, warnings = build(bundle, Path(a.manifest).read_text(encoding="utf-8"), a.strip_quotes, a.include_private)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"{out / name}: {len(content)} characters")
    for w in warnings:
        print("WARN", w, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
