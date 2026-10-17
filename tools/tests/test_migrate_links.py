import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import migrate_links as ml


def make(files):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return tmp, root


A = "---\ntype: Concept\naliases: [Psych Safety, Psychologische Sicherheit]\n---\n# Psychological Safety\n\nBody.\n"
B = "---\ntype: Source\n---\n# Gigerenzer (2015) - Risk Literacy\n"
SRC = """---
type: Source
---
# Quelle
- [[psychological-safety]] - Grund
- [[Psychologische Sicherheit|Label]] - Alias
- [[gigerenzer-2015-risk-literacy#Kapitel]] - Anker
- [[fehlt-noch]] - noch nicht da
- `[[im-code]]` bleibt
```
[[im-block]]
```
"""


class T(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root = make({"10_Concepts/psychological-safety.md": A,
                                    "40_Sources/gigerenzer-2015-risk-literacy.md": B,
                                    "40_Sources/quelle.md": SRC})

    def tearDown(self):
        self.tmp.cleanup()

    def test_dry_run_writes_nothing(self):
        stats = ml.run(self.root)
        self.assertEqual(stats["converted"], 3)
        self.assertEqual((self.root / "40_Sources/quelle.md").read_text(encoding="utf-8"), SRC)

    def test_apply_converts_with_title_and_path(self):
        ml.run(self.root, apply=True)
        text = (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8")
        self.assertIn("[Psychological Safety](/10_Concepts/psychological-safety.md) - Grund", text)
        self.assertIn("[Psychological Safety](/10_Concepts/psychological-safety.md) - Alias", text)
        self.assertIn("[Gigerenzer (2015) - Risk Literacy](/40_Sources/gigerenzer-2015-risk-literacy.md) - Anker", text)

    def test_missing_left_and_code_untouched(self):
        ml.run(self.root, apply=True)
        text = (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8")
        self.assertIn("[[fehlt-noch]]", text)
        self.assertIn("`[[im-code]]`", text)
        self.assertIn("[[im-block]]", text)

    def test_missing_to_makes_todo_link(self):
        ml.run(self.root, apply=True, missing_to="10_Concepts")
        text = (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8")
        self.assertIn("[fehlt-noch](/10_Concepts/fehlt-noch.md)", text)

    def test_ambiguous_not_changed(self):
        (self.root / "20_Frameworks").mkdir()
        (self.root / "20_Frameworks/psychological-safety.md").write_text(A, encoding="utf-8")
        stats = ml.run(self.root)
        self.assertIn("psychological-safety", stats["ambiguous"])

    def test_slug_umlaut(self):
        self.assertEqual(ml.slug("Führung Ä"), "fuehrung-ae")

    def test_second_run_is_noop(self):
        ml.run(self.root, apply=True)
        stats = ml.run(self.root)
        self.assertEqual(stats["converted"], 0)


if __name__ == "__main__":
    unittest.main()
