---
name: capture-inbox
description: Put a raw input (link, excerpt, idea from outside) into 00_Inbox as a short capture note, with minimal friction and no draft.
---

# Capture into the inbox

Follow `AGENTS.md`. Tool-neutral: use whatever file access you have; without it, show the note in the chat.

## Procedure
1. **Take what comes.** A link, a short excerpt, a photo transcript, a few keywords. Do not process it yet; that is the job of Distill.
2. **Check quickly for duplicates.** Use [`find-existing`](../find-existing/SKILL.md) with the title, author or URL. If the source already has a source note or capture, say so and ask whether to add to it instead.
3. **Fill the template.** Use `templates/capture.md`: source (URL, book, date), raw material (short; no long copied passages), one line why it was captured, next step if clear.
4. **Save directly.** No draft needed. File name: `00_Inbox/<short-title>.md`, lowercase-with-hyphens. Sign the review status with your tag.
5. **Report.** One line: what was saved where, and the suggested next step (usually Distill).

## Final check
- `type: Capture`, review status line present, file name rule kept.
- Raw material is short; nothing invented (no guessed author, year or location).
