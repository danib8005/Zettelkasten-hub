---
type: Agent
translation_of: templates/agent.md   # Übersetzung, nicht massgebend; beim Kopieren entfernen
name: [Phasenname, klein: capture / distill / connect / answer / maintain]
description: [Ein Satz, was dieser Agent tut und wann man ihn nutzt.]
phase: [1–5]
skills: [skill-a, skill-b]
reads: [Ordner oder Dateien, z. B. 00_Inbox, 40_Sources, perspective.md]
writes: [Ordner, z. B. 40_Sources; leere Liste, wenn er nichts schreibt]
---
# Agent: [Name] (Phase [n] von 5)

## Role
[Ein Satz: wer du in der Schleife bist.] Zeichne deine Arbeit mit `agent:[name]`.

## Goal and when to use
[Was diese Phase erreicht. Konkrete Auslöser: «nutze diesen Agenten, wenn …». Wann stattdessen ein anderer Agent.]

## Reads
- [Ordner oder Datei] — [wofür]

## Writes
- [Ordner] — [welcher Notiz-Typ; unter welcher Bedingung (nach Bestätigung, nach Zustimmung)]
Sonst nichts. Änderungen ausserhalb dieser Ordner sind Vorschläge für den Agenten, dem sie gehören.

## Skills
- [`skill-name`](../skills/skill-name/SKILL.md) — [wann in dieser Phase]

## Phase rules
[Nur die Regeln, die für diese Phase gelten. Gemeinsame Regeln bleiben in AGENTS.md.]

## Handoff
- **Next:** [Phase und Agent] — [Auslöser: wann vorschlagen, was übergeben].
- [Weitere Übergaben oder Abkürzungen.]

## Final check
- [Die kritischen Regeln dieser Phase als kurze Checkliste wiederholen.]
- Jede Aussage hat eine Herkunft; nichts erfunden; nichts gelöscht; nur die Ordner unter Writes berührt.

<!-- Die Abschnittstitel bleiben englisch: tools/check.py prüft sie in agents/. -->
