# Diagrams

## 1. Layers and the link rule
```mermaid
flowchart TB
  subgraph Tools["Checks and bundling (no AI)"]
    C["tools/check.py"]
    P["tools/pack.py"]
  end
  subgraph Agents["Agents (one per phase, plain Markdown)"]
    AG["agents/capture · distill · connect · answer · maintain"]
    SK["skills/ (procedures the agents use)"]
  end
  R["Rules: AGENTS.md (shared core)"]
  D["Data: your bundle (Markdown notes)"]
  R --> Agents
  AG --> SK
  Agents --> D
  Tools --> D
  Core["Core (this repo, no knowledge)"] -.rules, agents and templates.-> R
  Project["Project notes"] -- links only to the more general --> Own["Own bundle"]
  Own -- links only to the more general --> Shared["Shared bundle"]
  Shared -- links only to the more general --> Core
  Own -. promotion: generalise, pseudonymise, move up .-> Shared
```
Links point only to the more general. The way back is promotion.

## 2. The loop
```mermaid
flowchart LR
  C["1 Capture"] --> D["2 Distill"] --> N["3 Connect"] --> A["4 Answer"] --> M["5 Maintain"]
  M -- "open links, open questions, captures" --> C
  D -. "after saving" .-> M
  N -. "after saving" .-> M
```
One agent per phase; the person picks it, and each agent suggests the next. Writing agents also suggest Maintain after saving (dotted). What each agent reads, writes and uses: [README, How it works](../README.md#how-it-works).

## 3. From clone to first answer
```mermaid
flowchart LR
  S1["1 Clone"] --> S2["2 Fill in perspective.md"]
  S2 --> S3["3 First source note (distill)"]
  S3 --> S4["4 First concept (connect)"]
  S4 --> S5{"5 Ask a question (answer)"}
  S5 -- "agent has file access" --> F["Agent follows agents/answer.md"]
  S5 -- "chat tool only" --> PK["tools/pack.py -a answer writes pack.md"] --> F2["Upload or paste pack.md"]
  F --> ANS["Answer with a source per statement and a gap list"]
  F2 --> ANS
  ANS --> S6["6 tools/check.py (maintain)"]
  S6 --> S3
```

More diagrams (components, how a question is answered) are in [architecture.md](architecture.md).
