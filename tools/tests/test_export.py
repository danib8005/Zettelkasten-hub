import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import export  # noqa: E402


def note(vis=None, body="# T\n\nText.\n"):
    fm = "---\ntype: Source\n" + (f"visibility: {vis}\n" if vis else "") + "---\n"
    return fm + body


class Export(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bundle = self.root / "bundle"
        self.out = self.root / "copy"
        files = {
            "40_Sources/a-team.md": note("team", "# A\n\n> quote (Loc. 5)\n\nSee [B](/40_Sources/c-private.md).\n"),
            "40_Sources/b-none.md": note(),
            "40_Sources/c-private.md": note("privat"),
            "40_Sources/d-public.md": note("öffentlich"),
            "65_Consulting/x/plan.md": note(),
            "65_Consulting/x/secret.md": note("private"),
            "65_Consulting/y/other.md": note("team"),
            "95_System/key.md": "---\ntype: System\n---\n| Kürzel | Name | Rolle |\n|---|---|---|\n| AB | Anna Beispiel | PO |\n",
        }
        for rel, text in files.items():
            p = self.bundle / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        self.profile = self.root / "work.md"

    def tearDown(self):
        self.tmp.cleanup()

    def prof(self, **kw):
        fm = {"name": "work", "audience": "owner", "folders": "[40_Sources]", "visibility": "[team, public]"}
        fm.update(kw)
        self.profile.write_text("---\n" + "".join(f"{k}: {v}\n" for k, v in fm.items()) + "---\n", encoding="utf-8")

    def run_export(self, *extra):
        return export.main([str(self.bundle), str(self.profile), "-o", str(self.out), *extra])

    def exported(self):
        return sorted(p.relative_to(self.out).as_posix() for p in self.out.rglob("*.md") if p.name != "EXPORT.md")

    def test_visibility_filter_missing_means_private(self):
        self.prof()
        self.assertEqual(self.run_export(), 0)
        self.assertEqual(self.exported(), ["40_Sources/a-team.md", "40_Sources/d-public.md"])

    def test_default_is_public_only(self):
        self.prof(visibility="[public]")
        self.run_export()
        self.assertEqual(self.exported(), ["40_Sources/d-public.md"])

    def test_include_by_name_but_private_still_blocked(self):
        self.prof(include="[65_Consulting/x]")
        self.run_export()
        got = self.exported()
        self.assertIn("65_Consulting/x/plan.md", got)
        self.assertNotIn("65_Consulting/x/secret.md", got)
        self.assertNotIn("65_Consulting/y/other.md", got)

    def test_exclude_wins(self):
        self.prof(exclude="[40_Sources/a-*.md]")
        self.run_export()
        self.assertEqual(self.exported(), ["40_Sources/d-public.md"])

    def test_private_in_profile_visibility_is_ignored(self):
        self.prof(visibility="[team, private]")
        self.run_export()
        self.assertNotIn("40_Sources/c-private.md", self.exported())
        self.assertNotIn("40_Sources/b-none.md", self.exported())

    def test_leak_aborts_and_writes_nothing(self):
        (self.bundle / "40_Sources/a-team.md").write_text(note("team", "# A\n\nAnna Beispiel said so.\n"), encoding="utf-8")
        self.prof(**{"leak-terms": "95_System/key.md"})
        self.assertEqual(self.run_export(), 1)
        self.assertFalse(self.out.exists())

    def test_leak_clean_and_key_file_never_exported(self):
        self.prof(**{"leak-terms": "95_System/key.md", "include": "[95_System]"})
        self.assertEqual(self.run_export(), 0)
        self.assertNotIn("95_System/key.md", self.exported())

    def test_links_to_missing_notes_stay_and_are_counted(self):
        self.prof()
        self.run_export()
        text = (self.out / "40_Sources/a-team.md").read_text(encoding="utf-8")
        self.assertIn("(/40_Sources/c-private.md)", text)
        self.assertIn("open links to notes that are not in this copy: 1", (self.out / "EXPORT.md").read_text(encoding="utf-8"))

    def test_regenerate_removes_revoked_files(self):
        self.prof()
        self.run_export()
        (self.bundle / "40_Sources/a-team.md").write_text(note("private"), encoding="utf-8")
        self.run_export()
        self.assertEqual(self.exported(), ["40_Sources/d-public.md"])

    def test_refuses_non_empty_foreign_folder(self):
        self.prof()
        self.out.mkdir()
        (self.out / "mine.txt").write_text("x", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.run_export()
        self.assertTrue((self.out / "mine.txt").exists())

    def test_out_inside_bundle_refused(self):
        self.prof()
        with self.assertRaises(SystemExit):
            export.main([str(self.bundle), str(self.profile), "-o", str(self.bundle / "copy")])

    def test_strip_quotes_and_dry_run(self):
        self.prof()
        self.assertEqual(self.run_export("--dry-run"), 0)
        self.assertFalse(self.out.exists())
        self.run_export("--strip-quotes")
        text = (self.out / "40_Sources/a-team.md").read_text(encoding="utf-8")
        self.assertNotIn("quote", text)

    def test_workbench_is_never_exported(self):
        (self.bundle / "perspective.md").write_text("---\ntype: Perspective\nkind: workbench\n---\n# P\n", encoding="utf-8")
        self.prof()
        with self.assertRaises(SystemExit) as cm:
            self.run_export()
        self.assertIn("workbench", str(cm.exception))
        self.assertFalse(self.out.exists())

    def test_audience_required(self):
        self.prof(audience="")
        with self.assertRaises(SystemExit):
            self.run_export()

    def test_non_owner_needs_strip_quotes(self):
        self.prof(audience="team")
        with self.assertRaises(SystemExit):
            self.run_export()
        self.assertFalse(self.out.exists())
        self.prof(audience="team", **{"strip-quotes": "true"})
        self.assertEqual(self.run_export(), 0)
        self.assertNotIn("quote", (self.out / "40_Sources/a-team.md").read_text(encoding="utf-8"))

    def test_manifest_states_audience(self):
        self.prof()
        self.run_export()
        self.assertIn("Audience: owner", (self.out / "EXPORT.md").read_text(encoding="utf-8"))

    def test_never_dirs(self):
        d = self.bundle / "40_Sources/reflexion"
        d.mkdir()
        (d / "r.md").write_text(note("team"), encoding="utf-8")
        self.prof()
        self.run_export()
        self.assertNotIn("40_Sources/reflexion/r.md", self.exported())


if __name__ == "__main__":
    unittest.main()
