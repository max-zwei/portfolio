---
version: alpha
name: Max Pinkert — Portfolio
description: Portfolio of Max Pinkert — UX and product designer working towards children and education technology.
omitted:
  - section: components
    reason: 'Component styling is transcribed per Figma set into src/components/*.astro. A second copy here would be a second source.'
colors:
  lemon-100: '#faf9c8'
  lemon-200: '#fdfab3'
  lemon-300: '#faf587'
  lemon-400: '#fdf56b'
  lemon-500: '#f0e511'
  pickled-100: '#fee8e9'
  pickled-200: '#fdc5c8'
  pickled-300: '#ff99a2'
  pickled-400: '#ee687a'
  pickled-500: '#d73457'
  herbs-100: '#d2e5d0'
  herbs-200: '#a0ce9c'
  herbs-300: '#69b764'
  herbs-400: '#41993d'
  herbs-500: '#1a8d1a'
  herbs-600: '#006c00'
  tomato-100: '#f2d6d0'
  tomato-200: '#eba99b'
  tomato-300: '#e57663'
  tomato-400: '#ca4f3d'
  tomato-500: '#c22e1c'
  tomato-600: '#9b0a00'
  neutral-white: '#fdfcf8'
  neutral-100: '#efeeea'
  neutral-200: '#dfdeda'
  neutral-300: '#cfceca'
  neutral-400: '#bfbeba'
  neutral-500: '#9f9e9b'
  neutral-600: '#81807d'
  neutral-700: '#484844'
  neutral-800: '#171613'
  neutral-black: '#040302'
typography:
  h1:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.3xl}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: '{lineHeight.none}'
    letterSpacing: '{letterSpacing.normal}'
  h2:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.2xl}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: '{lineHeight.none}'
    letterSpacing: '{letterSpacing.normal}'
  h3:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.xl}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: '{lineHeight.none}'
    letterSpacing: '{letterSpacing.normal}'
  h4:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.lg}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: '{lineHeight.none}'
    letterSpacing: '{letterSpacing.normal}'
  h5:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.base}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: '{lineHeight.none}'
    letterSpacing: '{letterSpacing.normal}'
  body:
    fontFamily: '{fontFamily.sans}'
    fontSize: '{fontSize.base}'
    fontWeight: '{fontWeight.regular}'
    lineHeight: '{lineHeight.normal}'
    letterSpacing: '{letterSpacing.normal}'
  body-small:
    fontFamily: '{fontFamily.sans}'
    fontSize: '{fontSize.sm}'
    fontWeight: '{fontWeight.regular}'
    lineHeight: '{lineHeight.relaxed}'
    letterSpacing: '{letterSpacing.normal}'
  body-large:
    fontFamily: '{fontFamily.sans}'
    fontSize: '{fontSize.lg}'
    fontWeight: '{fontWeight.regular}'
    lineHeight: '{lineHeight.normal}'
    letterSpacing: '{letterSpacing.normal}'
  body-bold:
    fontFamily: '{fontFamily.sans}'
    fontSize: '{fontSize.base}'
    fontWeight: '{fontWeight.bold}'
    lineHeight: '{lineHeight.normal}'
    letterSpacing: '{letterSpacing.normal}'
  mono:
    fontFamily: '{fontFamily.mono}'
    fontSize: '{fontSize.base}'
    fontWeight: '{fontWeight.regular}'
    lineHeight: '{lineHeight.loose}'
    letterSpacing: '{letterSpacing.extra-wide}'
  mono-small:
    fontFamily: '{fontFamily.mono}'
    fontSize: '{fontSize.sm}'
    fontWeight: '{fontWeight.regular}'
    lineHeight: '{lineHeight.loose}'
    letterSpacing: '{letterSpacing.extra-wide}'
  captions:
    fontFamily: '{fontFamily.sans}'
    fontSize: '{fontSize.xs}'
    fontWeight: '{fontWeight.regular}'
    lineHeight: '{lineHeight.relaxed}'
    letterSpacing: '{letterSpacing.normal}'
fontFamily:
  sans: ['Satoshi Variable', 'system-ui', 'sans-serif']
  serif: ['Erode Variable', 'serif']
  mono: ['JetBrains Mono Variable', 'monospace']
fontSize:
  xs: 0.5rem
  sm: 0.75rem
  base: 1rem
  lg: 'clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)'
  xl: 'clamp(1.55rem, 1.4rem + 0.75vw, 2rem)'
  2xl: 'clamp(2rem, 1.7rem + 1.5vw, 3rem)'
  3xl: 'clamp(2.5rem, 1.9rem + 3vw, 4.5rem)'
fontWeight:
  regular: 400
  medium: 500
  semibold: 600
  bold: 700
lineHeight:
  none: 1
  tight: 1.1
  snug: 1.3
  relaxed: 1.4
  normal: 1.6
  loose: 2
letterSpacing:
  tight: '-0.02em'
  normal: '0'
  wide: '0.08em'
  extra-wide: '0.19em'
spacing:
  3xs: 0.25rem
  2xs: 0.5rem
  xs: 0.75rem
  sm: 1rem
  md: 1.5rem
  lg: 2.5rem
  xl: 4rem
  2xl: 6rem
  3xl: 9rem
rounded:
  sm: 0.25rem
  md: 0.5rem
  lg: 1rem
  full: 999rem
shadows:
  sm: '0 1px 2px rgb(20 17 15 / 0.06)'
  md: '0 4px 16px rgb(20 17 15 / 0.08)'
  md-lemon: '0 8px 32px #f0e511, 0 8px 32px #f0e511'
  lg: '0 12px 40px rgb(20 17 15 / 0.12)'
motion:
  duration:
    fast: 120ms
    base: 240ms
    slow: 480ms
  easing:
    standard: [0.2, 0, 0, 1]
    entrance: [0, 0, 0, 1]
sizes:
  chat-choice: 25rem
layout:
  grid-frame: 80rem
  grid-margin: 6rem
  grid-columns: 10
  grid-gutter: 1.5rem
  grid-column: 'calc((var(--grid-frame) - 2 * var(--grid-margin) - (var(--grid-columns) - 1) * var(--grid-gutter)) / var(--grid-columns))'
  measure: 68ch
focus:
  ring: '2px solid var(--color-pickled-500)'
  ring-offset: 2px
---

# Design system rule book

All changes to this file need to be approved by Max.

## Overview

Portfolio of Max Pinkert — UX and product designer working towards children and
education technology.

With one flat token tier there is no `--text-secondary` to tell you a colour is
for quiet text — that layer was deliberately removed, and this document is the
replacement for it. **Prose, not tokens.** Nothing here introduces a name. If
you find yourself wanting to add `--color-status-error` because this file
mentions error states, stop: that is the role layer coming back in through the
side door. See L4 in
[`behind-the-scenes/skills/figma-to-astro.md`](behind-the-scenes/skills/figma-to-astro.md).

**The Figma file is the design decision, not a draft.** Every value in it is a
decision Max made, including the ones that look like oversights: a ramp that
stops one step short, a colour that misses a contrast threshold, an asymmetry
between two scales.

An agent's job when it finds one of those is to solely report it.
Say it in the audit, in the PR description, in the contrast table on
`/styleguide` — all of those are the right channel. What is never the right move
is resolving it: adding a token, darkening a value, extending a ramp, or
swapping in a different step because the design appeared to need one.

### The generation chain

This file is written in the [DESIGN.md format](docs/design-md-format.md) (spec
alpha, vendored verbatim). The front matter above is the one human-edited token
source. `src/styles/tokens.css` and `design/tokens.json` are **generated** from
it by [`scripts/build-tokens.mjs`](scripts/build-tokens.mjs): change the front
matter, run `npm run tokens`, never edit either output by hand.
`npm run tokens:check` runs inside `npm run verify` and in CI, so a hand-edit or
a stale output fails the build.

DESIGN.md and the Figma variable collections are the pair that has to agree, and
Figma is the decision — a front-matter value that disagrees with Figma is
reported, then corrected to follow Figma, never the other way round.

Group names in the front matter are the CSS custom property name minus its
prefix, which is how the one-to-one Figma ↔ CSS mapping survives generation:

| Front-matter group | CSS custom property  | `tokens.json` path     | `$type`       | In export                      |
| ------------------ | -------------------- | ---------------------- | ------------- | ------------------------------ |
| `colors`           | `--color-*`          | `color/<ramp>/<step>`  | `color`       | yes                            |
| `typography`       | none                 | `text/*`               | `typography`  | yes, as CSS names              |
| `fontFamily`       | `--font-*`           | `font/family/*`        | `fontFamily`  | yes                            |
| `fontSize`         | `--font-size-*`      | `font/size/*`          | `dimension`   | yes                            |
| `fontWeight`       | `--font-weight-*`    | `font/weight/*`        | `fontWeight`  | yes                            |
| `lineHeight`       | `--line-height-*`    | `font/lineHeight/*`    | `number`      | yes                            |
| `letterSpacing`    | `--letter-spacing-*` | `font/letterSpacing/*` | `dimension`   | yes                            |
| `spacing`          | `--space-*`          | `space/*`              | `dimension`   | yes                            |
| `rounded`          | `--radius-*`         | `radius/*`             | `dimension`   | yes                            |
| `shadows`          | `--shadow-*`         | `shadow/*`             | `shadow`      | yes                            |
| `motion.duration`  | `--duration-*`       | `motion/duration/*`    | `duration`    | yes                            |
| `motion.easing`    | `--easing-*`         | `motion/easing/*`      | `cubicBezier` | yes                            |
| `sizes`            | `--size-*`           | `size/*`               | `dimension`   | yes                            |
| `layout`           | `--<key>`            | —                      | —             | no — Figma holds no variable   |
| `focus`            | `--focus-*`          | —                      | —             | no — accessibility, not design |

## Colors

### Lemon

Primarily used for areas of user input, for example buttons or the custom cursor. And apart from that used as accent color.

### Pickled

Primarily used for text of user input, for example ghost buttons. And as alternative accent color to Lemon.

### Herbs

"Secondary" color used for the website areas inspiration and curiosity.

### Tomato

"Primary" color used for the talking head, my work and other primary content.

### Neutrals

| Token                                 | Job today                                                                                                          |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `neutral-white`                       | "Primary background", meaning for example the page ground. `body` background (`global.css`, the reset).            |
| `neutral-100`                         | "Secondary Background", for example the first hierarchy level for the raised ground, things sitting above the page |
| `neutral-200` up to `-500` and `-700` | Additional shades for secondary text or backgrounds.                                                               |
| `neutral-600`                         | Quiet text, for example notes, footers, metadata.                                                                  |
| `neutral-800`                         | Body text.                                                                                                         |
| `neutral-black`                       | Heading ink                                                                                                        |

**Every page's ground is `neutral-white`, and that is the default rather than a
per-page choice.** It is set once on `body` in `global.css`'s reset; a page that
wants a different ground has to be drawn that way, and the frame's own fill is
what says so. `neutral-100` is the step above it — the raised ground for
something sitting _on_ the page, not an alternative page colour.

## Typography

**Sans (`--font-sans`)**
Body text, subtitles and captions

**Serif (`--font-serif`)**
Headings

Erode ships no drawn italic — Fontshare packages italics as separate
`*-VariableItalic` files. The italicised word in the homepage slogan is a
browser-synthesised slant until one is added to `public/fonts/`.

**Mono (`--font-mono`)**
Always paired with `--letter-spacing-extra-wide` for readability
The nav button at Figma node `109:1378` is the file's exception: its raw
settings use `--letter-spacing-wide` and line-height `1.6`.
Used for the chat interaction and subtitles.

### Text styles

The five Figma heading styles live centrally in `src/styles/global.css` as
element rules on `h1`–`h5`. Body, Mono and Captions styles are deliberately
transcribed per component under a `/* Figma text style: … */` comment so each
component's Figma diff remains readable. `/styleguide`'s **Text styles** table
is the live index of all twelve named styles. The nav button at `109:1378` is
the exception: its raw mono settings are not the `Typography/Mono` style.

Five of the twelve — `body`, `body-large`, `body-bold`, `mono` and `captions` —
are **inferred** from component usage rather than transcribed from a Figma text
style, and still need confirming against the file.

## Layout

| Kind                                 | Governed by                   | Expressed as                                     |
| ------------------------------------ | ----------------------------- | ------------------------------------------------ |
| **Measure** — how wide text may run  | characters, per face and size | `ch` tokens, like the existing `--measure: 68ch` |
| **Layout** — columns, grids, gutters | the page frame                | one grid definition, not per-page widths         |
| **Component** — a fixed element      | the component                 | last resort, named for the component             |

`--size-*` is the last resort, not the first.

**The grid.** Every 1280-wide desktop frame carries the same layout grid:
`COLUMNS` ×10, gutter 24, margin 96 — so 1088 of content and an 87.2 column.
The 375 `Mobile` frames draw ×5, gutter 16, margin 24. That is the page grid,
and it is drawn on the frames rather than held in a variable, because a layout
grid is not a Figma variable. `src/styles/tokens.css` transcribes it as
`--grid-frame` (80rem), `--grid-margin` (6rem), `--grid-columns` (10),
`--grid-gutter` (1.5rem) and `--grid-column`, which computes one column from
the other four. Those five and `--measure` are the front matter's `layout`
group: a CSS-only group, generated into `src/styles/tokens.css` and excluded
from `design/tokens.json` because Figma holds no variable for them. `focus` is
the other such group.

**The chat widths, reclassified.** Both are layout, so both are column spans
rather than tokens: the message column is 8 columns (54.1rem, against the 866
drawn on `home - chat`) and a message bubble is 5 columns (33.25rem, against
531). Computing them costs 0.4px and 1px respectively, and buys `/projects`
the same maths instead of two more per-page widths. `--size-chat-choice`
(400px) is the only `--size-*` left: four columns is 420.8px, so 400 is the
component's own cap — and the design's own chip instances exceed it.

**The page container.** `--content-max: 72rem` is retired. No frame drew 1152;
the drawn frame is 1280 with 96px margins, so `.container` is now
`max-width: var(--grid-frame)` with `var(--grid-margin)` of padding above
48rem and `--space-md` (24px, the `Mobile` frame's margin) below it. `NavBar`
follows the same frame — `210:1625` `Mode=Default` is 1280 wide with its own
64px padding.

`size/chat-column` (866) and `size/chat-bubble` (531) still exist in the Figma
`Size` collection with nothing in the CSS reading them. Their deletion is
recorded in `design/components.json` under `outstanding.variableWrites`.

## Elevation & Depth

The Figma effect styles `Elevation / sm|md|lg` map to `--shadow-sm|md|lg` by
name. Read the style name, not the drop-shadow the MCP emits; the two agree
today and both must change together. The Figma effect style `md-lemon` maps to
`--shadow-md-lemon`: two identical lemon-500 layers, each at x 0, y 8,
blur 32, spread 0 and full opacity. Layering increases color density without
changing the geometry or the color token. Icon glows merge two independent
copies of the same blurred source alpha; chained drop-shadows would instead
cast a second shadow from the first and enlarge the effect.

## Shapes

The `rounded` scale ships as `--radius-sm|md|lg|full` and comes from the Figma
`Radius` collection. `full` ships `999rem` while the Figma variable holds
`9999px` — both are a pill, and neither is derived from the other, which is why
the generator carries that one value as an explicit exchange override.

## Components

### Atoms

https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=114-14

### Organisms

https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=114-15

A component set **published in those library pages** may become a file in
`src/components/` before its first page use; anything not in the library stays
inline on the page until its second use (CLAUDE.md R8).

### States to draw

What a component needs before it can be built without invention: default,
hover, focus, selected or active, disabled, and — for anything rendering a
collection — empty. And the other half of the rule: where a state should not
exist, the design has to say so, because silence reads as "not drawn yet" and
invites invention.

## Motion

- `--duration-fast` + `--easing-standard` for hover and focus transitions —
  the chip's `background-color` and `box-shadow` (`index.astro:684-686`).
- `--duration-base` + `--easing-entrance` for a bubble or a choice group
  arriving (`index.astro:563,577`).
- Arrival is staggered by `animation-delay`, and with the script running a row
  arrives when its own first character does, not on a fixed index stagger
  (`index.astro:567-571`).
- The typing pace — 12ms per character, a 160ms beat between paragraphs in one
  bubble — is a page-level constant Max signed off, deliberately not a token
  (`src/lib/chat-typing.ts:1-2`).
- Four prototype connections exist on /home — the `Chat` instances (`115:806`,
  `118:1469`, `128:93`, `128:117`) navigate to `home - skip` (`117:898`) — but
  each carries `transition: null`, so no duration or easing is named in Figma
  and both still arrive as prose.
- The caveat: `global.css:149-162` zeroes durations under
  `prefers-reduced-motion: reduce` but not `animation-delay`.

## Do's and Don'ts

**Every style declaration has to trace back to a decision in the Figma file** —
or to `global.css`, or to an accessibility requirement (focus rings,
reduced-motion, contrast). Nothing else.

- **Do** leave a state undesigned when the design leaves it undesigned. If the
  design does not say what a link does on hover, the answer is that links do not
  do anything on hover yet.
- **Don't** "pick something sensible", and don't pick a palette colour so that
  at least it is token-driven. An invented style is harder to find later than a
  missing one, because it looks deliberate. This covers hover and focus colours,
  shadows, transitions, radii, and any state the design has not drawn.
- **Do** put a state that is genuinely needed before it is designed — a focus
  ring, say — in `global.css` where it is visible, as the accessibility
  requirement it is, and flag it.
- **Do** run `npm run tokens` after changing the front matter.
- **Don't** hand-edit `src/styles/tokens.css` or `design/tokens.json`. They are
  generated, and `npm run tokens:check` will catch it.
- **Do** measure contrast on `/styleguide` and report the number.
- **Don't** repaint the design to make a pairing pass.

**Worked example — the two invented states.**

| What was invented                 | What the frames drew     | What it cost         |
| --------------------------------- | ------------------------ | -------------------- |
| A "Run the prototype" submit chip | No submit control at all | Two rounds of review |
| A lemon fill on a ticked option   | No selected-option state | Two rounds of review |

Both were flagged honestly as invented, both were carried as open questions
for two rounds, and both vanished when the interaction model was corrected —
the cost was two rounds of review, not a wrong colour.
