---
name: figma-to-astro
description: 'Build a page of this site from its Figma design: HTML, CSS, Astro and Decap. Covers the page archetypes, the Handoff frame, the Figma MCP read order, the component inventory and library drift check, mapping Figma variables and effect styles to CSS custom properties, content-collection pages, translating prototype interactions into CSS-only motion, and the accessibility and verification gate before a page is called done. Use when a Figma page or frame is handed over to be built, or when an implemented page has to be re-synced with an updated design. Read-direction only — it does not write to Figma.'
disable-model-invocation: false
---

# Figma → Astro

This file is both the contract and the procedure. Build one frame at a time, in
the order below, and stop where it says STOP.

Read alongside: [`docs/design-system.md`](../../docs/design-system.md) — what the
tokens are _for_. Read it before choosing any colour.

Out of scope: writing to Figma. Any `use_figma` call requires the `figma-use`
skill and has left this skill's scope.

---

## 0. The standing checklist

Read before every job — the takeaways from the first page built this way:

- A frame is a still, not a screen. Ask what it is a still _of_.
- Needing to invent a control means the model is wrong.
- A near-miss token is drift.
- With every run, check if the library was updated, and compare against the
  version history of `src/components/`.
- Read the whole declaration, not the part that looks like a token.
- Verify behaviour over time, not the end state.
- Assert outcomes, not mechanisms.

---

## 1. Laws

These hold for every step. A run that breaks one is wrong even if the page looks
right.

| #   | Law                                                                                                                                                                                                  | Violation looks like                                                                     |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| L1  | The Figma file is the decision, not a draft. Report what looks wrong; never resolve it.                                                                                                              | Darkening a colour to pass contrast; extending a ramp; substituting a step.              |
| L2  | Author no style the design has not defined. Every declaration traces to a frame, to `global.css`, or to an accessibility requirement.                                                                | `a:hover { color: … }` invented because links "need" a hover.                            |
| L3  | Never write a literal that has a token.                                                                                                                                                              | `#d73457`, `16px`, `font-family:` in a component.                                        |
| L4  | One flat tier. No role names.                                                                                                                                                                        | `--text-secondary`, `--surface-default`.                                                 |
| L5  | No CSS before `get_variable_defs` has returned.                                                                                                                                                      | Values written first, reconciled with tokens after. Hex codes get committed. Every time. |
| L6  | Never `get_design_context` for more than one frame.                                                                                                                                                  | A page-sized response that crowds out the decisions you needed.                          |
| L7  | No-JS baseline. The page must be complete with the script blocked; client JS is progressive enhancement layered on top, never the thing that makes the page work. Say what it adds before adding it. | A page that is blank, or a dead-end flow, with JS off.                                   |
| L8  | Accessibility is part of done, not a follow-up.                                                                                                                                                      | Shipping and filing the focus states as a follow-up.                                     |

`src/pages/index.astro:706-712` is the worked example for L7: its own comment
states the contract — with the script blocked every chip is still a real link,
`:target` still moves between steps, and CSS still plays the arrival; the script
only adds what CSS cannot reach.

When a value in the design has no token and no obvious home: **STOP and ask.**
A magic number that ships is a magic number forever.

---

## 2. Archetypes

The archetype comes first — it decides routing and what has to survive testing.
`/home` is the least representative page this site will ever build: it is
bespoke, and its design _is_ its content. Everything after it is a template over
a content collection, edited through Decap.

| Archetype         | Example                                                    | Routing                             | What varies                                            |
| ----------------- | ---------------------------------------------------------- | ----------------------------------- | ------------------------------------------------------ |
| Bespoke page      | `/home`, `/styleguide`                                     | one file                            | nothing                                                |
| Collection index  | `/projects`, `/inspiration`, `/playground`, `/curiosities` | `getCollection()`                   | how many entries, which optional fields each has       |
| Collection detail | a case study                                               | `[slug].astro` + `getStaticPaths()` | which of eight sections exist, how long each is        |
| Prose document    | `/handshake`, `/resume`                                    | `ProseLayout`                       | prints to PDF — editing means re-running `npm run pdf` |

For a collection page the frame shows **one filled-in example** and the code
must survive N entries including zero, absent optional fields, and text far
longer than the mockup. `projects` alone has eight optional case-study
sections, two teaser images with refined alt-text pairs, and a 280-character
`summary` cap. The plan has to name those cases before building, not discover
them.

It also has to reconcile design against schema in both directions: a frame
showing a field the schema lacks is a three-file change (`content.config.ts`,
`public/admin/config.yml`, `docs/cms.md`); a schema field no frame shows is
either dead or the design is incomplete — ask, do not delete.

---

## 3. Connection

The Figma MCP server is declared in [`.mcp.json`](../../.mcp.json) at the repo
root, so any session started in this repo picks it up. It is the remote server
(`https://mcp.figma.com/mcp`) — no desktop app required.

`whoami` before anything else. Most "cannot find node" failures are auth or seat
errors wearing a different hat, and thirty seconds here saves twenty minutes of
re-reading node IDs that were correct all along.

If a read fails, in order:

1. `whoami` — confirms auth and shows rate-limit state.
2. Check the file is in a plan the account has a seat on. Files in someone
   else's draft space are unreadable even with the link.
3. Re-read the node ID from the URL.

---

## 4. Procedure

A design is handed over as a URL pointing at **one frame**, not a file:

```
https://figma.com/design/<fileKey>/<name>?node-id=<int>-<int>
             ↑ fileKey                            ↑ nodeId — swap - for :
```

`?node-id=1-2` is `1:2` when you pass it.

### Step 0 — The Handoff frame

- Read the page's `Handoff` frame before any other frame, per
  [`docs/figma-handoff.md`](../../docs/figma-handoff.md).
- If there is no Handoff frame, ask these eight questions verbatim, as a
  numbered list, and do not start building on inferred answers:
  1. What is this page — one screen, a set of states, or one continuous flow?
     What carries over between frames?
  2. Which control leads where, and where does each link go — including pages
     that do not exist yet?
  3. Which text is final and which is placeholder?
  4. Which states are drawn, and for the ones that aren't — derive them, or
     leave them out?
  5. What happens below the breakpoint?
  6. For each motion: what triggers it, what moves, and what must it still feel
     like if I cannot do it exactly?
  7. _(collection pages)_ Which layer is which field, and what does the layout
     do when an optional one is empty?
  8. What did you deliberately leave open, so I ask instead of inventing?
- **Output:** the archetype, and the interaction model in one paragraph. If you
  cannot write that paragraph, you are not ready to read a frame.

### Step 1 — Orient

`get_metadata` with the `fileKey` and that `nodeId`. Cheap structural overview;
use it to confirm you are pointed at the frame you think you are before pulling
anything heavy. With no `nodeId` it lists the file's pages.

If the frame needs a full text sweep — checking for placeholder copy, or every
outgoing link — remember `findAllWithCriteria` does not descend into instances.
Recurse into instance children explicitly, or the sweep silently misses whatever
content lives inside a component instance.

### Step 2 — Look at it

`get_screenshot`. **Never skip this.** The XML tells you structure; only the
image tells you intent — which element is the gesture, what is meant to be
quiet, where the eye is supposed to land.

**Output:** one sentence on what the frame is for. If you cannot write it, you
are not ready to build it, and the fix is to ask, not to start typing.

### Step 3 — Tokens

`get_variable_defs` for the frame. The mapping is mechanical:
`color/neutral/700` → `--color-neutral-700`. Swap `/` for `-`, prefix `--`. A
name that does not transform cleanly is itself the finding.

Diff every value against `src/styles/tokens.css`, then per value:

| What you find                    | What to do                                                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Matches a token                  | Use the token name. Never the literal.                                                                           |
| No token exists                  | Add it to all three: `design/tokens.json`, `src/styles/tokens.css`, the Figma collection. Two of three is a bug. |
| Close to a token but not equal   | **STOP and ask.** Either the design drifted or the system is missing a step.                                     |
| Emits `var(--color\/lemon\/500)` | Not a CSS bug — that variable is missing its WEB code syntax in Figma. Use the correct name and flag it.         |
| A one-off with no system home    | **STOP and ask.**                                                                                                |

**Output:** the token diff — matched, missing, disagreeing. Ask before
continuing if anything is in the last three rows.

### Step 4 — Component inventory and drift check

1. Read the library pages, not the page frames: Atoms (`114:14`) and Organisms
   (`114:15`) — the two URLs recorded in `docs/design-system.md:42-50`.
2. Diff the sets found against [`design/components.json`](../../design/components.json)
   (the component-set equivalent of `design/tokens.json`). It exists as of the
   library port and is the reuse mechanism — read it, do not re-derive it. Its
   shape: `figmaFile`, `readOn`, a `pages` name→id map, a `sets` array of
   `{ figmaName, nodeId, page, component, variantProperties, combinations, notes }`,
   and an `unbound` list of values the design uses that no variable holds.
   `notes` is where a code name or shape departs from the Figma name, and it is
   the field to read before assuming a rename is drift.
3. Read the delta only: a set with no manifest entry is new design work to
   port; an entry with no file under `src/components/` means the port is
   incomplete; a changed variant property means a prop signature changed; a
   `combinations` list that grew means the matrix filled in.
4. Variant properties map to props mechanically — `Type=Primary` → `type="primary"`
   — the same one-to-one rule that keeps tokens honest. A name that does not
   transform cleanly is the finding.
5. **Code Connect is unavailable on this account, not merely demoted.**
   `get_code_connect_map` and `add_code_connect_map` both answer _"You need a
   Dev or Full seat on an Organization or Enterprise plan"_ on a student seat —
   verified 29 Aug 2026, having previously been misread as "silently returned
   nothing". Do not spend a call on either. `design/components.json` is the
   replacement and the better one here: it is diffable, it lives in the commit,
   and it holds the `notes` a mapping table has nowhere to put.
6. Keep the "build it inline" fallback but restate it against amended R8: a set
   published in the library MAY become a component before its first page use;
   anything not in the library stays inline until its second use.

### Step 5 — The spec

`get_design_context`. One frame. Last. Translate:

| Figma                         | Code                                                                                                                       |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Auto-layout                   | `flex` or `grid` — pick from what the layout _is_, not from the panel                                                      |
| Item spacing / gap            | `gap: var(--space-*)`                                                                                                      |
| Padding                       | `var(--space-*)`                                                                                                           |
| Fill                          | `var(--color-*)`                                                                                                           |
| Corner radius                 | `var(--radius-*)`                                                                                                          |
| Effect style `Elevation / md` | `var(--shadow-md)` — read the **style name**, not the emitted `drop-shadow-[…]`                                            |
| Text style                    | The font tokens, plus whatever `global.css` already sets for that element                                                  |
| Absolute position             | Usually a flex/grid relationship in disguise. Reach for `position: absolute` only when the design genuinely layers things. |

Three readings to distrust — see §9.

### Step 6 — Build

`src/pages/index.astro` is the reference shape:

- `BaseLayout`, `<main id="main">`, `.container` for the page frame.
- A scoped `<style>` block at the bottom. Nothing global unless the pattern
  genuinely repeats across pages.
- `block__element` class naming (`.hero__eyebrow`, `.cv__download`).
- Semantic HTML first. A `<div>` with a click handler is a bug. Sections get
  `aria-labelledby` pointing at their real heading, as `/styleguide` does.
- Headings come pre-styled from `global.css` — pick the level, don't restate the
  styling.
- The one breakpoint in use is `48rem`, in `rem`. Add a second only if the
  design actually needs it.

### Step 7 — Motion

`get_motion_context` for prototype interactions and smart animate;
`export_video` when the timing has to be watched rather than read.

**The ceiling is CSS `transition` and `@keyframes`.** Within it use the motion
tokens: `--duration-fast` for hover and focus, `--duration-base` for state
change and entrance, `--duration-slow` for large ambient movement;
`--easing-standard` for anything that starts and ends on screen,
`--easing-entrance` for things arriving.

Animate `transform`, `opacity`, `color`, `border-color`, `box-shadow`. Not
`width`, `height`, `top` or `margin` — they force layout every frame.

**Do not add a `prefers-reduced-motion` block.** `global.css` already blankets
every transition and animation on the site.

**STOP and ask** — never decide these alone:

- Motion driven by scroll position (CSS `animation-timeline` included)
- View Transitions
- Anything needing a line of client JS
- Anything where the honest CSS-only version loses what the design was doing

When you stop, say three things: what the design specified, what the CSS-only
version would be, what it loses. Then wait. **Never silently downgrade a
prototype interaction into a fade and call the frame done** — a quiet downgrade
is worse than an open question, because nobody knows to look for it.

**Needing to invent a control means the model is wrong — it is a stop signal,
not a gap to fill.** Two inventions from `/home` show exactly what that looks
like: a "Run the prototype" submit chip, and a lemon fill for a ticked option.
Both were flagged honestly as invented, both were carried as open questions for
two rounds, and both vanished once the interaction model was corrected
(`reflections/2026-08-28.md:142-146`).

### Step 8 — Verify

1. **Screenshot beside build.** Look at both. Fidelity is judged by eye, not by
   whether each value matched.
2. **Contrast.** Any new colour pairing gets checked on `/styleguide`, which
   renders every colour against every ground the site uses. One colour scheme
   means no dark-mode escape hatch for a weak pairing. Report the number;
   do not repaint the design (L1).
3. **Keyboard.** Tab through it. Every interactive element shows a visible focus
   ring, and the order matches the visual order.
4. **`npm run verify`** — check, build, HTML lint, format check. The HTML lint
   enforces alt text, heading order and labels against the built output, and it
   runs in CI, so a regression fails the PR either way.
5. **Motion over time, not at rest.** Every timed behaviour needs an assertion
   about an _intermediate_ state. The `/home` failure: a settled screenshot
   passed while every bubble was on screen inside 600ms with text still typing
   for seconds (`reflections/2026-08-28.md:122-126`).
6. **Assert outcomes, not mechanisms.** `hasAttribute('hidden')` passed while
   the chips were visible, because `.chat__choices` sets `display` explicitly
   and that beats the UA `[hidden]` rule. Assert computed `display`.
7. **A JS-off pass and a keyboard pass.** Block the page script: the flow must
   still be complete (L7). Then tab through: visible ring on every interactive
   element, order matching visual order.

**Output:** tokens added, drift found, motion downgraded or deferred, questions
raised. If nothing needed a decision, say that too — it is useful information
about the design.

---

## 5. Collection pages

A collection page's frame shows one filled-in example; the code has to survive
however many entries the collection actually holds. Work through, in order:

1. **Layer-to-field mapping.** Name which layer is which schema field before
   writing markup — a title layer is not always the `title` field once a card
   layout reorders things.
2. **Zero, one and many entries.** Check the empty state, a single card, and a
   full grid. The frame draws exactly one of these.
3. **Absent optional fields.** For every optional field, look at the layout
   with it missing. `projects` alone carries eight optional case-study
   sections, two teaser images with paired alt text, and a 280-character
   `summary` cap (`reflections/2026-08-28.md:213-215`) — each is a case to
   check, not assume.
4. **Text longer than the mockup.** The frame's copy is one length. Real
   entries will run longer; check wrapping and truncation before calling a card
   done.
5. **`astro:assets` for collection images**, not a raw `<img>` — it gives every
   collection entry consistent optimisation without a per-entry decision.
6. **Design ↔ schema reconciliation, in both directions.** A frame showing a
   field the schema lacks is the three-file change already in
   [`CLAUDE.md`](../../CLAUDE.md) §6 (`src/content.config.ts`,
   `public/admin/config.yml`, `docs/cms.md`). A schema field no frame shows is
   either dead or the design is incomplete — ask, do not delete.

**Read order:** read the schema in `src/content.config.ts` and one real entry
under `src/content/<collection>/` _before_ the frame. Reading the frame first
means guessing at field names and shapes the schema already fixed.

**The text-walk caveat** (also true in Step 1): `findAllWithCriteria` does not
descend into instances. A text sweep — checking for placeholder copy, or every
outgoing link — has to recurse into instance children explicitly, or it
silently misses whatever content lives inside a component instance.

---

## 6. Phases, and who does what

The measured cost of building `/home` this way: 40,720,868 cache reads against
68,095 output tokens (`reflections/2026-08-28.md:268-289`). Practically nothing
was spent writing; almost all of it was re-reading context on every turn. The
lever is not "write less" — it is keeping bulk out of the main thread entirely,
because a subagent's reading happens in _its_ context and only its summary
returns to yours.

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

**Phase 4 — Verify.** Subagents again: one runs the probes and returns
pass/fail plus _only_ the failing detail; one returns the contrast table and
keyboard order. A full green list printed into the main thread becomes
permanent context for the rest of the session — don't print it there.

**Phase 5 — Ship.** Main thread, with tight tooling.

Rules that fall out of this, and hold regardless of phase:

- A subagent returns a **summary**, never raw material.
- Anything bulky that will not be needed on later turns is produced in a
  subagent, not the main thread.
- The main thread holds three things: the design decisions, the file being
  edited, and the conversation with Max.
- When a tool returns far more than asked for, **stop calling it that way** —
  listing the entire workflow history four times after seeing it misbehave once
  is the failure mode this guards against.

---

## 7. Token discipline

Anything large that lands in context is paid for on every remaining turn, not
once — a 6k-token tool result arriving with 70 turns left in the session costs
nearer 420k in cache reads by the end. That arithmetic is what makes the
discipline below worth keeping.

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

## 8. Token sync

`design/tokens.json` is the exchange format; `src/styles/tokens.css` is what
ships. They are kept in step by hand — the file is small and changes rarely, and
a generator would be more machinery than the problem deserves.

**Figma → code** (the normal direction): `get_variable_defs` for a frame, diff
against `tokens.css`, update `tokens.css` and `tokens.json` in the same commit.

**Code → Figma** (when the system is being built out): `design/tokens.json` is
DTCG-shaped, so a token plugin can import it, or `use_figma` can write the
variables directly. Load the `figma-use` skill first.

### The collections, as built

80 variables across 7 collections. The first 77 were verified against the file
on 27 Aug 2026; the three added by the library port on 29 Aug 2026
(`font/weight/bold`, `line-height/none`, `line-height/relaxed`) landed in
`tokens.css` and `design/tokens.json` but **not yet in Figma** — the MCP server
was unreachable that session, so the third leg of the three-file rule is
outstanding. Every variable carries a description and WEB code syntax, and no
two emit the same code syntax.

| Figma collection | Vars | JSON key | CSS prefix                                          |
| ---------------- | ---- | -------- | --------------------------------------------------- |
| Color            | 32   | `color`  | `--color-*`                                         |
| Typography       | 24   | `font`   | `--font-*`, `--line-height-*`, `--letter-spacing-*` |
| Spacing          | 9    | `space`  | `--space-*`                                         |
| Radius           | 4    | `radius` | `--radius-*`                                        |
| Size             | 3    | `size`   | `--size-*`                                          |
| Motion           | 5    | `motion` | `--duration-*`, `--easing-*`                        |
| Elevation        | 3    | `shadow` | `--shadow-*`                                        |

There is no Semantic collection. One existed briefly and was deleted — see L4.
Size holds layout widths read off the `/home` chat frames — named for what
they size (`size/chat-column`) rather than as a scale, because 400/531/866 is
not one. `--measure` and `--content-max` are the older layout constants and
live in `tokens.css` alone; the three-file rule has never been applied to them.

Every collection has exactly one mode, named `Value`. No light/dark split, by
decision. With no role tier there is nothing to remap, so a dark scheme would
mean touching every component — a known and accepted consequence of the flat
structure, not an oversight.

The ramps are `lemon`, `pickled`, `herbs`, `tomato`, `neutral`. Lemon and
pickled stop at 500; herbs and tomato run to 600. Where a ramp ends is a design
decision (L1). The neutral ends are **named, not numbered** —
`color/neutral/white` (`#fdfcf8`) and `color/neutral/black` (`#040302`).

> **Definition of done for a new variable:** a value, a description matching its
> _current_ name, scopes, **WEB code syntax**, and matching entries in
> `design/tokens.json` and `src/styles/tokens.css`. Code syntax is the one that
> gets forgotten, and forgetting it makes the MCP emit
> `var(--color\/lemon\/500)`, which is not valid CSS.

---

## 9. What Figma cannot hold faithfully

Five places where reading Figma literally produces the wrong code.

- **Fluid type.** `--font-size-*` is a `clamp()`. Figma is a fixed-size medium,
  so `font/size/*` carries the desktop (maximum) end. The scale is
  8 / 12 / 16 / 24 / 32 / 48 / 72px; `xs`, `sm` and `base` ship fixed, only `lg`
  and up interpolate. Matching Figma exactly at every viewport is wrong, not
  faithful.
- **Elevation.** Figma variables have no shadow type, so `shadow/*` are STRING
  variables holding the CSS value, paired with `Elevation / sm|md|lg` effect
  styles for applying them on canvas. The MCP reads the _effect_ and emits a
  literal `drop-shadow-[…]`. **The effect style name is the contract**:
  `Elevation / md` means `var(--shadow-md)`. Change one, change both.
- **Letter-spacing units.** Figma applies FLOAT letter-spacing in **px** and
  cannot express em. `letter-spacing/wide` reads `0.08` there and means
  `0.08em` here; `letter-spacing/extra-wide` reads `3` (px) and ships as
  `0.19em`. `letter-spacing/tight` cannot be applied in Figma at all, which is
  why the heading text styles bind `normal` — the `-0.02em` on `h1`–`h4` is a
  code-side refinement, not drift. **Do not read Figma's letter-spacing
  bindings as design intent.**
- **`nowrap` and `max-width` disagree.** In Figma, `nowrap` text grows past a
  max-width; in CSS the `max-width` clips it. `max-w-[400px]` and
  `whitespace-nowrap` in the same emitted class list only mean anything
  together — reading half of it wrapped the `/home` chips to two lines.
- **An asset's intrinsic size is not a token.** The avatars are 87px. Reaching
  for `--space-2xl` (96px) because it is close is exactly the near-miss the
  token table forbids. Intrinsic asset dimensions go on the element
  (`width`/`height` attributes, as `index.astro:418-419` does), not into the
  scale.

---

## 10. Traps in this codebase

- **Astro scoped CSS does not reach JS-created nodes.** Scoped styles are
  hashed at build time; nodes a script creates afterwards never match.
  `/home`'s `.chat__char` rule lives in a `<style is:global>` block for exactly
  this reason (`index.astro:918-927`).
- **`[hidden]` versus an explicit `display`.** A rule that sets `display` beats
  the UA's `[hidden]`. Hiding means removing the display rule too, and
  asserting computed `display`.
- **The `animation` shorthand resets `animation-delay`.** Order matters: a
  shorthand written after a delay wipes it (`index.astro:563-564,577-581`).
- **The reduced-motion blanket covers duration, not delay.** `global.css:149-162`
  zeroes `animation-duration` and `transition-duration` but leaves
  `animation-delay` — so a CSS stagger still waits under
  `prefers-reduced-motion: reduce`. Do not re-add a per-page block (R7); if a
  delay is load-bearing, raise it.

---

## 11. Mechanics

- `www.figma.com` is blocked by the egress policy, so image and vector assets
  come out through `exportAsync({ format: 'SVG_STRING' })` rather than a
  download URL.
- The code-syntax platform enum is `iOS`, not `IOS`.

---

## 12. Failure modes

| Symptom                                             | What it actually means                                                                                                                                                                                                                                                 |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Cannot find node"                                  | Usually auth, not the ID. Run `whoami`. Files in someone else's draft space are unreadable even with the link.                                                                                                                                                         |
| `var(--color\/lemon\/500)` in the output            | Missing WEB code syntax on that Figma variable. Fix in Figma; don't paste it into CSS.                                                                                                                                                                                 |
| _"the font family Satoshi Variable does not exist"_ | A Figma-side gap, not a site one. Satoshi and Erode are installed on Max's machine rather than shared with the file, so the MCP runtime cannot see them. Any script that loads a font before editing a text node fails outright. Expected — not a bug to fix mid-task. |
| `get_design_context` response is enormous           | You asked for too much. Narrow to one frame.                                                                                                                                                                                                                           |
| Variable names don't transform cleanly to CSS       | Real drift. Report it rather than inventing a name that works.                                                                                                                                                                                                         |

---

## 13. Anti-patterns

- ❌ Skipping the screenshot because the XML "looks clear"
- ❌ `get_design_context` on a whole page, or several frames at once
- ❌ Writing CSS before `get_variable_defs` came back
- ❌ Hardcoding a value "just for now"
- ❌ Inventing a style the design never specified — a hover colour, a shadow, a
  transition "because it needs one"
- ❌ Inventing a role name — `--text-secondary`, `--surface-default`
- ❌ Adding a `prefers-color-scheme` block or a dark mode
- ❌ Re-adding `prefers-reduced-motion` per page
- ❌ Building a component that is neither a published library set nor already
  used twice
- ❌ Spending a call on `get_code_connect_map` — the seat cannot use it; read
  `design/components.json` instead
- ❌ Porting a set that `design/components.json` already maps to a file
- ❌ Adding client JS that the page depends on, rather than layers on
- ❌ Writing placeholder copy that reads as real content — no invented case
  studies, clients, metrics or bio copy, ever
- ❌ Copying Figma's letter-spacing bindings as if they were intent
- ❌ Verifying timed motion from a settled screenshot

---

## 14. Checkpoints

| After  | Show                                                      | Ask                                                                  |
| ------ | --------------------------------------------------------- | -------------------------------------------------------------------- |
| Step 0 | The archetype, and the interaction model in one paragraph | "Is that the model?" — required, every page                          |
| Step 2 | One sentence on what the frame is for                     | "Is that the intent?" — only if the screenshot left it ambiguous     |
| Step 3 | Token diff: matched, missing, disagreeing                 | "These N values have no token. Add them, or is the design drifting?" |
| Step 4 | Which components are reused vs. built new                 | Which sets came from the library, which are new design work          |
| Step 7 | Design intent vs. CSS-only version                        | Required whenever the ceiling is hit. Never skip.                    |
| Step 8 | Screenshot comparison, contrast, verify run               | "Done — here's what needed a decision."                              |
