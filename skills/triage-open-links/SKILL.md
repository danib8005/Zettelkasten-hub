---
name: triage-open-links
description: Turn open links, open questions and unprocessed captures into a short, ranked list of next inputs for Capture, Distill and Connect.
---

# Triage open links and questions

Follow `AGENTS.md` and your agent file. Tool-neutral.

## Procedure
1. **Collect.** Open links (the WARN lines of `tools/check.py`), notes in `50_Open-Questions/` with status ❓ open, and captures in `00_Inbox/` still marked 📥 unprocessed.
2. **Count demand.** For each open link target: how many notes want it. For each open question: how often it came up and how long it has been open.
3. **Rank** by demand and by closeness to the core topics in `perspective.md`. Keep the list short (five to ten items).
4. **Assign the next phase** per item: needs a source → Capture; a capture waits → Distill; the material exists but the note does not → Connect; no longer relevant → propose dropping (the person decides; nothing is deleted).
5. **Report** the ranked list with one line each: item, reason, next phase and agent.

## Final check
- The list is short and ranked; every item names its next phase.
- Nothing was created, changed or deleted by the triage itself.
