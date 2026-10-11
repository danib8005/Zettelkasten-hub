---
type: System
translation_of: README.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist die englische README.md. -->
# Zettelkasten-Hub

Ein kleines, werkzeugneutrales System für eine Wissensbasis, die **belegt antwortet, ihre Lücken kennt und mit anderen zusammen wachsen kann**. Einfache Markdown-Notizen, eine Regeldatei (`AGENTS.md`), drei Verfahren, acht Notiz-Vorlagen, zwei Skripte. Keine Bindung an einen Anbieter: Es läuft mit jedem Agenten, der Dateien lesen kann, und mit Chat-Werkzeugen über eine gebündelte Datei.

> Stand: MVP 1, in Arbeit. Noch nicht von anderen Personen als dem Autor getestet.

## Was du bekommst
| Schicht | Inhalt | Läuft mit |
|---|---|---|
| Daten | Markdown-Notizen in einem Bundle (`example/` zeigt eines) | überall |
| Regeln | [`AGENTS.md`](AGENTS.md) | Agenten, die Repo-Dateien lesen |
| Verfahren | [`skills/answer`](skills/answer/SKILL.md), [`skills/write`](skills/write/SKILL.md), [`skills/check`](skills/check/SKILL.md) als normale Markdown-Anleitung | jeder Agent: «folge skills/answer» |
| Prüfung und Bündeln | [`tools/check.py`](tools/check.py), [`tools/pack.py`](tools/pack.py), nur Python-Standardbibliothek | von Hand, in CI |

## Gebaut auf Standards
Notizen sind Markdown mit YAML-Frontmatter und als Bundle nach dem [Open Knowledge Format](de/standards.md) organisiert (geprüft von `tools/check.py`); Regeln stehen in `AGENTS.md`; Verfahren sind `SKILL.md`-Dateien; Versionierung läuft über Git. Einzelheiten und Abweichungen: [de/standards.md](de/standards.md). Wie die Teile zusammenspielen: [de/architecture.md](de/architecture.md).

## Notiz-Typen
Gedanke, Konzept, Framework, Synthese, Source (leicht oder vollständig), Tool. Vorlagen in [`templates/`](templates/) (deutsch: [`de/templates/`](de/templates/)).

## Der 30-Minuten-Weg
Siehe die [Anleitung](de/guide.md) (deutsch) bzw. [guide](docs/guide.md) (massgebend, englisch). [Diagramme](docs/diagrams.md) zeigen Schichten und den Weg vom Klonen zur ersten Antwort.

## Am Beispiel ausprobieren
```
python tools/check.py example --example
python tools/pack.py example -k "addition bias" -s answer     # schreibt pack.md für Chat-Werkzeuge
```
Dann deinem Agenten: *«Folge skills/answer. Warum ergänzen Organisationen lieber, als wegzulassen?»*

## Agenten
- **Mit Dateizugriff** (Claude Code, Open-Source-CLIs wie Codex CLI oder OpenCode, GitHub Copilot im Agent-Modus): lesen `AGENTS.md` und die Skills direkt.
- **Chat ohne Repo-Zugriff** (zum Beispiel M365 Copilot): `pack.md` hochladen oder einfügen. Erwartung: etwas schwächere Qualität.
- Ob das trägt, steht ehrlich in [docs/acceptance.md](docs/acceptance.md).

## Sprache
Englisch ist Hauptsprache; deutsche Übersetzungen der Systemdokumente liegen unter `de/`. Notizen bleiben in der Sprache ihrer Quelle. Das Beispielbundle ist deutsch.

## Lizenz
Code in `tools/`: Apache 2.0 ([`LICENSE`](LICENSE)). Alle Texte, Vorlagen, Skills, Dokumentation und das Beispiel: CC BY 4.0 ([`LICENSE-CONTENT`](LICENSE-CONTENT)). Beispielnotizen: Daniel Boos; wo Claude den Ursprungstext verfasst hat, steht «DB+Claude».
