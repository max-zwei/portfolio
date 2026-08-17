# CLAUDE.md

Guidance for Claude Code (and any other agent) working in this repository.

## What this is

Max Pinkert's personal portfolio. A designer's site: it shows the work, the
person, and what is currently being worked on. The focus is UX and product
design, moving towards children's and education technology.

**Design happens in Figma. This repo implements it.** You are usually not being
asked to invent a visual design — you are being asked to build one faithfully.
When there is no design yet, keep it restrained and token-driven so the real
design drops in cleanly later.

The bar for the visual result is "professional, but not plain". Restraint is not
the same as blandness — the site should feel considered, with one or two
deliberate gestures rather than a page full of them.

## Stack

| Concern   | Choice                        | Notes                                                                                                   |
| --------- | ----------------------------- | ------------------------------------------------------------------------------------------------------- |
| Framework | Astro (static output)         | No SSR. Zero client JS unless a feature genuinely needs it.                                             |
| Styling   | Plain CSS + custom properties | No Tailwind, no CSS-in-JS. Scoped `<style>` blocks in `.astro` files.                                   |
| Content   | Astro content collections     | Markdown in `src/content/projects/`, schema in `src/content.config.ts`.                                 |
| CMS       | Decap CMS                     | `public/admin/`. Writes markdown back to the repo. Local editing only, by decision — see `docs/cms.md`. |
| Hosting   | GitHub Pages via Actions      | `.github/workflows/deploy.yml`, pushes to `main` only.                                                  |
| Design    | Figma via MCP                 | `.mcp.json`, workflow in `docs/design-to-code.md`.                                                      |

## Non-negotiables

**Tokens.** Never hardcode a value that exists as a token. No hex colours, no
`16px`, no `font-family` in components. Use the token names directly —
`var(--color-neutral-700)`, `var(--space-md)`. If a design needs a value that
has no token, add the token; don't inline it.

**One tier, no role layer.** There is no `--text-secondary` / `--surface-default`
tier and there should not be one. Max designs in terms of the palette, not in
terms of roles, so a second set of names for the same values only adds a
translation step in both directions. Don't reintroduce it — this was tried and
deliberately removed. The token names in `tokens.css` are the same names as the
Figma variables, and that one-to-one mapping is the whole anti-drift mechanism.

The cost of this is that nothing enforces contrast for you: changing a colour is
a real decision at every site that uses it. `/styleguide` renders every colour
against every background it actually sits on — check it.

**One colour scheme.** There is no dark mode, by decision. Don't add
`prefers-color-scheme` blocks or a theme toggle. Without a role layer a dark
scheme would be a real refactor, not a remap — which is a known and accepted
consequence of the choice above, not a problem to solve pre-emptively.

**Accessibility is part of "done", not a follow-up.**

- Semantic HTML first. A `<div>` with a click handler is a bug.
- Every interactive element needs a visible `:focus-visible` state.
- Every image needs alt text — the content schema fails the build without it.
- Respect `prefers-reduced-motion`; the global stylesheet already does, so don't
  reintroduce unconditional animation.
- Check contrast. One scheme means no dark-mode escape hatch for a weak pairing.
- `npm run lint:html` enforces alt text, heading order and labels against the
  built output. It runs in CI, so a regression fails the PR.

**Static and fast.** This is a portfolio, not an app. Adding a client-side
framework, a state library, or an analytics script needs a reason and an ask.

**Keep it small.** No speculative structure — no fields, options or helpers for
a use case that doesn't exist yet. Max reads this repo to understand and change
it himself, and every unused abstraction is a thing he has to decode first. A
content field costs three files to keep in sync; add one when a design needs it.

**No invented content.** Do not write case studies, testimonials, client names,
metrics, or bio copy on Max's behalf. Placeholder copy must read as placeholder.
Real content comes from Max, through the CMS or a direct instruction.

## Layout

```
src/
  config/site.ts        Site-wide constants (name, slogan, links). Edit here, not inline.
  config/resume.ts      CV intro + timeline. The only place a position is written down.
  content.config.ts     Project schema (zod). Mirror changes in public/admin/config.yml.
  content/projects/     Case studies as markdown; images in _media/.
  layouts/              BaseLayout.astro — head, meta, OG tags, skip link.
                        ProseLayout.astro — markdown document pages.
  pages/                File-based routes. handshake.md is a markdown page.
  styles/
    tokens.css          Design tokens. One flat tier. Start here.
    global.css          Reset, typography defaults, a11y helpers, .container.
design/tokens.json      DTCG token export — the Figma exchange format.
public/admin/           Decap CMS shell + config.
public/cv/              The CV as PDF. Generated by npm run cv — never hand-edited.
scripts/render-cv.mjs   Prints the built /resume page to that PDF.
docs/                   Deployment, content schema, design-to-code handoff, CMS, CV.
```

The CV is `/resume` printed to A4 — one source (`src/config/resume.ts`), two
outputs. Change the data and re-run `npm run cv`, or the committed PDF goes stale.
See `docs/resume-and-handshake.md`.

## Commands

```bash
npm run dev      # local dev server
npm run verify   # check + build + HTML lint + format check — run before pushing
npm run cv       # rebuild, then re-print /resume to public/cv/max-pinkert-cv.pdf
npm run format   # prettier, write mode
npx decap-server # local CMS backend, so /admin works without OAuth
```

`npm run verify` is the same chain CI runs (CI adds `npm audit`). Run it before
pushing; it catches schema mismatches and accessibility regressions that are
otherwise invisible until the build fails.

## When changing content fields

A project field lives in three places. Change all three or the CMS will write
frontmatter the build rejects:

1. `src/content.config.ts` — the zod schema (the enforcer)
2. `public/admin/config.yml` — the CMS form
3. `docs/content-schema.md` — the human explanation

## Working with Figma

Read `docs/design-to-code.md` first. The short version: `get_metadata` to orient,
`get_screenshot` to actually look at it, `get_variable_defs` to get the tokens,
`get_design_context` last and one frame at a time. Never skip the screenshot —
the XML tells you structure, the image tells you intent.

Before any `use_figma` call, load the `figma-use` skill. It is a hard
prerequisite, not a recommendation.

## Conventions

- Commit messages: `<area>: <what changed>` — e.g. `tokens: add status colours`,
  `content: add lesekiste case study`. Present tense, lowercase.
- Work on a branch, open a PR, let CI run. `main` deploys straight to production.
- Comments explain _why_, not _what_. The token files are the exception — there,
  the naming rationale is the useful part.
