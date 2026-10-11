# Guide: your own bundle in 30 minutes

You need: a clone of this repository, a text editor, Python 3, and an agent (or a chat tool for `pack.md`).

## 1. Clone and look around
```
git clone https://github.com/danib8005/Zettelkasten-Hub.git
cd Zettelkasten-Hub
python tools/check.py example --example
```
Open `example/` to see what a bundle looks like. Your own bundle is a new folder, for example `mybundle/`, with the folders `00_Inbox`, `10_Concepts`, `40_Sources`, `50_Open-Questions`, `70_Tools`, `95_System`.

## 2. Fill in `perspective.md`
Copy `templates/perspective.md` to `mybundle/perspective.md`. Set `language:` (en or de), your author tag, purpose, two or three core topics and your anchors (authors or theories you read from). Five minutes; keep it short.

## 3. Write your first source note
Take one book or article you know well. Copy `templates/source-lightweight.md` to `mybundle/40_Sources/lastname-year-shorttitle.md`. Paraphrase 3–6 key statements, add your own thought after `📝 Deine Notiz:`. Do not copy long passages.

## 4. Write your first concept
Copy `templates/concept.md` to `mybundle/10_Concepts/<concept-name>.md`. State the core idea in 2–3 sentences, name the source, link it as `[Title](/40_Sources/your-note.md)` with a reason. Links to notes that do not exist yet are fine.

## 5. Ask your first question
Tell your agent: *"Follow skills/answer. [Your question]"* Check that every statement names a note and that the answer lists what is missing. Ask *"Warum diese Zettel?"* to see why those notes were chosen. Without file access: `python tools/pack.py mybundle -k <keywords> -s answer`, then upload or paste `pack.md`.

## 6. Check the bundle
```
python tools/check.py mybundle
```
Fix every ERROR; warnings about open links are your to-do list. Ask your agent to follow `skills/check` for help with the findings.

## Where next
Grow the bundle one source at a time. Draft first: have the agent show a new note in the chat before it saves it. See [diagrams](diagrams.md) for the layers and the link rule (links go only to the more general).
