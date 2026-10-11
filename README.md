# Zettelkasten-Hub

A small, tool-neutral system for a knowledge base that **answers with sources, knows its gaps and can grow together with others**. Plain Markdown notes, one rules file (`AGENTS.md`), two procedures, two checking scripts. No lock-in: it works with any agent that can read files, and with chat tools via a single bundled file.

> Status: MVP 1, work in progress. Not yet tested by people other than the author. German translation: [README.de.md](README.de.md).

## What you get
| Layer | What | Works with |
|---|---|---|
| Data | Markdown notes in a bundle (`example/` shows one) | everything |
| Rules | [`AGENTS.md`](AGENTS.md) | agents that read repository files |
| Procedures | [`skills/answer`](skills/answer/SKILL.md), [`skills/check`](skills/check/SKILL.md) as plain Markdown | any agent: "follow skills/answer" |
| Checks and bundling | [`tools/check.py`](tools/check.py), [`tools/pack.py`](tools/pack.py), Python standard library only | by hand, in CI |

## 30-minute path
Follow the [guide](docs/guide.md): clone, fill in `perspective.md`, write your first source note and concept, ask your first question, run the check. [Diagrams](docs/diagrams.md) show the layers and the way from clone to first answer.

## Try it on the example
```
python tools/check.py example --example
python tools/pack.py example -k "addition bias" -s answer     # writes pack.md for chat tools
```
Then ask your agent: *"Follow skills/answer. Why do organisations prefer adding to removing?"*

## Agents
- **With file access** (Claude Code, open-source CLIs such as Codex CLI or OpenCode, GitHub Copilot in agent mode): they read `AGENTS.md` and the skills directly. `CLAUDE.md` only points to `AGENTS.md`.
- **Chat without repository access** (for example M365 Copilot): upload or paste `pack.md` made by `pack.py`. Expect somewhat weaker results; procedures arrive as text and instruction length is limited.
- Whether all of this holds up is checked in [docs/acceptance.md](docs/acceptance.md) and reported honestly there.

## Language
English is the main language; German translations of the system documents are in `de/` and `README.de.md`. Notes stay in the language of their source. The example bundle is German and exists once.

## License
Code in `tools/`: Apache 2.0 ([`LICENSE`](LICENSE)). All texts, templates, skills, documentation and the example bundle: CC BY 4.0 ([`LICENSE-CONTENT`](LICENSE-CONTENT)). Example notes are by Daniel Boos; where Claude wrote the original text this is stated as "DB+Claude".
