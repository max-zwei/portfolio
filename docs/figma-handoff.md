# The Handoff frame

Every page gets one `Handoff` frame, sitting with that page's own frames in
Figma, and it is read before any other frame for that page — see Step 0 of
[`figma-to-astro.md`](../behind-the-scenes/skills/figma-to-astro.md). Twelve
sections, each answering one question the frames themselves cannot: what kind
of page this is, what persists, where things link, what's final, what's
missing. Writing one is a checklist, not a blank page — that's what this
document is for.

If a page has no Handoff frame yet, the skill falls back to asking its
questions directly, one at a time, rather than inferring the answers.

## Archetype

**Why it exists:** decides routing and what has to be tested.

**Good answer looks like:** one of bespoke page, collection index, collection
detail, prose document — named, not implied.

## What this is

**Why it exists:** the question that cost two rewrites.

**Good answer looks like:** one sentence — a single screen, a fixed set of
states, or one continuous flow — plus what persists across frames and where a
visitor enters.

## Frame index

**Why it exists:** stops frames reading as pages.

**Good answer looks like:** every frame in the page, each with one line on
what it is a still _of_.

## Content map _(collection pages)_

**Why it exists:** the frame shows one example; the code faces N.

**Good answer looks like:** every layer mapped to its schema field, plus what
the layout does with zero entries and with every optional field absent.

## Flow

**Why it exists:** the whole graph got inferred from button labels last time.

**Good answer looks like:** every control named, with the frame or route it
leads to — a graph, not prose.

## Link map

**Why it exists:** six chips currently 404.

**Good answer looks like:** every outgoing link, including ones with no page
yet, each marked built or not.

## Copy

**Why it exists:** `[bracketed]` is already the repo's placeholder convention
(R1 §1, R6).

**Good answer looks like:** every string marked final or placeholder, using
that convention for placeholders.

## Components

**Why it exists:** pairs with the library drift check in Step 4 of the skill.

**Good answer looks like:** every library set the page uses, by name and node
id, plus any set the page needs that the library doesn't have yet.

## States

**Why it exists:** every state that got invented was one the frames hadn't
drawn.

**Good answer looks like:** every state per component marked drawn, not
drawn, or deliberately absent — never left silent.

## Motion

**Why it exists:** three prose sentences covered a whole page's motion last
time, and it wasn't enough.

**Good answer looks like:** per element — trigger, what moves, duration and
easing named as variables, and what the CSS-only fallback must still convey.

## Responsive

**Why it exists:** the `Mobile` frame is empty.

**Good answer looks like:** what changes below `48rem`, or an explicit "no
mobile design yet."

## Open questions

**Why it exists:** so the next read asks instead of invents.

**Good answer looks like:** what was left undecided on purpose.

---

## Worked example — /home

`/home` shipped before this document existed, so this example is reconstructed
from the repo record rather than from an actual Handoff frame. Any cell that
can't be grounded that way says so rather than guessing.

### Archetype

Bespoke page (`reflections/2026-08-28.md:200-206`) — the least representative
page the site will ever build, because its design _is_ its content.

### What this is

One continuous, accumulating conversation, not a set of screens. With the
script running, each visited step moves into the transcript and stays
scrollable (`index.astro:510-515`); the no-JS baseline shows one exchange at a
time via `:target` (`index.astro:464-467`). The visitor enters at the top, at
the `start` step.

### Frame index

The `/home` frames, plus `Mobile` (`103:1103`), which is empty. `home - 7` is
named as the frame carrying the `…` runs
(`figma-to-code-improvements.md:90`); the rest of the index is
**[not recorded — confirm in Figma]**.

### Content map _(collection pages)_

Not applicable — `/home` is a bespoke page, not a collection.

### Flow

Ten steps and their branches, literal in `index.astro:55-379`:

```
start ──▶ skip
  │        (chip links, six: /resume, /inspiration, /projects,
  │         /playground, /behind-the-scenes, /curiosities)
  ▼
team ──▶ skip
  │
  ▼
questions ──▶ skip
  │           (also carries /letters as an inline text link in its
  │            message body, not a chip — see Link map)
  ▼
prototype ──▶ skip
  │
  ▼
questionnaire
  │
  ▼
field ──▶ role ──▶ stack ──▶ result
                               (chip links, six: /resume, /inspiration,
                                /projects, /playground, /behind-the-scenes,
                                /curiosities)
```

The graph was reconstructed from chip labels because the frames have no
prototype connections (`reflections/2026-08-28.md:159-162`). The chip sets
above are not the complete outgoing-link set — see Link map for that,
including `/letters`.

### Link map

Built target: `/resume`. Unbuilt targets, all 404 today: `/inspiration`,
`/projects`, `/playground`, `/behind-the-scenes`, `/curiosities`, `/letters`
(`index.astro:92-97,175-205,372-377`, checked against `src/pages/`).

### Copy

The `…` runs are placeholders for values the tool would compute, not final
text. The frames don't mark them as such; the repo's placeholder convention is
`[bracketed]` (R6).

### Components

| Set       | Node ID    | Variant axes                                                        |
| --------- | ---------- | ------------------------------------------------------------------- |
| `Buttons` | `109:1382` | Type = Primary / Secondary / Nav / Inline × State = Default / Hover |
| `Chat`    | `109:1389` | Type = message / request / response × Variant = text / selection    |
| `user`    | `117:1308` | moritz / karina / paula / all                                       |
| `logo`    | `108:1372` | favicon / chat-tomato / chat-herbs                                  |
| `Icons`   | `109:1374` | Cursor / Figma Make                                                 |

(`figma-to-code-improvements.md:132-138`)

### States

Hover is drawn on `Buttons`. Two states were **not** drawn and were invented
instead: a submit control for the questionnaire, and a fill for a
selected/ticked option. Both were removed once the interaction model was
corrected (`reflections/2026-08-28.md:142-146`).

### Motion

- `--duration-fast` + `--easing-standard` for hover and focus transitions — the
  chip's `background-color` and `box-shadow` (`index.astro:684-686`).
- `--duration-base` + `--easing-entrance` for a bubble or a choice group
  arriving (`index.astro:563,577`).
- Arrival is staggered by `animation-delay`; with the script running, a row
  arrives when its own first character does, not on a fixed index stagger
  (`index.astro:567-571`).
- Typing pace — 18ms per character, a 240ms beat between paragraphs in one
  bubble — is a page-level constant, deliberately not a token
  (`index.astro:724-727`).
- Still undefined _in Figma_: there are no prototype connections, so
  `get_motion_context` returns nothing for this page.
- Caveat: `global.css:149-162` zeroes durations under
  `prefers-reduced-motion: reduce` but not `animation-delay`.

### Responsive

One breakpoint, `48rem`. The `Mobile` frame is empty, so everything below it
is unreviewed.

### Open questions

The six unbuilt routes (`/inspiration`, `/projects`, `/playground`,
`/behind-the-scenes`, `/curiosities`, `/letters`), and the missing mobile
design.
