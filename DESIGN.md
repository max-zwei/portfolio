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
  title:
    fontFamily: '{fontFamily.serif}'
    fontSize: 6.75rem
    fontWeight: '{fontWeight.semibold}'
    lineHeight: 1.2
    letterSpacing: '{letterSpacing.normal}'
  h1:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.3xl}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: 1.2
    letterSpacing: '{letterSpacing.normal}'
  h2:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.2xl}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: 1.2
    letterSpacing: '{letterSpacing.normal}'
  h3:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.xl}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: 1.2
    letterSpacing: '{letterSpacing.normal}'
  h4:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.lg}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: 1.2
    letterSpacing: '{letterSpacing.normal}'
  h5:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.base}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: 1.2
    letterSpacing: '{letterSpacing.normal}'
  h6:
    fontFamily: '{fontFamily.serif}'
    fontSize: '{fontSize.sm}'
    fontWeight: '{fontWeight.semibold}'
    lineHeight: '{lineHeight.relaxed}'
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
    fontSize: 1.25rem
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
  xl: 2.5rem
  full: 999rem
shadows:
  sm: '0 1px 2px rgb(20 17 15 / 0.06)'
  md: '0 4px 16px rgb(20 17 15 / 0.08)'
  md-lemon: '0 8px 16px #f0e511, -4px 4px 16px #f0e511, 4px -4px 16px #f0e511, 0 -8px 16px #f0e511'
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
  chat-column: 54.125rem
  chat-bubble: 33.1875rem
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

| Front-matter group | CSS custom property  | `tokens.json` path     | `$type`       | In export                           |
| ------------------ | -------------------- | ---------------------- | ------------- | ----------------------------------- |
| `colors`           | `--color-*`          | `color/<ramp>/<step>`  | `color`       | yes                                 |
| `typography`       | none                 | `text/*`               | `typography`  | yes, as CSS names or literal values |
| `fontFamily`       | `--font-*`           | `font/family/*`        | `fontFamily`  | yes                                 |
| `fontSize`         | `--font-size-*`      | `font/size/*`          | `dimension`   | yes                                 |
| `fontWeight`       | `--font-weight-*`    | `font/weight/*`        | `fontWeight`  | yes                                 |
| `lineHeight`       | `--line-height-*`    | `font/lineHeight/*`    | `number`      | yes                                 |
| `letterSpacing`    | `--letter-spacing-*` | `font/letterSpacing/*` | `dimension`   | yes                                 |
| `spacing`          | `--space-*`          | `space/*`              | `dimension`   | yes                                 |
| `rounded`          | `--radius-*`         | `radius/*`             | `dimension`   | yes                                 |
| `shadows`          | `--shadow-*`         | `shadow/*`             | `shadow`      | yes                                 |
| `motion.duration`  | `--duration-*`       | `motion/duration/*`    | `duration`    | yes                                 |
| `motion.easing`    | `--easing-*`         | `motion/easing/*`      | `cubicBezier` | yes                                 |
| `sizes`            | `--size-*`           | `size/*`               | `dimension`   | yes                                 |
| `layout`           | `--<key>`            | —                      | —             | no — Figma holds no variable        |
| `focus`            | `--focus-*`          | —                      | —             | no — accessibility, not design      |

### Library sync — 5 October 2026

Read all 79 local variables across the seven single-`Value` collections: Color
(32), Typography (21), Spacing (9), Radius (5), Motion (5), Elevation (4) and
Size (3). The new `radius/xl` is 40px (`rounded.xl: 2.5rem`); `radius/lg`
remains 16px. All other primitive values retain their established translations,
except the reported shadow STRING/effect disagreement below. Font family
registration suffixes, fluid type maxima, tracking units and the pill radius
retain their documented web translations rather than pretending Figma supports
them directly.

`radius/xl` (`VariableID:697:526`) incorrectly advertises WEB code syntax
`var(--radius-lg)` and Android/iOS `radius.lg`. Code follows the actual variable
name with `--radius-xl`, not the misleading syntax or a compatibility alias.
The `shadow/md-lemon` STRING now says
`0 8px 32px #f0e511, 0 8px 32px #f0e511`, but the applied `md-lemon` effect
still draws four 16px-blur layers. The source and icon filter retain that
drawn effect; neither finding authorizes a Figma mutation.

The two live Size variables `size/chat-column` (866px) and `size/chat-bubble`
(531px) are restored to the source. No deletion or other Figma mutation is
part of this read-only sync. `layout` and `focus` remain CSS-only exceptions,
not local variable collections.

Three existing code primitives still have no Figma variable:
`font-weight-bold` (700), `line-height-none` (1) and `line-height-relaxed`
(1.4). They remain for existing consumers outside this library-only sync;
they are not evidence of matching variable definitions. The live text styles
do draw bold text and 1.4 line heights, but headings no longer use 1.
`Typography/Body - Bold` renders Satoshi Bold while its weight binding points
to `font/weight/semibold` (600); the style transcription keeps the drawn Bold
weight and records that Figma inconsistency rather than changing the binding.

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

All fourteen local text styles were read directly on 2 October 2026: Title,
H1–H6, Body - Large, Body, Body - Bold, Body - Small, Mono, Mono - Small and
Captions. Title is 108px; H1–H5 retain their 72/48/32/24/16px sizes but now use
1.2 line height. H6 is 12px with 1.4 line height. Body - Large is 20px, not the
24px `font/size/lg` step. No style is inferred from component usage.

The front matter keeps variable references where they exist. Raw style metrics
remain literal values, not invented variables or a semantic alias tier.
`text/*` in the JSON contains CSS custom-property names for token references
and strings for literals (`"1.2"`, `"6.75rem"` and `"1.25rem"`). Consumers must
wrap only names beginning with `--` in `var()`. Title remains fixed-size
because Figma supplies no fluid range for it.

The 3 October 2026 page refresh applies the same literal 1.2 line height to
global H1–H5 rules. H6 uses serif semibold at 12px/1.4 with normal tracking.
The `/styleguide` text-style table handles literal values directly and wraps
only custom-property names in `var()`. Body, Mono and Captions styling stays
local to each component. The nav button at `109:1378` has raw mono settings
rather than the `Typography/Mono` style. No additional style tokens are needed.

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

**The chat widths.** The Size collection holds `--size-chat-column` (866px),
`--size-chat-bubble` (531px) and `--size-chat-choice` (400px). All three are
transcribed, without replacing the first two by near-matching grid spans.
Page layouts may compute their own column spans; those spans are not substitutes
for the chat component widths. The 400px choice cap is not a column span either
— four columns would be 420.8px.

**The page container.** `--content-max: 72rem` is retired. The page frame is
1280 with 96px margins, so `.container` is now
`max-width: var(--grid-frame)` with `var(--grid-margin)` of padding above
48rem and `--space-md` (24px, the `Mobile` frame's margin) below it. The live
NavBar is the standalone component `210:1624`, not the removed `210:1625`
Mode set. Its separate 64px side insets yield a 1152px inner row; that footer
geometry is not a page-container token.

## Elevation & Depth

The Figma effect styles `Elevation / sm`, `Elevation/md` and `Elevation / lg`
map to `--shadow-sm|md|lg` by name. Their effects and variables still agree.
Read the style name, not the drop-shadow the MCP emits.
The applied effect style `md-lemon` maps to
`--shadow-md-lemon`: four lemon-500 layers at (0, 8), (-4, 4), (4, -4)
and (0, -8), each with blur 16, spread 0 and full opacity. Its conflicting
two-layer, 32px-blur STRING variable is recorded in the library sync above,
not substituted for the unchanged drawn effect. Shadows show behind
transparent areas. Icon glows share one blurred source alpha and merge four
independently offset, colored copies behind the source; chained drop-shadows
would instead cast shadows from earlier shadows.

## Shapes

The `rounded` scale ships as `--radius-sm|md|lg|xl|full` and comes from the
five-variable Figma `Radius` collection: sm 4px, md 8px, lg 16px, xl 40px and
full 9999px. The new xl surfaces keep a square top-left corner unless the
frame reverses that corner; lg remains the distinct 16px radius, not an alias
for xl. `full` ships `999rem` while the Figma variable holds `9999px` — both
are a pill, and neither is derived from the other, which is why the generator
carries that one value as an explicit exchange override.

## Components

### Atoms

https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=114-14

### Organisms

https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=114-15

A component set **published in those library pages** may become a file in
`src/components/` before its first page use; anything not in the library stays
inline on the page until its second use (AGENT.md R8).

### Current library boundary

The 5 October 2026 read contains the same five atom sets (logo, Icons, Buttons,
Chat and user) and nine organism entries (NavBar, Flipcard, Post-it, Text, CV,
Focus, Release Notes, Tech and Project Bentos). `design/components.json`
records the live node IDs and unchanged sparse variant matrices, not an assumed
Cartesian product. Text, Focus and NavBar are standalone components, not
variant sets. This surface refresh changes no component prop APIs.

`Text` maps directly to `TextSection.astro`; `BlankSection.astro` is its
existing named-content composition. CuriosityRow remains reusable code, but
its old Figma node has no page parent. The obsolete ProjectPreview and
ProjectSection components have been removed: CV previews are inline within
`CvSection`, and case-study sections are inline on the project detail page.
ProjectSection's former Figma set remains in `Graveyard`, not Organisms.

The 3 October 2026 page migration consumes the current library contracts
without compatibility aliases. Its interaction and content decisions are
recorded in [`docs/figma-handoff.md`](docs/figma-handoff.md).

`Button` now exposes `state="default" | "hover"` as well as interactive
hover/focus. Secondary hover keeps regular weight 400. Button slots contain
plain labels; the component owns decorative nav `#` and secondary `→` marks.
`ChatBubble` accepts only `user="talking-head" | "visitor"`; the former `user="user"` hover specimen
is now `user="visitor" state="hover"`. Talking-head bubbles use the live
531px cap rather than a near-matching grid span.

`Icon` accepts only drawn name/color/state combinations. Only the eight
AI/social marks have hover variants; all other marks are default-only.
Triangle is herbs, square is tomato and circle is black. Unsupported
combinations are errors, not recoloring requests. The atom library defines
no prototype reactions or timed motion, so Button, ChatBubble and Icon do
not introduce transition durations.

Share (`377:2143`) keeps its 28px canvas and geometry; only its two connecting
strokes change from raw black to bound `neutral-black` (`#040302`), matching
the discs. The Icon API and asset path stay unchanged.

`TextSection` transcribes Text's 1105px outer surface: 64px padding around
310px title + 135px gap + up to 532px body. Its neutral-100 ground has
0/40/40/40 corners (top-left clockwise), using radius-xl. The uppercase
108px/1.2 Title stays; the body shrinks in constrained parents.
`FocusAreas` uses the same ground and corners with 40px padding, H2, 24px
root gap, 12px list gap, 13px unbound marker gap and 8px tomato markers.
`ToolBox` Web adds the same 40px-padded surface around its 411.302307px,
seven-column intrinsic grid, for 491.302307px overall. Its twenty tools,
order and assets stay. PDF retains H3, eleven columns, a 412.529053px grid
and no surface fill, padding or radii. Global and component headings retain
the existing line-height contract.

`ReleaseNote` paints only its content panel: 64px padding, 0/40/40/40 corners,
lemon-100 active and neutral-100 inactive. Existing state-specific copy colors
remain. The 16px rail and unbound 95px rail gap remain outside the panel, as
does the 144px bottom spacing. Optional attachments sit 40px below the panel,
right aligned; the content gap remains 24px. Text and release-panel padding
reduce to 24px on narrow screens as an accessibility fallback.

`NavBar` remains a 220px-high desktop neutral-black footer, with 40px vertical
and 64px horizontal padding around a 1152 × 140px space-between row. The left
column now places the existing neutral Max Avatar (87px) above Explore With,
without inventing a logo link. Impressum moves below Behind the Scenes in the
right about list; the four main links, AI/social order, destinations and
hover/focus behavior remain. The right groups retain 96px separation; left
and rightmost vertical groups use space-between with a 12px minimum gap.
The main navigation column retains the measured, unbound 263px width. Figma's
invisible stale “go back in time” overrides inflate that column, but are not
real link labels or accessible names and are not rendered.

Buttons, ChatBubble, Avatar, Logo, Icon geometry/API, PostIt, CvSection,
ProjectBento and Tech PDF retain their existing contracts. Stored padding on
empty image-fill frames does not imply an inset for the artwork.

`CvSection.projects` entries require `href` and `title`, with optional
`image`/`detailImage` (`{ src, alt }`) and optional palette positions. `/resume`
maps `img_1_1`, `img_1_2_s` and `color1`–`color4` directly; missing artwork is
hidden. The inline CV-specific preview replaces `caption`/`artefacts` and the
old ProjectPreview dependency. PDF still suppresses project previews.
`ReleaseNote.screenshots` and its slideshow are removed because neither live
state contains them. `NavBar.mode` is removed: the live standalone footer has
one black ground and white marks. No old prop is retained as an alias.

Narrow-width reflow in these compositions is an accessibility fallback,
not a claim that Figma supplies mobile library variants.

`ProjectBento.astro` implements the six-variant Project Bentos set. It requires
`title` and `href`; optional `hmw` supplies the only visible project copy.
`images` is an optional partial record of `0.8h`, `0.6h_l`, `0.6h_s`, `1_2_l`,
`1_2_s`, `1_1` and `1_2` (`{ src, alt }`), matching the content keys without
`img_`. The eight `colors` positions are optional too. Missing slots are
hidden, never replaced with Figma checkerboard fixtures.
`variant` is `"1"`–`"6"`; `state` is `"default"` or `"hover"`. Real hover and
visible keyboard focus expose the expanded design. On `/projects`, the six
variants cycle and the active bento expands to page width on a black page
ground; other bentos are invisible and noninteractive. That host ground
provides contrast for the drawn neutral-white expanded copy.

PostIt's initial rotation applies to the paper, not the pin. Its black copy
and the Flipcard back's black copy are the unbound `#000000` Figma fills,
not near-matching neutral tokens. Flipcard Front/Back keep their 200 × 300
reference geometry and shadow-lg, with corners 0/16/16/16 (radius-lg).
The 87 × 130.5 small variant uses 0/8/8/8 (radius-md) and shadow-sm.
Faces and enhanced-stage clipping share the same radius; existing fitting,
image-driven proportions, readable no-JS faces and flip controls remain.

The four-page surface refresh retains existing content and interactions.
Project detail paints active tomato-100 and inactive neutral-100 panels,
keeping headings neutral-black and body neutral-800 in both states; 144px
inter-section gaps remain unpainted. Behind the Scenes adds the same xl
surfaces, retains equal-height Design/Code cards and shows only DESIGN.md in
the Code card by explicit user decision, not a rendered README panel. Its
Figma and document embeds use lg 16px, with a plain `/Design System` caption
8px below the Figma embed. Résumé uses a 162px screen portrait and an
866px-wide, 24px-padded tomato-100 intro with 0/16/16/16 corners; print/PDF
stays separate. The Web ToolBox (491.302307px) and Focus (419px) sit at
opposite edges of its 1088px strip, top aligned, with source-order mobile
stacking rather than the obsolete four-column constraint.
The `/ai` Text instance fills 1088px with 96px horizontal and 64px vertical
padding, allowing the body to flex rather than forcing the library's full
532px width. It retains the existing neutral-white page ground: the frame's
raw `#FFFFFF` is a pre-existing mismatch outside this surface delta, not a
new token. Current editorial copy, the 40px/s project strip with hidden
scrollbar, playground wrapping and 96px card spacing remain unchanged.

### Historical library verification — 2026-10-02

Before this surface refresh, the isolated Astro component matrix built
successfully; component-only checking reported 19 files, zero errors and zero
warnings. Browser checks covered all six compact (421 × 210) and expanded
(1280 × 538) Bento layouts, hover, visible keyboard focus and link navigation,
Flipcard controls, and the no-JavaScript content baseline. No page files were
migrated in that check. These are historical results, not verification of the
5 October surface refresh.

Two visual findings from that check remain recorded rather than silently
corrected:

- Release Notes' former inactive neutral-600 copy on neutral-white measured
  **3.85:1**, below AA for normal-sized text. The new inactive panel is
  neutral-100; the historical ratio is not a measurement of that new pairing.
- Text's 310px title column uses the drawn 108px/120%, weight 600 and zero
  tracking. The loaded self-hosted Erode Variable wraps “HONEST” as “HONE / ST”
  in the desktop browser, while Figma's Erode Semibold render shows “HON / EST”.
  No artificial width, tracking or content break was added to conceal that
  font-rendering difference.

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
