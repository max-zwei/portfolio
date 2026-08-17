# Design system rule book

`tokens.css` says what the values are. This says what they are _for_.

With one flat token tier there is no `--text-secondary` to tell you a colour is
for quiet text — that layer was deliberately removed, and this document is the
replacement for it. **Prose, not tokens.** Nothing here introduces a name. If
you find yourself wanting to add `--color-status-error` because this file
mentions error states, stop: that is the role layer coming back in through the
side door. See rule 2 in [`design-to-code.md`](./design-to-code.md).

Everything below is either **decided** — visible in the code today, with the
line to prove it — or listed under [Open questions](#open-questions), which is
where anything not yet decided stays until Max decides it. Nothing in the
decided sections was invented to fill a gap.

## The rule that outranks the rest

**Colour never carries meaning on its own.** Every place the site uses colour to
say something, the thing is also said in text or shape: the CV timeline dots are
backed by a written `.entry__kind` label (`src/pages/resume.astro:240`), and the
styleguide's contrast tints are backed by the printed ratio and a
visually-hidden verdict (`src/pages/styleguide.astro:418`). Both carry a comment
saying so. Keep it that way — a status that exists only as a hue is a bug.

## Colour

Contrast figures are WCAG 2.1 ratios against the four grounds the site actually
uses, computed by `src/lib/tokens.ts` and rendered on `/styleguide`. "Body text"
means ≥ 4.5, "large text and UI" means ≥ 3.0.

### Lemon — the signature accent

The one colour that says this is Max's site. Used as **atmosphere and marker,
never as ink**: the radial wash bleeding into the hero corner at 22% opacity
(`src/pages/index.astro:53-58`), the underline that appears on link hover
(`index.astro:125`, `resume.astro:179`), the timeline dot for work entries
(`resume.astro:231`).

**Hard limit:** every lemon step is decorative-only on every light ground —
`lemon/500` is 1.28:1 on `neutral/white` and 1.14:1 on the `neutral/100` page
background. Lemon can never carry text, an icon that means something, or a
border that is the only indication of state. On `neutral/black` it is 15.62:1
and entirely safe, which is the one place it can be ink.

Use it once per view. The hero has one lemon gesture, not three.

### Pickled — the counterweight

Sharp pink-red against the yellow. Two established jobs:

- **The focus ring**, `pickled/500` (`tokens.css:171`). It is a non-text UI
  indicator, so the 3.45–4.00:1 it scores on the grounds clears the 3.0 bar.
  Don't reuse this colour for decoration that could be mistaken for focus.
- **Emphasis in running text**, `pickled/600` — the link hover colour
  (`global.css:100`) and the italic serif emphasis in the hero slogan
  (`index.astro:93`).

**Limit:** `pickled/600` is the text-safe step (6.39:1 on white, 4.88:1 on
`neutral/200`). `pickled/500` is AA on white but drops to AA Large on the
`neutral/100` page background — treat 500 as the ring and large display type,
600 as the one you set body-sized text in. 100–400 are decorative.

### Herbs — the settled green

Currently the quiet positive: the education dot in the CV timeline
(`herbs/400`, `resume.astro:237`) and the "passes for body text" tint in the
styleguide contrast table (`herbs/100`, `styleguide.astro:420`). Both are
paired with words, per the rule above.

**Limit:** `herbs/600` is the only step that carries body text on light
(6.50:1). `herbs/500` and `400` are large-text-and-UI only; `100`–`300` are
tints.

### Tomato — the warm signal

Declared as "used sparingly" (`tokens.css:53`) and **not yet used anywhere on
the site**. What it is for is an open question below; what is already true is
the contrast: `tomato/600` is the strongest signal colour available on light
grounds (8.39:1 on white, AAA), `tomato/500` carries body text on white and
`neutral/100`, and `300` and below are decorative.

### Neutrals — ground and ink

Warm-tinted, so they sit with the palette rather than against it.

| Token                 | Job today                                                                                                                                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `neutral-100`         | The page ground. `body` background (`global.css:30`).                                                                                                                                                           |
| `neutral-white`       | The raised ground — things sitting above the page (the skip link, the styleguide callouts) — and the print ground, since the warm off-white is a screen decision and a CV prints on white (`resume.astro:297`). |
| `neutral-200` / `300` | Hairlines. Section rules and borders (`index.astro:118,132`).                                                                                                                                                   |
| `neutral-700`         | Quiet text — eyebrows, notes, footers, metadata. 7.91:1 on the page ground, so it is genuinely readable, not greyed-out decoration.                                                                             |
| `neutral-black`       | Body and heading ink (`global.css:29`).                                                                                                                                                                         |

**Limit:** `neutral-600` and lighter never carry body text — 600 is 3.40:1 on
the page ground, which is large-text-and-UI only. `neutral-700` is the lightest
neutral that can hold a sentence. There is no third text weight below it;
if something needs to recede further, use size or space, not a paler grey.

## Type

Two voices, deliberately:

- **Sans (`--font-sans`)** — everything by default. Body, UI, headings.
- **Serif (`--font-serif`)** — the display voice, used for statements rather
  than paragraphs: the hero slogan is serif, `2xl`, regular weight, snug
  leading, italic on the emphasised word (`index.astro:82-94`). This is the
  site's one typographic gesture. It does not belong on body copy or headings.
  That italic is currently browser-synthesised — Erode ships its italic as a
  separate file that isn't vendored yet, so the slant is a sheared roman. See
  the italic gap in [`design-to-code.md`](./design-to-code.md).

Established patterns:

- **The small label.** `font-size-sm`, `font-weight-medium`,
  `letter-spacing-wide`, uppercase, `neutral-700` — eyebrows, link rows, the CV
  entry kind. Used seven times; it is a pattern, so match it rather than
  inventing a second one.
- **Headings** come pre-set from `global.css:64-85` — semibold, tight leading,
  tight tracking, balanced wrapping. Don't restate those in a page's scoped
  styles; pick the right level and let the cascade do it.
- **Paragraphs** are capped at `--measure` (68ch) globally (`global.css:88`).
  For display text, a tighter explicit `max-width` in `ch` is the established
  override (`index.astro:83`).
- `--font-size-xs` (8px) is not body text at any size. It exists for the type
  scale's bottom end.

Only `lg` and up are fluid; `xs`, `sm` and `base` are fixed on purpose. See
[`design-to-code.md`](./design-to-code.md) for why, and for what Figma reports.

## Space

4px grid. The steps are not linear — they jump at the top (`lg` 40, `xl` 64,
`2xl` 96, `3xl` 144), and that jump is the point: small steps for the inside of
things, big steps for the gaps between them.

| Range         | Job                                                              |
| ------------- | ---------------------------------------------------------------- |
| `3xs` – `2xs` | Inside a component. Icon gaps, label offsets, hairline padding.  |
| `xs` – `md`   | Between related elements. `md` is the workhorse — 27 uses.       |
| `lg`          | Between blocks within a section.                                 |
| `xl` – `3xl`  | Section rhythm. `2xl` is the current page-section block padding. |

`--content-max` (72rem) with `.container` is the page frame; `--measure` is the
prose frame. They are different jobs — don't set a paragraph to `content-max`.

## Motion

The vocabulary is small on purpose: three durations, two easings.

| Token               | For                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------- |
| `--duration-fast`   | Hover, focus, and anything responding directly to the pointer. The only duration in use today (six uses). |
| `--duration-base`   | State changes and elements arriving on screen.                                                            |
| `--duration-slow`   | Large or ambient movement — something crossing a lot of the viewport.                                     |
| `--easing-standard` | Anything that starts and ends on screen. Symmetrical.                                                     |
| `--easing-entrance` | Things arriving from outside. Decelerating, no ease-in.                                                   |

Rules:

1. **Animate `transform`, `opacity`, `color`, `border-color`, `box-shadow`.**
   Not `width`, `height`, `top` or `margin` — they force layout on every frame.
2. **Motion is never the only signal.** Same principle as colour. If an
   animation communicates something, the something must also survive with the
   animation removed.
3. **Reduced motion is already handled globally** (`global.css:141-154`) and
   blankets every transition and animation on the site. Do not add a
   `prefers-reduced-motion` block to a page — it is noise, and a second
   implementation is a second thing to get wrong.
4. **The ceiling is CSS transitions and `@keyframes`.** Scroll-driven
   animation, View Transitions, and anything needing client JS are a
   stop-and-ask, not a judgement call. See the skill file for how to raise it.

## Elevation

Three levels, one real use: the skip link lifts on focus with `--shadow-md`
(`global.css:132`). This is a flat site — a shadow is for something genuinely
floating above the page, not for giving a card "definition".

The Figma effect styles `Elevation / sm|md|lg` map to `--shadow-sm|md|lg` by
name. Read the style name, not the drop-shadow the MCP emits; the two agree
today and both must change together.

## Radius

`--radius-sm` for small chips and swatches, `--radius-md` for panels,
`--radius-full` for pills and dots (the CV download button, the timeline dots).
`--radius-lg` is unused so far.

The focus ring applies `--radius-sm` globally (`global.css:110`), so a focusable
element with a different radius will show a ring that doesn't match its shape —
override it in that element's own rule when it happens.

## Open questions

Genuinely undecided. An agent hitting one of these should ask rather than pick.

1. **What is tomato for?** It is described as a warm signal colour and used
   nowhere. Error and destructive states are the obvious reading, but pickled is
   also a red and already carries focus and emphasis — so the question is really
   _tomato vs pickled for anything that means "wrong"_, and it needs answering
   before the first form or error message ships.
2. **How far does herbs go?** Two small positive uses so far. Is it the status
   green generally, or is it the CV/education colour specifically?
3. **What is `--font-mono` for on the site?** Currently only on the styleguide itself, in its
   own value display. `--letter-spacing-extra-wide` is documented as the
   wide-tracked mono label and has no site usage — that pairing looks intended
   but has never been built.
4. **`--easing-entrance`, `--duration-base` and `--duration-slow` are unused.**
   The intent table above is the stated intent, not observed practice. First
   real entrance animation on the site settles it.
5. **`--shadow-sm` and `--shadow-lg` are unused,** and so is `--radius-lg`.
   Three levels may be one more than this site needs.
6. **Is there a second ground?** `neutral-white` currently lifts small things —
   the skip link, a callout — and carries print. Whether whole sections alternate
   white against `neutral-100` is a layout decision that hasn't come up yet, and
   it changes which contrast column matters for everything on those sections.
