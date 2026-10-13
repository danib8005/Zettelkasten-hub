---
type: System
translation_of: docs/guide.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist docs/guide.md. -->
# Anleitung: dein eigenes Bundle in 30 Minuten

Du brauchst: einen Klon dieses Repos, einen Texteditor, Python 3 und einen Agenten (oder ein Chat-Werkzeug für `pack.md`).
Die Arbeit läuft in einer Schleife aus fünf Phasen (Capture → Distill → Connect → Answer → Maintain), je ein Agent; siehe [Wie es funktioniert](../README.de.md#wie-es-funktioniert). Diese Anleitung geht sie einmal durch.

## 1. Klonen und umsehen
```
git clone https://github.com/danib8005/Zettelkasten-Hub.git
cd Zettelkasten-Hub
python tools/check.py example --example
```
In `example/` siehst du ein Bundle. Dein eigenes ist ein neuer Ordner, z. B. `meinbundle/`, mit `00_Inbox`, `10_Concepts`, `40_Sources`, `50_Open-Questions`, `70_Tools`, `95_System`. `20_Frameworks` und `30_Syntheses` bei Bedarf ergänzen.

## 2. `perspective.md` ausfüllen
`templates/perspective.md` nach `meinbundle/perspective.md` kopieren. `language:` setzen (en oder de), Kürzel, Zweck, zwei oder drei Kernthemen und Ankerpunkte. Fünf Minuten, kurz halten.

## 3. Erste Source Note
Ein Buch oder ein Artikel, den du gut kennst. `templates/source-lightweight.md` nach `meinbundle/40_Sources/nachname-jahr-kurztitel.md` kopieren. 3–6 Kernaussagen paraphrasieren, eigenen Gedanken unter `📝 Deine Notiz:` ergänzen. Keine langen Passagen kopieren.
Oder den Agenten **distill** machen lassen: *«Folge agents/distill.md. Mach eine Source Note aus [Quelle].»* Er zeigt zuerst einen Entwurf und speichert erst nach Bestätigung. Etwas zum späteren Lesen geht stattdessen an den Agenten **capture**, der es in `00_Inbox` ablegt.

## 4. Erstes Konzept
`templates/concept.md` nach `meinbundle/10_Concepts/<konzept>.md` kopieren. Kernidee in 2–3 Sätzen, Quelle nennen, verlinken als `[Titel](/40_Sources/deine-notiz.md)` mit Begründung. Links auf noch fehlende Notizen sind erlaubt. Der Agent **connect** hilft bei Konzepten, Synthesen, Frameworks und Tools, ebenfalls Draft first.

## 5. Erste Frage
Den Agenten **answer** wählen (oder zum Agenten: *«Folge agents/answer.md. [Deine Frage]»*). Prüfe, dass jede Aussage eine Notiz nennt und die Antwort Lücken ausweist. Mit *«Warum diese Zettel?»* erfährst du die Auswahl. Findet die Antwort eine Lücke, die du behalten willst, stimmst du zu und sie landet in `50_Open-Questions`. Ohne Dateizugriff: `python tools/pack.py meinbundle -k <stichworte> -a answer`, dann `pack.md` hochladen oder einfügen.

## 6. Bundle prüfen
```
python tools/check.py meinbundle
```
Jeden ERROR beheben; Warnungen zu offenen Links sind deine Bestellliste. Der Agent **maintain** erklärt die Befunde, schlägt Korrekturen vor, prüft Notizen und macht aus offenen Links und offenen Fragen eine kurze Liste, was als Nächstes zu erfassen oder zu schreiben ist. Damit schliesst sich die Schleife.

## Wie weiter
Wachse Quelle für Quelle, Runde für Runde. Draft first: Distill und Connect zeigen neue Notizen erst im Chat. Links zeigen nur zum Allgemeineren (siehe [Diagramme](../docs/diagrams.md)).
