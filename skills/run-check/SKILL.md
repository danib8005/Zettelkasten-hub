---
name: run-check
description: Run tools/check.py on a bundle, explain the findings grouped by cause, and propose fixes per file and line.
---

# Run the structure check

Follow `AGENTS.md` and your agent file. Tool-neutral: if you cannot run commands, ask the person to run the command and paste the output.

## Procedure
1. **Run the checker** from the repository root:
   `python tools/check.py <bundle-dir>`  (for the example bundle add `--example`; for the repository itself `python tools/check.py --i18n .`).
2. **Read the output.** Each line is `file:line: LEVEL message`. ERROR must be fixed; WARN is for judgement.
3. **Explain the findings** in plain words, grouped by cause, most important first:
   - missing `type:` → add the frontmatter field matching the template in `templates/`;
   - file name → rename to lowercase-with-hyphens, no umlauts (source notes: `lastname-year-shorttitle.md`), and update links;
   - missing review status → add the closing review block from the template;
   - link not bundle-relative → rewrite as `[Title](/folder/file.md)`;
   - open link (WARN) → allowed; it is a to-do list entry. Hand the list to [`triage-open-links`](../triage-open-links/SKILL.md).
4. **Propose fixes, do not apply silently.** Show what you would change per file and line; apply after confirmation. Never delete notes.
5. **Report.** One short summary: number of errors and warnings before and after, what remains, what needs the owner's decision.

## Final check
- The checker was run (or its output was provided), not guessed.
- Every proposed fix names file and line.
- Nothing was changed without confirmation.
