# Design system rule book

`tokens.css` says what the values are. This says what they are _for_.

With one flat token tier there is no `--text-secondary` to tell you a colour is
for quiet text — that layer was deliberately removed, and this document is the
replacement for it. **Prose, not tokens.** Nothing here introduces a name. If
you find yourself wanting to add `--color-status-error` because this file
mentions error states, stop: that is the role layer coming back in through the
side door. See rule 2 in [`design-to-code.md`](./design-to-code.md).

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

| Token                 | Job today                                                                                                                                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `neutral-white`         | "Primary background", meaning for example the page ground. `body` background (`global.css:30`).                                                                                                                                                           |
| `neutral-100`       | "Secondary Background", for example the first hierarchy level for the raised ground, things sitting above the page |
| `neutral-200` up to `-500` and `-700` | Additional shades for secondary text or backgrounds.                                                                                                                                      |
| `neutral-600`         | Quiet text, for example notes, footers, metadata.                                                                             |
| `neutral-800` | Body text.
| `neutral-black`       | Heading ink                                                                                                                                           |

## Type

**Sans (`--font-sans`)** 
Body text, subtitles and captions

**Serif (`--font-serif`)** 
Headings

**Mono (`--font-mono`)** 
Always paired with `--letter-spacing-extra-wide` for readability
Used for the chat interaction and subtitles.

## Motion



## Elevation

The Figma effect styles `Elevation / sm|md|lg` map to `--shadow-sm|md|lg` by
name. Read the style name, not the drop-shadow the MCP emits; the two agree
today and both must change together.
