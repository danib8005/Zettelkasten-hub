#!/usr/bin/env python3
"""Read highlights from a running Zotero desktop app (local API, read-only). Standard library only.

Usage:
  python tools/zotero_highlights.py status                   is Zotero running, is the local API on?
  python tools/zotero_highlights.py search QUERY             find items by title, creator or year
  python tools/zotero_highlights.py fetch BUNDLE_DIR [--item KEY] [--lang en|de]
  python tools/zotero_highlights.py mark-done BUNDLE_DIR [--items KEY ...] [--none]

fetch prints one Markdown block per Zotero item with the highlights not yet imported and keeps their
keys in BUNDLE_DIR/.zotero-sync.pending.json. Without --item it reads only what changed since the last
pull. mark-done moves the pending keys into BUNDLE_DIR/.zotero-sync.json; run it after the notes are
saved. --items limits it to chosen items, --none records only the library version ("start from now").

Zotero must run with Settings > Advanced > "Allow other applications on this computer to communicate
with Zotero". Only the personal library is read; nothing in Zotero is changed.

Exit codes: 0 ok · 1 usage or state error · 2 Zotero not running · 3 local API not enabled.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

BASE = "http://127.0.0.1:23119"
API = BASE + "/api/users/0"
STATE = ".zotero-sync.json"
PENDING = ".zotero-sync.pending.json"
TEXT_TYPES = {"highlight", "underline"}
NOTE_TYPES = {"note", "text"}
PAGE_SIZE = 100
NOTE_MARK = {"en": "📝 Your note:", "de": "📝 Deine Notiz:"}
PAGE_MARK = {"en": "p.", "de": "S."}
NOT_RUNNING = "Zotero is not running (nothing answers on 127.0.0.1:23119). Start Zotero and try again."
API_OFF = ("Zotero is running, but its local API is off. In Zotero: Settings > Advanced > tick "
           "\"Allow other applications on this computer to communicate with Zotero\".")


class ZoteroError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


def http_get(url, timeout=10):
    """Return (status, headers, body). Raise ZoteroError if nothing answers."""
    req = urllib.request.Request(url, headers={"Zotero-API-Version": "3"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as e:
        raise ZoteroError(NOT_RUNNING, 2) from e


def header(headers, name):
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
    return None


class Zotero:
    """Read-only client for the Zotero local API. `get` is injectable for tests."""

    def __init__(self, get=http_get):
        self._get = get
        self._items = {}

    def api(self, path, **params):
        url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
        status, headers, body = self._get(url)
        if status == 403:
            raise ZoteroError(API_OFF, 3)
        if status != 200:
            raise ZoteroError(f"Zotero answered {status} for {path}: {body[:200]}", 1)
        return headers, json.loads(body)

    def check(self):
        """Return the library version; raise ZoteroError if Zotero or its local API is unavailable."""
        status, _, _ = self._get(BASE + "/connector/ping")
        if status != 200:
            raise ZoteroError(NOT_RUNNING, 2)
        headers, _ = self.api("/items/top", limit=1)
        return int(header(headers, "Last-Modified-Version") or 0)

    def all(self, path, **params):
        """All results of a list request (paged), plus the library version of the first page."""
        out, seen, start, version = [], set(), 0, None
        while True:
            headers, page = self.api(path, start=start, limit=PAGE_SIZE, **params)
            if version is None:
                version = int(header(headers, "Last-Modified-Version") or 0)
            new = [o for o in page if o.get("key") not in seen]
            out += new
            seen.update(o.get("key") for o in new)
            total = header(headers, "Total-Results")
            if len(page) < PAGE_SIZE or not new or (total and len(out) >= int(total)):
                return out, version
            start += PAGE_SIZE

    def item(self, key):
        if key not in self._items:
            self._items[key] = self.api(f"/items/{key}")[1]
        return self._items[key]

    def top_item(self, attachment_key):
        """The bibliographic item an attachment belongs to (or the attachment itself if standalone)."""
        att = self.item(attachment_key)
        parent = att["data"].get("parentItem")
        return self.item(parent) if parent else att

    def annotations_since(self, version):
        params = {"itemType": "annotation"}
        if version is not None:
            params["since"] = version
        return self.all("/items", **params)

    def annotations_of(self, key):
        item = self.item(key)
        if item["data"].get("itemType") == "attachment":
            attachments = [key]
        else:
            children, _ = self.all(f"/items/{key}/children")
            attachments = [c["key"] for c in children if c["data"].get("itemType") == "attachment"]
        result = []
        for att in attachments:
            children, _ = self.all(f"/items/{att}/children")
            result += [c for c in children if c["data"].get("itemType") == "annotation"]
        return result

    def search(self, query):
        found, _ = self.all("/items/top", q=query, qmode="titleCreatorYear")
        return [describe(i) for i in found if i["data"].get("itemType") not in ("note", "attachment")]


def describe(item):
    """Title, creators, year and link of a Zotero item, exactly as Zotero holds them."""
    data, meta = item["data"], item.get("meta", {})
    creators = data.get("creators", [])
    authors = [c for c in creators if c.get("creatorType") == "author"] or creators
    names = [c.get("name") or ", ".join(p for p in (c.get("lastName"), c.get("firstName")) if p)
             for c in authors]
    year = re.search(r"\d{4}", meta.get("parsedDate") or data.get("date") or "")
    return {"key": item["key"], "title": data.get("title", ""), "creators": "; ".join(names),
            "year": year.group(0) if year else "",
            "zotero": f"zotero://select/library/items/{item['key']}"}


def usable(data):
    kind = data.get("annotationType")
    if kind in TEXT_TYPES:
        return bool((data.get("annotationText") or "").strip())
    if kind in NOTE_TYPES:
        return bool((data.get("annotationComment") or "").strip())
    return False


def collect(zot, annotations, done):
    """Group new usable annotations by top-level item. Returns (groups, skipped counts)."""
    groups, skipped = {}, Counter()
    for a in annotations:
        data = a["data"]
        if data.get("itemType") != "annotation" or data.get("deleted") or a["key"] in done:
            continue
        if not usable(data):
            skipped[data.get("annotationType") or "unknown"] += 1
            continue
        top = zot.top_item(data["parentItem"])
        groups.setdefault(top["key"], {"item": describe(top), "annotations": []})["annotations"].append(data)
    for g in groups.values():
        g["annotations"].sort(key=lambda d: (d.get("parentItem", ""), d.get("annotationSortIndex", "")))
    return groups, skipped


def render(annotations, lang="en"):
    """Markdown for the raw-material section: exact text, page label, the owner's comment."""
    blocks = []
    for d in annotations:
        page = (d.get("annotationPageLabel") or "").strip()
        loc = f"({PAGE_MARK[lang]} {page})" if page else ""
        comment = (d.get("annotationComment") or "").strip()
        if d.get("annotationType") in TEXT_TYPES:
            lines = [f"> {line}".rstrip() for line in d["annotationText"].strip().splitlines()]
            if loc:
                lines.append(f"> {loc}")
            if comment:
                lines += ["", f"{NOTE_MARK[lang]} {comment}"]
        else:
            lines = [f"{NOTE_MARK[lang]} {comment}" + (f" {loc}" if loc else "")]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except ValueError as e:
        raise ZoteroError(f"{path.name} is not valid JSON: {e}", 1) from e


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def load_state(bundle):
    state = load_json(bundle / STATE, {})
    state.setdefault("library_version", None)
    state.setdefault("imported", {})
    return state


def bundle_language(bundle):
    try:
        text = (bundle / "perspective.md").read_text(encoding="utf-8")
    except OSError:
        return "en"
    m = re.search(r"^language:\s*['\"]?(\w\w)", text, re.M | re.I)
    return "de" if m and m.group(1).lower() == "de" else "en"


def fetch(zot, bundle, item=None, lang=None):
    """Read new highlights, write the pending file, return the report text."""
    lang = lang or bundle_language(bundle)
    state = load_state(bundle)
    done = {k for keys in state["imported"].values() for k in keys}
    version = zot.check()
    first = state["library_version"] is None
    if item:
        annotations = zot.annotations_of(item)
        version = None
    else:
        annotations, version = zot.annotations_since(state["library_version"])
    groups, skipped = collect(zot, annotations, done)
    pending = bundle / PENDING
    if not groups:
        pending.unlink(missing_ok=True)
        head = "No new Zotero highlights" + (f" for item {item}." if item else " since the last pull.")
        return head + skipped_line(skipped)
    write_json(pending, {"library_version": version,
                         "items": {k: sorted(a["key"] for a in g["annotations"])
                                   for k, g in groups.items()}})
    n = sum(len(g["annotations"]) for g in groups.values())
    out = [f"Zotero highlights: {len(groups)} item(s), {n} highlight(s). "
           + (f"Named item: {item}." if item else f"First pull: {'yes' if first else 'no'}. "
              f"Library version: {version}.") + skipped_line(skipped),
           f'Next: save the notes, then run: python tools/zotero_highlights.py mark-done "{bundle}"', ""]
    for key, g in groups.items():
        meta = g["item"]
        out += [f"=== ITEM {key} ===",
                f"Title: {meta['title'] or '(none in Zotero)'}",
                f"Creators: {meta['creators'] or '(none in Zotero)'}",
                f"Year: {meta['year'] or '(none in Zotero)'}",
                f"Zotero: {meta['zotero']}",
                f"Highlights: {len(g['annotations'])}",
                "--- RAW MATERIAL (paste unchanged) ---",
                render(g["annotations"], lang),
                f"--- END ITEM {key} ---", ""]
    return "\n".join(out).rstrip()


def skipped_line(skipped):
    if not skipped:
        return ""
    return "\nSkipped (no quotable text): " + ", ".join(f"{n} {k}" for k, n in sorted(skipped.items())) + "."


def mark_done(bundle, items=None, none=False):
    """Move pending keys into the state file after the notes are saved. Returns the report text."""
    pending_path = bundle / PENDING
    pending = load_json(pending_path, None)
    if pending is None:
        raise ZoteroError("Nothing pending; run fetch first.", 1)
    unknown = [k for k in items or [] if k not in pending["items"]]
    if unknown:
        raise ZoteroError(f"Not in the pending pull: {', '.join(unknown)}", 1)
    chosen = [] if none else (items or list(pending["items"]))
    state = load_state(bundle)
    for key in chosen:
        state["imported"][key] = sorted(set(state["imported"].get(key, [])) | set(pending["items"][key]))
    if pending.get("library_version") is not None:
        state["library_version"] = pending["library_version"]
    write_json(bundle / STATE, state)
    pending_path.unlink()
    n = sum(len(pending["items"][k]) for k in chosen)
    return (f"Recorded {n} highlight(s) from {len(chosen)} item(s) in {STATE}; "
            f"library version {state['library_version']}.")


def main(argv=None, zot=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="is Zotero running and its local API on?")
    s = sub.add_parser("search", help="find items by title, creator or year")
    s.add_argument("query")
    f = sub.add_parser("fetch", help="print new highlights per item and keep them pending")
    f.add_argument("bundle")
    f.add_argument("--item", help="Zotero item key: all its highlights not yet imported")
    f.add_argument("--lang", choices=sorted(NOTE_MARK), help="marker language (default: perspective.md)")
    m = sub.add_parser("mark-done", help="record the pending highlights after the notes are saved")
    m.add_argument("bundle")
    m.add_argument("--items", nargs="+", help="only these item keys")
    m.add_argument("--none", action="store_true", help="record only the library version (start from now)")
    args = ap.parse_args(argv)
    zot = zot or Zotero()
    try:
        if args.cmd == "status":
            print(f"Zotero is running; local API on; library version {zot.check()}.")
        elif args.cmd == "search":
            zot.check()
            found = zot.search(args.query)
            print("\n".join(f"{i['key']} · {i['creators'] or '?'} ({i['year'] or '?'}): {i['title']}"
                            for i in found) or "No matching items.")
        else:
            bundle = Path(args.bundle)
            if not bundle.is_dir():
                raise ZoteroError(f"Not a directory: {bundle}", 1)
            if args.cmd == "fetch":
                print(fetch(zot, bundle, args.item, args.lang))
            else:
                print(mark_done(bundle, args.items, args.none))
    except ZoteroError as e:
        print(e, file=sys.stderr)
        return e.code
    return 0


if __name__ == "__main__":
    sys.exit(main())
