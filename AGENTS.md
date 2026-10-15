# AGENTS.md — Zettelkasten-Hub

Shared core for every agent working in a knowledge bundle (a folder of Markdown notes). Read this file first, then the agent file for your phase in `agents/`.

## Never break
- Work from the notes, with sources; say what is missing. Every statement names its origin (note path, own note, or «not in the notes»).
- Never invent quotes, locations or sources. Label general knowledge «not from the notes» and hypotheses as hypotheses.
- Never delete without being asked. Announce every change to an existing note (what, why).
- Notes without `visibility: public` are never shared or exported.

## The loop
Capture → Distill → Connect → Answer → Maintain → back to Capture. The person picks the agent; each agent ends by suggesting the next one.
| Phase | Agent | Does | Writes |
|---|---|---|---|
| 1 Capture | `agents/capture.md` | takes in raw input and own thoughts | `00_Inbox`, thoughts in `10_Concepts` |
| 2 Distill | `agents/distill.md` | turns one source into a source note | `40_Sources` |
| 3 Connect | `agents/connect.md` | concepts, frameworks, syntheses, tools; links with reasons | `10_Concepts`, `20_Frameworks`, `30_Syntheses`, `70_Tools` |
| 4 Answer | `agents/answer.md` | answers from the notes, lists gaps | `50_Open-Questions` (after consent) |
| 5 Maintain | `agents/maintain.md` | checks structure and review status, turns gaps into next inputs | fixes after confirmation |
Two optional agents work beside the loop and feed it: `agents/reflect.md` turns inward (challenges a position, brings processed notes back, secures the owner's own thinking) and `agents/explore.md` turns outward (maps where the notes end, finds connections as hypotheses). Explore hands new sources and questions to Capture; Reflect hands the owner's thoughts to Capture and rework to Connect.
An agent file names its role, what it reads and writes, its skills (`skills/<name>/SKILL.md`, step-by-step procedures) and its handoff. Without agent support, read the agent file of the phase you work in.
Format: plain Markdown with YAML frontmatter, aligned with the Open Knowledge Format (see [docs/standards.md](docs/standards.md)). The owner's perspective (topics, anchors, authors, language) is in `perspective.md`; read it for substantive work, not for plain maintenance.

## Structure
`00_Inbox` unprocessed captures · `10_Concepts` concepts and thoughts · `20_Frameworks` · `30_Syntheses` · `40_Sources` source notes · `50_Open-Questions` open questions, link verdicts · `70_Tools` checklists, formats, decision aids · `95_System` templates, system notes. Create only the folders you need. `index.md` and `log.md` are reserved file names (optional overview and change history).

## Note types
Templates: `templates/<name>.md` (single source). The type is set in the frontmatter as `type:`; its value is free text (English or German). Capture · Thought (raw idea) · Concept (1–2 pages) · Framework (3–5 pages) · Synthesis · Source · Tool · Open question.

## Conventions
- File names: lowercase-with-hyphens.md, no umlauts (ä→ae). Source notes: `lastname-year-shorttitle.md`.
- Frontmatter: `type:` is required in every note. `aliases:` (list) for name variants. `visibility:` (private | team | public; German privat | team | öffentlich is equivalent) controls sharing; if missing, private.
- Links: standard Markdown, relative to the bundle root: `[Title](/10_Concepts/file.md)`. Link text is the target's title line. Always give a reason. Targets that do not exist yet are allowed (a to-do list). No wikilinks.
- Citations: quote in the original language, with location when available.
- Language: set in `perspective.md` (`language:`). Notes keep the language of their source; you answer in the language of the question.
- Annotation markers, in the bundle's language: your own note (`📝 Your note:` / `📝 Deine Notiz:`), synthesis (`📝 Synthesis:`), agent addition (`📝 Agent:`). Never mix them.
- Review status at the end of each note: created, last review, ✓ current / ⚠️ outdated / 🔄 under revision. Initials per author; each agent signs with its own tag (`agent:capture`, `agent:distill`, …).
- People: source notes use real names; project and reflection notes use a role or an agreed abbreviation. If you pseudonymise, keep the key table outside any exportable note and never export it. Pseudonymisation is not anonymisation.

## Quality principles (all phases)
1. **Answer with sources.** Every statement names its origin; name gaps; mark interpretation and hypotheses as such.
2. **Precise and simple.** Core statement first, in one sentence. One standard definition per concept: link instead of redefining.
Principles 3–5 apply to single phases and are in the agent files.

## Tools
`tools/check.py` checks structure and format conformance. `tools/pack.py` bundles these rules, one agent (or one skill) and chosen notes into one file for chat tools without file access. `tools/catalog.py` builds a catalog of source notes.

## Confidentiality (read last)
- Notes without `visibility: public` are never shared or exported.
- Verbatim quotes from books stay out of any public bundle; use paraphrase with source.
- Never invent quotes, locations or sources. Never delete without being asked.