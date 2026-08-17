---
name: figma-implement
description: 'Implement a Figma frame as a static Astro page or component, faithfully and without token drift. Covers connecting to the Figma MCP server, the read order (metadata → screenshot → variables → design context), mapping Figma variables and effect styles to CSS custom properties, reusing components via Code Connect, translating prototype interactions into CSS-only motion, and the accessibility and verification gate before a page is called done. Use when a Figma URL or frame is handed over to be built, or when an implemented page has to be re-synced with an updated design. Read-direction only — it does not write to Figma.'
disable-model-invocation: false
---

# Figma → page

Build one frame at a time, in this order, and stop where it says stop.

**Prerequisites**

- [`docs/design-to-code.md`](../../docs/design-to-code.md) — the contract. Token
  sync, the collections as built, the three things Figma cannot express
  faithfully. This skill does not repeat it; when they appear to disagree, the
  doc wins and the skill is out of date.
- [`docs/design-system.md`](../../docs/design-system.md) — what the tokens are
  _for_. Read it before choosing any colour.
- The `figma-use` skill — a hard prerequisite for any `use_figma` call. This
  skill never needs one; if you reach for `use_figma` you have left its scope.

---

## 1. The one rule that matters most

**Never pull `get_design_context` for a whole page.** One frame at a time, and
last. It is by far the largest response, and a page's worth of it will crowd out
the design decisions you needed to keep in mind while writing the CSS.

Second rule, same weight: **no CSS before `get_variable_defs` has come back.**
Writing values first and reconciling them with tokens afterwards is how hex
codes end up committed. Every time.

---

## 2. Workflow

### Step 0 — Connect and orient

`whoami` first. Most "cannot find node" failures are auth or seat errors wearing
a different hat, and thirty seconds here saves twenty minutes of re-reading node
IDs that were correct all along.

Then take the URL apart:

```
https://figma.com/design/<fileKey>/<name>?node-id=<int>-<int>
             ↑ fileKey                            ↑ nodeId — swap - for :
```

`?node-id=1-2` is `1:2` when you pass it. Run `get_metadata` with the `fileKey`
and that `nodeId` for a cheap structural overview, and use it to confirm you are
pointed at the frame you think you are before pulling anything heavy.

### Step 1 — Look at it

`get_screenshot`. **Never skip this.** The XML tells you structure; only the
image tells you intent — which element is the gesture, what is meant to be
quiet, where the eye is supposed to land.

Before moving on, write one sentence: what is this frame trying to do? If you
can't, you are not ready to build it, and the fix is to ask, not to start
typing.

### Step 2 — Tokens

`get_variable_defs` for the frame. Diff every value against
`src/styles/tokens.css`. Then, per value:

| What you find                                 | What to do                                                                                                                       |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Matches a token                               | Use the token name. Never the literal.                                                                                           |
| No token exists                               | Add it — `design/tokens.json`, `src/styles/tokens.css`, and the Figma collection. Three files or it's a bug.                     |
| Close to an existing token but not equal      | **Stop and ask.** Either the design drifted or the system is missing a step. Both are cheap to ask about and expensive to guess. |
| Emits `var(--color\/lemon\/500)` with slashes | Not a CSS bug — that variable is missing its WEB code syntax in Figma. Note it, use the correct name, and flag it.               |
| A one-off value with no system home           | Ask. A magic number that ships is a magic number forever.                                                                        |

The mapping is mechanical: `color/neutral/700` → `--color-neutral-700`. Swap `/`
for `-`, prefix `--`. If a name doesn't transform cleanly, that is the finding.

### Step 3 — Components before you build anything

Check for an existing implementation before assuming this is new work:

1. `get_code_connect_map` — if the frame's components are mapped, use the Astro
   component named there. This is the whole point of the mapping.
2. `get_libraries` / `search_design_system` — for components that exist in the
   file but aren't mapped yet.

When there is no component to reuse: **build it inline on the page first.**
`src/components/` does not exist yet, and it should not be created for a single
use — speculative structure is against `CLAUDE.md`, and every unused abstraction
is something Max has to decode later. Extract on the second use, not the first.

Once a component is stable, map it back with `add_code_connect_map`. After that
`get_design_context` reports _"this is `<ProjectCard>`"_ instead of a wall of
divs, which is the difference between the next agent reusing your component and
rebuilding it.

### Step 4 — The spec

`get_design_context`, one frame, last. Translate:

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

**Three things to read sceptically**, all explained in `design-to-code.md`:

- **Type sizes** — Figma holds the desktop end of a `clamp()`. Matching it
  exactly at every viewport is wrong, not faithful.
- **Elevation** — the `shadow/*` variables are strings; the effect style name is
  the contract.
- **Letter-spacing** — Figma applies it in px and cannot express em.
  `letter-spacing/tight` cannot be applied there at all, so headings binding
  `normal` is a Figma limitation, not design intent. **Do not read Figma's
  letter-spacing bindings as instructions.**

### Step 5 — Build

Copy the established page shape — `src/pages/index.astro` is the reference:

- `BaseLayout`, `<main id="main">`, `.container` for the page frame.
- A scoped `<style>` block at the bottom. No global additions unless the pattern
  genuinely repeats across pages.
- `block__element` class naming (`.hero__eyebrow`, `.cv__download`).
- Semantic HTML first. A `<div>` with a click handler is a bug. Sections get
  `aria-labelledby` pointing at their real heading, as `/styleguide` does.
- Headings come pre-styled from `global.css` — pick the right level, don't
  restate the styling.
- The one breakpoint in use is `48rem`. Add a second only if the design actually
  needs it, and use `rem`.
- Zero client JS. If the design seems to require it, that's Step 6.

### Step 6 — Motion

What Figma gives you: `get_motion_context` for prototype interactions and smart
animate, `export_video` when you need to see the timing rather than read it.

**The ceiling is CSS `transition` and `@keyframes`.** Within it, use the motion
tokens per the intent table in `docs/design-system.md`: `--duration-fast` for
hover and focus, `--duration-base` for state change and entrance,
`--duration-slow` for large ambient movement; `--easing-standard` for anything
that starts and ends on screen, `--easing-entrance` for things arriving.

Animate `transform`, `opacity`, `color`, `border-color`, `box-shadow`. Not
`width`, `height`, `top` or `margin` — they force layout every frame.

**Do not add a `prefers-reduced-motion` block.** `global.css` already blankets
every transition and animation on the site. A second implementation is a second
thing to get wrong.

**Stop and ask** — do not decide these yourself:

- Motion driven by scroll position (CSS `animation-timeline` included)
- View Transitions
- Anything needing a line of client JS
- Anything where the honest CSS-only version loses what the design was doing

When you stop, say three things: what the design specified, what the CSS-only
version would be, and what it loses. Then wait. **Never silently downgrade a
prototype interaction into a fade and call the frame done** — a quiet downgrade
is worse than an open question, because nobody knows to look for it.

### Step 7 — Verify before calling it done

1. **Screenshot beside build.** Look at both. Fidelity is judged by eye, not by
   whether each value matched.
2. **Contrast.** Any new colour pairing gets checked on `/styleguide`, which
   renders every colour against every ground the site uses. One colour scheme
   means no dark-mode escape hatch for a weak pairing.
3. **Keyboard.** Tab through it. Every interactive element shows a visible
   focus ring, and the order matches the visual order.
4. **`npm run verify`** — check, build, HTML lint, format check. The HTML lint
   enforces alt text, heading order and labels against the built output, and it
   runs in CI, so a regression fails the PR either way.

Then report back, briefly: tokens added, drift found, motion downgraded or
deferred, questions raised. If nothing needed a decision, say that too — it is
useful information about the design.

---

## 3. Failure modes

| Symptom                                             | What it actually means                                                                                                                                                                                                                                                                                                                               |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Cannot find node"                                  | Usually auth, not the ID. Run `whoami`. Files in someone else's draft space are unreadable even with the link.                                                                                                                                                                                                                                       |
| `var(--color\/lemon\/500)` in the output            | Missing WEB code syntax on that Figma variable. Fix in Figma; don't paste it into CSS.                                                                                                                                                                                                                                                               |
| _"the font family Satoshi Variable does not exist"_ | A Figma-side gap, not a site one. Both faces are self-hosted in `public/fonts/` and the built site renders correctly; they're installed on Max's machine rather than shared with the file, so the MCP runtime can't see them. Any script that loads a font before editing a text node or style fails outright. Expected — not a bug to fix mid-task. |
| `get_design_context` response is enormous           | You asked for too much. Narrow to a single frame.                                                                                                                                                                                                                                                                                                    |
| Variable names don't transform cleanly to CSS       | Real drift. Report it rather than inventing a name that works.                                                                                                                                                                                                                                                                                       |

---

## 4. Anti-patterns

- ❌ Skipping the screenshot because the XML "looks clear"
- ❌ `get_design_context` on a whole page, or on several frames at once
- ❌ Writing CSS before `get_variable_defs` came back
- ❌ Hardcoding a value "just for now"
- ❌ Inventing a role name — `--text-secondary`, `--surface-default`. That tier
  was deliberately removed; reintroducing it in a component is the same mistake
  in a smaller box
- ❌ Adding a `prefers-color-scheme` block or a dark mode
- ❌ Re-adding `prefers-reduced-motion` per page
- ❌ Creating `src/components/` for a single use
- ❌ Adding client JS to match a prototype without asking
- ❌ Writing placeholder copy that reads as real content — no invented case
  studies, clients, metrics or bio copy, ever
- ❌ Copying Figma's letter-spacing bindings as if they were intent

---

## 5. Checkpoints

| After  | Show                                        | Ask                                                                  |
| ------ | ------------------------------------------- | -------------------------------------------------------------------- |
| Step 1 | One sentence on what the frame is for       | "Is that the intent?" — only if the screenshot left it ambiguous     |
| Step 2 | Token diff: matched, missing, disagreeing   | "These N values have no token. Add them, or is the design drifting?" |
| Step 3 | Which components are reused vs. built new   | Only if extracting to `src/components/`                              |
| Step 6 | Design intent vs. CSS-only version          | Required whenever the ceiling is hit. Never skip.                    |
| Step 7 | Screenshot comparison, contrast, verify run | "Done — here's what needed a decision."                              |
