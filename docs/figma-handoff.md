# The Handoff frame

Every page gets one frame named `Handoff`, sitting with that page's own frames
in Figma, and it is read before any other frame for that page — see Step 0 of
[`figma-to-astro.md`](../behind-the-scenes/skills/figma-to-astro.md). Answering
it means ticking boxes and filling short blanks, not writing prose. A blank is
not a default: a blank is an open question, and the implementer asks it rather
than infers it.

If a page has no Handoff frame yet, the skill walks this template section by
section, skipping the sections the table below says do not apply.

## Fill it in, in three moves

1. Add a frame named `Handoff` to the page's own canvas, first in reading
   order.
2. Paste the template below into one text layer.
3. Delete the lines that do not apply, tick one box per question, and keep the
   numbered headings — the headings are what gets read.

## Which sections apply

Routing is by what the page _does_, not only by its archetype: `/resume` is a
prose document that reads the `resume` collection, so it fills section 4.

| Section           | Fill it when                                                | Skip when                                     |
| ----------------- | ----------------------------------------------------------- | --------------------------------------------- |
| 1 Archetype       | always                                                      | never                                         |
| 2 What this is    | always                                                      | never                                         |
| 3 Frame index     | the page has more than one frame                            | single-frame page — say so in §2              |
| 4 Content map     | the page reads a content collection, whatever its archetype | nothing on the page comes from `src/content/` |
| 5 Flow            | something on the page is clickable or changes state         | a static document                             |
| 6 Link map        | anything links out                                          | nothing links out                             |
| 7 Copy            | always                                                      | never                                         |
| 8 Components      | always                                                      | never                                         |
| 9 States          | the page uses any interactive component                     | nothing interactive is drawn                  |
| 10 Motion         | anything moves                                              | nothing moves — write `none`                  |
| 11 Responsive     | always                                                      | never                                         |
| 12 Open questions | always                                                      | never                                         |

## The template

```
HANDOFF — /route
Figma page: <page name>                    Updated: YYYY-MM-DD

1 ARCHETYPE — pick one
[ ] page                  one route, one file, nothing repeats
[ ] collection index      lists many entries of one collection
[ ] collection detail     one entry as example
[ ] prose document        long-form text; prints to PDF

2 WHAT THIS IS — pick one
[ ] one screen            everything is there at once
[ ] a set of states       the same screen, drawn several times
[ ] one continuous flow   steps accumulate, or replace each other
Carries across frames: ____________  (or: nothing)
Visitor arrives at: ____________

3 FRAME INDEX — one line per frame on this page
<frame name> — a still of: ____________
<frame name> — not a build target: [ ] reference [ ] unfinished [ ] to delete

4 CONTENT MAP — whenever the page reads a content collection; otherwise: n/a
Collection: [ ] projects [ ] playground [ ] inspiration [ ] questions
            [ ] curiosity [ ] resume [ ] releaseNotes
<layer name> -> <field name>               (field names: docs/cms.md)
Optional field empty   -> [ ] hide the element [ ] keep the space [ ] fall back to: ______
No entries at all      -> [ ] cannot happen [ ] show: ______
Text longer than drawn -> [ ] let it wrap [ ] clamp at ___ lines [ ] must not grow
A layer with no field, or a field with no layer: ____________

5 FLOW — one line per control; nothing clickable: none
<control label> -> <frame name, or /route>
Prototype links wired in Figma: [ ] yes [ ] no — the lines above are the graph

6 LINK MAP — every outgoing link, including ones with no page yet
/route  [ ] page exists  [ ] not built yet -> [ ] link anyway [ ] render as plain text

7 COPY — pick one
[ ] all final
[ ] all placeholder
[ ] mixed, placeholders marked [bracketed] in the frames
[ ] mixed, not marked — the placeholders are: ____________

8 COMPONENTS
Library sets this page uses: ____________
Anything drawn here that is not a library set: [ ] no [ ] yes: ____________
  for each -> [ ] build it inline on the page
              [ ] it belongs in the library, add it there first

9 STATES — per interactive component on this page; leave nothing silent
<component>  drawn: ______  needed, not drawn: ______  deliberately none: ______
(the six worth answering: hover, focus, selected/active, disabled, empty, loading)

10 MOTION — per moving element; nothing moves: none
<element>
  trigger:  [ ] page load [ ] hover [ ] focus [ ] click [ ] scroll position (ask me first)
  moves:    [ ] fade [ ] slide [ ] scale [ ] colour [ ] shadow [ ] other: ______
  duration: [ ] duration/fast [ ] duration/base [ ] duration/slow
  easing:   [ ] easing/standard [ ] easing/entrance
  if CSS cannot do it exactly, it must still: ____________

11 RESPONSIVE — below 48rem
[ ] mobile frame: <frame name>
[ ] no mobile design yet -> [ ] stack in source order, ask before anything else
                            [ ] rules: ____________

12 OPEN QUESTIONS — deliberately undecided
- ____________
(nothing open: write none)
```

The options are the repo's own vocabulary, so they are picked, not substituted:
the seven collections are the seven in `src/content.config.ts`; `duration/*` and
`easing/*` are the Figma variable names for the five motion tokens in
`src/styles/tokens.css`; `[bracketed]` is the placeholder convention (CLAUDE.md
R6); `48rem` is the site's single breakpoint. Scroll-driven motion is asked
about rather than ticked because it is above the CSS ceiling and is never
decided alone.

## Why each section is asked

| Section           | Why it is asked                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| 1 Archetype       | Decides routing and what has to survive testing.                                                    |
| 2 What this is    | The question that cost two rewrites on `/home`.                                                     |
| 3 Frame index     | Stops a frame being read as a page — a frame is a still, and of what is not always visible.         |
| 4 Content map     | The frame shows one filled-in example; the code faces zero, one and many.                           |
| 5 Flow            | The whole `/home` graph was reconstructed from button labels, because no frames were wired.         |
| 6 Link map        | Six chips on `/home` still 404; a link with no page needs a decision, not a guess.                  |
| 7 Copy            | A `…` run read as final text once; placeholders have a convention, so use it.                       |
| 8 Components      | Pairs with the library drift check in Step 4 of the skill and `design/components.json`.             |
| 9 States          | Every state invented on `/home` was one the frames had not drawn.                                   |
| 10 Motion         | Three prose sentences covered a whole page's motion last time, and it was not enough to build from. |
| 11 Responsive     | The `Mobile` frame is empty, so everything below `48rem` on `/home` is unreviewed.                  |
| 12 Open questions | So the next read asks instead of invents.                                                           |

## What not to put in it

- **No values.** Colours, spacing, type sizes, radii and shadows are read from
  the variables (`get_variable_defs`). Naming them twice is how they drift.
- **No description of what the frame looks like.** The screenshot is read every
  time, without exception.
- **No rationale.** The Figma file is the decision (CLAUDE.md R5). The handoff
  records what, not why.
- **Nothing the template did not ask for.** If an answer is "nothing", write
  `none` — that is a complete answer, and it is shorter than a paragraph.

---

## Worked example — /home

`/home` shipped before this document existed, so this example is reconstructed
from the repo record rather than from an actual Handoff frame. Any answer that
cannot be grounded that way says so rather than guessing — which is also what
an honest blank looks like.

```
HANDOFF — /
Figma page: chat-ground                    Updated: 2026-08-28

1 ARCHETYPE
[x] bespoke page          (reflections/2026-08-28.md:200-206)

2 WHAT THIS IS
[x] one continuous flow   steps accumulate: with the script running each
                          visited step moves into the transcript and stays
                          scrollable (index.astro:510-515); the no-JS baseline
                          shows one exchange at a time via :target
                          (index.astro:464-467)
Carries across frames: the transcript so far
Visitor arrives at: the `start` step, top of the page

3 FRAME INDEX
Mobile (103:1103) — not a build target: [x] unfinished — the frame is empty
home - 7 — a still of: the steps carrying the `…` runs
the rest of the index: [not recorded — confirm in Figma]

4 CONTENT MAP
n/a — /home reads no collection

5 FLOW
start ──▶ skip
  │        (chip links, six: /resume, /inspiration, /projects,
  │         /playground, /behind-the-scenes, /curiosities)
  ▼
team ──▶ skip
  │
  ▼
questions ──▶ skip
  │           (also carries /letters as an inline text link in its
  │            message body, not a chip — see 6)
  ▼
prototype ──▶ skip
  │
  ▼
questionnaire
  │
  ▼
field ──▶ role ──▶ stack ──▶ result
                               (chip links, six: /resume, /inspiration,
                                /projects, /playground, /behind-the-scenes,
                                /curiosities)
Prototype links wired in Figma: [x] no — the graph above was reconstructed from
chip labels (reflections/2026-08-28.md:159-162) and is literal in
index.astro:55-379

6 LINK MAP
/resume            [x] page exists
/inspiration       [x] not built yet -> [x] link anyway
/projects          [x] not built yet -> [x] link anyway
/playground        [x] not built yet -> [x] link anyway
/behind-the-scenes [x] not built yet -> [x] link anyway
/curiosities       [x] not built yet -> [x] link anyway
/letters           [x] not built yet -> [x] link anyway
(index.astro:105-110,176-205,341-346, checked against src/pages/)

7 COPY
[x] mixed, not marked — the placeholders are: the `…` runs, which stand for
values the tool would compute, not final text

8 COMPONENTS
Library sets this page uses: Buttons, Chat, user, logo, Icons
                             (node ids: design/components.json)
Anything drawn here that is not a library set: [x] no

9 STATES
Buttons  drawn: hover  needed, not drawn: —  deliberately none: —
Two states were not drawn and were invented instead — a submit control for the
questionnaire, and a fill for a selected/ticked option — then removed once the
interaction model was corrected (reflections/2026-08-28.md:142-146)

10 MOTION
chip background-color and box-shadow (index.astro:684-686)
  trigger:  [x] hover [x] focus
  moves:    [x] colour [x] shadow
  duration: [x] duration/fast
  easing:   [x] easing/standard
  if CSS cannot do it exactly, it must still: read as the chip responding to
  the pointer, not as a new element
a bubble or a choice group arriving (index.astro:563,577)
  trigger:  [x] page load
  moves:    [x] fade [x] slide
  duration: [x] duration/base
  easing:   [x] easing/entrance
  if CSS cannot do it exactly, it must still: read as arriving into the
  transcript rather than having always been there
arrival stagger (index.astro:567-571)
  trigger:  [x] page load
  moves:    [x] other: animation-delay per row — with the script running a row
            arrives when its own first character does, not on a fixed index
            stagger
  duration: [x] duration/base
  easing:   [x] easing/entrance
  if CSS cannot do it exactly, it must still: keep the rows in order
typing pace — 12ms per character, a 160ms beat between paragraphs in one bubble
  — is a page-level constant, deliberately not a token (src/lib/chat-typing.ts:1-2)
Notes: nothing here is defined in Figma — there are no prototype connections,
so get_motion_context returns nothing for this page. global.css:149-162 zeroes
durations under prefers-reduced-motion: reduce but not animation-delay.

11 RESPONSIVE — below 48rem
[x] no mobile design yet -> [x] stack in source order, ask before anything else
One breakpoint, 48rem. The Mobile frame is empty, so everything below it is
unreviewed.

12 OPEN QUESTIONS
- the unbuilt routes, all six ticked "link anyway": /inspiration, /projects,
  /playground, /behind-the-scenes, /curiosities, /letters
- the missing mobile design
- the frame index above §3's two named frames
```
