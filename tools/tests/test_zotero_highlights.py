import io
import json
import sys
import tempfile
import unittest
import urllib.parse
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import zotero_highlights as zh  # noqa: E402


def item(key, version, **data):
    data.setdefault("itemType", "annotation")
    return {"key": key, "version": version, "data": {"key": key, **data}, "meta": {}}


def library():
    book = item("BOOK1", 1, itemType="book", title="Thinking, Fast and Slow", date="2011-10-25",
                creators=[{"creatorType": "author", "firstName": "Daniel", "lastName": "Kahneman"},
                          {"creatorType": "editor", "name": "Some Editor"}])
    return [
        book,
        item("ATT1", 1, itemType="attachment", parentItem="BOOK1", title="PDF"),
        item("ATT2", 1, itemType="attachment", title="Standalone.pdf"),
        item("HL1", 2, parentItem="ATT1", annotationType="highlight", annotationText="System 1 operates\nautomatically.",
             annotationComment="Core claim", annotationPageLabel="20", annotationSortIndex="00002"),
        item("UL1", 2, parentItem="ATT1", annotationType="underline", annotationText="WYSIATI",
             annotationPageLabel="85", annotationSortIndex="00085"),
        item("NT1", 3, parentItem="ATT1", annotationType="note", annotationComment="Compare with Simon",
             annotationPageLabel="9", annotationSortIndex="00001"),
        item("INK1", 3, parentItem="ATT1", annotationType="ink"),
        item("IMG1", 3, parentItem="ATT1", annotationType="image"),
        item("EMPTY1", 3, parentItem="ATT1", annotationType="highlight", annotationText="  "),
        item("HL2", 4, parentItem="ATT2", annotationType="highlight", annotationText="Loose text"),
    ]


class FakeZotero:
    """Serves the local-API routes the script uses from an in-memory library."""

    def __init__(self, items, running=True, api_on=True):
        self.items = {i["key"]: i for i in items}
        self.running, self.api_on, self.urls = running, api_on, []

    def version(self):
        return max(i["version"] for i in self.items.values())

    def __call__(self, url):
        self.urls.append(url)
        if not self.running:
            raise zh.ZoteroError(zh.NOT_RUNNING, 2)
        parts = urllib.parse.urlparse(url)
        q = dict(urllib.parse.parse_qsl(parts.query))
        if parts.path == "/connector/ping":
            return 200, {}, "Zotero is running"
        if not self.api_on:
            return 403, {}, "Local API is not enabled"
        path = parts.path.removeprefix("/api/users/0/items")
        values = list(self.items.values())
        if path == "/top":
            found = [i for i in values if not i["data"].get("parentItem")
                     and i["data"]["itemType"] not in ("annotation", "attachment")]
            if "q" in q:
                found = [i for i in found if q["q"].lower() in json.dumps(i["data"]).lower()]
        elif path == "":
            found = [i for i in values if i["data"]["itemType"] == q.get("itemType", i["data"]["itemType"])
                     and i["version"] > int(q.get("since", -1))]
        elif path.endswith("/children"):
            parent = path.split("/")[1]
            found = [i for i in values if i["data"].get("parentItem") == parent]
        else:
            key = path.strip("/")
            if key not in self.items:
                return 404, {}, "Not found"
            return 200, {"Last-Modified-Version": str(self.version())}, json.dumps(self.items[key])
        start, limit = int(q.get("start", 0)), int(q.get("limit", 1000))
        headers = {"last-modified-version": str(self.version()), "Total-Results": str(len(found))}
        return 200, headers, json.dumps(found[start:start + limit])


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.bundle = Path(self._tmp.name)
        self.fake = FakeZotero(library())
        self.zot = zh.Zotero(self.fake)

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *argv, fake=None):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = zh.main(list(argv), zh.Zotero(fake or self.fake))
        return code, out.getvalue(), err.getvalue()


class Status(Base):
    def test_not_running(self):
        code, _, err = self.run_cli("status", fake=FakeZotero(library(), running=False))
        self.assertEqual(code, 2)
        self.assertIn("not running", err)

    def test_api_off(self):
        code, _, err = self.run_cli("status", fake=FakeZotero(library(), api_on=False))
        self.assertEqual(code, 3)
        self.assertIn("Allow other applications", err)

    def test_running(self):
        code, out, _ = self.run_cli("status")
        self.assertEqual(code, 0)
        self.assertIn("library version 4", out)

    def test_real_http_get_reports_not_running(self):
        with self.assertRaises(zh.ZoteroError) as cm:
            zh.http_get("http://127.0.0.1:9/", timeout=1)
        self.assertEqual(cm.exception.code, 2)


class Rendering(Base):
    def test_render_quote_page_and_comment(self):
        text = zh.render([self.fake.items["HL1"]["data"], self.fake.items["NT1"]["data"]], "en")
        self.assertEqual(text, "> System 1 operates\n> automatically.\n> (p. 20)\n\n📝 Your note: Core claim"
                               "\n\n📝 Your note: Compare with Simon (p. 9)")

    def test_render_german_markers(self):
        text = zh.render([self.fake.items["HL1"]["data"]], "de")
        self.assertIn("> (S. 20)", text)
        self.assertIn("📝 Deine Notiz: Core claim", text)

    def test_describe_uses_authors_and_year(self):
        meta = zh.describe(self.fake.items["BOOK1"])
        self.assertEqual(meta["creators"], "Kahneman, Daniel")
        self.assertEqual(meta["year"], "2011")
        self.assertEqual(meta["zotero"], "zotero://select/library/items/BOOK1")

    def test_language_from_perspective(self):
        self.assertEqual(zh.bundle_language(self.bundle), "en")
        (self.bundle / "perspective.md").write_text("---\ntype: Perspective\nlanguage: de-CH\n---\n", encoding="utf-8")
        self.assertEqual(zh.bundle_language(self.bundle), "de")


class Fetch(Base):
    def test_first_pull_groups_sorts_and_skips(self):
        out = zh.fetch(self.zot, self.bundle)
        self.assertIn("2 item(s), 4 highlight(s). First pull: yes. Library version: 4.", out)
        self.assertIn("Skipped (no quotable text): 1 highlight, 1 image, 1 ink.", out)
        self.assertIn("=== ITEM BOOK1 ===", out)
        self.assertIn("=== ITEM ATT2 ===", out)
        book = out.split("=== ITEM BOOK1 ===")[1].split("--- END ITEM BOOK1 ---")[0]
        self.assertLess(book.index("Compare with Simon"), book.index("System 1"))
        self.assertLess(book.index("System 1"), book.index("WYSIATI"))
        pending = json.loads((self.bundle / zh.PENDING).read_text(encoding="utf-8"))
        self.assertEqual(pending, {"library_version": 4,
                                   "items": {"BOOK1": ["HL1", "NT1", "UL1"], "ATT2": ["HL2"]}})
        self.assertFalse((self.bundle / zh.STATE).exists())

    def test_missing_year_is_not_guessed(self):
        out = zh.fetch(self.zot, self.bundle)
        self.assertIn("Year: (none in Zotero)", out.split("=== ITEM ATT2 ===")[1])

    def test_mark_done_then_only_new_highlights(self):
        zh.fetch(self.zot, self.bundle)
        self.assertIn("4 highlight(s) from 2 item(s)", zh.mark_done(self.bundle))
        self.assertFalse((self.bundle / zh.PENDING).exists())
        self.assertIn("No new Zotero highlights since the last pull.", zh.fetch(self.zot, self.bundle))
        self.assertTrue(any("since=4" in u for u in self.fake.urls))
        self.fake.items["HL3"] = item("HL3", 5, parentItem="ATT1", annotationType="highlight",
                                      annotationText="New one", annotationPageLabel="99")
        self.fake.items["HL1"]["version"] = 5
        self.fake.items["HL1"]["data"]["annotationComment"] = "Edited later"
        out = zh.fetch(self.zot, self.bundle)
        self.assertIn("1 item(s), 1 highlight(s). First pull: no.", out)
        self.assertIn("New one", out)
        self.assertNotIn("Edited later", out)

    def test_nothing_is_recorded_without_mark_done(self):
        zh.fetch(self.zot, self.bundle)
        self.assertIn("First pull: yes", zh.fetch(self.zot, self.bundle))

    def test_mark_done_chosen_items_and_none(self):
        zh.fetch(self.zot, self.bundle)
        zh.mark_done(self.bundle, ["ATT2"])
        state = json.loads((self.bundle / zh.STATE).read_text(encoding="utf-8"))
        self.assertEqual(state, {"imported": {"ATT2": ["HL2"]}, "library_version": 4})
        with self.assertRaises(zh.ZoteroError):
            zh.mark_done(self.bundle)

    def test_start_from_now_records_only_version(self):
        zh.fetch(self.zot, self.bundle)
        zh.mark_done(self.bundle, none=True)
        state = json.loads((self.bundle / zh.STATE).read_text(encoding="utf-8"))
        self.assertEqual(state, {"imported": {}, "library_version": 4})
        self.assertIn("No new Zotero highlights", zh.fetch(self.zot, self.bundle))

    def test_unknown_item_in_mark_done(self):
        zh.fetch(self.zot, self.bundle)
        with self.assertRaises(zh.ZoteroError):
            zh.mark_done(self.bundle, ["NOPE"])
        self.assertTrue((self.bundle / zh.PENDING).exists())

    def test_named_item_skips_imported_and_keeps_version(self):
        zh.fetch(self.zot, self.bundle)
        zh.mark_done(self.bundle, none=True)
        out = zh.fetch(self.zot, self.bundle, item="BOOK1")
        self.assertIn("1 item(s), 3 highlight(s). Named item: BOOK1.", out)
        self.assertNotIn("Loose text", out)
        zh.mark_done(self.bundle)
        out = zh.fetch(self.zot, self.bundle, item="BOOK1")
        self.assertIn("No new Zotero highlights for item BOOK1.", out)
        state = json.loads((self.bundle / zh.STATE).read_text(encoding="utf-8"))
        self.assertEqual(state["library_version"], 4)
        self.assertEqual(state["imported"]["BOOK1"], ["HL1", "NT1", "UL1"])

    def test_paging_collects_every_page(self):
        zh_page, zh.PAGE_SIZE = zh.PAGE_SIZE, 2
        try:
            out = zh.fetch(self.zot, self.bundle)
        finally:
            zh.PAGE_SIZE = zh_page
        self.assertIn("4 highlight(s)", out)


class Cli(Base):
    def test_search(self):
        code, out, _ = self.run_cli("search", "kahneman")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "BOOK1 · Kahneman, Daniel (2011): Thinking, Fast and Slow")

    def test_fetch_and_mark_done(self):
        code, out, _ = self.run_cli("fetch", str(self.bundle), "--lang", "de")
        self.assertEqual(code, 0)
        self.assertIn("📝 Deine Notiz:", out)
        code, out, _ = self.run_cli("mark-done", str(self.bundle))
        self.assertEqual(code, 0)
        self.assertIn("library version 4", out)

    def test_fetch_when_not_running_writes_nothing(self):
        code, _, _ = self.run_cli("fetch", str(self.bundle), fake=FakeZotero(library(), running=False))
        self.assertEqual(code, 2)
        self.assertFalse((self.bundle / zh.PENDING).exists())

    def test_bad_bundle(self):
        code, _, err = self.run_cli("fetch", str(self.bundle / "missing"))
        self.assertEqual(code, 1)
        self.assertIn("Not a directory", err)


if __name__ == "__main__":
    unittest.main()
