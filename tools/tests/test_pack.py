import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import pack  # noqa: E402

EX = ROOT / "example"


class Pack(unittest.TestCase):
    def test_keyword_selection_finds_concept(self):
        notes = pack.select(EX, ["Addition", "Bias"], [], 3)
        self.assertEqual(notes[0].name, "addition-bias-subtraction.md")

    def test_notes_verbatim_with_path_headings(self):
        notes = pack.select(EX, [], ["/10_Concepts/addition-bias-subtraction.md"], 1)
        text = pack.build(EX, notes, "answer")
        self.assertIn("### /10_Concepts/addition-bias-subtraction.md", text)
        self.assertIn(notes[0].read_text(encoding="utf-8").rstrip(), text)
        self.assertIn("AGENTS.md", text)

    def test_cli_writes_file_and_counts(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "pack.md"
            self.assertEqual(pack.main([str(EX), "-k", "friction", "-o", str(out)]), 0)
            self.assertTrue(out.read_text(encoding="utf-8").startswith("# Knowledge pack"))

    def test_no_match_exits(self):
        with self.assertRaises(SystemExit):
            pack.main([str(EX), "-k", "xyzzyqq", "-o", "/tmp/never.md"])

    def test_missing_file_exits(self):
        with self.assertRaises(SystemExit):
            pack.select(EX, [], ["10_Concepts/nope.md"], 1)


class Filters(unittest.TestCase):
    def make(self, d, name, vis, body):
        f = Path(d) / "10_Concepts"
        f.mkdir(exist_ok=True)
        head = f"---\ntype: Concept\n{('visibility: ' + vis + chr(10)) if vis else ''}---\n"
        (f / name).write_text(head + body, encoding="utf-8")

    def test_default_excludes_private_and_missing(self):
        with tempfile.TemporaryDirectory() as d:
            self.make(d, "a.md", "team", "# A\n\nzebra\n")
            self.make(d, "b.md", "", "# B\n\nzebra\n")
            self.make(d, "c.md", "öffentlich", "# C\n\nzebra\n")
            names = [p.name for p in pack.select(Path(d), ["zebra"], [], 9, {"public"})]
            self.assertEqual(names, ["c.md"])
            names = [p.name for p in pack.select(Path(d), ["zebra"], [], 9, {"public", "team"})]
            self.assertEqual(sorted(names), ["a.md", "c.md"])
            self.assertEqual(len(pack.select(Path(d), ["zebra"], [], 9, None)), 3)

    def test_explicit_private_file_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            self.make(d, "b.md", "", "# B\n")
            with self.assertRaises(SystemExit):
                pack.select(Path(d), [], ["10_Concepts/b.md"], 1, {"public"})

    def test_strip_quotes_and_locations(self):
        text = "# T\n> a quote\n> (Autor 2020, Loc. 12)\nParaphrase (Autor 2020, S. 5) bleibt.\n"
        out = pack.strip_quotes(text)
        self.assertNotIn("quote", out)
        self.assertNotIn("Loc.", out)
        self.assertNotIn("S. 5", out)
        self.assertIn("Paraphrase bleibt.", out)

    def test_keep_sections(self):
        text = "---\ntype: X\n---\n# Titel\n\n## Kernidee\nWichtig\n\n## Details\nLang\n"
        out = pack.keep_sections(text, ["Kernidee"])
        self.assertIn("# Titel", out)
        self.assertIn("Wichtig", out)
        self.assertNotIn("Lang", out)
        self.assertNotIn("type: X", out)


if __name__ == "__main__":
    unittest.main()
