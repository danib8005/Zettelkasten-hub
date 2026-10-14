---
type: System
translation_of: AGENTS.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Agenten lesen die englische AGENTS.md. -->
# AGENTS.md — Zettelkasten-Hub (deutsche Lesefassung)

Gemeinsamer Kern für jeden Agenten, der in einem Wissens-Bundle (Ordner mit Markdown-Notizen) arbeitet. Zuerst diese Datei lesen, dann die Agenten-Datei der eigenen Phase in `agents/`.

## Nie brechen
- Aus den Notizen arbeiten, mit Quellen; sagen, was fehlt. Jede Aussage nennt ihre Herkunft (Notizpfad, eigene Notiz oder «nicht im Zettelkasten»).
- Nie Zitate, Fundstellen oder Quellen erfinden. Allgemeinwissen als «nicht aus den Notizen» kennzeichnen, Hypothesen als Hypothesen.
- Nichts ohne Auftrag löschen. Jede Änderung an einer bestehenden Notiz ankündigen (was, warum).
- Notizen ohne `visibility: öffentlich` werden nie geteilt oder exportiert.

## Die Schleife
Capture → Distill → Connect → Answer → Maintain → zurück zu Capture. Die Person wählt den Agenten; jeder Agent schlägt am Ende den nächsten vor.
| Phase | Agent | Tut | Schreibt |
|---|---|---|---|
| 1 Capture | `agents/capture.md` | nimmt Rohes und eigene Gedanken auf | `00_Inbox`, Gedanken in `10_Concepts` |
| 2 Distill | `agents/distill.md` | macht aus einer Quelle eine Source Note | `40_Sources` |
| 3 Connect | `agents/connect.md` | Konzepte, Frameworks, Synthesen, Tools; Links mit Begründung | `10_Concepts`, `20_Frameworks`, `30_Syntheses`, `70_Tools` |
| 4 Answer | `agents/answer.md` | antwortet aus den Notizen, nennt Lücken | `50_Open-Questions` (nach Zustimmung) |
| 5 Maintain | `agents/maintain.md` | prüft Struktur und Review-Status, macht Lücken zu nächsten Eingaben | Korrekturen nach Bestätigung |
Eine Agenten-Datei nennt Rolle, was gelesen und geschrieben wird, die Skills (`skills/<name>/SKILL.md`, Schritt-für-Schritt-Verfahren) und die Übergabe. Ohne Agenten-Unterstützung: die Agenten-Datei der Phase lesen, in der man arbeitet.
Format: Markdown mit YAML-Frontmatter nach dem Open Knowledge Format (siehe [de/standards.md](standards.md)). Die Perspektive der Besitzerin oder des Besitzers (Themen, Ankerpunkte, Autorinnen, Sprache) steht in `perspective.md`; für inhaltliche Arbeit lesen, nicht für reine Wartung.

## Struktur
`00_Inbox` Unverarbeitetes · `10_Concepts` Konzepte und Gedanken · `20_Frameworks` · `30_Syntheses` · `40_Sources` Source Notes · `50_Open-Questions` offene Fragen, Link-Verdikte · `70_Tools` Checklisten, Formate, Entscheidungshilfen · `95_System` Vorlagen, Systemnotizen. Nur anlegen, was nötig ist. `index.md` und `log.md` sind reservierte Dateinamen (optional).

## Notiz-Typen
Vorlagen in `templates/<name>.md`; der Typ steht im Frontmatter als `type:` (freier Text, englisch oder deutsch). Capture · Gedanke · Konzept (1–2 Seiten) · Framework (3–5 Seiten) · Synthese · Source · Tool · Offene Frage.

## Konventionen
- Dateinamen: klein-mit-bindestrichen.md, keine Umlaute (ä→ae); Source Notes `nachname-jahr-kurztitel.md`.
- Frontmatter: `type:` Pflicht; `aliases:` (Liste) für Namensvarianten; `visibility:` (privat | team | öffentlich) steuert das Teilen, fehlt es, gilt privat.
- Links: Standard-Markdown, bundle-relativ `[Titel](/10_Concepts/datei.md)`, Linktext = Titelzeile des Ziels, immer mit Begründung. Fehlende Ziele sind erlaubt (Bestellliste). Keine Wikilinks.
- Zitate in der Originalsprache, mit Fundstelle, wenn vorhanden.
- Sprache: laut `perspective.md` (`language:`); Notizen bleiben in der Sprache der Quelle; Antworten in der Sprache der Frage.
- Annotationen: `📝 Deine Notiz:`, `📝 Synthese:`, `📝 Agent:`; nie vermischen.
- Review-Status am Ende jeder Notiz: erstellt, letztes Review, ✓ aktuell / ⚠️ veraltet / 🔄 in Überarbeitung. Kürzel pro Person; jeder Agent zeichnet mit eigenem Tag (`agent:capture`, `agent:distill`, …).
- Personen: Source Notes mit echten Namen; Projekt- und Reflexionsnotizen mit Rolle oder vereinbartem Kürzel. Bei Pseudonymen die Schlüsseltabelle ausserhalb jeder exportierbaren Notiz halten und nie exportieren. Pseudonymisierung ist keine Anonymisierung.

## Qualitätsprinzipien (alle Phasen)
1. **Belegt antworten:** jede Aussage mit Herkunft; Lücken benennen; Deutung und Hypothesen kennzeichnen.
2. **Präzise und einfach:** Kernaussage zuerst, in einem Satz. Eine Standarddefinition pro Konzept: verlinken statt neu definieren.
Die Prinzipien 3–5 gelten für einzelne Phasen und stehen in den Agenten-Dateien.

## Werkzeuge
`tools/check.py` prüft Struktur und Formatkonformität. `tools/pack.py` bündelt diese Regeln, einen Agenten (oder einen Skill) und ausgewählte Notizen in eine Datei für Chat-Werkzeuge ohne Dateizugriff. `tools/catalog.py` erstellt einen Katalog der Source Notes.

## Vertraulichkeit (zuletzt lesen)
- Notizen ohne `visibility: öffentlich` werden nie geteilt oder exportiert.
- Wörtliche Buchzitate bleiben aus öffentlichen Bundles heraus; Paraphrase mit Quelle.
- Nie Zitate, Fundstellen oder Quellen erfinden. Nichts ohne Auftrag löschen.
