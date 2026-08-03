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

Then implement the frame in Astro using **semantic tokens only** (see below), and
compare against the screenshot before calling it done.

## Rules that keep design and code in sync

These are non-negotiable, and they are repeated in [`CLAUDE.md`](../CLAUDE.md) so
every agent session picks them up.

1. **Never hardcode a value that exists as a token.** No hex colours, no `16px`,
   no `font-family` declarations in components. If the design uses a value that
   has no token, that is a signal — add the token, don't inline the value.
2. **Components consume semantic tokens, not primitives.** Use
   `var(--text-secondary)`, never `var(--color-neutral-500)`. Primitives exist so
   semantics have something to point at; the semantic layer is the only place a
   value can be changed once and land everywhere it belongs.
3. **A Figma variable and a CSS custom property with the same meaning must have
   the same name.** `semantic/text/secondary` ↔ `--text-secondary`. When names
   match, drift is visible; when they don't, it's invisible.
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

The variables exist in the Figma file today — 94 of them across 7 collections,
every one carrying a `$description` and WEB code syntax.

| Figma collection | Vars | JSON key   | CSS prefix                                                         |
| ---------------- | ---- | ---------- | ------------------------------------------------------------------ |
| Color            | 35   | `color`    | `--color-*`                                                        |
| Semantic         | 19   | `semantic` | `--surface-*`, `--text-*`, `--border-*`, `--brand-*`, `--status-*` |
| Typography       | 19   | `font`     | `--font-*`, `--line-height-*`, `--letter-spacing-*`                |
| Spacing          | 9    | `space`    | `--space-*`                                                        |
| Radius           | 4    | `radius`   | `--radius-*`                                                       |
| Motion           | 5    | `motion`   | `--duration-*`, `--easing-*`                                       |
| Elevation        | 3    | —          | `--shadow-*`                                                       |

**The variable name _is_ the CSS custom property.** Code syntax is set so that
`surface/default` reports as `var(--surface-default)` in Dev Mode — swap `/` for
`-`, prefix `--`, and you have the token to type. That mechanical correspondence
is the whole anti-drift mechanism; don't break it when adding tokens.

Two things Figma can't hold faithfully, so they live in code:

- **Fluid type.** `--font-size-*` is a `clamp()` in CSS. Figma is a fixed-size
  medium, so `font/size/*` carries the desktop (maximum) end of each clamp. The
  browser interpolates below it.
- **Elevation.** Figma variables have no shadow type, so `shadow/*` are STRING
  variables holding the CSS value, paired with matching `Elevation / sm|md|lg`
  effect styles for actually applying them on canvas. Change one, change both.

**Every collection has exactly one mode**, named `Value`. There is no light/dark
split — one colour scheme, by decision. If a dark scheme is ever wanted, it is
added as a second mode on the **Semantic** collection only; the primitives and
every component stay untouched. That is what the two-tier split buys you.

## Code Connect

Once components exist in `src/components/`, map them to their Figma counterparts
with `add_code_connect_map`. After that, `get_design_context` returns _"this is
`<ProjectCard>`"_ instead of a wall of divs, which is the difference between an
agent reusing your component and rebuilding it from scratch. Do this as soon as a
component is stable — it pays for itself on the second use.
