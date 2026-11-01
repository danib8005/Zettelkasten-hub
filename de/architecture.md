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
- **Wissen getrennt vom System:** Der Kern enthält Regeln, Agenten, Verfahren, Vorlagen und Werkzeuge; Wissen liegt in Bundles.
- **Kleiner, fokussierter Kontext pro Schritt:** Die Arbeit ist in fünf Phasen mit je einem Agenten geteilt; ein Agent lädt nur den gemeinsamen Kern, seine eigenen Regeln und seine Skills, die kritischen Regeln am Anfang und am Ende.
- Nicht Ziel von MVP 1: Capture-Kanäle, MCP-Server, Hosting, Projektmodul, ein Router-Agent, der die Phase wählt.

## 2. Schichten und Komponenten
Diagramm: [architecture.md](../docs/architecture.md#2-layers-and-components). Strikte Trennung: **Daten** (Markdown) · **Regeln** (`AGENTS.md`) · **Rollen** (`agents/`) · **Verfahren** (`skills/`) · **Prüfung und Bündeln** (Skripte, ohne KI). Jede Schicht ist austauschbar, ohne die anderen zu berühren.

## 3. Datenmodell
**Bundle-Aufbau** (nur anlegen, was nötig ist): `00_Inbox`, `10_Concepts`, `20_Frameworks`, `30_Syntheses`, `40_Sources`, `50_Open-Questions`, `70_Tools`, `95_System`, dazu `perspective.md` im Bundle-Wurzelordner.

| Typ | Ordner | Vorlage | Zweck |
|---|---|---|---|
| Capture | `00_Inbox` | `capture.md` | Rohes, unverarbeitet; eine Zeile, warum es aufgehoben wird |
| Gedanke | `10_Concepts` | `thought.md` | Rohidee, Originalwortlaut bleibt |
| Konzept | `10_Concepts` | `concept.md` | eine Idee, 1–2 Seiten, die Standard-Definition |
| Framework | `20_Frameworks` | `framework.md` | wiederverwendbare Denkweise, 3–5 Seiten |
| Synthese | `30_Syntheses` | `synthesis.md` | mehrere Quellen in Spannung; Divergenzen sichtbar |
| Source | `40_Sources` | `source-lightweight.md`, `source-full.md` | eine pro Buch, Artikel oder Talk |
| Offene Frage | `50_Open-Questions` | `open-question.md` | eine Lücke aus einer Antwort, bewusst festgehalten |
| Tool | `70_Tools` | `tool.md` | nutzbare Checkliste, Format oder Methode |

**Identität und Links.** Die Identität einer Notiz ist ihr Pfad im Bundle. Links: `[Titel](/ordner/datei.md)`, immer mit Begründung; Richtung nur zum Allgemeineren; fehlende Ziele sind erlaubt. Eine Notiz trägt `type:` (Pflicht), optional `aliases:` und `visibility:`.

**Autorschaft und Vertrauen.** Der Review-Block hält Erstellung, letztes Review und Status fest, mit Initialen; jeder Agent zeichnet mit eigenem Tag (`agent:capture`, `agent:distill`, …), so bleibt sichtbar, welche Phase eine Notiz erstellt oder zuletzt berührt hat. Annotationsmarker trennen eigene Notiz, Synthese-Bemerkung und Agenten-Ergänzung.

## 4. Komponenten
**`AGENTS.md`**: der gemeinsame Kern, den jeder Agent zuerst liest: die Nie-brechen-Regeln (oben und am Ende wiederholt), die Schleife und ihre Agenten, Struktur, Notiz-Typen, Konventionen, Prinzipien 1–2, Vertraulichkeit. Rund 50 Zeilen. `CLAUDE.md` importiert sie.
**`agents/`**: eine Datei pro Phase (`capture`, `distill`, `connect`, `answer`, `maintain`), nach `templates/agent.md`. Frontmatter: `type: Agent`, `name`, `description`, `phase`, `skills`, `reads`, `writes`. Abschnitte: Role, Goal and when to use, Reads, Writes, Skills, Phase rules, Handoff, Final check. Die phasenspezifischen Regeln stehen hier (z. B. Draft first in Distill und Connect, Prinzipien 3–5). Die Person wählt den Agenten; jeder schlägt die nächste Phase vor.
**Adapter**: `.github/agents/<name>.agent.md` (GitHub Copilot) und `.claude/agents/<name>.md` (Claude Code) enthalten nur das Frontmatter des Werkzeugs und eine Zeile mit Verweis auf `AGENTS.md` und die neutrale Agenten-Datei. Ihre `tools:` folgen dem Schreibbereich: alle Agenten lesen, suchen und bearbeiten; nur Maintain darf Befehle ausführen, und Capture darf `tools/zotero_highlights.py` ausführen und sonst nichts. Ordnergenaue Schreibgrenzen können diese Werkzeuge nicht erzwingen; sie sind in der Agenten-Datei deklariert und werden im Abnahmetest geprüft. `.vscode/settings.json` zeigt VS Code den Ordner `skills/`.
**`skills/`**: neunzehn Verfahren, benannt als Verb-Objekt, wo sinnvoll geteilt: `capture-inbox`, `capture-thought`, `capture-zotero` (Capture) · `find-existing` (Capture, Distill, Connect) · `draft-first` (Distill, Connect) · `distill-source` (Distill) · `write-concept`, `synthesize`, `write-tool` (Connect) · `answer-from-notes`, `record-open-question` (Answer) · `run-check`, `review-notes`, `triage-open-links` (Maintain) · `map-frontier`, `discover-connections`, `inspire` (Explore) · `challenge-position`, `revisit-notes` (Reflect). Sie nennen kein Werkzeug; Ausnahme ist `capture-zotero`, das `tools/zotero_highlights.py` braucht (ohne Befehlszugriff führt die Person es aus und fügt die Ausgabe ein).
**`tools/check.py`** (ohne KI, Exit-Code 1 bei Fehlern): `type:` auf jeder `.md` ausser `index.md`/`log.md` (OKF-Konformität), Dateinamen, Review-Status (in allen Notiz-Ordnern, auch `00_Inbox` und `50_Open-Questions`), keine Wikilinks, bundle-relative Links (alles ERROR); fehlende Linkziele und Source-Namen als Warnung; `--example`: keine Zitate, keine `Loc.`/`S.`-Fundstellen, keine Links aus dem Beispiel hinaus (ausser Allow-Liste), `visibility: public`; `--i18n` (Repo-Prüfung): jede deutsche Datei nennt `translation_of:`, das Ziel existiert, die Pflichtdokumente haben eine Übersetzung; Agenten haben alle Frontmatter-Felder, `name` = Dateiname, `phase` 1–5, vorhandene Skills, `writes` nur Bundle-Ordner, die acht Abschnitte, je einen Adapter pro Werkzeug und keine Adapter ohne Agent (ERROR); ein Skill, den kein Agent nutzt, ist eine Warnung.
**`tools/pack.py`** (ohne KI): wählt Notizen per Stichwort-Punktzahl (Titel zählt dreifach) oder Dateiliste und schreibt eine `pack.md`. Mit `-a <agent>`: Vorspann → `AGENTS.md` → Agenten-Datei → ihre Skills → `perspective.md` → Notizen, je unter ihrem Pfad als Überschrift → die Schlussprüfung des Agenten nochmals am Ende; die Notizen kommen dann nur aus den `reads:`-Ordnern des Agenten. Mit `-s <skill>` (nicht zusammen mit `-a`): ein einzelnes Verfahren statt eines Agenten. Notizen werden unverändert kopiert. Warnung ab 30'000 Zeichen.
**`tools/export.py`** (ohne KI): erzeugt aus einem Profil (`templates/export-profile.md`) eine gefilterte, generierte Kopie des Bundles für ein anderes Gerät oder Werkzeug (Arbeitslaptop, Copilot, Kolleg:in). Allowlist: nur Notizen aus den genannten Ordnern mit erlaubtem `visibility:` oder ausdrücklich freigegeben; `visibility: private`, `.git`, `90_Originals`, `99_Raw-Data`, jeder `reflexion`-Ordner und die Leak-Terms-Datei verlassen das Bundle nie. Das Profil muss seine `audience` nennen (`owner`, `team` oder `public`); wörtliche Buchzitate gehen nur in eine Owner-Kopie, sonst erzwingt das Werkzeug `strip-quotes`. Ein Leak-Check gegen eine Namensliste bricht den Lauf ab, ohne etwas zu schreiben. Die Kopie bekommt eine `EXPORT.md`; ein erneuter Lauf entfernt Dateien, die nicht mehr freigegeben sind. Zuerst `--dry-run`.

**`tools/catalog.py`** (ohne KI): erstellt aus einem Manifest einen thematischen Katalog der Source Notes (eine Datei pro Gruppe; Titel, Angabe, Kernthese und Tags unverändert, je unter dem Notizpfad), für Chat-Werkzeuge, die einen Überblick über viele Quellen brauchen. Vom Agenten Answer ohne Dateizugriff genutzt.
**`tools/zotero_highlights.py`** (ohne KI): liest Markierungen aus einer laufenden Zotero-Desktop-App über deren lesende lokale API (`127.0.0.1:23119`, nur die persönliche Bibliothek; Zotero-Einstellung «Allow other applications on this computer to communicate with Zotero»). `status` prüft Zotero, `search` findet einen Eintrag, `fetch` gibt pro Eintrag einen Markdown-Block aus (genauer Text, Seitenangabe, eigener Kommentar) mit den noch nicht übernommenen Markierungen, `mark-done` hält sie nach dem Speichern der Notizen in `.zotero-sync.json` des Bundles fest (Bibliotheksversion und übernommene Annotationsschlüssel). Zeichnungen und Bildausschnitte werden übersprungen. Vom Agenten Capture über `capture-zotero` genutzt.

## 5. Wie eine Frage beantwortet wird
Person wählt den Agenten answer und stellt die Frage → Agent liest gemeinsame Regeln, Agenten-Datei und `answer-from-notes` → durchsucht das Bundle, liest Treffer, bewertet (Kern / Ergänzung / Rand) → Antwort mit Kernaussage, Aussagen mit Notizpfad, Lückenliste → auf Nachfrage «Warum diese Zettel?» die Auswahl → auf Wunsch wird eine Lücke mit `record-open-question` in `50_Open-Questions` festgehalten, dann Vorschlag Maintain. Ohne Dateizugriff: `python tools/pack.py <bundle> -k <stichworte> -a answer`, dann `pack.md` hochladen oder einfügen.

## 6. Mehrere Bundles (MVP 2, nicht gebaut)
Eigenes und gemeinsames Bundle nebeneinander; `bundles.md` deklariert Einhängepunkte und Zugriff. Das Prüfskript meldet jeden Link vom gemeinsamen ins eigene Bundle. Beiträge fliessen per **Promotion** nach oben (verallgemeinern, pseudonymisieren, hochlegen; Pull-Request oder Inbox-Datei). Ein Projektmodul baut auf denselben Regeln auf.

## 7. Sichtbarkeit und Sicherheit
`visibility:` pro Notiz (privat | team | öffentlich), fehlend heisst privat; standardmässig werden nur öffentliche Notizen exportiert, ein Export-Profil der Person darf `team`-Notizen zulassen oder Notizen ausdrücklich freigeben (ein Agent erweitert ein Profil nie). Öffentliche Bundles enthalten keine wörtlichen Buchzitate (`check.py --example` erzwingt das für Beispiele). Skripte lesen und schreiben nur lokale Dateien und senden nichts; `zotero_highlights.py` liest zusätzlich aus Zotero auf demselben Rechner (`127.0.0.1`), nie aus dem Internet.

## 8. Entscheide und Kosten
Markdown + Frontmatter nach OKF-Modell (portabel; einige Konventionen sind unsere) · `AGENTS.md` als einzige gemeinsame Regeldatei (agentenübergreifend; unterschiedlich zuverlässig befolgt) · ein Agent pro Phase, Skills als geteilte Verfahren (kleiner Kontext, Regeln nahe Anfang und Ende, klarer Schreibbereich; mehr Dateien, die Person wählt den Agenten) · neutrale Agenten-Dateien + schlanke, handgeschriebene Adapter (werkzeugneutrale Quelle, native Agentenlisten in Copilot und Claude Code; Adapter können abweichen, `check.py --i18n` findet fehlende und verwaiste) · Skills als Markdown (kein Loader nötig; schwächer in Chat-Werkzeugen) · nur Standardbibliothek (kein Setup; einfacher Frontmatter-Parser) · Englisch massgebend, Deutsch als Übersetzung der Systemdokumente (zwei Fassungen; `--i18n` prüft nur die Paarung).

## 9. Bekannte Grenzen
Stichwortauswahl in `pack.py` ist einfach (Zählung, kein Stemming; `-f` für exakte Kontrolle) · `check.py` prüft Struktur, nicht Qualität · Schreibbereiche sind pro Agent deklariert; Werkzeuge erzwingen nur grobe Grenzen (bearbeiten ja/nein, Befehle ja/nein), keine Ordner · Chat-Werkzeuge kürzen lange Eingaben, über `pack.md` sind schwächere Ergebnisse zu erwarten · kein Suchindex; für Hunderte Notizen genügt es.

## 10. Fahrplan
MVP 1 (dieses Repo): gemeinsame Regeln, fünf Phasen-Agenten mit Adaptern, neunzehn Skills, Vorlagen, sechs Skripte, Beispiel. Danach: zwei Bundles zusammen (MVP 2); Projektmodul; ein Router-Agent; Capture-Kanäle; MCP-Server (lesend) und Hosting; Überraschungs- und Review-Impulse.
