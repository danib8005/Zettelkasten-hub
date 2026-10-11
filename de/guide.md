---
type: System
translation_of: docs/guide.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist docs/guide.md. -->
# Anleitung: dein eigenes Bundle in 30 Minuten

Du brauchst: einen Klon dieses Repos, einen Texteditor, Python 3 und einen Agenten (oder ein Chat-Werkzeug für `pack.md`).

## 1. Klonen und umsehen
```
git clone https://github.com/danib8005/Zettelkasten-Hub.git
cd Zettelkasten-Hub
python tools/check.py example --example
```
In `example/` siehst du ein Bundle. Dein eigenes ist ein neuer Ordner, z. B. `meinbundle/`, mit `00_Inbox`, `10_Concepts`, `40_Sources`, `50_Open-Questions`, `70_Tools`, `95_System`.

## 2. `perspective.md` ausfüllen
`templates/perspective.md` nach `meinbundle/perspective.md` kopieren. `language:` setzen (en oder de), Kürzel, Zweck, zwei oder drei Kernthemen und Ankerpunkte. Fünf Minuten, kurz halten.

## 3. Erste Source Note
Ein Buch oder ein Artikel, den du gut kennst. `templates/source-lightweight.md` nach `meinbundle/40_Sources/nachname-jahr-kurztitel.md` kopieren. 3–6 Kernaussagen paraphrasieren, eigenen Gedanken unter `📝 Deine Notiz:` ergänzen. Keine langen Passagen kopieren.

## 4. Erstes Konzept
`templates/concept.md` nach `meinbundle/10_Concepts/<konzept>.md` kopieren. Kernidee in 2–3 Sätzen, Quelle nennen, verlinken als `[Titel](/40_Sources/deine-notiz.md)` mit Begründung. Links auf noch fehlende Notizen sind erlaubt.

## 5. Erste Frage
Zum Agenten: *«Folge skills/answer. [Deine Frage]»* Prüfe, dass jede Aussage eine Notiz nennt und die Antwort Lücken ausweist. Mit *«Warum diese Zettel?»* erfährst du die Auswahl. Ohne Dateizugriff: `python tools/pack.py meinbundle -k <stichworte> -s answer`, dann `pack.md` hochladen oder einfügen.

## 6. Bundle prüfen
```
python tools/check.py meinbundle
```
Jeden ERROR beheben; Warnungen zu offenen Links sind deine Bestellliste. Für Hilfe: Agent mit `skills/check`.

## Wie weiter
Wachse Quelle für Quelle. Draft first: Der Agent zeigt neue Notizen erst im Chat. Links zeigen nur zum Allgemeineren (siehe [Diagramme](../docs/diagrams.md)).
