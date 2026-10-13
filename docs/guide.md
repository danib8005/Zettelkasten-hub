# Guide: your own bundle in 30 minutes

You need: a clone of this repository, a text editor, Python 3, and an agent (or a chat tool for `pack.md`).
The work runs in a loop of five phases (Capture → Distill → Connect → Answer → Maintain), one agent each; see [How it works](../README.md#how-it-works). This guide walks through it once.

## 1. Clone and look around
```
git clone https://github.com/danib8005/Zettelkasten-Hub.git
cd Zettelkasten-Hub
python tools/check.py example --example
```
Open `example/` to see what a bundle looks like. Your own bundle is a new folder, for example `mybundle/`, with the folders `00_Inbox`, `10_Concepts`, `40_Sources`, `50_Open-Questions`, `70_Tools`, `95_System`. Add `20_Frameworks` and `30_Syntheses` when you need them.

## 2. Fill in `perspective.md`
Copy `templates/perspective.md` to `mybundle/perspective.md`. Set `language:` (en or de), your author tag, purpose, two or three core topics and your anchors (authors or theories you read from). Five minutes; keep it short.

## 3. Write your first source note
Take one book or article you know well. Copy `templates/source-lightweight.md` to `mybundle/40_Sources/lastname-year-shorttitle.md`. Paraphrase 3–6 key statements, add your own thought after `📝 Deine Notiz:`. Do not copy long passages.
Or let the **distill** agent do it: *"Follow agents/distill.md. Make a source note from [source]."* It shows a draft first and saves only after you confirm. Something to read later goes to the **capture** agent instead, which puts it into `00_Inbox`.

## 4. Write your first concept
Copy `templates/concept.md` to `mybundle/10_Concepts/<concept-name>.md`. State the core idea in 2–3 sentences, name the source, link it as `[Title](/40_Sources/your-note.md)` with a reason. Links to notes that do not exist yet are fine. The **connect** agent helps with concepts, syntheses, frameworks and tools, again draft first.

## 5. Ask your first question
Pick the **answer** agent (or tell your agent: *"Follow agents/answer.md. [Your question]"*). Check that every statement names a note and that the answer lists what is missing. Ask *"Warum diese Zettel?"* to see why those notes were chosen. If the answer finds a gap worth keeping, agree and it is saved in `50_Open-Questions`. Without file access: `python tools/pack.py mybundle -k <keywords> -a answer`, then upload or paste `pack.md`.

## 6. Check the bundle
```
python tools/check.py mybundle
```
Fix every ERROR; warnings about open links are your to-do list. The **maintain** agent explains the findings, proposes fixes, reviews notes and turns open links and open questions into a short list of what to capture or write next. That closes the loop.

## Where next
Grow the bundle one source at a time, going round the loop. Draft first: Distill and Connect show a new note in the chat before they save it. See [diagrams](diagrams.md) for the loop, the layers and the link rule (links go only to the more general).
