---
name: write
description: Create or revise a note (thought, concept, framework, synthesis, source, tool) draft-first, with sources, links with reasons and the right template.
---

# Write a note

Follow the rules in `AGENTS.md`. Tool-neutral: use whatever file access you have; without it, show the draft in the chat.

## Procedure
1. **Pick the type.** Raw idea → thought. One idea in 1–2 pages → concept. A reusable way of thinking with components and guiding question → framework. Several sources in tension → synthesis. One book/article/talk → source (lightweight; full only for dense books and reports). A usable checklist or method → tool. Take the template from `templates/`.
2. **Check what exists.** Search for the key terms and `aliases:`. If a concept with this idea exists, extend or link it instead of creating a duplicate; if the idea exists under another name, add an alias.
3. **Gather the material.** Read the sources the person points to. Use only what is in them or in the notes; never invent a quote, a location or a source. Prefer paraphrase; quote briefly, with source.
4. **Draft in the chat first.** Show: the note (filled template, core statement first), the context (what it relates to), the links with a reason each, one or two questions to think about. Questions stay out of the note.
5. **Type-specific care.**
   - Source: organise by theme, not by chapter; keep only what carries the argument; link to other sources only on direct relation.
   - Concept: one standard definition in the core idea; other notes link instead of redefining.
   - Synthesis: make divergences visible; label each divergence combinable / conflicting / incommensurable; mark emergent insights as hypotheses.
   - Framework: name the guiding question; say where it fits and where it does not.
   - Thought: keep the raw wording; do not polish it away.
6. **Save after confirmation.** Use the file naming rule, set `type:`, add the review status block with the agent tag. Open links are fine.
7. **Afterwards.** Suggest affected notes to review (new source → concepts and syntheses that use it) and run `python tools/check.py <bundle>`.

## Final check
- Template followed; core statement first; every statement has an origin.
- Links are bundle-relative, each with a reason; no wikilinks.
- Nothing saved without confirmation; nothing deleted.
