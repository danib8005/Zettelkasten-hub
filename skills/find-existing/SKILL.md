---
name: find-existing
description: Search the bundle for notes that already cover a term, source or idea (including aliases), to extend or link instead of duplicating.
---

# Find what already exists

Follow `AGENTS.md`. Tool-neutral: use whatever search you have (file search, grep, the notes in a pack file).

## Procedure
1. **Collect search terms.** The key terms, their synonyms and translations (the bundle may mix languages), author names, the year, the URL.
2. **Search.** Titles and full text in the folders that matter for the task, plus `aliases:` in the frontmatter. For sources also search `00_Inbox/` for an unprocessed capture.
3. **Rate the hits.** Same idea / same source → extend or link, do not create a new note. Same idea under another name → propose an alias. Related but different → candidate link with a reason.
4. **Report.** List the hits as `/folder/file.md` with one line each: same, alias, or related (and why). Say plainly if nothing was found.

## Final check
- Aliases and other languages were searched, not only the literal term.
- The verdict per hit is stated; no note is created or changed by this skill.
