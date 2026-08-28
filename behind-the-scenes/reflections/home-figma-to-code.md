# Reflection — the first Figma → code job

`/home`, translated from the `/home` page of the Figma file into
`src/pages/index.astro`. Shipped across five PRs (#32–#36) on 27–28 Aug 2026.

**Two of those five were rewrites of work that was already merged and live.**
The building was fine. The _reading_ of the design was wrong, twice, in the same
way. This is the record of why, and what both sides change before the next page.

Written jointly: Max raised three of the findings, I raised the rest.

The actionable counterpart is
[`figma-to-code-improvements.md`](./figma-to-code-improvements.md) — this file
says what happened and why, that one says what changes.

---

## What actually shipped

| PR  | What                                                                 | New work or rework?    |
| --- | -------------------------------------------------------------------- | ---------------------- |
| #32 | The chat: seven steps, tokens, avatars, motion, a11y                 | new                    |
| #33 | Bubbles arrived before their text; sequencing tied to the typewriter | rework of #32          |
| #34 | The selected-response chip rendered as unstyled plain text           | rework of #32          |
| #35 | Seven discrete states → one continuous transcript                    | **rewrite of #32**     |
| #36 | The questionnaire form → four ordinary chat turns                    | **rewrite of #32/#33** |

Everything below is an attempt to make #35 and #36 not happen again.

---

## The three things Max found

### 1. "Having multiple frames didn't help in bringing across the concept of scrolling the page and having a chat-like interface"

Correct, and this was the expensive one.

Seven frames named `home - 1` … `home - 7` read as seven pages. I built seven
pages — one on screen at a time via `:target` — because that is literally what
the frames showed. They were stills of one continuous transcript.

What makes it worse: I wrote the reasoning down and shipped it. In #33 I said,
about the questionnaire, _"Turning them into a four-turn exchange would be a
different design, so it is not in here."_ I used a frame's literal composition
to overrule an obvious interaction and called that faithfulness. Then did the
same thing again, which is #36.

**A frame is a still, not a screen.** The question that was never asked, by
either of us: _what is this a still of?_

Neither a better frame name nor more frames would have fixed this. What fixes it
is one sentence somewhere in the file saying "this is one continuous flow; the
frames are moments in it". See the Handoff frame below.

### 2. "You missed the component set in Figma for user responses entirely in the first run"

Also correct, and entirely my fault. The `Chat` set (`109:1389`) has five
variants, including `response/selection` — exactly the chip I needed. I built it
as page-scoped CSS instead, hit a bug because of that, and only found the
component when Max pointed at it in round four.

I never opened the library pages. I read frames. The library was **well built and
I did not look at it**, which also means I missed:

| Set                    | Variants                                          | Status                                                                                       |
| ---------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `Buttons` (`109:1382`) | 10 — Primary/Secondary/Nav/Inline × Default/Hover | not built; link styles are duplicated across `index.astro`, `resume.astro` and `ProseLayout` |
| `Icons` (`109:1374`)   | 2                                                 | not built                                                                                    |
| `logo` (`108:1372`)    | 3                                                 | one variant inlined as SVG                                                                   |
| `user` (`117:1308`)    | 4                                                 | inlined as SVGs                                                                              |

`Buttons` carrying **Nav** variants says a nav bar is already designed, and that
four link treatments are already decided while three files invent their own.

**The rule this produces** (Max's framing): a published Figma component set is
the designer's statement that something is reusable, so it becomes a component in
`src/components/`. That is checkable _before_ building, unlike "extract on the
second use", which requires the second use to have happened. It needs R8
amended — see below.

### 3. "The width of chat bubbles, which I manually defined in Figma but didn't use tokens for, as the existing ones don't cover different width usages"

This is a real gap in the system, not a mistake by either of us — and it is the
most interesting of the three.

We papered over it mid-build by adding a `Size` collection: `size/chat-column`
866, `size/chat-bubble` 531, `size/chat-choice` 400. **Those names will not
generalise.** `/projects` will want card widths and grid columns, and if we keep
going this way we accumulate one-off width tokens per page.

Looking at what the three widths actually _are_:

- **866px** is a layout column — the readable width of the page's content.
  `--content-max: 72rem` already exists for this job.
- **531px** is a _measure_: at `--font-size-sm` in mono with
  `--letter-spacing-extra-wide`, it is roughly 46 characters. It is a
  typographic constant, not a spacing one. `--measure: 68ch` already exists on
  exactly that principle.
- **400px** was a cap that the design's own instances ignore — Figma's `nowrap`
  text grows past a max-width constraint, so the real longest chip is 452px.

So the missing thing is not "more spacing steps". It is a distinction the system
has never drawn:

| Kind of width                        | Governed by                   | Should be expressed as                                 |
| ------------------------------------ | ----------------------------- | ------------------------------------------------------ |
| **Measure** — how wide text may run  | characters, per face and size | `ch` tokens, like `--measure`                          |
| **Layout** — columns, grids, gutters | the page frame                | a grid definition (columns + gutter), not fixed widths |
| **Component** — a fixed element      | the component itself          | last resort; name it for the component                 |

**Proposal for the design system:** define measure tokens in `ch` for the faces
and sizes that carry body text, and define the page grid once, rather than
adding a width token per page. Revisit `--size-chat-*` when `/projects`
introduces a grid — they are the last-resort category and should stay small.

---

## What I found

Things Max did not raise, in rough order of what they cost.

**I verified end states, not behaviour over time.** In #32 I screenshotted the
settled page and called the motion done. Every bubble was on screen inside 600ms
while its text typed in over seconds — visible immediately to anyone who watched
it, invisible to a screenshot. Any timed behaviour now needs an assertion about
an _intermediate_ state.

**I asserted mechanisms, not outcomes.** My first test for the withdrawn options
checked `hasAttribute('hidden')`. It passed while the chips sat there in my own
screenshot, because `.chat__choices` sets `display` explicitly and that beats the
UA's `[hidden]` rule. Asserting computed `display` caught it.

**I substituted a near-miss token.** Avatars are 87px; I reached for
`--space-2xl` (96px). That is precisely the "close to a token but not equal →
STOP and ask" case the skill already names, and I did it anyway. The check needs
to be mechanical rather than remembered.

**I read half a declaration.** I took `max-w-[400px]` from the emitted class list
and dropped `whitespace-nowrap` from the same list. The pair only means anything
together — which is why chips wrapped to two lines.

**Inventing UI was a symptom I ignored.** I invented a "Run the prototype" submit
chip and a lemon fill for a ticked option, flagged both honestly as mine, and
Max carried them as open questions for two rounds. Both vanished the moment the
model was corrected in #36. **Needing to invent a control means the model is
wrong** — it is a stop signal, not a gap to fill.

**No route manifest.** Six chips point at pages that do not exist. That was Max's
explicit call, but the design never said where they go, and nothing in the repo
lists intended routes.

**No mobile design.** The `Mobile` frame (`103:1103`) is empty. Everything below
`48rem` is mine and unreviewed.

**Placeholder vs final copy is unmarked.** The `…` runs are placeholders and the
repo already has a `[bracketed]` convention (R6), but the frames do not
distinguish them. I guessed correctly; I might not next time.

**The flow graph was inferred from chip labels.** There are no prototype
connections between the frames, so I reconstructed the entire branching
structure by reading button text. Real connections would also make
`get_motion_context` useful, which it currently is not.

---

## Max's questions

### What is missing in Figma to hand off reliably

In order of what it cost:

1. **The interaction model.** One screen, a set of states, or one continuous
   flow? What persists between frames? Where does a visitor enter?
2. **The flow graph** — prototype connections, not inferred from labels.
3. **Motion as a spec, not a paragraph.** Per element: trigger, what moves,
   duration and easing _by variable name_, and what it must still feel like if
   the honest version cannot match.
4. **States that aren't drawn** — hover, focus, selected, empty. Every state I
   invented was one the frames did not draw.
5. **Which copy is final** and which is placeholder.
6. **Link targets**, including routes that do not exist yet.
7. **Responsive intent**, or an explicit "no mobile design yet".
8. **For collection pages** (everything after `/home`): which layer is which
   schema field, and what the layout does when an optional field is absent.

The proposal: a **Handoff frame** per page, sitting with that page's frames,
which I read _first_, before any other frame. Max writes it; I only read it. The
repo gets `docs/figma-handoff.md` describing what it must contain, so writing one
is a checklist rather than a blank page:

> archetype · what this is · frame index (what each is a still _of_) · content
> map · flow · link map · copy status · components used · states drawn/not
> drawn · motion per element · responsive · deliberately open questions

### How the plan should look

The plans this session were mostly right. Three things were missing, and one
thing about the _next_ pages changes the shape entirely.

**The archetype comes first.** `/home` is the least representative page we will
ever build — it is bespoke, and its design _is_ its content. Everything
remaining is a **template over a content collection, edited through Decap**:

| Archetype         | Example                                                    | Routing                             | What varies                                            |
| ----------------- | ---------------------------------------------------------- | ----------------------------------- | ------------------------------------------------------ |
| Bespoke page      | `/home`, `/styleguide`                                     | one file                            | nothing                                                |
| Collection index  | `/projects`, `/inspiration`, `/playground`, `/curiosities` | `getCollection()`                   | how many entries, which optional fields each has       |
| Collection detail | a case study                                               | `[slug].astro` + `getStaticPaths()` | which of eight sections exist, how long each is        |
| Prose document    | `/handshake`, `/resume`                                    | `ProseLayout`                       | prints to PDF — editing means re-running `npm run pdf` |

For a collection page the frame shows **one filled-in example** and the code must
survive N entries including zero, absent optional fields, and text far longer
than the mockup. `projects` alone has eight optional case-study sections, two
teaser images with refined alt-text pairs, and a 280-character `summary` cap. The
plan has to name those cases before building, not discover them.

It also has to reconcile design against schema in both directions: a frame
showing a field the schema lacks is a three-file change
(`content.config.ts`, `public/admin/config.yml`, `docs/cms.md`); a schema field
no frame shows is either dead or the design is incomplete.

**Then add, in every plan:**

- the interaction model, stated in a paragraph and confirmed before any code;
- a component inventory taken from the **library pages**, not the frames;
- named motion assertions, not "check by eye".

**Keep, they worked:** the token diff before any CSS; reporting drift rather than
resolving it; stating explicitly what I will _not_ do; and costing the honest
version out loud when the design asks for something the ceiling will not reach.

### Questions worth asking Max

These are the standing questions. The Handoff frame is simply their answers,
written once per page instead of asked every time.

1. What is this page — one screen, a set of states, or one continuous flow?
   What carries over between frames?
2. Which control leads where, and where does each link go — including pages that
   do not exist yet?
3. Which text is final and which is placeholder?
4. Which states are drawn, and for the ones that aren't — derive them, or leave
   them out?
5. What happens below the breakpoint?
6. For each motion: what triggers it, what moves, and what must it still feel
   like if I cannot do it exactly?
7. _(collection pages)_ Which layer is which field, and what does the layout do
   when an optional one is empty?
8. What did you deliberately leave open, so I ask instead of inventing?

### Takeaways for upcoming plans

- A frame is a still, not a screen. Ask what it is a still _of_.
- Check the Figma library before writing markup. A component set is a component.
- Needing to invent a control means the model is wrong.
- A near-miss token is drift.
- Read the whole declaration, not the part that looks like a token.
- Verify behaviour over time, not the end state.
- Assert outcomes, not mechanisms.

---

## Token and model use

Measured for this session:

|              |                                |
| ------------ | ------------------------------ |
| Model        | `claude-opus-5`, effort `high` |
| Cache reads  | 40,720,868                     |
| Cache writes | 1,040,857                      |
| Output       | 68,095                         |
| Cost         | $81.44                         |
| Wall clock   | ~15 hours                      |

_(Max asked about "Opus 6 High" — this ran on Opus 5 at high effort.)_

**The shape of that bill is the finding.** Output was only 68k tokens; cache
reads were 40.7M — six hundred times more. Almost nothing was spent _writing_.
Practically all of it was spent re-reading the conversation on every turn.

Which means: **anything large that lands in context is not paid for once, it is
paid for on every remaining turn.** A 6k-token tool result arriving with 70 turns
to go costs something closer to 420k cache-read tokens. That reframes what
"wasteful" means here.

### Where it went well

- **One Explore agent at the start** (~74k tokens) read the whole repo and
  returned a dense map. Its 74k stayed in _its_ context; only a summary entered
  mine. Because of it I never re-read `tokens.css`, `global.css`, `BaseLayout` or
  `content.config.ts` all session. This is the single best-value call I made.
- **`get_variable_defs` before any CSS** — a few hundred tokens that prevented
  every hardcoded value.
- **One `get_design_context`, not seven.** The other six frames came from
  screenshots plus a recursive text walk. Roughly an order of magnitude cheaper,
  and it lost nothing.
- **Tests written once, re-run across five PRs.**

### Where it did not

- **`list_workflow_runs` with `per_page: 1` returned the entire 20+ run history,
  four times.** Each dump then sat in context for the rest of the session. The
  waste is not the first call — it is that I saw it misbehave and called it three
  more times. _Rule: when a tool returns far more than asked for, stop calling
  it that way._
- **Full PR bodies read back before each merge**, four times, when I needed two
  fields. _Rule: narrow every GitHub read with `fields`._
- **Failed `python3` edits dumping the whole of `index.astro`** — four or more
  times, hundreds of lines each, because I matched against text Prettier had
  reformatted. _Rule: format first, match on short anchors, write before
  asserting._
- **Plan-file rewrites** instead of section edits.

### Where it should have been _raised_

- **Reading the Figma library**: I spent zero. It would have cost perhaps 10k and
  saved the #34 rework.
- **Motion verification in #32**: near zero. The bugs cost far more than the
  probes would have.
- **For collection pages**: reading the schema and a real entry before the frame
  — currently zero, and it will matter immediately.

### Orchestrator vs subagents

Honest answer: **high effort was right for the design translation and wasteful
for everything around it.**

The work that genuinely needed a large model with full context: the interaction
model, the token diff, the motion ceiling decisions, and the checkpoints with
Max. Those are judgement calls where being wrong cost a rewrite.

The work that did not, and should be delegated next time:

| Work                                      | Why it delegates well                                                                                       |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Repo survey                               | already delegated, and it paid for itself                                                                   |
| Copy extraction and asset pull from Figma | mechanical, scriptable, returns something compact                                                           |
| Verification runs                         | should return pass/fail plus _only_ failing detail; the full green lists I printed became permanent context |
| PR / merge / deploy checking              | the biggest avoidable sink, and almost pure mechanism                                                       |

The build itself does not split well — each fix depended on the last, and
handing that to a subagent would mean re-establishing context every time.

So for the next page: same model for the design work, subagents for the survey,
the extraction and the verification loop, and much tighter GitHub reads.

---

## What changes, and where

### `docs/figma-handoff.md` — new

The Handoff frame spec: what the frame must contain, with `/home` filled in as a
worked example.

### `behind-the-scenes/skills/figma-implement.md`

Currently a single-frame procedure. It should become a page-building method:

- **archetypes** as the opening move;
- **Step 0 — the Handoff frame**, or the eight questions if there isn't one;
- **component inventory from the library** as a required step — the current
  Step 4 leans on Code Connect, which needs a Dev/Full seat and silently did
  nothing all session;
- **a collection-pages section**: layer-to-field mapping, zero and many, absent
  optional fields, `astro:assets`, design ↔ schema reconciliation;
- **the read order** including the text-walk recipe —
  `findAllWithCriteria` does not descend into instances;
- **Step 7** gains the invention heuristic; **Step 8** gains motion assertions, a
  JS-off pass, a keyboard pass, and "assert outcomes, not mechanisms";
- **§4 "What Figma cannot hold faithfully"** gains: `nowrap` text grows past a
  max-width in Figma but is clipped by `max-width` in CSS; an asset's intrinsic
  size is not a token;
- **new "Traps in this codebase"**: Astro's scoped CSS vs JS-created nodes;
  `[hidden]` vs an explicit `display`; the `animation` shorthand resetting
  `animation-delay`; the `prefers-reduced-motion` blanket covering duration but
  not delay;
- **new "Mechanics"**: `www.figma.com` is blocked by the egress policy, so assets
  come through `exportAsync({format:'SVG_STRING'})`; the code-syntax platform
  enum is `iOS`, not `IOS`;
- **a token-discipline note** from the section above.

### `docs/design-system.md`

- **Widths**: the measure / layout / component distinction, and the rule that
  `--size-*` is the last resort rather than the first.
- **Motion**: currently reads "Not defined in Figma yet". It is now defined for
  one page — record what `/home` established.
- **States to draw**: what a component needs before it can be built without
  invention.
- **The two invented states** as a worked example, in the same shape that section
  already uses for `pickled/600`.

### `CLAUDE.md` — proposals only (R1)

1. **Drop R11** ("Zero client JS…"), per Max's call. Worth recording alongside
   it: the no-JS baseline is what made `/home` degrade into seven readable steps
   and what caught the focus-on-load bug. Suggest keeping it as a _practice_ in
   `figma-implement` — my file, easy to strike — rather than a rule in Max's.
2. **Amend R8** so components are discovered in the Figma library rather than by
   counting uses in code, and `src/components/` exists for them. The
   anti-speculation intent survives: a set in the library, or inline.
3. **§3 Stack** — the "Zero client JS" row must match whatever replaces R11.
4. **§4 Map** — add `public/avatars/`, `docs/figma-handoff.md`, and
   `src/components/` once it exists.
5. **§6 Procedures** — point the Figma procedure at the Handoff frame and the
   archetypes; add design ↔ schema reconciliation to "changing a content field".

---

## How we will know it worked

Not "does the page look right" — that was true after #32, and two rewrites
followed. On the next page:

1. The interaction model can be stated in a paragraph from the Handoff frame
   alone, before any frame is read.
2. The component inventory is written down before any markup, and nothing gets
   built that the library already had.
3. For a collection page: zero entries, one entry, many entries, and every
   optional field absent are all looked at before the PR.
4. Every value with no token is listed before any CSS is written.
5. Motion has assertions about intermediate states.
6. Nothing gets invented; anything that wants inventing surfaces as a question.
7. **Zero rewrites of merged work.**

Count how many of the seven hold.
