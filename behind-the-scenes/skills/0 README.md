# Skills

A _skill_ is a markdown file that teaches an AI agent how to do one job
properly. It loads when the job comes up and shapes how the agent works —
what order to do things in, what to validate, what never to do.

They're the closest thing I have to design principles that the machine can
actually follow. Writing a good one is a design exercise: you're specifying a
process precisely enough that something without taste can execute it without
producing garbage.

These are the real files. Drop one into `.claude/skills/` and it works.

On this repo they aren't installed there — `CLAUDE.md` points at the one that
has to load on every Figma session instead, which keeps a single copy and no
drift between an installed version and a published one.

## In this folder

| Skill                                        | What it does                                                                                                                                                                  | Used on this project for                                                                                                                                                              |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`token-system.md`](./token-system.md)       | Builds a two-tier design token system in Figma variables — primitives, then semantic aliases, one collection per category, code syntax on every variable.                     | Writing the site's 94 design tokens into the Figma file with names that match the CSS one-for-one.                                                                                    |
| [`figma-implement.md`](./figma-implement.md) | Turns one Figma frame into a static Astro page — read order, token diff, component reuse via Code Connect, a hard ceiling on motion, and an accessibility gate before "done". | Written for the run of page builds starting now, so the rules survive being repeated fifteen times. No page has been built with it yet — this row gets an honest update when one has. |

## Also used here, but not republished

| Skill       | Why not                                                                                                                                   | Where to find it                                                                        |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `figma-use` | It's Figma's own guidance for their Plugin API, not something I wrote. Republishing it under my name would misrepresent whose work it is. | Ships with the [Figma MCP server](https://developers.figma.com/docs/figma-mcp-server/). |

## What makes one of these work

Things I've learned the hard way, mostly by watching the agent do something
technically correct and completely wrong:

**Say what not to do, not just what to do.** "Never batch everything into one
call" prevents more damage than any amount of positive instruction.

**Build in checkpoints.** The `token-system` skill stops and validates after
each collection. That's not caution for its own sake — it's so a mistake costs
one step instead of ninety-four variables.

**Name the failure modes.** A table of _"this error message means you did this
specific thing"_ turns a stuck agent into an agent that fixes itself. Both
errors hit during the token run were recovered from without me intervening,
because the skill described them.

**Don't let it decide anything aesthetic.** Skills should encode process, not
taste. Taste is the part I'm not delegating.

The clearest case of this so far: an agent found that my accent colour hits
4.00:1 against the page background, below the 4.5 threshold for body text. Good
catch. It then invented a darker step, added it to the Figma file and to the
palette, and shipped it. Every part of that was competent except the part that
mattered — the colour was mine to choose. The finding was worth having; the fix
wasn't its to make. `CLAUDE.md` now opens with that rule, because a system that
can spot a problem will reach for a solution unless you tell it not to.

## Adding one

Drop the `.md` file in here, add a row to the first table, and say what it was
actually used for on this project — not what it could theoretically do. If it's
not mine, it goes in the second table with a link instead.
