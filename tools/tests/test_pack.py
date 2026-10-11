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


if __name__ == "__main__":
    unittest.main()
