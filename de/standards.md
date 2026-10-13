---
type: System
translation_of: docs/standards.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist docs/standards.md. -->
# Standards, auf denen das System aufbaut

Prinzip: **offene, portable Standards statt proprietärer Konventionen.** Ein Bundle muss ohne dieses Repo, ohne bestimmten Editor und ohne bestimmten KI-Anbieter les- und nutzbar bleiben.

| Schicht | Standard | Verwendung |
|---|---|---|
| Dokumente | Markdown (CommonMark-kompatibel), UTF-8, mit YAML-Frontmatter | Jede Notiz ist eine einfache Datei. Jeder Editor, GitHub und Static-Site-Werkzeuge stellen sie dar. |
| Wissens-Bundle | **Open Knowledge Format (OKF) v0.2** | Unsere Bundles folgen dem Modell: Verzeichnisbaum aus Markdown-Konzeptdokumenten, je mit `type` im Frontmatter, Standard-Links relativ zur Bundle-Wurzel, optional `index.md` / `log.md`. Zuordnung unten. |
| Agenten-Anweisungen | `AGENTS.md` (offene, werkzeugneutrale Konvention für Repo-Anweisungen) | Eine gemeinsame Regeldatei im Wurzelordner. `CLAUDE.md` enthält nur `@AGENTS.md`. Keine herstellerspezifischen Schlüssel. |
| Agenten | `agents/<phase>.md` (Markdown mit Frontmatter `type: Agent`, `name`, `description`, `phase`, `skills`, `reads`, `writes`) | Eine Rolle pro Phase, werkzeugneutral. Schlanke Adapter für Werkzeuge, die Agenten auflisten: `.github/agents/<name>.agent.md` (GitHub Copilot) und `.claude/agents/<name>.md` (Claude Code); sie verweisen nur auf die neutrale Datei und beschränken Werkzeuge. |
| Verfahren | `skills/<name>/SKILL.md` (Markdown mit Frontmatter `name`, `description`) | Als normale Anleitung geschrieben. «Folge `skills/answer-from-notes`» funktioniert in jedem Agenten; nichts braucht einen Skill-Loader. VS Code findet sie über `.vscode/settings.json`. |
| Versionierung, Beiträge | Git | Verlauf ist der Prüfpfad; Beiträge per Pull-Request oder Inbox-Datei. |
| Diagramme | Mermaid in Markdown | GitHub rendert sie; die Quelle bleibt lesbarer Text. |
| Code | Python 3, nur Standardbibliothek | Keine Abhängigkeiten, kein Build. |
| Lizenzen | SPDX `Apache-2.0` (Code), `CC-BY-4.0` (Inhalt) | Zwei Lizenzdateien, siehe README. |
| Geplant | Model Context Protocol (MCP) | Lesender Zugriff für Agenten und gehostete Variante, nach MVP 1. Heute hängt nichts davon ab. |

## Zuordnung zu OKF
OKF ist ein schlankes, werkzeugunabhängiges Format für Wissenskorpora von Google Cloud (knowledge-catalog, `okf/SPEC.md`). Stand: gegen v0.2 gelesen am 2026-10-11; neuere Versionen im Original prüfen.

| OKF v0.2 | Dieses System |
|---|---|
| Bundle = Verzeichnisbaum aus `.md`-Dateien, als Git-Repo verteilbar | Gleich. Ein Bundle ist ein Ordner (das Beispiel ist `example/`); Ordnernamen sind unsere Konvention, OKF lässt sie frei. |
| Jede nicht reservierte `.md` hat lesbares Frontmatter mit nicht leerem `type` (Konformität, §11) | Gleich; **`tools/check.py` erzwingt es** für jede `.md` im Bundle ausser `index.md` und `log.md`. |
| `type`-Werte sind nicht registriert; Konsumenten tolerieren unbekannte | Freier Text. Vorlagen nutzen `Capture`, `Thought`, `Concept`, `Framework`, `Synthesis`, `Source`, `Tool`, `Open question`; deutsche Bundles `Gedanke`, `Konzept`, `Synthese`, `Offene Frage`. |
| Links: Standard-Markdown, bundle-relativ `/pfad.md` empfohlen, kaputte Links toleriert | Gleich. Fehlende Ziele sind eine gewollte Bestellliste; `check.py` meldet sie als Warnung. |
| Reservierte `index.md`, `log.md` (optional) | Reserviert, in MVP 1 nicht erzeugt. |
| Empfohlen `title`, `description`, `tags`, `resource` | Nicht verlangt. Der Titel ist die erste `#`-Überschrift (Linktext = Titelzeile); Tags vorerst als `#tags` im Text. Später kann `title`/`tags` als Frontmatter erzeugt werden. |
| Herkunft: `sources` im Frontmatter, Fussnoten pro Aussage | Noch nicht erzeugt. Herkunft führen wir über Source Notes und Links und verlangen sie pro Aussage in Antworten (`AGENTS.md`, Prinzip 1). Kompatibel, nicht identisch. |
| Lebenszyklus `status` (`draft`, `stable`, `deprecated`), Vertrauensstufen über `verified` | Unser Review-Block am Notizende (aktuell / veraltet / in Überarbeitung, Initialen). Noch keine automatische Zuordnung. |
| Erweiterungen: Erzeuger dürfen Schlüssel ergänzen; Konsumenten bewahren sie | Wir ergänzen `aliases`, `visibility`, `example` (Beispielbundle), `translation_of` (Übersetzungen), `language` (in `perspective.md`). |

Bewusst **nicht** standardkonform: der Review-Block steht im Text; Ebenen heissen `Level:` / `Ebene:` (Mikro, Meso, Makro); Annotationsmarker (`📝 …`) zeigen, wer was sagt. Das sind Konventionen dieses Systems, dokumentiert in `AGENTS.md`.
