# Improvements — Figma → code

Companion to [`home-figma-to-code.md`](./home-figma-to-code.md). That one records
what happened on the first job and why. This one is only the changes, split by
who owns them.

Nothing here is done yet. Items marked **(R1)** need Max's approval because they
change `CLAUDE.md`.

---

## Sequence

Two of these block the rest, so order matters:

1. **B1 — port the Figma library into `src/components/`.** Until this exists,
   every page build re-decides what a button looks like. Max's framing: the full
   design system should already be in the repo, so translating a page becomes
   _matching_ Figma definitions to code definitions rather than inventing them.
2. **B2 — settle the width tokens.** `/projects` introduces a grid and will
   expose the gap immediately; fixing it after means renaming tokens already in
   use.
3. **A1 — one Handoff frame**, for whichever page is next. The rest of the Figma
   work can follow page by page.
4. Everything else, in any order.

---

## The standing checklist

Max's takeaways, which belong at the top of the skill file and get read before
every job:

- A frame is a still, not a screen. Ask what it is a still _of_.
- Needing to invent a control means the model is wrong.
- A near-miss token is drift.
- With every run, check if the library was updated, and compare against the
  version history of `src/components/`.
- Read the whole declaration, not the part that looks like a token.
- Verify behaviour over time, not the end state.
- Assert outcomes, not mechanisms.

---

## A. The Figma file — Max

### A1. A `Handoff` frame per page

One frame per page, sitting with that page's frames, read before any other
frame. Required sections:

| #   | Section                                                                                                                                         | Why it exists                                          |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 1   | **Archetype** — bespoke / collection index / collection detail / prose doc                                                                      | decides routing and what to test                       |
| 2   | **What this is** — one screen, a set of states, or one continuous flow; what persists; where a visitor enters                                   | the question that cost two rewrites                    |
| 3   | **Frame index** — each frame, and what it is a still _of_                                                                                       | stops frames reading as pages                          |
| 4   | **Content map** _(collection pages)_ — layer → schema field; what the layout does when an optional field is empty; what "no entries" looks like | the frame shows one example; the code faces N          |
| 5   | **Flow** — which control leads where                                                                                                            | I inferred the whole graph from button labels          |
| 6   | **Link map** — every link to a route, including routes not built                                                                                | six chips currently 404                                |
| 7   | **Copy** — what is final, what is placeholder                                                                                                   | `[bracketed]` is already the repo convention (R6)      |
| 8   | **Components** — which library sets this page uses, and any new one it needs                                                                    | pairs with the drift check in B3                       |
| 9   | **States** — drawn / not drawn / derive                                                                                                         | every state I invented was one not drawn               |
| 10  | **Motion** — per element: trigger, what moves, duration and easing _by variable name_, and the fallback intent                                  | three prose sentences covered the whole page last time |
| 11  | **Responsive** — what changes below `48rem`, or "no mobile design yet"                                                                          | the `Mobile` frame is empty                            |
| 12  | **Open questions** — what was deliberately left undecided                                                                                       | so I ask instead of invent                             |

**Done when:** a page has a Handoff frame and I can state its interaction model
in one paragraph without opening another frame.

### A2. Prototype connections between frames

Wire the frames with real prototype links. Two payoffs: the flow graph stops
being something I reconstruct from copy, and `get_motion_context` starts
returning something — right now it has nothing to read.

### A3. Motion as a spec

Per animated element rather than per page: what triggers it, what moves, and the
duration and easing **named as variables** (`duration/base`, `easing/entrance`),
so the handoff carries token names rather than adjectives.

### A4. Draw the states that are missing

Per component: hover, focus, selected, disabled, empty. Where a state should not
exist, say so. Both things I invented on `/home` — a submit control and a
selected-option fill — were states the frames did not draw.

### A5. Mark placeholder vs final copy

The `…` runs on `home - 7` are placeholders for values the tool would compute. I
guessed right; the convention should not depend on that.

### A6. A route map

Every link target, including pages that do not exist yet, so the code can point
somewhere deliberate rather than somewhere plausible.

### A7. Responsive intent

`Mobile` (`103:1103`) is an empty frame. Everything below `48rem` on `/home` is
mine and unreviewed. Either a mobile frame, or a written rule per page.

### A8. Width definitions

See B2 — the code side needs a decision from the design side first:

- which widths are a **measure** (a character count for a given face and size),
- which are **layout** (columns and gutters of a page grid),
- which are genuinely a **component's own** fixed width.

### A9. Housekeeping

- Delete `Sizes/L: 24` — it duplicates a computed line height and sits outside
  the seven collections.
- Rebind the `/home` frames to the new `line-height/loose` variable, so the file
  and the code agree.
- Keep WEB code syntax set on every new variable; without it the MCP emits
  `var(--name\/with\/slashes)`, which is not valid CSS.

---

## B. The repo — before the next page build

### B1. Port the whole Figma library into `src/components/`

**The keystone.** Max's idea, and the one that changes the shape of every future
job: if the design system already exists in code, translating a page is matching
definitions rather than inventing them.

What exists in Figma today, and what it becomes:

| Figma set              | Variants                                                            | Becomes                                                             |
| ---------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `Buttons` (`109:1382`) | Type = Primary / Secondary / Nav / Inline × State = Default / Hover | `Button.astro` — `type` as a prop; hover is a CSS state, not a prop |
| `Chat` (`109:1389`)    | Type = message / request / response × Variant = text / selection    | `ChatBubble.astro` — `type` and `variant` props                     |
| `user` (`117:1308`)    | moritz / karina / paula / all                                       | `Avatar.astro` — SVGs already in `public/avatars/`                  |
| `logo` (`108:1372`)    | favicon / chat-tomato / chat-herbs                                  | `Logo.astro`                                                        |
| `Icons` (`109:1374`)   | Cursor / Figma Make                                                 | `Icon.astro`                                                        |

**Variant properties map mechanically to props** — `Type=Primary` becomes
`type="primary"` — the same one-to-one trick that keeps the tokens honest. A
name that does not transform cleanly is itself the finding.

Three things to be honest about:

- **This is not free.** `/home` currently carries the chat as page-scoped CSS
  and would be refactored onto `ChatBubble`. `index.astro`, `resume.astro` and
  `ProseLayout` each invent their own link styles and would move onto `Button`.
  It is its own PR — or a few — not something smuggled into a page build.
- **It deliberately contradicts R8**, which forbids building a component before
  its second use. That needs the R8 amendment in C4 to be honest rather than
  quietly broken.
- **`/styleguide` should render every component**, so nothing built ahead of its
  first page use is dead code, and so there is one place to compare against
  Figma by eye.

**Done when:** every published Figma component set has a counterpart in
`src/components/`, rendered on `/styleguide`, and no page defines its own version
of one.

### B2. Settle the widths

The three we hardcoded are three different kinds of constraint:

| Kind                                 | Governed by                   | Expressed as                                     |
| ------------------------------------ | ----------------------------- | ------------------------------------------------ |
| **Measure** — how wide text may run  | characters, per face and size | `ch` tokens, like the existing `--measure: 68ch` |
| **Layout** — columns, grids, gutters | the page frame                | one grid definition, not per-page widths         |
| **Component** — a fixed element      | the component                 | last resort, named for the component             |

`--size-chat-column` (866) is layout, `--size-chat-bubble` (531) is a measure
(~46 characters of mono at `--font-size-sm`), `--size-chat-choice` (400) is a
component cap the design's own instances exceed. **Those names will not survive
`/projects`.** Define the grid and the measures once; keep `--size-*` small and
name it for the component when it is genuinely unavoidable.

### B3. A library ↔ code drift check

Max's takeaway: _check with every run whether the library changed._ Make it
cheap by mirroring what already works for tokens.

`design/tokens.json` is the exchange record for variables. Add
**`design/components.json`** as the exchange record for component sets: each
set's name, node id, variant properties and description. Then:

- a session reads the library once and diffs against the manifest — the delta is
  small, so it costs little and lands in context cheaply;
- a component in Figma with no entry means new design work to port;
- an entry with no component in `src/components/` means the port is incomplete;
- a changed variant property means a prop signature changed.

**Done when:** the diff is a documented step in the skill, and the manifest is
committed alongside the components.

### B4. `docs/figma-handoff.md`

The template behind A1, so writing a Handoff frame is a checklist rather than a
blank page. `/home` filled in as the worked example.

---

## C. Skills and docs

### C1. Rename and restructure `figma-implement.md`

Max is right that the name hides what it is for. Proposed:
**`figma-to-astro.md`**, with a description line naming the whole target —
HTML, CSS, Astro, Decap. Easy to rename again; the content matters more.

Restructure from a single-frame procedure into a page-building method:

- **the standing checklist** at the top;
- **archetypes** as the opening move — bespoke, collection index, collection
  detail, prose document — with the routing and failure modes each implies;
- **Step 0: the Handoff frame**, or its twelve questions asked directly;
- **component inventory and the drift check** as a required step, replacing the
  current lean on Code Connect — which needs a Dev/Full seat and silently did
  nothing all session;
- **a collection-pages section**: layer-to-field mapping, zero and many entries,
  absent optional fields, `astro:assets`, and design ↔ schema reconciliation in
  both directions;
- **the read order**, including the recursive text walk —
  `findAllWithCriteria` does not descend into instances;
- **the invention heuristic** in the motion step;
- **verification**: motion assertions about intermediate states, a JS-off pass,
  a keyboard pass, and "assert outcomes, not mechanisms";
- **§4 gains**: `nowrap` text grows past a max-width in Figma but is clipped by
  `max-width` in CSS; an asset's intrinsic size is not a token;
- **new "Traps in this codebase"**: Astro's scoped CSS vs JS-created nodes;
  `[hidden]` vs an explicit `display`; the `animation` shorthand resetting
  `animation-delay`; the `prefers-reduced-motion` blanket covering duration but
  not delay;
- **new "Mechanics"**: `www.figma.com` is blocked by the egress policy, so
  assets come through `exportAsync({format:'SVG_STRING'})`; the code-syntax
  platform enum is `iOS`, not `IOS`.

### C2. Plan mode and an orchestrator, written into the skill

Max's proposal, designed against what the session actually cost. The measured
shape was **40.7M cache reads against 68k output** — almost nothing was spent
writing, nearly all of it re-reading context every turn. So the lever is not
"write less", it is **keep large material out of the main thread entirely**.

A subagent's reading happens in _its_ context; only its summary reaches mine.
That is the whole mechanism.

**Phase 1 — Survey.** Subagents, in parallel, each returning a decision-ready
brief rather than raw material:

| Agent          | Reads                                | Returns                                                                   |
| -------------- | ------------------------------------ | ------------------------------------------------------------------------- |
| Design reader  | Handoff frame, metadata, screenshots | archetype, interaction model, frame index, flow — a page or two           |
| Library differ | Figma component sets and variables   | the delta against `design/components.json` and `tokens.css`, nothing else |
| Repo mapper    | the code areas in scope              | file map and existing patterns                                            |

**Phase 2 — Plan.** Main thread, high effort, in plan mode. Consumes the three
briefs, produces the plan — archetype, interaction model, token diff, component
inventory, motion spec — and ends by putting the open questions to Max.
**Nothing is built.**

**Phase 3 — Build.** Main thread. This does not split: each step depends on the
last, and handing it off means re-establishing context every time.

**Phase 4 — Verify.** Subagents again: one runs the probes and returns pass/fail
plus _only_ the failing detail; one returns the contrast table and keyboard
order. The full green lists I printed last time became permanent context for the
rest of the session.

**Phase 5 — Ship.** Main thread, with tight tooling.

Rules that fall out, and belong in the skill:

- A subagent returns a **summary**, never raw material.
- Anything bulky that will not be needed on later turns is produced in a
  subagent, not the main thread.
- The main thread holds three things: the design decisions, the file being
  edited, and the conversation with Max.
- When a tool returns far more than asked for, **stop calling it that way** —
  I listed the entire workflow history four times after seeing it misbehave once.

### C3. `docs/design-system.md`

- **Widths**: the measure / layout / component distinction from B2, and the rule
  that `--size-*` is the last resort rather than the first.
- **Motion**: currently reads "Not defined in Figma yet". One page has now
  defined it — record what `/home` established.
- **States to draw**: what a component needs before it can be built without
  invention.
- **The two invented states** as a worked example, in the shape that section
  already uses for `pickled/600`.

### C4. `CLAUDE.md` — proposals **(R1)**

1. **Drop R11** ("Zero client JS…"), per Max's call. Worth recording alongside:
   the no-JS baseline is what made `/home` degrade into seven readable steps and
   what caught the focus-on-load bug. Suggest it survives as a _practice_ in the
   skill — my file, easy to strike — rather than a rule in Max's.
2. **Amend R8** so components are discovered in the Figma library rather than by
   counting uses in code, and `src/components/` exists for them. The
   anti-speculation intent survives, with a sharper test: _a set in the library,
   or inline on the page._ Without this, B1 contradicts the rule book.
3. **§3 Stack** — the "Zero client JS" row must match whatever replaces R11.
4. **§4 Map** — add `public/avatars/`, `src/components/`,
   `design/components.json`, `docs/figma-handoff.md`.
5. **§6 Procedures** — point the Figma procedure at the Handoff frame and the
   archetypes; add design ↔ schema reconciliation to "changing a content field".

---

## D. Token discipline

Measured, from the session that produced `/home`: 40,720,868 cache reads,
1,040,857 cache writes, 68,095 output, $81.44, ~15 hours.

**Anything large that lands in context is paid for on every remaining turn.** A
6k-token tool result arriving with 70 turns to go costs closer to 420k. That is
what makes the items below worth the discipline.

**Spend less on:**

- repeated GitHub reads — never re-list workflow runs; narrow every read;
- full PR bodies when two fields were wanted;
- failed edits that dump a whole file back — format first, match on short
  anchors, write before asserting;
- printing full green test output after the first run.

**Spend more on:**

- reading the Figma library (zero last time; it caused a rework);
- motion verification during the build rather than after the report;
- for collection pages, reading the schema and one real entry before the frame.

---

## Done when

Measured on the next page, not on whether it looks right — it looked right after
#32, and two rewrites followed:

1. The interaction model can be stated in a paragraph from the Handoff frame
   alone, before any frame is read.
2. The component inventory is written before any markup, and nothing is built
   that the library already had.
3. For a collection page: zero, one and many entries, and every optional field
   absent, are all looked at before the PR.
4. Every value with no token is listed before any CSS is written.
5. Motion has assertions about intermediate states.
6. Nothing is invented; anything that wants inventing surfaces as a question.
7. **Zero rewrites of merged work.**
