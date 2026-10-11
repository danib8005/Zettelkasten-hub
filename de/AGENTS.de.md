---
type: System
translation_of: AGENTS.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Agenten lesen die englische AGENTS.md. -->
# AGENTS.md — Zettelkasten-Hub (deutsche Lesefassung)

Regeln für jeden Agenten, der in einem Wissens-Bundle (Ordner mit Markdown-Notizen) arbeitet. Kernprinzip: aus den Notizen antworten, mit Quellen; sagen, was fehlt.
Die Perspektive der Besitzerin oder des Besitzers (Themen, Ankerpunkte, Autorinnen, Sprache) steht in `perspective.md`.

## Struktur
00_Inbox (Unverarbeitetes) · 10_Concepts (Konzepte, Gedanken) · 40_Sources (Source Notes) · 50_Open-Questions · 70_Tools · 95_System (Vorlagen, Systemnotizen).

## Notiz-Typen
Vorlagen in `templates/<typ>.md`; der Typ steht im Frontmatter als `type:`. Gedanke · Konzept (1–2 Seiten) · Source (eine pro Buch, Artikel, Talk) · Tool. Source Notes standardmässig leicht.

## Konventionen
- Dateinamen: klein-mit-bindestrichen.md, keine Umlaute; Source Notes `nachname-jahr-kurztitel.md`.
- Frontmatter: `type:` Pflicht; `aliases:` für Namensvarianten; `visibility:` (privat | team | öffentlich) steuert das Teilen, fehlt es, gilt privat.
- Links: Standard-Markdown, bundle-relativ `[Titel](/10_Concepts/datei.md)`, immer mit Begründung. Fehlende Ziele sind erlaubt. Keine Wikilinks. Links zeigen nur zum Allgemeineren.
- Zitate in der Originalsprache, mit Fundstelle; nie Zitate oder Quellen erfinden.
- Sprache: laut `perspective.md`; Notizen bleiben in der Sprache der Quelle; Antworten in der Sprache der Frage.
- Annotationen: `📝 Deine Notiz:`, `📝 Synthese:`, `📝 Agent:`; nie vermischen.
- Review-Status am Ende jeder Notiz. `Ebene:` (optional): Mikro, Meso oder Makro, Spannen erlaubt; Interaktion ist keine Ebene.

## Qualitätsprinzipien
1. **Belegt antworten:** jede Aussage mit Herkunft (Quelle, Konzept, eigene Notiz oder «nicht im Zettelkasten»); Lücken benennen; Hypothesen kennzeichnen; Allgemeinwissen nie als Befund ausgeben. Die Auswahlbegründung nur auf Nachfrage («Warum diese Zettel?»).
2. **Präzise und einfach:** Kernaussage zuerst; verlinken statt neu definieren.
3. **Aus dem Material schöpfen;** eigene Gedanken als eigene Gedanken-Notizen sichern.
4. **Mehrere Perspektiven bewahren.**
5. **Source Notes verlinken sich nur bei direkter Beziehung** (baut auf, kritisiert).

## Arbeitsweise
Draft first: neue Notizen erst im Chat zeigen, erst nach Bestätigung speichern. Änderungen ankündigen; nichts ohne Auftrag löschen. Verfahren: `skills/answer`, `skills/check`. Werkzeuge: `tools/check.py`, `tools/pack.py`.

## Vertraulichkeit
Notizen ohne `visibility: öffentlich` werden nie geteilt. Wörtliche Buchzitate bleiben aus öffentlichen Bundles heraus.
