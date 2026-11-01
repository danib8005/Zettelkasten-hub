---
type: Export profile
name: work
audience: owner
folders: [40_Sources, 70_Tools]
visibility: [team, public]
include: []
exclude: []
strip-quotes: false
leak-terms: 95_System/people-key.md
---
# Export profile: [target, e.g. work laptop]

Use with `python tools/export.py BUNDLE_DIR THIS_FILE -o OUT_DIR` (add `--dry-run` first). The frontmatter above is the profile; this text is for people.

## What the keys mean
- `audience`: who may read the copy: `owner` (only you, on your own device), `team` or `public`. Required. Verbatim book quotes only go into an owner copy; for the others `strip-quotes` must be `true`.
- `folders`: note folders to take from. A note needs `visibility:` with one of the listed values; without it a note is private.
- `include`: paths or globs you approve by name, e.g. `65_Consulting/project-a/**`. These notes need no `visibility:`; a note marked `private` is never exported.
- `exclude`: paths or globs that never leave, whatever else says yes.
- `strip-quotes`: `true` drops blockquotes and Loc./S. references (for copies others will read).
- `leak-terms`: a file in the bundle with names that must not appear in the copy (a table with a «Name» column, or one term per line). It is never exported.

## Why this target gets what it gets
[One or two sentences: which device or tool, who sees it, what is deliberately left out.]

---

## Review status
- **Created:** [YYYY-MM-DD] by [initials]
- **Last review:** [YYYY-MM-DD] by [initials]
- **Review status:** ✓ current / ⚠️ outdated / 🔄 under revision
