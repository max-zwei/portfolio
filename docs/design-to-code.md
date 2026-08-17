# Design-to-code handoff

All design happens in Figma. Code implements it. This document is the contract
between the two — read it before implementing any screen.

## Connection

The Figma MCP server is declared in [`.mcp.json`](../.mcp.json) at the repo root,
so any Claude Code session started in this repo picks it up. It is the **remote**
server (`https://mcp.figma.com/mcp`), which means it works in cloud sessions and
does not require the Figma desktop app to be running.

Verify the connection with `whoami` before assuming a read failure is a bad node
ID — most "cannot find node" errors are actually auth or permission errors.
A working connection returns the account handle and the plan the file lives on.

> Status: verified working.

If a read fails:

1. `whoami` — confirms auth and shows rate-limit state.
2. Check the file is in a plan the account has a seat on. Files in someone
   else's draft space are not readable even with the link.
3. Re-read the node ID from the URL. `?node-id=1-2` → pass `1:2`.

## The workflow

Designs are handed over as a Figma URL pointing at a **specific frame**, not a
whole file. From that URL:

```
https://figma.com/design/<fileKey>/<name>?node-id=<int>-<int>
             ↑ fileKey                            ↑ nodeId (swap - for :)
```

1. **`get_metadata`** with the `fileKey` (and `nodeId` if you have one) — cheap
   structural overview. Use it to find the frame you actually want before pulling
   anything heavy. With no `nodeId` it lists the file's pages.
2. **`get_screenshot`** — look at the design. Do not skip this. The XML tells you
   structure; only the image tells you what it is supposed to feel like.
3. **`get_variable_defs`** — the variables bound to that frame. These map to the
   tokens in `src/styles/tokens.css`. This is the step that keeps the
   implementation honest.
4. **`get_design_context`** — the detailed spec for the frame. Pull it last and
   for one frame at a time; it is by far the largest response.

Then implement the frame in Astro using the token names directly (see below), and
compare against the screenshot before calling it done.

## Rules that keep design and code in sync

These are non-negotiable, and they are repeated in [`CLAUDE.md`](../CLAUDE.md) so
every agent session picks them up.

1. **Never hardcode a value that exists as a token.** No hex colours, no `16px`,
   no `font-family` declarations in components. If the design uses a value that
   has no token, that is a signal — add the token, don't inline the value.
2. **One flat tier — no role layer.** Components use `var(--color-neutral-700)`
   directly. There is no `--text-secondary`. This was tried and deliberately
   removed: the design is done in terms of the palette, not in terms of roles,
   so role names only added a translation step in both directions. Don't
   reintroduce them.

   What this costs, stated plainly: changing a colour is a decision at every
   site that uses it, and nothing enforces contrast. `/styleguide` renders every
   colour against every background it sits on — that is the check, and it is
   worth actually reading before picking a colour for text.

3. **A Figma variable and a CSS custom property must have the same name.**
   `color/neutral/700` ↔ `--color-neutral-700`. Since there is only one tier,
   this is now a pure mechanical transform with nothing in between: swap `/` for
   `-`, prefix `--`. When names match, drift is visible; when they don't, it's
   invisible.
4. **New token → three files.** `design/tokens.json` (Figma exchange format),
   `src/styles/tokens.css` (what ships), and the Figma variable collection. A
   token that exists in only two of the three is a bug waiting to happen.
5. **The design is the source of truth for values; the code is the source of
   truth for behaviour.** Spacing, colour and type come from Figma. Focus states,
   reduced-motion handling, keyboard order and semantic HTML are yours to get
   right — Figma has nothing to say about them.
6. **When the design and the token system disagree, ask.** A one-off value in a
   design usually means either the design drifted or the system is missing
   something. Both are worth a five-second question and expensive to guess at.

## Token sync

`design/tokens.json` is the exchange format; `src/styles/tokens.css` is what
ships. They are kept in step by hand — the file is small and changes rarely, and
a generator would be more machinery than the problem deserves.

**Figma → code** (the normal direction): pull `get_variable_defs` for a frame,
diff the values against `tokens.css`, update both `tokens.css` and `tokens.json`
in the same commit.

**Code → Figma** (when the system is being built out): `design/tokens.json` is
DTCG-shaped, so a token plugin can import it, or the `use_figma` tool can write
the variables directly. Load the `figma-use` skill first — it is a hard
prerequisite for that tool, not a suggestion.

### The collections, as built

74 variables across 6 collections, verified against the file on 17 Aug 2026.
Every one carries a description and WEB code syntax, and no two variables emit
the same code syntax.

| Figma collection | Vars | JSON key | CSS prefix                                          |
| ---------------- | ---- | -------- | --------------------------------------------------- |
| Color            | 33   | `color`  | `--color-*`                                         |
| Typography       | 20   | `font`   | `--font-*`, `--line-height-*`, `--letter-spacing-*` |
| Spacing          | 9    | `space`  | `--space-*`                                         |
| Radius           | 4    | `radius` | `--radius-*`                                        |
| Motion           | 5    | `motion` | `--duration-*`, `--easing-*`                        |
| Elevation        | 3    | `shadow` | `--shadow-*`                                        |

There is no Semantic collection. One existed briefly and was deleted — see rule
2 above.

The colour ramps are `lemon`, `pickled`, `herbs`, `tomato` and `neutral`. Lemon
stops at 500; the others run to 600. The neutral ends are **named, not
numbered** — `color/neutral/white` and `color/neutral/black`, because neither is
a pure white (`#fdfcf8`) or a pure black (`#040302`).

**The variable name _is_ the CSS custom property.** Code syntax is set so that
`color/neutral/700` reports as `var(--color-neutral-700)` in Dev Mode — swap `/`
for `-`, prefix `--`, and you have the token to type. That mechanical
correspondence is the whole anti-drift mechanism; don't break it when adding
tokens.

> **Definition of done for a new variable:** a value, a description that matches
> its _current_ name, scopes, **WEB code syntax**, and matching entries in
> `design/tokens.json` and `src/styles/tokens.css`. Code syntax is the one that
> gets forgotten, and forgetting it makes the MCP emit `var(--color\/lemon\/500)`,
> which is not valid CSS.

Three things Figma can't hold faithfully, so they live in code:

- **Fluid type.** `--font-size-*` is a `clamp()` in CSS. Figma is a fixed-size
  medium, so `font/size/*` carries the desktop (maximum) end of each clamp. The
  scale is 8 / 12 / 16 / 24 / 32 / 48 / 72px. `xs`, `sm` and `base` ship as fixed
  values rather than clamps — shrinking 16px body copy on a phone costs more than
  it buys — so only `lg` and up interpolate.
- **Elevation.** Figma variables have no shadow type, so `shadow/*` are STRING
  variables holding the CSS value, paired with matching `Elevation / sm|md|lg`
  effect styles for actually applying them on canvas. The MCP reads the _effect_,
  not the string, so it emits a literal `drop-shadow-[...]`. **Treat the effect
  style name as the contract**: `Elevation / md` means `var(--shadow-md)`. The
  two currently agree exactly; if you change one, change both.
- **Letter-spacing units.** Figma applies FLOAT letter-spacing variables in
  **px**, so it cannot express an em value. `letter-spacing/wide` reads `0.08`
  there and means `0.08em` here; `letter-spacing/extra-wide` reads `3` (px) and
  ships as `0.19em`, the em equivalent at the base size. `letter-spacing/tight`
  cannot be applied in Figma at all, which is why the heading text styles bind
  `normal` — the `-0.02em` on `h1`–`h4` is a code-side refinement, not drift.
  **Do not read Figma's letter-spacing bindings as design intent.**

**Every collection has exactly one mode**, named `Value`. There is no light/dark
split — one colour scheme, by decision. With no role tier there is nothing to
remap, so a dark scheme would mean touching every component. That is a known and
accepted consequence of the flat structure, not an oversight.

### Fonts

`font/sans` is **Satoshi Variable** and `font/serif` is **Erode Variable** (both
Fontshare); `font/mono` is JetBrains Mono. `--font-sans` and `--font-serif` name
them first, but **none of the three is vendored yet** — the stacks fall through
to system faces, so the built site is currently rendering in fallbacks.

Two things to know before picking this up:

1. Neither face is on npm or Fontsource. They have to be downloaded from
   Fontshare and self-hosted from `public/fonts/`, under their licence. No CDN
   link — the site makes no third-party requests, by decision.
2. Neither face is available to the Figma MCP runtime either. It reports
   _"the font family Satoshi Variable does not exist"_, which means they are
   installed locally on Max's machine rather than shared with the file. Anyone
   opening the file without them sees substituted type, and any script that has
   to load a font before editing a text node or style will fail.

## Code Connect

Once components exist in `src/components/`, map them to their Figma counterparts
with `add_code_connect_map`. After that, `get_design_context` returns _"this is
`<ProjectCard>`"_ instead of a wall of divs, which is the difference between an
agent reusing your component and rebuilding it from scratch. Do this as soon as a
component is stable — it pays for itself on the second use.
