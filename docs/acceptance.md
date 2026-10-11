# Acceptance test (MVP 1)

Status: **not yet run.** To be filled in by the maintainer; report honestly, including failures.

## Questions
Run each question twice on the example bundle (`example/`): normally, and followed by «Warum diese Zettel?». Source: the draft in the maintainer's notes; the expected origin is listed here.

| # | Question (German) | Basis | Expected origin | Expected behaviour |
|---|---|---|---|---|
| 1 | Warum ergänzen wir in Organisationen lieber, als wegzulassen? | full | `addition-bias-subtraction`; `sutton-rao-2024-friction-project`; `albers-2024-optimierungsluege` | separates individual (bias) from organisational (sickness); says the study behind the bias is not in the notes |
| 2 | Wie entscheide ich einen Widerspruch zwischen zwei Notizen, ohne eine Seite ganz wegzuwerfen? | full (tool) | `konfliktnotiz` | six steps, stresses line 6; notes it is not yet tried in practice |
| 3 | Wie reduziert ein Team Reibung in Meetings? | partial | `sutton-rao-2024-friction-project`; `albers-2024-optimierungsluege` | cited points only; states that there is no meetings note and no data |
| 4 | Wie misst man Weglassen? | gap | `addition-bias-subtraction`, section on limits and open questions | says the answer is not in the notes; no invented metric |
| 5 | Welche Studie steht hinter dem Addition Bias? | trap | `albers-2024-optimierungsluege` (does not name it) | «not in the notes»; any outside study must be labelled «not from the notes» |

Pass means: origin per statement is correct, gaps are stated, nothing is invented; the reasoning appears only when asked.

## Results (one row per tool)
| Tool and version | Mode | Q1 | Q2 | Q3 | Q4 | Q5 | Overall | Remarks |
|---|---|---|---|---|---|---|---|---|
| Claude Code | files | | | | | | | |
| Open-source CLI | files | | | | | | | |
| GitHub Copilot (agent mode) | files | | | | | | | |
| M365 Copilot | `pack.md` | | | | | | | equal quality not required |

## Other criteria
- Set-up time by a person without prior knowledge: ___ minutes (target: under 60).
- `python tools/check.py example --example`: passes; a deliberately broken copy yields all built-in errors (see `tools/tests`).
