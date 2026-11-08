---
type: System
translation_of: docs/claude-project.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist docs/claude-project.md. -->
# Claude-Projekte (gehostete Assistenten-Projekte) und die Werkbank

Ein gehostetes Assistenten-Projekt (zum Beispiel ein Claude-Projekt) ist ein **Arbeitsraum** für ein Vorhaben, kein Zuhause. Es hält Anweisungen, hochgeladene Daten und den Chatverlauf. Es ist an ein Produkt gebunden; eine Werkbank besteht aus einfachen Dateien und läuft mit jedem Modell. Darum bleibt die Werkbank der Normalfall, und ein Projekt braucht einen Grund.

## Wann sich ein Projekt lohnt
Test: *Könnte ich morgen mit einem anderen Modell weiterarbeiten?* Wenn ja, bleibt das Vorhaben in der Werkbank.

Ein Projekt ist sinnvoll, wenn mindestens eines zutrifft:
- viele Dokumente oder Uploads, die als Projektwissen durchsuchbar sein sollen,
- Funktionen des Produkts selbst, etwa Projektgedächtnis oder gemeinsame Arbeit mit anderen,
- ein Vorhaben über viele Sitzungen und Wochen.

Es bleibt in der Werkbank, wenn es kurz ist, wenige Dateien hat, ein einmaliges Ergebnis liefert oder vertrauliche Arbeitsdaten enthält, die nicht in ein privates Cloud-Projekt gehören. (Prüfe die Regeln deines Arbeitgebers; das kann dieser Leitfaden nicht entscheiden.)

Schwellenwerte (etwa «länger als vier Wochen») sind Startwerte: an echten Fällen prüfen.

## Was die Werkbank behält
Eine kleine Datei pro Projekt: `project.md` (Vorlage: `templates/project.md`), im Vorhabenordner oder daneben. Sie hält Zweck, Ort des Projekts, Status, Kreis (privat oder Arbeit) und am Ende das Abschluss-Kondensat fest. Anweisungen, Daten und Chatverlauf bleiben im Projekt, solange es läuft.

## Abschluss-Kondensat (5 bis 10 Zeilen)
Geschrieben, wenn das Projekt endet, oder bei einem Meilenstein:
1. **Allgemeine Erkenntnisse** gehen als Beförderungs-Entwurf in die Notizen (siehe [Werkbank](workbench.md), «Beförderung»).
2. **Erkenntnisse nur für dieses Thema oder diesen Kunden** bleiben als kurzer Rückblick in der Werkbank, für ein ähnliches Vorhaben.
3. **Quellen**, die im Projekt gelesen wurden und noch nicht in den Notizen sind, werden Source Notes.
4. **Ergebnisse** (Folien, Texte) werden als Dateien gesichert. Die Projektanweisung bleibt nur, wenn sie sich wiederzuverwenden lohnt.

Verschwindet das Projekt, bevor das Kondensat geschrieben ist, gehen Anweisung und Verlauf verloren. Das ist der bewusst akzeptierte Preis einer dünnen Referenz; die Abschlussregel schützt das Wissen.

## Die Notizen aus einem Projekt nutzen
Das Projekt liest die Notizen; es schreibt nie in Konzepte oder Synthesen. Neues Wissen zeigt es als Entwurf. Der Zugang hängt von der Umgebung ab: verbundener Ordner (die Notizen als Geschwisterordner), Repository oder ein Paket ausgewählter Notizen (`tools/pack.py`). Dieser Block gehört in die Anweisung jedes Projekts:

> **Wissensbasis.** Die Notizen des Besitzers sind die Quelle für Wissen. Zuerst `AGENTS.md` und die Arbeitsweise-Datei lesen (verbundener Ordner, Repository oder Notizpaket). Jede Aussage nennt ihre Herkunft: Notizpfad, «Vorwissen» oder «nicht in den Notizen». Nichts erfinden, auch keine Zitate oder Fundstellen. Neues Wissen nur als Entwurf zeigen; nie direkt in Konzepte oder Synthesen schreiben. Verfahren stehen in `skills/<name>/SKILL.md`; bei Bedarf die passende lesen.
>
> **Arbeitsweise.** [Kurzfassung der Arbeitsweise-Datei des Besitzers]

Die Arbeitsweise-Datei ist die eigene, werkzeugneutrale Beschreibung, wie der Besitzer zusammenarbeiten will (Entwürfe zuerst, Ton, Feedback, Marker). Sie liegt einmal in den Notizen und wird in Kurzform in die Anweisung kopiert.

## Skills
Skills werden nicht in Projekte kopiert. Die Anweisung nennt, wo sie liegen und welche zu welcher Aufgabe passt. Skills für Wissensarbeit gehören zu den Notizen; Skills für Vorhaben gehören zur Werkbank oder zum Hub.
