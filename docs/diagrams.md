# Diagrams

## 1. Layers and the link rule
```mermaid
flowchart TB
  subgraph Tools["Checks and bundling (no AI)"]
    C["tools/check.py"]
    P["tools/pack.py"]
  end
  subgraph Proc["Procedures (plain Markdown)"]
    A["skills/answer"]
    K["skills/check"]
  end
  R["Rules: AGENTS.md"]
  D["Data: your bundle (Markdown notes)"]
  R --> Proc
  Proc --> D
  Tools --> D
  Core["Core (this repo, no knowledge)"] -.rules and templates.-> R
  Project["Project notes"] -- links only to the more general --> Own["Own bundle"]
  Own -- links only to the more general --> Shared["Shared bundle"]
  Shared -- links only to the more general --> Core
  Own -. promotion: generalise, pseudonymise, move up .-> Shared
```
Links point only to the more general. The way back is promotion.

## 2. From clone to first answer
```mermaid
flowchart LR
  S1["1 Clone"] --> S2["2 Fill in perspective.md"]
  S2 --> S3["3 First source note"]
  S3 --> S4["4 First concept"]
  S4 --> S5{"5 Ask a question"}
  S5 -- "agent has file access" --> F["Agent follows skills/answer"]
  S5 -- "chat tool only" --> PK["tools/pack.py writes pack.md"] --> F2["Upload or paste pack.md"]
  F --> ANS["Answer with a source per statement and a gap list"]
  F2 --> ANS
  ANS --> S6["6 tools/check.py"]
  S6 --> S3
```

More diagrams (components, how a question is answered) are in [architecture.md](architecture.md).
