# The Handoff frame

Every page gets one frame named `Handoff`, sitting with that page's own frames
in Figma, and it is read before any other frame for that page — see Step 0 of
[`figma-to-astro.md`](../behind-the-scenes/skills/figma-to-astro.md). Answering
it means ticking boxes and filling short blanks, not writing prose. A blank is
not a default: a blank is an open question, and the implementer asks it rather
than infers it.

If a page has no Handoff frame yet, the skill walks this template section by
section, skipping the sections the table below says do not apply.

## Fill it in, in three moves

1. Add a frame named `Handoff` to the page's own canvas, first in reading
   order.
2. Paste the template below into one text layer.
3. Delete the lines that do not apply, tick one box per question, and keep the
   numbered headings — the headings are what gets read.

## Which sections apply

Routing is by what the page _does_, not only by its archetype: `/resume` is a
prose document that reads the `resume` collection, so it fills section 4.

| Section           | Fill it when                                                | Skip when                                     |
| ----------------- | ----------------------------------------------------------- | --------------------------------------------- |
| 1 Archetype       | always                                                      | never                                         |
| 2 What this is    | always                                                      | never                                         |
| 3 Frame index     | the page has more than one frame                            | single-frame page — say so in §2              |
| 4 Content map     | the page reads a content collection, whatever its archetype | nothing on the page comes from `src/content/` |
| 5 Flow            | something on the page is clickable or changes state         | a static document                             |
| 6 Link map        | anything links out                                          | nothing links out                             |
| 7 Copy            | always                                                      | never                                         |
| 8 Components      | always                                                      | never                                         |
| 9 States          | the page uses any interactive component                     | nothing interactive is drawn                  |
| 10 Motion         | anything moves                                              | nothing moves — write `none`                  |
| 11 Responsive     | always                                                      | never                                         |
| 12 Open questions | always                                                      | never                                         |
| 13 PDF rendering  | the page prints to PDF — `/resume/cv`, `/handshake`         | it only ever exists on screen                 |

## The template

```
HANDOFF — /route
Figma page: <page name>                    Updated: YYYY-MM-DD

1 ARCHETYPE — pick one
[ ] page                  one route, one file, nothing repeats
[ ] collection index      lists many entries of one collection
[ ] collection detail     one entry as example
[ ] prose document        long-form text; prints to PDF

2 WHAT THIS IS — pick one
[ ] one screen            everything is there at once
[ ] a set of states       the same screen, drawn several times
[ ] one continuous flow   steps accumulate, or replace each other
Carries across frames: ____________  (or: nothing)
Visitor arrives at: ____________

3 FRAME INDEX — one line per frame on this page
<frame name> — a still of: ____________
<frame name> — not a build target: [ ] reference [ ] unfinished [ ] to delete

4 CONTENT MAP — whenever the page reads a content collection; otherwise: n/a
Collection: [ ] projects [ ] playground [ ] inspiration [ ] questions
            [ ] curiosity [ ] resume [ ] releaseNotes
<layer name> -> <field name>               (field names: docs/cms.md)
Optional field empty   -> [ ] hide the element [ ] keep the space [ ] fall back to: ______
No entries at all      -> [ ] cannot happen [ ] show: ______
Text longer than drawn -> [ ] let it wrap [ ] clamp at ___ lines [ ] must not grow
A layer with no field, or a field with no layer: ____________

5 FLOW — one line per control; nothing clickable: none
<control label> -> <frame name, or /route>
Prototype links wired in Figma: [ ] yes [ ] no — the lines above are the graph

6 LINK MAP — every outgoing link, including ones with no page yet
/route  [ ] page exists  [ ] not built yet -> [ ] link anyway [ ] render as plain text

7 COPY — pick one
[ ] all final
[ ] all placeholder
[ ] mixed, placeholders marked [bracketed] in the frames
[ ] mixed, not marked — the placeholders are: ____________

8 COMPONENTS
Library sets this page uses: ____________
Anything drawn here that is not a library set: [ ] no [ ] yes: ____________
  for each -> [ ] build it inline on the page
              [ ] it belongs in the library, add it there first

9 STATES — per interactive component on this page; leave nothing silent
<component>  drawn: ______  needed, not drawn: ______  deliberately none: ______
(the six worth answering: hover, focus, selected/active, disabled, empty, loading)

10 MOTION — per moving element; nothing moves: none
<element>
  trigger:  [ ] page load [ ] hover [ ] focus [ ] click [ ] scroll position (ask me first)
  moves:    [ ] fade [ ] slide [ ] scale [ ] colour [ ] shadow [ ] other: ______
  duration: [ ] duration/fast [ ] duration/base [ ] duration/slow
  easing:   [ ] easing/standard [ ] easing/entrance
  if CSS cannot do it exactly, it must still: ____________

11 RESPONSIVE — below 48rem
[ ] mobile frame: <frame name>
[ ] no mobile design yet -> [ ] stack in source order, ask before anything else
                            [ ] rules: ____________

12 OPEN QUESTIONS — deliberately undecided
- ____________
(nothing open: write none)

13 PDF RENDERING — prose documents that print; otherwise: n/a
Renderer: HTML/CSS -> Chromium PDF, scale 1
Paper: A4 portrait, 210 x 297mm
Figma full-sheet frame: 793.7007874 x 1122.5196850
Units: 1 Figma unit = 1 CSS px; no manual px-to-pt conversion
Margins: owned by @page; guides mark the same content rectangle
Calibration margin: 10.5mm = 39.68503937 Figma units on each side
Type: exact installed/self-hosted font versions and weights
Text: fixed content width, auto height, explicit numeric line height and tracking
Flow: normal entries stay together; over-page entries may fragment
Headings: keep with the beginning of their section
Overflow: continue onto another sheet; never truncate or shrink to fit
Hard page breaks: only where explicitly marked in the print design
Motion: none
Authority: Figma print composition; Chromium-generated PDF is the physical proof
```

The options are the repo's own vocabulary, so they are picked, not substituted:
the seven collections are the seven in `src/content.config.ts`; `duration/*` and
`easing/*` are the Figma variable names for the five motion tokens in
`src/styles/tokens.css`; `[bracketed]` is the placeholder convention (CLAUDE.md
R6); `48rem` is the site's single breakpoint. Scroll-driven motion is asked
about rather than ticked because it is above the CSS ceiling and is never
decided alone.

## Why each section is asked

| Section           | Why it is asked                                                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 Archetype       | Decides routing and what has to survive testing.                                                                                            |
| 2 What this is    | The question that cost two rewrites on `/home`.                                                                                             |
| 3 Frame index     | Stops a frame being read as a page — a frame is a still, and of what is not always visible.                                                 |
| 4 Content map     | The frame shows one filled-in example; the code faces zero, one and many.                                                                   |
| 5 Flow            | The whole `/home` graph was reconstructed from button labels, because no frames were wired.                                                 |
| 6 Link map        | Six chips on `/home` still 404; a link with no page needs a decision, not a guess.                                                          |
| 7 Copy            | A `…` run read as final text once; placeholders have a convention, so use it.                                                               |
| 8 Components      | Pairs with the library drift check in Step 4 of the skill and `design/components.json`.                                                     |
| 9 States          | Every state invented on `/home` was one the frames had not drawn.                                                                           |
| 10 Motion         | Three prose sentences covered a whole page's motion last time, and it was not enough to build from.                                         |
| 11 Responsive     | The `Mobile` frame is empty, so everything below `48rem` on `/home` is unreviewed.                                                          |
| 12 Open questions | So the next read asks instead of invents.                                                                                                   |
| 13 PDF rendering  | Paper is a second medium with its own geometry, and a sheet drawn in the wrong coordinate system is the one error a screenshot cannot show. |

## What not to put in it

- **No values.** Colours, spacing, type sizes, radii and shadows are read from
  the variables (`get_variable_defs`). Naming them twice is how they drift.
- **No description of what the frame looks like.** The screenshot is read every
  time, without exception.
- **No rationale.** The Figma file is the decision (CLAUDE.md R5). The handoff
  records what, not why.
- **Nothing the template did not ask for.** If an answer is "nothing", write
  `none` — that is a complete answer, and it is shorter than a paragraph.
- **Section 13 is the exception to the first bullet.** Its numbers are facts
  about the medium — paper size, the sheet's Figma dimensions, the unit
  convention — not token values. Type sizes, colours and spacing still come
  from the variables.

## Component surfaces refresh — 2026-10-05

This records the current surface contract and exercised verification for the
shared components and four page frames.

- **Tokens:** `rounded.xl` adds a 40px radius; `rounded.lg` remains 16px.
  Spacing tokens are unchanged. The Figma xl variable's lg code syntax is a
  naming defect, not an alias. Preserve the drawn four-layer, 16px-blur
  `md-lemon` effect despite the conflicting two-layer, 32px-blur STRING value.
- **Shared surfaces:** `TextSection` uses neutral-100, 64px padding and
  0/40/40/40px corners (top-left, top-right, bottom-right, bottom-left).
  `FocusAreas` and Web `ToolBox` use the same fill/corners with 40px padding;
  Web ToolBox retains its seven-column desktop grid and tool order. PDF ToolBox
  remains unpainted and unchanged. `ReleaseNote` paints only its 64px-padded
  panel, lemon-100 active or neutral-100 inactive; its right-aligned attachment
  sits outside the panel with a 40px gap. `FlipCard` uses 0/16/16/16px corners,
  or 0/8/8/8px for Small, including animation-stage clipping. Component APIs
  and content remain unchanged.
- **Navbar:** the desktop contract is a 1280×220px neutral-black footer with
  40px vertical/64px horizontal padding and a 1152×140px inner area. A
  neutral Max avatar is 87px square above the left Explore row and links to
  `/home`, with the accessible name “Home”.
  Impressum moves into the right About list below Behind the Scenes. Right
  groups retain a 96px gap, with 12px minimum vertical separation in the
  left and rightmost groups. Existing links, social order, hover and focus
  behavior are unchanged. Browser measurements confirm a 220px desktop footer,
  263px main navigation column and 87px avatar.
- **Project detail (`128:366`):** active tomato-100 and inactive neutral-100
  panels replace text fading; neutral-black headings and neutral-800 body copy
  remain legible in both states. Panels have 64px desktop padding and 40px
  corners except the square top-left, or top-right on reversed rows. The
  observer, markers and six optional CMS sections remain; 144px section gaps
  stay outside the painted surfaces.
- **Behind the scenes (`103:1117`):** the hero, credits and release heading
  gain neutral-100 surfaces with 64px padding and 40px corners, square at
  top-left except the credits' top-right. Design/Code cards retain their fills
  and padding and gain 0/40/40/40px corners. By explicit user decision, the
  Code card renders only `DESIGN.md`: the README panel/import/link are removed,
  not the repository README. The real Figma iframe and DESIGN document retain
  16px radii; a plain `/Design System` caption sits 8px below the iframe.
- **Résumé (`103:1123`):** the screen portrait is 162px square, retaining the
  square top-left and fully rounded remaining corners; the printed CV portrait
  remains 80px. The introduction uses a tomato-100 surface with 24px padding
  and 0/16/16/16px corners. Web ToolBox (about 491.3px wide) and FocusAreas
  (419px wide) sit at opposite edges of the 1088px desktop strip, top-aligned,
  and stack in source order on mobile.
- **AI (`103:1120`):** `/ai` uses the neutral-100 TextSection surface within
  1088px, with a local 96px horizontal/64px vertical desktop padding override.
  The neutral-white page ground and 144px top/bottom margins remain.
- **Responsive accessibility fallback:** project-detail and behind-the-scenes
  surfaces stack below 64rem; TextSection responds to both the 48rem viewport
  breakpoint and a constrained container. Narrow text panels use 24px padding,
  including the `/ai` override. Web ToolBox retains its narrow-layout fallback
  rather than clipping the intrinsic desktop grid. These are accessibility
  adaptations, not changes to the spacing or radius scales.
- **Contrast:** neutral-800 body text measures 15.59:1 on neutral-100 and
  13.19:1 on tomato-100; neutral-black headings measure 17.75:1 and 15.02:1
  respectively. Inactive ReleaseNote neutral-600 on neutral-100 is 3.40:1,
  below the 4.5:1 normal-text minimum. The supplied paint is preserved, not
  silently substituted.
- **Unchanged scope:** content, CMS schemas, PDF layout, existing strip
  motion/pause behavior, reduced-motion handling and no-JavaScript access are
  not redesigned by this surface refresh.
- **Browser verification:** all four routes fit 320, 375, 768, 1024 and 1280px
  viewports without horizontal document overflow. Desktop/mobile screenshots,
  active/inactive release panels, default/small card corners, card flipping,
  footer keyboard focus and native destinations were checked. Project artwork
  moved 20px in 500ms, paused on hover, then resumed; reduced motion removed
  clones. SHOW ME still reveals the case study. At 375px with JavaScript off,
  project sections and both playground card faces remain available without
  document overflow. The printed CV retains its 80px portrait and unpainted,
  unpadded ToolBox.

## Implemented refresh contract — 2026-10-03

This records the agreed page migration after the library sync, not a replacement
for the template or the historical `/home` example below.

This dated record is historical; the 2026-10-05 section above supersedes the
affected surface and portrait contracts. Its browser and contrast observations
below remain the results recorded on 2026-10-03.

- **Projects index:** cycle through six `ProjectBento` variants. Hover/focus
  expands the current bento to page width on a black page ground; other bentos
  are invisible and noninteractive. HMW is the only visible project copy.
  Seven named optional image slots and eight optional colors map directly from
  content; missing slots are hidden, never populated with production fixtures.
- **Project detail:** the back/“SHOW ME” chat gates the full case study, not
  individual section selection. Clicking noninteractive transcript content
  finishes the current message sequence up to its choices, as on `/home`.
  Entering details hides the intro; returning to the intro hash restores it.
  Render sections inline; deep anchors and no-JavaScript access remain supported.
  The sticky header retains 96px top padding and gains 40px bottom padding
  while scrolled; measured section-anchor offsets include both.
  Its 180px image strip loops horizontally at 40px/s, including on wide screens
  where the original images fit. Hover, focus, and active gestures pause it
  temporarily; it resumes from the current position afterward. Reduced motion
  stops the loop and removes clones. The strip's scrollbar is hidden; native
  touch and keyboard scrolling remain available. Summary/year/tags are metadata only.
  The final “Behind the scenes” row owns the 32px Figma/GitHub source icons
  (reference node `668:5181`) and renders for source links alone.
- **Résumé:** current headings, 154px portrait corner, and inline CV project
  previews using `img_1_1`, `img_1_2_s` and the first four colors. Focus includes
  User Research and Data Science. Screen social icons are 24px high, preserving
  their aspect ratios; PDF previews remain suppressed.
- **Other routes:** `/behind-the-scenes` uses current Title/heading styles,
  design/code icon links and `ReleaseNote`. Embedded Markdown headings shift
  two ranks (H1 → H3), capped at H6, using the rendered rank's typography;
  code fences are unchanged. `/ai` uses Title and left alignment;
  `/impressum` uses the updated heading style.
- **Shared components:** button callers supply plain labels; `Button` owns
  decorative nav `#` and secondary arrows. The Left secondary variant used for
  “Back to projects” keeps ← before the label at rest and on hover/focus.
  Obsolete `ProjectPreview` and `ProjectSection` components are removed,
  without compatibility aliases. The updated four-layer `md-lemon` effect is
  recorded in DESIGN.md and regenerated into the existing token.
  The shared Figma icon uses a square canvas for both Black and White variants.
- **Cursor:** fine-pointer movement leaves at most 42 copies of the native
  cursor artwork. The oldest disappears every 30ms, without restarting that
  timer on movement. The trail never intercepts input; reduced motion, print,
  pointer exit, hidden pages and loss of window focus suppress or clear it.
- **Project artwork:** all three projects now supply seven local WebP images
  with descriptive alt text. Paths are entry-relative (`./_media/...`); supplied
  palette values are quoted YAML strings, not comments.
- **Browser verification:** the requested routes fit 320px and 375px viewports
  without horizontal document overflow. Refreshed Bento/CV specimens fit too,
  but existing styleguide ToolBox and inline Button specimens still overflow
  narrow viewports; this is not a claim that the whole styleguide is mobile-fit.
  Inactive case-study body text retains Figma's neutral-600: at 16px,
  `rgb(129, 128, 125)` on `rgb(253, 252, 248)` measured 3.85:1, below the
  4.5:1 normal-text minimum. The supplied color is preserved, not silently
  substituted.

---

## Worked example — /home

`/home` shipped before this document existed, so this example is reconstructed
from the repo record rather than from an actual Handoff frame. Any answer that
cannot be grounded that way says so rather than guessing — which is also what
an honest blank looks like.

```
HANDOFF — /
Figma page: chat-ground                    Updated: 2026-08-28

1 ARCHETYPE
[x] bespoke page          (reflections/2026-08-28.md:200-206)

2 WHAT THIS IS
[x] one continuous flow   steps accumulate: with the script running each
                          visited step moves into the transcript and stays
                          scrollable (index.astro:510-515); the no-JS baseline
                          shows one exchange at a time via :target
                          (index.astro:464-467)
Carries across frames: the transcript so far
Visitor arrives at: the `start` step, top of the page

3 FRAME INDEX
Mobile (103:1103) — not a build target: [x] unfinished — the frame is empty
home - 7 — a still of: the steps carrying the `…` runs
the rest of the index: [not recorded — confirm in Figma]

4 CONTENT MAP
n/a — /home reads no collection

5 FLOW
start ──▶ skip
  │        (chip links, six: /resume, /inspiration, /projects,
  │         /playground, /behind-the-scenes, /curiosities)
  ▼
team ──▶ skip
  │
  ▼
questions ──▶ skip
  │           (also carries /letters as an inline text link in its
  │            message body, not a chip — see 6)
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
Prototype links wired in Figma: [x] no — the graph above was reconstructed from
chip labels (reflections/2026-08-28.md:159-162) and is literal in
index.astro:55-379

6 LINK MAP
/resume            [x] page exists
/inspiration       [x] not built yet -> [x] link anyway
/projects          [x] not built yet -> [x] link anyway
/playground        [x] not built yet -> [x] link anyway
/behind-the-scenes [x] not built yet -> [x] link anyway
/curiosities       [x] not built yet -> [x] link anyway
/letters           [x] not built yet -> [x] link anyway
(index.astro:105-110,176-205,341-346, checked against src/pages/)

7 COPY
[x] mixed, not marked — the placeholders are: the `…` runs, which stand for
values the tool would compute, not final text

8 COMPONENTS
Library sets this page uses: Buttons, Chat, user, logo, Icons
                             (node ids: design/components.json)
Anything drawn here that is not a library set: [x] no

9 STATES
Buttons  drawn: hover  needed, not drawn: —  deliberately none: —
Two states were not drawn and were invented instead — a submit control for the
questionnaire, and a fill for a selected/ticked option — then removed once the
interaction model was corrected (reflections/2026-08-28.md:142-146)

10 MOTION
chip background-color and box-shadow (index.astro:684-686)
  trigger:  [x] hover [x] focus
  moves:    [x] colour [x] shadow
  duration: [x] duration/fast
  easing:   [x] easing/standard
  if CSS cannot do it exactly, it must still: read as the chip responding to
  the pointer, not as a new element
a bubble or a choice group arriving (index.astro:563,577)
  trigger:  [x] page load
  moves:    [x] fade [x] slide
  duration: [x] duration/base
  easing:   [x] easing/entrance
  if CSS cannot do it exactly, it must still: read as arriving into the
  transcript rather than having always been there
arrival stagger (index.astro:567-571)
  trigger:  [x] page load
  moves:    [x] other: animation-delay per row — with the script running a row
            arrives when its own first character does, not on a fixed index
            stagger
  duration: [x] duration/base
  easing:   [x] easing/entrance
  if CSS cannot do it exactly, it must still: keep the rows in order
typing pace — 12ms per character, a 160ms beat between paragraphs in one bubble
  — is a page-level constant, deliberately not a token (src/lib/chat-typing.ts:1-2)
Notes: nothing here is defined in Figma — there are no prototype connections,
so get_motion_context returns nothing for this page. global.css:149-162 zeroes
durations under prefers-reduced-motion: reduce but not animation-delay.

11 RESPONSIVE — below 48rem
[x] no mobile design yet -> [x] stack in source order, ask before anything else
One breakpoint, 48rem. The Mobile frame is empty, so everything below it is
unreviewed.

12 OPEN QUESTIONS
- the unbuilt routes, all six ticked "link anyway": /inspiration, /projects,
  /playground, /behind-the-scenes, /curiosities, /letters
- the missing mobile design
- the frame index above §3's two named frames
```
