# Design system rule book

`tokens.css` says what the values are. This says what they are _for_.

With one flat token tier there is no `--text-secondary` to tell you a colour is
for quiet text — that layer was deliberately removed, and this document is the
replacement for it. **Prose, not tokens.** Nothing here introduces a name. If
you find yourself wanting to add `--color-status-error` because this file
mentions error states, stop: that is the role layer coming back in through the
side door. See L4 in
[`behind-the-scenes/skills/figma-to-astro.md`](../behind-the-scenes/skills/figma-to-astro.md).

## No style without a design

**Every style declaration has to trace back to a decision in the Figma file** —
or to `global.css`, or to an accessibility requirement (focus rings,
reduced-motion, contrast). Nothing else.

If the design does not say what a link does on hover, the answer is that links
do not do anything on hover yet. Not "pick something sensible", not "pick a
palette colour so at least it's token-driven". An invented style is harder to
find later than a missing one, because it looks deliberate.

This applies to hover and focus colours, shadows, transitions, radii, and any
state the design has not drawn. When a state is genuinely needed before it is
designed — a focus ring, say — it is an accessibility requirement, it goes in
`global.css` where it is visible, and it gets flagged.

**Worked example — the two invented states.**

| What was invented                 | What the frames drew     | What it cost         |
| --------------------------------- | ------------------------ | -------------------- |
| A "Run the prototype" submit chip | No submit control at all | Two rounds of review |
| A lemon fill on a ticked option   | No selected-option state | Two rounds of review |

Both were flagged honestly as invented, both were carried as open questions
for two rounds, and both vanished when the interaction model was corrected —
the cost was two rounds of review, not a wrong colour.

## Decision Owner

**The Figma file is the design decision, not a draft.** Every value in it is a
decision Max made, including the ones that look like oversights: a ramp that
stops one step short, a colour that misses a contrast threshold, an asymmetry
between two scales.

An agent's job when it finds one of those is to solely report it.
Say it in the audit, in the PR description, in the contrast table on
`/styleguide` — all of those are the right channel. What is never the right move
is resolving it: adding a token, darkening a value, extending a ramp, or
swapping in a different step because the design appeared to need one.

## Figma Library

### Atoms

https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=114-14

### Organisms

https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=114-15

## Colour

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
| `neutral-white`                       | "Primary background", meaning for example the page ground. `body` background (`global.css:30`).                    |
| `neutral-100`                         | "Secondary Background", for example the first hierarchy level for the raised ground, things sitting above the page |
| `neutral-200` up to `-500` and `-700` | Additional shades for secondary text or backgrounds.                                                               |
| `neutral-600`                         | Quiet text, for example notes, footers, metadata.                                                                  |
| `neutral-800`                         | Body text.                                                                                                         |
| `neutral-black`                       | Heading ink                                                                                                        |

## Type

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

## Widths

| Kind                                 | Governed by                   | Expressed as                                     |
| ------------------------------------ | ----------------------------- | ------------------------------------------------ |
| **Measure** — how wide text may run  | characters, per face and size | `ch` tokens, like the existing `--measure: 68ch` |
| **Layout** — columns, grids, gutters | the page frame                | one grid definition, not per-page widths         |
| **Component** — a fixed element      | the component                 | last resort, named for the component             |

`--size-*` is the last resort, not the first.

The three `--size-chat-*` tokens (`tokens.css:140-142`) were read off the
`/home` chat frames — `--size-chat-column` (866px) is layout,
`--size-chat-bubble` (531px) is a measure (~46 characters of mono at
`--font-size-sm`), `--size-chat-choice` (400px) is a component cap the
design's own instances exceed. **Those names will not survive `/projects`.**
Reclassifying them is blocked on a design-side decision — which widths are
measure, layout, component — and the rename is a three-file change
(`design/tokens.json`, `src/styles/tokens.css`, and the Figma Size
collection), so it lands in one commit with the Figma variables, never half
of it.

## Motion

- `--duration-fast` + `--easing-standard` for hover and focus transitions —
  the chip's `background-color` and `box-shadow` (`index.astro:684-686`).
- `--duration-base` + `--easing-entrance` for a bubble or a choice group
  arriving (`index.astro:563,577`).
- Arrival is staggered by `animation-delay`, and with the script running a row
  arrives when its own first character does, not on a fixed index stagger
  (`index.astro:567-571`).
- The typing pace — 18ms per character, a 240ms beat between paragraphs in one
  bubble — is a page-level constant Max signed off, deliberately not a token
  (`index.astro:724-727`).
- Still undefined _in Figma_: there are no prototype connections, so
  `get_motion_context` returns nothing. Duration and easing arrive as prose
  until the design names them by variable.
- The caveat: `global.css:149-162` zeroes durations under
  `prefers-reduced-motion: reduce` but not `animation-delay`.

## States to draw

What a component needs before it can be built without invention: default,
hover, focus, selected or active, disabled, and — for anything rendering a
collection — empty. And the other half of the rule: where a state should not
exist, the design has to say so, because silence reads as "not drawn yet" and
invites invention.

## Elevation

The Figma effect styles `Elevation / sm|md|lg` map to `--shadow-sm|md|lg` by
name. Read the style name, not the drop-shadow the MCP emits; the two agree
today and both must change together.
