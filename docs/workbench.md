# Workbench

A workbench is a second bundle for the work you do, next to the notes bundle for what you know. The notes bundle holds knowledge: sources, concepts, syntheses, your own texts. The workbench holds **undertakings**: projects, assignments, workshops, preparations. They differ in the one thing that matters for sharing: an undertaking belongs to a place and a circle of people; a concept does not.

## Why separate
- **Confidentiality by structure, not by list.** Without a workbench, project notes sit inside the notes and every export needs a list of what may leave. With one, an undertaking that must stay on one device simply never is in the other bundle.
- **Each bundle can live where it belongs.** The notes can be copied to several devices (see [architecture](architecture.md), §7); a workbench stays where its undertakings belong, for example one on the work laptop and one on a private computer.
- **One direction of dependence.** Undertakings build on knowledge; knowledge must not depend on an undertaking that may not be there.

## Layout
```
Notes/          the notes bundle (all devices that need it; generated copies elsewhere)
Workbench/      one workbench per confidentiality circle, e.g. Workbench-Work, Workbench-Private
```
Bundles sit side by side. **The notes folder keeps the same name on every device**, because undertakings link to it by relative path.

Inside a workbench:
```
00_Inbox/         unprocessed
10_Undertakings/  one folder per undertaking, with undertaking.md (template: templates/undertaking.md)
20_Material/      slides, PDFs, raw data (no frontmatter required)
30_Decisions/     decisions with reasons that outlive one undertaking
95_System/        templates, system notes
```
Mark a bundle as a workbench in its `perspective.md`: `kind: workbench`.

## Rules
1. **One home per undertaking.** One device, one confidentiality level. If an undertaking spans two circles (for example work and research), make two undertakings and name each other in `counterpart:` as plain text. Nothing is synchronised between workbenches.
2. **Links run one way.** From the workbench into the notes, as a relative path to the sibling folder: `[Concept](../Notes/10_Concepts/x.md)`. The notes never link into a workbench. `tools/check.py` flags both mistakes.
3. **Knowledge comes back only by promotion.** What an undertaking taught you and what holds without it is written anew as a general, anonymised note in the notes bundle, as a draft first. Files are never moved or copied from an undertaking into the notes. The section "May become a note" in the template collects the candidates.
4. **A mixed file is split, not synchronised.** The part that only exists because of the undertaking stays; the general part becomes a note.
5. **Nothing is exported from a workbench.** `tools/export.py` refuses a bundle with `kind: workbench`, and `visibility:` has no meaning there (`tools/check.py` reports it).
6. **Reflections stay out of work tools.** Personal reflections (experience logs, feedback reports, notes on individuals) belong in a private workbench or the private notes, even when they are about work.
7. **People by role.** Use a role or an agreed abbreviation, as in `AGENTS.md`.

## Promotion (procedure)
Knowledge first: a new question or analysis becomes a note, not an undertaking. When a document in an undertaking holds knowledge:
1. **Split the strands.** Separate what exists only because of the undertaking (assignment, names, numbers, status) from what holds without it.
2. **Choose the type per strand.** A synthesis only if the sources it combines are in the notes; otherwise a concept or thought. Literature the owner knows without a source note is labelled «prior knowledge».
3. **Check the notes first.** Is the general part already there? Then link, do not duplicate.
4. **Anonymise and write anew.** Put the experience context at the top as the owner's own note, without organisation names or figures.
5. **Draft first,** then save. Afterwards the undertaking may link to the note (one way).

## Check
`python tools/check.py Workbench --workbench` (or just the path, when `perspective.md` says `kind: workbench`). It checks structure and review status like for notes, allows `../<notes-folder>/…` links, and reports `visibility:`.

## Not built yet
- A promotion skill that automates the procedure above (undertaking → draft note, with anonymisation check).
- Skills around undertakings: briefing, to-dos, plan, presentation.
- A backup rule for a workbench that lives on one device only: that is the owner's decision.
