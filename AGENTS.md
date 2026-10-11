# AGENTS.md — Zettelkasten-Hub

Rules for any agent working in a knowledge bundle (a folder of Markdown notes). Core principle: answer from the notes, with sources; say what is missing.
Format: plain Markdown with YAML frontmatter, aligned with the Open Knowledge Format (see [docs/standards.md](docs/standards.md)). The owner's perspective (topics, anchors, authors, language) is in `perspective.md`; read it for substantive work (answering, linking), not for plain maintenance.

## Structure
| Folder | Content |
|---|---|
| 00_Inbox | unprocessed captures |
| 10_Concepts | concept and thought notes |
| 20_Frameworks | frameworks (operative tools for thinking, 3–5 pages) |
| 30_Syntheses | syntheses across several sources |
| 40_Sources | source notes (books, articles, talks) |
| 50_Open-Questions | open questions, link verdicts |
| 70_Tools | checklists, formats, decision aids |
| 95_System | templates, system notes |
Create only the folders you need. `index.md` and `log.md` are reserved file names (optional overview and change history).

## Note types
Templates: `templates/<name>.md` (single source). The type is set in the frontmatter as `type:`; its value is free text (English or German: Thought/Gedanke, Concept/Konzept, Synthesis/Synthese).
- Thought (raw idea) · Concept (1–2 pages) · Framework (3–5 pages) · Synthesis · Source · Tool.
- Source notes: `source-lightweight` by default; `source-full` only for dense books and reports.
- Granularity: one source note per book, article or author series; a second one only for a real theoretical break.

## Conventions
- File names: lowercase-with-hyphens.md, no umlauts (ä→ae). Source notes: `lastname-year-shorttitle.md`.
- Frontmatter: `type:` is required in every note. `aliases:` (list) for name variants. `visibility:` (private | team | public; German privat | team | öffentlich is equivalent) controls sharing; if missing, private.
- Links: standard Markdown, relative to the bundle root: `[Title](/10_Concepts/file.md)`. Link text is the target's title line. Always give a reason, ideally both ways. Targets that do not exist yet are allowed (a to-do list). No wikilinks.
- Links point only to the more general (project → own bundle → shared bundle → core), never the other way.
- Citations: quote in the original language, with location when available. Never invent quotes, locations or sources.
- Language: set in `perspective.md` (`language:`). Notes keep the language of their source; you answer in the language of the question.
- Annotation markers, in the bundle's language: your own note (`📝 Your note:` / `📝 Deine Notiz:`), synthesis (`📝 Synthesis:`), agent addition (`📝 Agent:`). Never mix them.
- Review status at the end of each note: created, last review, ✓ current / ⚠️ outdated / 🔄 under revision. Initials per author; agents use their own tag.
- `Level:` / `Ebene:` (optional): the scale a concept acts on: micro, meso or macro; ranges allowed. Interaction is not a level.
- People: source notes use real names; project and reflection notes use a role or an agreed abbreviation.

## Quality principles
1. **Answer with sources.** Every statement names its origin (source note, concept, own note, or «not in the notes»). Name gaps. Mark interpretation and hypotheses as such. Never present general knowledge as a finding; if you add it, label it «not from the notes».
   Explain *why these notes* only when asked («Warum diese Zettel?»). Keep the answer short; the reasoning must stay retrievable.
2. **Precise and simple.** Core statement first, in one sentence. One standard definition per concept: link instead of redefining. Source notes hold only what carries the argument.
3. **Draw from the material.** Let the material speak before attaching it to favourite topics. Save the owner's own thoughts as separate thought notes.
4. **Keep several perspectives.** Record agreement and contradiction; approaches may be combinable, conflicting or incommensurable.
5. **Source notes link to each other only on direct relation** (builds on, criticises). Thematic cross-links belong in a concept or synthesis.

## Working method
- Draft first: show a new note in the chat as a draft (content, context, links with reasons, one or two questions to think about). Save only after confirmation. The questions do not go into the note.
- No draft needed for small corrections or inbox captures. Announce changes to existing notes (what, why). Never delete without being asked.
- Procedures are plain Markdown in `skills/<name>/SKILL.md`: `answer`, `write`, `check`.
- `tools/check.py` checks structure and format conformance; `tools/pack.py` bundles rules, a skill and chosen notes into one file for chat tools without file access.

## Confidentiality
- Notes without `visibility: public` are never shared or exported.
- Verbatim quotes from books stay out of any public bundle; use paraphrase with source.
