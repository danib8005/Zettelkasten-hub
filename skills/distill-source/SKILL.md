---
name: distill-source
description: Turn one book, article or talk into a source note (lightweight by default, full for dense books and reports), organised by theme, with paraphrase and locations.
---

# Distill a source

Follow `AGENTS.md` and your agent file. Tool-neutral: read the source the person provides (file, text, transcript, their own notes on it).

## Procedure
1. **Choose the template.** `templates/source-lightweight.md` by default; `templates/source-full.md` only for dense books and reports. One source note per book, article or author series; a second one only for a real theoretical break.
2. **Read the material.** Use only what is in the source or in the person's notes on it. If parts are missing (no access to the full text), say which parts the note is based on.
3. **Write the core thesis** in one or two sentences.
4. **Pick the key statements** that carry the argument; organise by theme, not by chapter. Paraphrase; quote briefly, in the original language, with location when available. Never invent a quote, a location or a bibliographic detail; leave a gap marked `[?]` instead.
5. **Keep the owner's voice separate.** Their comments go after `📝 Your note:` / `📝 Deine Notiz:`, wording kept; your additions after `📝 Agent:`.
6. **Links.** To concepts the source supports or challenges, each with a reason. To other source notes only on direct relation (builds on, criticises).
7. **Hand over to [`draft-first`](../draft-first/SKILL.md).** After saving, list the concepts and syntheses the new source touches; if the source came from `00_Inbox`, name the capture so that Maintain can mark it as processed (Distill writes only `40_Sources`).

## Final check
- Core thesis first; only what carries the argument.
- Every quote has a source; no invented location; nothing copied at length.
- Source-to-source links only on direct relation.
