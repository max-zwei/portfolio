---
name: figma-implement
description: 'Implement a Figma frame as a static Astro page or component, faithfully and without token drift. Covers connecting to the Figma MCP server, the read order (metadata → screenshot → variables → design context), mapping Figma variables and effect styles to CSS custom properties, reusing components via Code Connect, translating prototype interactions into CSS-only motion, and the accessibility and verification gate before a page is called done. Use when a Figma URL or frame is handed over to be built, or when an implemented page has to be re-synced with an updated design. Read-direction only — it does not write to Figma.'
disable-model-invocation: false
---

# Figma → page

This file is both the contract and the procedure. Build one frame at a time, in
the order below, and stop where it says STOP.

Read alongside: [`docs/design-system.md`](../../docs/design-system.md) — what the
tokens are _for_. Read it before choosing any colour.

Out of scope: writing to Figma. Any `use_figma` call requires the `figma-use`
skill and has left this skill's scope.

---

## 0. Laws

These hold for every step. A run that breaks one is wrong even if the page looks
right.

| #   | Law                                                                                                                                   | Violation looks like                                                                     |
| --- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| L1  | The Figma file is the decision, not a draft. Report what looks wrong; never resolve it.                                               | Darkening a colour to pass contrast; extending a ramp; substituting a step.              |
| L2  | Author no style the design has not defined. Every declaration traces to a frame, to `global.css`, or to an accessibility requirement. | `a:hover { color: … }` invented because links "need" a hover.                            |
| L3  | Never write a literal that has a token.                                                                                               | `#d73457`, `16px`, `font-family:` in a component.                                        |
| L4  | One flat tier. No role names.                                                                                                         | `--text-secondary`, `--surface-default`.                                                 |
| L5  | No CSS before `get_variable_defs` has returned.                                                                                       | Values written first, reconciled with tokens after. Hex codes get committed. Every time. |
| L6  | Never `get_design_context` for more than one frame.                                                                                   | A page-sized response that crowds out the decisions you needed.                          |
| L7  | Zero client JS.                                                                                                                       | A script tag added to match a prototype.                                                 |
| L8  | Accessibility is part of done, not a follow-up.                                                                                       | Shipping and filing the focus states as a follow-up.                                     |

When a value in the design has no token and no obvious home: **STOP and ask.**
A magic number that ships is a magic number forever.

---

## 1. Connection

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

## 2. Procedure

A design is handed over as a URL pointing at **one frame**, not a file:

```
https://figma.com/design/<fileKey>/<name>?node-id=<int>-<int>
             ↑ fileKey                            ↑ nodeId — swap - for :
```

`?node-id=1-2` is `1:2` when you pass it.

### Step 1 — Orient

`get_metadata` with the `fileKey` and that `nodeId`. Cheap structural overview;
use it to confirm you are pointed at the frame you think you are before pulling
anything heavy. With no `nodeId` it lists the file's pages.

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

### Step 4 — Reuse before building

Check for an existing implementation before assuming this is new work:

1. `get_code_connect_map` — if the frame's components are mapped, use the Astro
   component named there. That is the whole point of the mapping.
2. `get_libraries` / `search_design_system` — for components that exist in the
   file but are not mapped yet.

With nothing to reuse: **build it inline on the page.** `src/components/` does
not exist and must not be created for a single use. Extract on the second use,
not the first.

Once a component is stable, map it back with `add_code_connect_map`. After that
`get_design_context` reports _"this is `<ProjectCard>`"_ instead of a wall of
divs — the difference between the next agent reusing your component and
rebuilding it.

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

Three readings to distrust — see §4.

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

**Output:** tokens added, drift found, motion downgraded or deferred, questions
raised. If nothing needed a decision, say that too — it is useful information
about the design.

---

## 3. Token sync

`design/tokens.json` is the exchange format; `src/styles/tokens.css` is what
ships. They are kept in step by hand — the file is small and changes rarely, and
a generator would be more machinery than the problem deserves.

**Figma → code** (the normal direction): `get_variable_defs` for a frame, diff
against `tokens.css`, update `tokens.css` and `tokens.json` in the same commit.

**Code → Figma** (when the system is being built out): `design/tokens.json` is
DTCG-shaped, so a token plugin can import it, or `use_figma` can write the
variables directly. Load the `figma-use` skill first.

### The collections, as built

77 variables across 7 collections, verified against the file on 27 Aug 2026.
Every one carries a description and WEB code syntax, and no two emit the same
code syntax.

| Figma collection | Vars | JSON key | CSS prefix                                          |
| ---------------- | ---- | -------- | --------------------------------------------------- |
| Color            | 32   | `color`  | `--color-*`                                         |
| Typography       | 21   | `font`   | `--font-*`, `--line-height-*`, `--letter-spacing-*` |
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

## 4. What Figma cannot hold faithfully

Three places where reading Figma literally produces the wrong code.

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

---

## 5. Failure modes

| Symptom                                             | What it actually means                                                                                                                                                                                                                                                 |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Cannot find node"                                  | Usually auth, not the ID. Run `whoami`. Files in someone else's draft space are unreadable even with the link.                                                                                                                                                         |
| `var(--color\/lemon\/500)` in the output            | Missing WEB code syntax on that Figma variable. Fix in Figma; don't paste it into CSS.                                                                                                                                                                                 |
| _"the font family Satoshi Variable does not exist"_ | A Figma-side gap, not a site one. Satoshi and Erode are installed on Max's machine rather than shared with the file, so the MCP runtime cannot see them. Any script that loads a font before editing a text node fails outright. Expected — not a bug to fix mid-task. |
| `get_design_context` response is enormous           | You asked for too much. Narrow to one frame.                                                                                                                                                                                                                           |
| Variable names don't transform cleanly to CSS       | Real drift. Report it rather than inventing a name that works.                                                                                                                                                                                                         |

---

## 6. Anti-patterns

- ❌ Skipping the screenshot because the XML "looks clear"
- ❌ `get_design_context` on a whole page, or several frames at once
- ❌ Writing CSS before `get_variable_defs` came back
- ❌ Hardcoding a value "just for now"
- ❌ Inventing a style the design never specified — a hover colour, a shadow, a
  transition "because it needs one"
- ❌ Inventing a role name — `--text-secondary`, `--surface-default`
- ❌ Adding a `prefers-color-scheme` block or a dark mode
- ❌ Re-adding `prefers-reduced-motion` per page
- ❌ Creating `src/components/` for a single use
- ❌ Adding client JS to match a prototype without asking
- ❌ Writing placeholder copy that reads as real content — no invented case
  studies, clients, metrics or bio copy, ever
- ❌ Copying Figma's letter-spacing bindings as if they were intent

---

## 7. Checkpoints

| After  | Show                                        | Ask                                                                  |
| ------ | ------------------------------------------- | -------------------------------------------------------------------- |
| Step 2 | One sentence on what the frame is for       | "Is that the intent?" — only if the screenshot left it ambiguous     |
| Step 3 | Token diff: matched, missing, disagreeing   | "These N values have no token. Add them, or is the design drifting?" |
| Step 4 | Which components are reused vs. built new   | Only if extracting to `src/components/`                              |
| Step 7 | Design intent vs. CSS-only version          | Required whenever the ceiling is hit. Never skip.                    |
| Step 8 | Screenshot comparison, contrast, verify run | "Done — here's what needed a decision."                              |
