---
type: System
translation_of: docs/architecture.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist docs/architecture.md (dort stehen die Diagramme im Detail). -->
# Technische Architektur

## 1. Ziele und Randbedingungen
- **Belegt antworten und Lücken kennen** (Q1), Argumente präzise halten (Q2), überraschende Verbindungen ermöglichen (Q3, später), den Bestand lebendig halten (Q4, später).
- **Agentenunabhängig:** läuft mit Claude Code, Open-Source-CLIs, GitHub Copilot (Agent-Modus) und über eine hochgeladene Datei mit Chat-Werkzeugen wie M365 Copilot.
- **Keine Bindung:** einfache Dateien, offene Standards ([standards.md](standards.md)), nur Python-Standardbibliothek, kein Dienst zu betreiben.
- **Wissen getrennt vom System:** Der Kern enthält Regeln, Vorlagen, Verfahren und Werkzeuge; Wissen liegt in Bundles.
- Nicht Ziel von MVP 1: Capture-Kanäle, MCP-Server, Hosting, Projektmodul.

## 2. Schichten und Komponenten
Diagramm: [architecture.md](../docs/architecture.md#2-layers-and-components). Strikte Trennung: **Daten** (Markdown) · **Regeln** (`AGENTS.md`) · **Verfahren** (`skills/`) · **Prüfung und Bündeln** (Skripte, ohne KI). Jede Schicht ist austauschbar, ohne die anderen zu berühren.

## 3. Datenmodell
**Bundle-Aufbau** (nur anlegen, was nötig ist): `00_Inbox`, `10_Concepts`, `20_Frameworks`, `30_Syntheses`, `40_Sources`, `50_Open-Questions`, `70_Tools`, `95_System`, dazu `perspective.md` im Bundle-Wurzelordner.

| Typ | Ordner | Vorlage | Zweck |
|---|---|---|---|
| Gedanke | `10_Concepts` | `thought.md` | Rohidee, Originalwortlaut bleibt |
| Konzept | `10_Concepts` | `concept.md` | eine Idee, 1–2 Seiten, die Standard-Definition |
| Framework | `20_Frameworks` | `framework.md` | wiederverwendbare Denkweise, 3–5 Seiten |
| Synthese | `30_Syntheses` | `synthesis.md` | mehrere Quellen in Spannung; Divergenzen sichtbar |
| Source | `40_Sources` | `source-lightweight.md`, `source-full.md` | eine pro Buch, Artikel oder Talk |
| Tool | `70_Tools` | `tool.md` | nutzbare Checkliste, Format oder Methode |

**Identität und Links.** Die Identität einer Notiz ist ihr Pfad im Bundle. Links: `[Titel](/ordner/datei.md)`, immer mit Begründung; Richtung nur zum Allgemeineren; fehlende Ziele sind erlaubt. Eine Notiz trägt `type:` (Pflicht), optional `aliases:` und `visibility:`.

**Autorschaft und Vertrauen.** Der Review-Block hält Erstellung, letztes Review und Status fest, mit Initialen; Agenten führen ein eigenes Kürzel. Annotationsmarker trennen eigene Notiz, Synthese-Bemerkung und Agenten-Ergänzung.

## 4. Komponenten
**`AGENTS.md`**: einzige Quelle der Konventionen; `CLAUDE.md` importiert sie.
**`skills/`**: `answer` (präzisieren, suchen, Quellen bewerten, Antwort mit Herkunft pro Aussage und Lückenliste; Auswahlbegründung nur auf Nachfrage), `write` (Draft-first für jeden Notiz-Typ), `check` (Prüfskript laufen lassen, erklären, Korrekturen vorschlagen). Sie nennen kein Werkzeug.
**`tools/check.py`** (ohne KI, Exit-Code 1 bei Fehlern): `type:` auf jeder `.md` ausser `index.md`/`log.md` (OKF-Konformität), Dateinamen, Review-Status, keine Wikilinks, bundle-relative Links (alles ERROR); fehlende Linkziele und Source-Namen als Warnung; `--example`: keine Zitate, keine `Loc.`/`S.`-Fundstellen, keine Links aus dem Beispiel hinaus (ausser Allow-Liste), `visibility: public`; `--i18n`: jede deutsche Datei nennt `translation_of:`, das Ziel existiert, die Pflichtdokumente haben eine Übersetzung.
**`tools/pack.py`** (ohne KI): wählt Notizen per Stichwort-Punktzahl (Titel zählt dreifach) oder Dateiliste und schreibt eine `pack.md`: Vorspann → `AGENTS.md` → `perspective.md` → gewähltes Verfahren → Notizen, je unter ihrem Pfad als Überschrift. Notizen werden unverändert kopiert. Warnung ab 30'000 Zeichen.

## 5. Wie eine Frage beantwortet wird
Person → Agent: «Folge skills/answer. <Frage>» → Agent liest Regeln und Verfahren → durchsucht das Bundle, liest Treffer, bewertet (Kern / Ergänzung / Rand) → Antwort mit Kernaussage, Aussagen mit Notizpfad, Lückenliste → auf Nachfrage «Warum diese Zettel?» die Auswahl. Ohne Dateizugriff: `python tools/pack.py <bundle> -k <stichworte> -s answer`, dann `pack.md` hochladen oder einfügen.

## 6. Mehrere Bundles (MVP 2, nicht gebaut)
Eigenes und gemeinsames Bundle nebeneinander; `bundles.md` deklariert Einhängepunkte und Zugriff. Das Prüfskript meldet jeden Link vom gemeinsamen ins eigene Bundle. Beiträge fliessen per **Promotion** nach oben (verallgemeinern, pseudonymisieren, hochlegen; Pull-Request oder Inbox-Datei). Ein Projektmodul baut auf denselben Regeln auf.

## 7. Sichtbarkeit und Sicherheit
`visibility:` pro Notiz (privat | team | öffentlich), fehlend heisst privat; nur öffentliche Notizen dürfen exportiert werden. Öffentliche Bundles enthalten keine wörtlichen Buchzitate (`check.py --example` erzwingt das für Beispiele). Skripte lesen und schreiben nur lokale Dateien und senden nichts.

## 8. Entscheide und Kosten
Markdown + Frontmatter nach OKF-Modell (portabel; einige Konventionen sind unsere) · `AGENTS.md` als einzige Regeldatei (agentenübergreifend; unterschiedlich zuverlässig befolgt) · Skills als Markdown (kein Loader nötig; schwächer in Chat-Werkzeugen) · nur Standardbibliothek (kein Setup; einfacher Frontmatter-Parser) · Englisch massgebend, Deutsch als Übersetzung der Systemdokumente (zwei Fassungen; `--i18n` prüft nur die Paarung).

## 9. Bekannte Grenzen
Stichwortauswahl in `pack.py` ist einfach (Zählung, kein Stemming; `-f` für exakte Kontrolle) · `check.py` prüft Struktur, nicht Qualität · Chat-Werkzeuge kürzen lange Eingaben, über `pack.md` sind schwächere Ergebnisse zu erwarten · kein Suchindex; für Hunderte Notizen genügt es.

## 10. Fahrplan
MVP 1 (dieses Repo): Regeln, Vorlagen, drei Verfahren, zwei Skripte, Beispiel. Danach: zwei Bundles zusammen (MVP 2); Projektmodul; Capture-Kanäle; MCP-Server (lesend) und Hosting; Überraschungs- und Review-Impulse.
