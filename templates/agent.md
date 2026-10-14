---
type: Agent
name: [phase name, lowercase: capture / distill / connect / answer / maintain]
description: [One sentence: what this agent does and when to use it.]
phase: [1–5, or `around` for agents beside the loop]
skills: [skill-a, skill-b]
reads: [folders or files, e.g. 00_Inbox, 40_Sources, perspective.md]
writes: [folders, e.g. 40_Sources; empty list if it writes nothing]
---
# Agent: [Name] (phase [n] of 5)

## Role
[One sentence: who you are in the loop.] Sign your work as `agent:[name]`.

## Goal and when to use
[What this phase achieves. Concrete triggers: "use this agent when …". When to use another agent instead.]

## Reads
- [Folder or file] — [what for]

## Writes
- [Folder] — [which note type; under which condition (after confirmation, after consent)]
Nothing else. Changes outside these folders are proposals for the agent that owns them.

## Skills
- [`skill-name`](../skills/skill-name/SKILL.md) — [when to use it in this phase]

## Phase rules
[Only the rules that apply to this phase. Shared rules stay in AGENTS.md.]

## Handoff
- **Next:** [phase and agent] — [trigger: when to suggest it, what to pass on].
- [Other handoffs or shortcuts.]

## Final check
- [Repeat the critical rules of this phase as a short checklist.]
- Every statement has an origin; nothing invented; nothing deleted; only the folders under Writes touched.
