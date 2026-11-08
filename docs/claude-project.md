---
type: System
---
# Claude projects (hosted assistant projects) and the workbench

A hosted assistant project (for example a Claude project) is a **working space** for an undertaking, not a home. It holds instructions, uploaded data and the chat history. It is tied to one product; a workbench is plain files and works with any model. So the workbench stays the default, and a project needs a reason.

## When a project is worth it
Test: *Could I continue tomorrow with another model?* If yes, keep the undertaking in the workbench.

A project makes sense when at least one holds:
- many documents or uploads that should be searchable as project knowledge,
- features of the product itself, such as project memory or shared work with others,
- an undertaking that runs over many sessions and weeks.

It stays in the workbench when it is short, has few files, produces a single result, or holds confidential work data that must not go into a private cloud project. (Check your employer's rules; this guide cannot decide that for you.)

Any thresholds (such as "longer than four weeks") are starting values: test them on real cases.

## What the workbench keeps
One small file per project: `project.md` (template: `templates/project.md`), in the undertaking folder or next to it. It records purpose, where the project is, status, circle (private or work), and, at the end, the closing digest. Instructions, data and chat history stay in the project while it runs.

## Closing digest (5 to 10 lines)
Written when the project ends, or at a milestone:
1. **General findings** go to the notes as a promotion draft (see [workbench](workbench.md), "Promotion").
2. **Findings that hold only for this topic or client** stay in the workbench as a short retrospective, for a similar undertaking.
3. **Sources** read in the project and not yet in the notes become source notes.
4. **Results** (slides, texts) are saved as files. The project instruction is kept only if it is worth reusing.

If the project disappears before the digest is written, the instruction and history are lost. That is the accepted price of a thin reference; the closing rule is what protects the knowledge.

## Using the notes from a project
The project reads the notes; it never writes into concepts or syntheses. New knowledge is shown as a draft. Access depends on the setting: a connected folder (the notes as sibling folder), a repository, or a pack of chosen notes (`tools/pack.py`). Put this block into the instruction of every project:

> **Knowledge base.** The owner's notes are the source for knowledge. Read `AGENTS.md` and the working-style file first (connected folder, repository or note pack). Every statement names its origin: note path, "prior knowledge" or "not in the notes". Invent nothing, including quotes and locations. Show new knowledge only as a draft; never write directly into concepts or syntheses. Procedures are in `skills/<name>/SKILL.md`; read the fitting one when needed.
>
> **Working style.** [short version of the owner's working-style file]

The working-style file is the owner's own, tool-neutral description of how they want to work together (drafts first, tone, feedback, markers). It is kept once in the notes and copied in short form into the instruction.

## Skills
Skills are not copied into projects. The instruction names where they are and which fits which task. Skills for knowledge work belong to the notes; skills for undertakings belong to the workbench or the hub.
