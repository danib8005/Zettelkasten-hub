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

    def test_missing_auto_picks_folder(self):
        (self.root / "40_Sources/q2.md").write_text("# Q2\n- [[urry-2013-societies-beyond-oil]] x\n", encoding="utf-8")
        ml.run(self.root, apply=True, missing_to="auto")
        self.assertIn("(/40_Sources/urry-2013-societies-beyond-oil.md)", (self.root / "40_Sources/q2.md").read_text(encoding="utf-8"))
        self.assertIn("(/10_Concepts/fehlt-noch.md)", (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8"))

    def test_similar_name_reported(self):
        (self.root / "40_Sources/q3.md").write_text("# Q3\n- [[psychological-safty]] x\n", encoding="utf-8")
        stats = ml.run(self.root)
        self.assertEqual(stats["similar"]["psychological-safty"], "psychological-safety")

    def test_map_file_redirects_name_to_existing_note(self):
        m = self.root / "map.md"
        m.write_text("# Zuordnung\n- `fehlt-noch` → `psychological-safety`\ngigerenzer-alt = gigerenzer-2015-risk-literacy\n", encoding="utf-8")
        ml.run(self.root, apply=True, map_file=m)
        text = (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8")
        self.assertIn("[Psychological Safety](/10_Concepts/psychological-safety.md) - noch nicht da", text)

    def test_map_with_unknown_target_is_an_error(self):
        m = self.root / "map.md"
        m.write_text("x = gibt-es-nicht\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            ml.run(self.root, map_file=m)

    def test_folder_qualified_and_outside_links(self):
        (self.root / "40_Sources/q4.md").write_text(
            "# Q4\n- [[70_Tools/neues-tool]] x\n- [[65_Consulting/projekt]] y\n- [[90_Originals/a/b|b]] z\n", encoding="utf-8")
        stats = ml.run(self.root, apply=True, missing_to="auto")
        text = (self.root / "40_Sources/q4.md").read_text(encoding="utf-8")
        self.assertIn("[neues-tool](/70_Tools/neues-tool.md)", text)
        self.assertIn("[[65_Consulting/projekt]]", text)
        self.assertIn("[[90_Originals/a/b|b]]", text)
        self.assertEqual(sum(stats["outside"].values()), 2)

    def test_target_in_a_folder_that_is_not_rewritten_is_still_found(self):
        (self.root / "60_Own-Work").mkdir()
        (self.root / "60_Own-Work/eigener-text.md").write_text("# Eigener Text\n", encoding="utf-8")
        (self.root / "40_Sources/q5.md").write_text("# Q5\n- [[eigener-text]] x\n", encoding="utf-8")
        ml.run(self.root, apply=True, missing_to="auto")
        self.assertIn("[Eigener Text](/60_Own-Work/eigener-text.md)", (self.root / "40_Sources/q5.md").read_text(encoding="utf-8"))

    def test_folders_option_rewrites_other_folders(self):
        (self.root / "60_Own-Work").mkdir()
        (self.root / "60_Own-Work/t.md").write_text("# T\n- [[psychological-safety]] x\n", encoding="utf-8")
        rc = ml.main([str(self.root), "--apply", "--allow-dirty", "--folders", "60_Own-Work"])
        self.assertEqual(rc, 0)
        self.assertIn("(/10_Concepts/psychological-safety.md)", (self.root / "60_Own-Work/t.md").read_text(encoding="utf-8"))
        self.assertIn("[[fehlt-noch]]", (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8"))

    def test_map_with_full_path_settles_ambiguity(self):
        (self.root / "20_Frameworks").mkdir()
        (self.root / "20_Frameworks/psychological-safety.md").write_text(A, encoding="utf-8")
        m = self.root / "map.md"
        m.write_text("psychological-safety = /20_Frameworks/psychological-safety.md\n", encoding="utf-8")
        stats = ml.run(self.root, apply=True, map_file=m)
        self.assertFalse(stats["ambiguous"])
        self.assertIn("(/20_Frameworks/psychological-safety.md) - Grund", (self.root / "40_Sources/quelle.md").read_text(encoding="utf-8"))

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
