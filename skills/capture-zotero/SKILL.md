---
name: capture-zotero
description: Pull new highlights from a running local Zotero (read-only) into 00_Inbox, one capture per Zotero item, after asking the person first.
---

# Capture highlights from Zotero

Follow `AGENTS.md` and your agent file. This procedure needs one helper, `tools/zotero_highlights.py` (Python standard library, reads the Zotero local API, changes nothing in Zotero). Run no other command. If you cannot run commands, ask the person to run the command and paste the output.

## When
Only when a capture is about reading (a book, article or paper) or the person mentions Zotero. Ask first: «Check your local Zotero for new highlights?» Do nothing without a yes.

## Procedure
1. **Check Zotero.** Run `python tools/zotero_highlights.py status`.
   - Exit 2: Zotero is not running. Say so and stop. Do not start Zotero.
   - Exit 3: the local API is off. Tell the person to tick Settings → Advanced → «Allow other applications on this computer to communicate with Zotero», then stop.
2. **Fetch.** Either everything new since the last pull, or one named item:
   - New: `python tools/zotero_highlights.py fetch <bundle-dir>`.
   - Named item: `python tools/zotero_highlights.py search "<title or author>"`. If several items match, show the list and let the person choose. Then `python tools/zotero_highlights.py fetch <bundle-dir> --item <KEY>`. This brings all highlights of that item not yet imported and leaves the regular pull untouched.
   The output has one block per Zotero item (`=== ITEM <KEY> ===`) with title, creators, year, Zotero link and the raw material. It reads only the personal library. Ink and image annotations are skipped; report the «Skipped» line.
3. **First pull** («First pull: yes»): before writing anything, show the items with their highlight counts and ask: import everything, choose items, or start from now (record nothing, only the starting point).
4. **Find the existing capture.** Search `00_Inbox` for `zotero_item: <KEY>` (see [`find-existing`](../find-existing/SKILL.md)). If found, add the new highlights to the end of its `## Raw material` and announce the change (file, how many highlights). Otherwise create one capture per item with `templates/capture.md`:
   - Frontmatter: `type: Capture`, `visibility: private` (German bundle: `privat`), `zotero_item: <KEY>`.
   - Title: the item title. File name `00_Inbox/<short-title>.md`, lowercase-with-hyphens.
   - `## Source`: creators, year and title exactly as printed; then the Zotero link as code, not as a Markdown link: `` `zotero://select/library/items/<KEY>` ``. Where the output says «(none in Zotero)», leave it out; never guess.
   - `## Raw material`: the block between `--- RAW MATERIAL` and `--- END ITEM` pasted **unchanged**: exact quotes with page, the owner's Zotero comments as `📝 Your note:` / `📝 Deine Notiz:`. These are excerpts the owner chose; keep all of them, do not shorten, summarise or translate.
   - `## Why captured`: «Highlights from Zotero» plus the date. `## Next step`: usually Distill.
5. **Record the pull, only after every note is saved.** `python tools/zotero_highlights.py mark-done <bundle-dir>`; with chosen items add `--items <KEY> …`; for «start from now» use `--none`. If saving failed, do not run it: the next fetch brings the same highlights again.
6. **Report.** One line per item: what was saved or extended where, and the suggested next step.

## Final check
- The person agreed before Zotero was contacted; only `tools/zotero_highlights.py` was run.
- One capture per Zotero item, `zotero_item:` set, `visibility: private`, review status signed.
- Quotes and pages exactly as fetched; nothing invented (no guessed author, year or page).
- `mark-done` ran only after the notes were saved; `.zotero-sync.json` stays in the bundle root.
