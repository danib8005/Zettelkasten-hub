import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import check  # noqa: E402


def run(path, **kw):
    report = check.Report()
    if kw.pop("i18n", False):
        check.check_i18n(Path(path), report)
    else:
        check.check_bundle(Path(path), kw.get("example", False), report)
    return report


def messages(report):
    return [m for _, _, _, m in report.items]


class ExampleBundle(unittest.TestCase):
    def test_example_is_clean(self):
        report = run(ROOT / "example", example=True)
        self.assertEqual(report.items, [])


class BrokenCopy(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / "example", self.tmp / "b")
        self.b = self.tmp / "b"
        broken = self.b / "10_Concepts" / "Kaputt Übung.md"
        broken.write_text(
            "# Kaputt\n"
            "> a quote\n"
            "See [[wikilink]] and [rel](10_Concepts/x.md) and [gone](/10_Concepts/nirgends.md).\n"
            "Fundstelle Loc. 123 und S. 45.\n",
            encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_all_builtin_errors_found_in_example_mode(self):
        msgs = " | ".join(messages(run(self.b, example=True)))
        for expected in ["missing `type:`", "file name must be", "missing review status",
                         "wikilink", "not bundle-relative", "leaves the example",
                         "blockquote", "location/page reference", "visibility"]:
            self.assertIn(expected, msgs)

    def test_open_link_is_only_warning_outside_example_mode(self):
        report = run(self.b)
        self.assertTrue(any("open link" in m for m in messages(report)))
        self.assertFalse(any("leaves the example" in m for m in messages(report)))

    def test_main_exit_code(self):
        self.assertEqual(check.main([str(self.b), "--example"]), 1)
        self.assertEqual(check.main([str(ROOT / "example"), "--example"]), 0)


class OkfConformance(unittest.TestCase):
    def test_non_note_file_needs_type_but_reserved_files_do_not(self):
        with tempfile.TemporaryDirectory() as d:
            b = Path(d)
            (b / "README.md").write_text("# no frontmatter\n", encoding="utf-8")
            (b / "index.md").write_text("# Index\n", encoding="utf-8")
            (b / "log.md").write_text("# Log\n", encoding="utf-8")
            msgs = messages(run(b))
            self.assertEqual(len(msgs), 1)
            self.assertIn("OKF", msgs[0])


class WikilinksInCode(unittest.TestCase):
    def test_wikilink_in_code_is_not_an_error_but_real_one_is(self):
        with tempfile.TemporaryDirectory() as d:
            b = Path(d)
            (b / "10_Concepts").mkdir()
            body = ("---\ntype: Concept\n---\n# T\n"
                    "Documented as `[[a]]` in text.\n```\n[[b]]\n```\n"
                    "Real [[c]] link.\n\n- Created: 2026-10-17\n- Last review: 2026-10-17\n- Review status: current\n")
            (b / "10_Concepts" / "t.md").write_text(body, encoding="utf-8")
            wiki = [i for i in run(b).items if "wikilink" in i[3]]
            self.assertEqual(len(wiki), 1)
            self.assertEqual(wiki[0][1], 9)


class InboxAndOpenQuestions(unittest.TestCase):
    def test_inbox_and_open_question_notes_need_review_status(self):
        with tempfile.TemporaryDirectory() as d:
            b = Path(d)
            for folder in ("00_Inbox", "50_Open-Questions"):
                (b / folder).mkdir()
                (b / folder / "x.md").write_text("---\ntype: Capture\n---\n# X\n", encoding="utf-8")
            msgs = [m for _, _, _, m in run(b).items]
            self.assertEqual(msgs.count("missing review status"), 2)


AGENT = """---
type: Agent
name: {name}
description: Test agent.
phase: 1
skills: [{skills}]
reads: [00_Inbox, perspective.md]
writes: [{writes}]
---
# Agent
{sections}
"""
SECTIONS = "\n".join(f"## {s}\ntext\n" for s in check.AGENT_SECTIONS)


class AgentSystem(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for skill in ("used", "unused"):
            (self.tmp / "skills" / skill).mkdir(parents=True)
            (self.tmp / "skills" / skill / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
        (self.tmp / "agents").mkdir()
        (self.tmp / ".github" / "agents").mkdir(parents=True)
        (self.tmp / ".claude" / "agents").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def agent(self, name="good", skills="used", writes="00_Inbox", sections=SECTIONS, adapters=True):
        (self.tmp / "agents" / f"{name}.md").write_text(
            AGENT.format(name=name, skills=skills, writes=writes, sections=sections), encoding="utf-8")
        if adapters:
            (self.tmp / ".github" / "agents" / f"{name}.agent.md").write_text("x", encoding="utf-8")
            (self.tmp / ".claude" / "agents" / f"{name}.md").write_text("x", encoding="utf-8")

    def findings(self):
        return run(self.tmp, i18n=True).items

    def test_repository_is_clean(self):
        self.assertEqual(run(ROOT, i18n=True).items, [])

    def test_valid_agent_only_warns_about_unused_skill(self):
        self.agent()
        items = self.findings()
        self.assertEqual([(i[2], i[3]) for i in items], [("WARN", "skill is not used by any agent")])
        self.assertIn("unused", items[0][0])

    def test_broken_agent_is_reported(self):
        self.agent(skills="used, missing-skill", writes="99_Nowhere", sections="## Role\n", adapters=False)
        (self.tmp / ".claude" / "agents" / "orphan.md").write_text("x", encoding="utf-8")
        msgs = " | ".join(m for _, _, _, m in self.findings())
        for expected in ["skill `missing-skill` not found", "not a bundle folder",
                         "section `## Final check` missing", "adapter missing for agent `good`",
                         "adapter without an agent"]:
            self.assertIn(expected, msgs)

    def test_missing_frontmatter_field_and_name_mismatch(self):
        (self.tmp / "agents" / "bad.md").write_text(
            "---\ntype: Agent\nname: other\n---\n" + SECTIONS, encoding="utf-8")
        msgs = " | ".join(m for _, _, _, m in self.findings())
        self.assertIn("needs `skills:`", msgs)
        self.assertIn("must match the file name", msgs)


class RepoAgents(unittest.TestCase):
    def test_repo_agents_including_around_phase_pass(self):
        report = check.Report()
        check.check_agents(Path(check.__file__).resolve().parents[1], report)
        self.assertEqual([m for _, _, s, m in report.items if s == "ERROR"], [])

    def test_bad_phase_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            (repo / "agents").mkdir()
            (repo / "agents" / "x.md").write_text("---\ntype: Agent\nname: x\ndescription: d\nphase: sideways\nskills: [s]\nreads: [a]\nwrites: []\n---\n# X\n", encoding="utf-8")
            report = check.Report()
            check.check_agents(repo, report)
            self.assertTrue(any("phase" in m for _, _, _, m in report.items))


class I18n(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "templates").mkdir()
        (self.tmp / "de" / "templates").mkdir(parents=True)
        (self.tmp / "AGENTS.md").write_text("# a\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_missing_translation_and_missing_header(self):
        (self.tmp / "de" / "x.md").write_text("# ohne Kopf\n", encoding="utf-8")
        msgs = " | ".join(messages(run(self.tmp, i18n=True)))
        self.assertIn("translation_of", msgs)
        self.assertIn("no German translation", msgs)

    def test_paired_files_pass(self):
        (self.tmp / "de" / "AGENTS.de.md").write_text(
            "---\ntype: System\ntranslation_of: AGENTS.md\n---\n# de\n", encoding="utf-8")
        self.assertEqual(run(self.tmp, i18n=True).items, [])

    def test_translation_target_must_exist(self):
        (self.tmp / "de" / "y.md").write_text(
            "---\ntranslation_of: nope.md\n---\n", encoding="utf-8")
        self.assertIn("does not exist", " ".join(messages(run(self.tmp, i18n=True))))


class Workbench(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.wb = self.tmp / "Workbench"
        (self.wb / "10_Undertakings" / "a").mkdir(parents=True)
        (self.wb / "20_Material").mkdir()
        (self.wb / "perspective.md").write_text("---\ntype: Perspective\nkind: workbench\n---\n# P\n", encoding="utf-8")
        (self.wb / "20_Material" / "raw.md").write_text("no frontmatter at all\n", encoding="utf-8")
        self.note = self.wb / "10_Undertakings" / "a" / "undertaking.md"

    def write(self, extra_fm="", body="See [C](../Notes/10_Concepts/c.md) for why.\n"):
        self.note.write_text(f"---\ntype: Undertaking\n{extra_fm}---\n# A\n{body}\n## Review status\n- Created: x\n", encoding="utf-8")

    def test_clean_workbench_with_sibling_link_and_raw_material(self):
        self.write()
        self.assertEqual(run(self.wb).items, [])

    def test_kind_is_detected_but_flag_also_works(self):
        self.write()
        (self.wb / "perspective.md").unlink()
        self.assertTrue(messages(run(self.wb)))
        report = check.Report()
        check.check_bundle(self.wb, False, report, workbench=True)
        self.assertEqual(report.items, [])

    def test_visibility_is_an_error_in_a_workbench(self):
        self.write("visibility: public\n")
        self.assertTrue(any("visibility" in m for m in messages(run(self.wb))))

    def test_link_must_go_one_level_up_only(self):
        self.write(body="See [C](../../x/c.md) and [D](../d.md).\n")
        self.assertEqual(sum("one level up" in m for m in messages(run(self.wb))), 2)

    def test_notes_never_link_into_a_workbench(self):
        notes = self.tmp / "Notes"
        (notes / "10_Concepts").mkdir(parents=True)
        (notes / "10_Concepts" / "c.md").write_text(
            "---\ntype: Concept\n---\n# C\nSee [A](../Workbench/10_Undertakings/a/undertaking.md).\n\n## Review status\n- x\n",
            encoding="utf-8")
        self.assertTrue(any("never link into a workbench" in m for m in messages(run(notes))))

    def test_example_and_repo_still_clean(self):
        self.assertEqual(run(ROOT / "example", example=True).items, [])


if __name__ == "__main__":
    unittest.main()
