# Cleanup

Working list. Answers to the questions are at the bottom.

# Answers

## A1 — Curiosity as a mind map: not ready

Today a curiosity entry is one `thought` + one `question`, both free text. To
group thoughts under a question you would have to match on the **question
string**, which is why `docs/content-schema.md` currently says to watch for
misspellings. That is a fragile way to build a graph: one typo and a node
splits in two, and renaming a question orphans every thought under it.

What it would take:

1. A `questions` collection — one file per question, the filename becoming the
   stable id.
2. `curiosity` (the thoughts) gets a `question` field that is a Decap
   **relation** widget pointing at that collection. That gives a dropdown of
   existing questions instead of retyped text, and the id survives a reword.
3. A page that groups thoughts by that id and draws the map.

Three files each for steps 1 and 2, plus a migration of the existing entries.

**Not done, because two things are your call and I should not invent them:**
does a question carry anything besides its text (a status — open / answered? a
date? a colour?), and does a thought belong to exactly one question or several?
The second decides whether this is a tree or a graph, which decides the
visualisation. Say which, and it is a small change.
**Response** Just text for the question. And a thought belongs only to one question.

**Done — the content side.** A `questions` collection (one field, `question`;
the filename is the id) and `curiosity.question` is now a reference to it, so
the CMS offers a dropdown of existing questions instead of retyped text. All
three files moved together: `src/content.config.ts`, `public/admin/config.yml`,
`docs/cms.md`. The one existing entry was migrated; the misspelling warning in
the docs is gone, because a wrong name now fails the build by name rather than
splitting a question in two.

**Not done — the map itself.** Step 3 was "a page that draws it", and there is
no curiosity page at all yet. Inventing that visualisation is a design
decision, not an implementation one (CLAUDE.md §0), so it waits for a Figma
frame. The data it needs is ready: thoughts group by `question.id`, exactly one
question each, so the shape to draw is a tree.

**Needs your approval (R1).** CLAUDE.md still says six collections and points at
`docs/content-schema.md`. The diff is in the chat — three lines.

## A5 — cms.md vs content-schema.md

They answer different questions and merging them would make one long document
with two audiences:

- **content-schema.md** — what a field means, what is required, how to add one.
  Read when writing content or changing the schema.
- **cms.md** — how to run the editor, why `/admin` is not deployed, what is
  load-bearing in its setup. Read roughly once a year, when something breaks.

Still relevant, yes — the local-editing instructions are the only record of how
to edit without OAuth. But it was carrying about 4 kB of planning for an OAuth
relay that does not exist and is not planned, which is exactly the speculative
structure the repo rules forbid elsewhere. That is gone; one sentence records
that the option exists.
**Response** Still merge the two together as cms.md.

**Done.** `docs/content-schema.md` is deleted; everything in it now lives in
[`cms.md`](./cms.md) — the fields first, then how to run the editor. Every
pointer moved with it: `README.md`, `docs/resume.md`, `public/admin/config.yml`,
`src/content.config.ts`. CLAUDE.md is the one exception, above.
