# Standards this system builds on

Principle: **open, portable standards over proprietary conventions.** A bundle must stay readable and usable without this repository, without a specific editor and without a specific AI vendor.

| Layer | Standard | How we use it |
|---|---|---|
| Documents | Markdown (CommonMark-compatible), UTF-8, with YAML frontmatter | Every note is one plain file. Any editor, GitHub and static-site tools render it. |
| Knowledge bundle | **Open Knowledge Format (OKF) v0.2** | Our bundles follow its model: a directory tree of Markdown concept documents, each with a frontmatter `type`, standard bundle-relative links, optional `index.md` / `log.md`. See the mapping below. |
| Agent instructions | `AGENTS.md` (open, tool-neutral convention for repository instructions) | One rules file at the root. `CLAUDE.md` contains only `@AGENTS.md`. No vendor-specific keys. |
| Procedures | `skills/<name>/SKILL.md` (Markdown with frontmatter `name`, `description`) | Written as plain instructions. "Follow `skills/answer`" works in any agent; nothing needs a skill loader. |
| Versioning and contribution | Git | History is the audit trail; contributions by pull request or inbox file. |
| Diagrams | Mermaid inside Markdown | Rendered by GitHub; the source stays readable text. |
| Code | Python 3, standard library only | No dependencies, no build step. |
| Licences | SPDX identifiers `Apache-2.0` (code), `CC-BY-4.0` (content) | Two licence files, see the README. |
| Planned | Model Context Protocol (MCP) | Read-only access for agents and a hosted variant, after MVP 1. Nothing depends on it today. |

## OKF mapping
OKF is a lean, tool-independent format for knowledge corpora published by Google Cloud (knowledge-catalog, `okf/SPEC.md`). Status here: read against v0.2 on 2026-10-11; check upstream for newer versions.

| OKF v0.2 | This system |
|---|---|
| Bundle = directory tree of `.md` files, distributable as a git repo | Same. A bundle is a folder (the example is `example/`); folder names are our convention, OKF leaves them free. |
| Every non-reserved `.md` has parseable frontmatter with a non-empty `type` (conformance, §11) | Same; **enforced by `tools/check.py`** for every `.md` in a bundle except `index.md` and `log.md`. |
| `type` values are not registered; consumers tolerate unknown types | Free text. Templates use `Thought`, `Concept`, `Framework`, `Synthesis`, `Source`, `Tool`; German bundles use `Gedanke`, `Konzept`, `Synthese`. |
| Links: standard Markdown, bundle-relative `/path.md` recommended, broken links tolerated | Same. Missing targets are a deliberate to-do list; `check.py` reports them as warnings. |
| Reserved `index.md`, `log.md` (optional) | Reserved, not generated in MVP 1. |
| Recommended `title`, `description`, `tags`, `resource` | Not required. The title is the first `#` heading (link text = title line); tags are inline `#tags` for now. A later step may emit `title`/`tags` frontmatter. |
| Provenance: `sources` frontmatter, per-claim footnotes | Not emitted yet. We record provenance as source notes plus links and require the origin per statement in answers (`AGENTS.md`, principle 1). Compatible, not identical. |
| Lifecycle `status` (`draft`, `stable`, `deprecated`), trust tiers via `verified` | Our review block at the end of a note (current / outdated / under revision, initials). No automatic mapping yet. |
| Extensions: producers may add keys; consumers preserve them | We add `aliases`, `visibility`, `example` (example bundle), `translation_of` (translations), `language` (in `perspective.md`). |

Where we are **not** standard, on purpose: the review block lives in the body; levels use `Level:` / `Ebene:` (micro, meso, macro); annotation markers (`📝 …`) mark who said what. These are conventions of this system, documented in `AGENTS.md`.
