# CLAUDE.md

Guidance for Claude Code (and any other agent) working in this repository.

## What this is

Max Pinkert's personal portfolio. A designer's site: it shows the work, the
person, and what is currently being worked on. The focus is UX and product
design, moving towards children's and education technology.

**Design happens in Figma. This repo implements it.** You are never being
asked to create a visual design or ideate user experiences. You are being asked to build faithfully.
When there is no design yet, keep it restrained and token-driven so the real design drops in cleanly later.

## Stack

| Concern   | Choice                        | Notes                                                                                                   |
| --------- | ----------------------------- | ------------------------------------------------------------------------------------------------------- |
| Framework | Astro (static output)         | No SSR. Zero client JS unless a feature genuinely needs it.                                             |
| Styling   | Plain CSS + custom properties | No Tailwind, no CSS-in-JS. Scoped `<style>` blocks in `.astro` files.                                   |
| Content   | Astro content collections     | Six collections. Markdown in `src/content/`, schemas in `src/content.config.ts`.                        |
| CMS       | Decap CMS                     | `public/admin/`. Writes markdown back to the repo. Local editing only, by decision — see `docs/cms.md`. |
| Hosting   | GitHub Pages via Actions      | `.github/workflows/deploy.yml`, pushes to `main` only.                                                  |
| Design    | Figma via MCP                 | `.mcp.json`, workflow in `docs/design-to-code.md`.                                                      |

## Non-negotiables

1. Dsicuss any improvements or changes of this CLAUDE.md with Max first and ask for approval.

1. **Never hardcode a value that has a token.** One flat tier — use the token
   names directly, and don't reintroduce a role layer.
2. **Accessibility is part of "done"** — semantic HTML, visible focus states, alt
   text, reduced-motion, and contrast that holds up.
3. **Don't invent content.** Placeholder copy must read as placeholder.
5. **Run `npm run check` before committing.** Zero warnings.

**The Figma file is the design decision, not a draft.** If it says
`color/pickled/500`, that is the answer — including when it fails a contrast
check, breaks a ramp's symmetry, or looks like an oversight. You may **raise**
it: in an audit, in a PR description, in the contrast table on `/styleguide`.
You may not **resolve** it. Do not add a token, darken a value, extend a ramp,
or substitute a different step because the design appeared to need one.

**Decided, so don't "fix" it**
- **No dark mode.** One colour scheme. Don't add `prefers-color-scheme` blocks.
- **`/admin` is local-only and is stripped from the production build.** It can't
  log in without an OAuth relay, so shipping it would put a 5 MB third-party
  script on the live domain for nothing. Editing happens via `npx decap-server`.
  See [docs/cms.md](docs/cms.md).
- **The content schema is deliberately small.** Ten fields. Adding one costs
  three files to keep in sync, so add them when a design needs them — not in
  advance.

**Tokens.** Never hardcode a value that exists as a token. No hex colours, no
`16px`, no `font-family` in components. Use the token names directly —
`var(--color-neutral-700)`, `var(--space-md)`. If a design needs a value that
has no token, discuss it with Max.

**One tier, no role layer.** There is no `--text-secondary` / `--surface-default`
tier and there should not be one. Max designs in terms of the palette, not in
terms of roles, so a second set of names for the same values only adds a
translation step in both directions. Don't reintroduce it — this was tried and
deliberately removed. The token names in `tokens.css` are the same names as the
Figma variables, and that one-to-one mapping is the whole anti-drift mechanism.

**Accessibility is part of "done", not a follow-up.**

- Semantic HTML first. A `<div>` with a click handler is a bug.
- Every interactive element needs a visible `:focus-visible` state.
- Every image needs alt text — the content schema fails the build without it.
- Respect `prefers-reduced-motion`; the global stylesheet already does, so don't
  reintroduce unconditional animation.
- Check contrast. One scheme means no dark-mode escape hatch for a weak pairing.
  Report what you measure; don't repaint the design to fix it — see the 
  non-negotiables.
- `npm run lint:html` enforces alt text, heading order and labels against the
  built output. It runs in CI, so a regression fails the PR.

**Keep it small.** No speculative structure — no fields, options or helpers for
a use case that doesn't exist yet. Max reads this repo to understand and change
it himself, and every unused abstraction is a thing he has to decode first. A
content field costs three files to keep in sync; add one when a design needs it. This applies to inline comments as well. Only use them where the code is more complex than usual or where it creates structure. The token files are the exception — there, the naming rationale is the useful part.

**No invented content.** Do not write case studies, testimonials, client names,
metrics, or bio copy on Max's behalf. Placeholder copy must read as placeholder.
Real content comes from Max, through the CMS or a direct instruction.

## Layout

```
src/
  config/site.ts        Site-wide constants (name, slogan, links, CV intro). Edit here, not inline.
  content.config.ts     Collection schemas (zod). Mirror changes in public/admin/config.yml.
  content/projects/     Case studies as markdown; images in _media/. Eight sections per project.
  content/playground/   Small self-directed builds.
  content/inspiration/  Other people's work worth pointing at.
  content/curiosity/    A thought and the question it leaves open.
  content/resume/       The CV, one entry per position. Printed to public/cv/.
  content/release-notes/ What changed on the site, and when.
  layouts/              BaseLayout.astro — head, meta, OG tags, skip link.
                        ProseLayout.astro — markdown document pages.
  pages/                File-based routes. handshake.md is a markdown page.
  styles/
    tokens.css          Design tokens. One flat tier. Start here.
    fonts.css           @font-face for Satoshi and Erode. Mono comes from npm.
    global.css          Reset, typography defaults, a11y helpers, .container.
design/tokens.json      DTCG token export — the Figma exchange format.
public/admin/           Decap CMS shell + config.
public/cv/              The CV as PDF. Generated by npm run cv — never hand-edited.
public/fonts/           Satoshi + Erode woff2, self-hosted, plus their LICENSE.
                        Third-party type — credit the foundry if you touch it.
scripts/render-cv.mjs   Prints the built /resume page to that PDF.
docs/                   Deployment, content schema, design-to-code handoff, CMS, CV.
```

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

A content field lives in three places. Change all three or the CMS will write
frontmatter the build rejects:

1. `src/content.config.ts` — the zod schema (the enforcer)
2. `public/admin/config.yml` — the CMS form
3. `docs/content-schema.md` — the human explanation

## Working with Figma

For Figma work, read
[behind-the-scenes/skills/figma-implement.md](behind-the-scenes/skills/figma-implement.md)
— the procedure for turning one frame into a page. Behind it:
[docs/design-to-code.md](docs/design-to-code.md) is the contract and
[docs/design-system.md](docs/design-system.md) is what the tokens are for. The
read order is `get_metadata` to orient → `get_screenshot` to actually look at it
→ `get_variable_defs` for tokens → `get_design_context` last, one frame at a
time. Never skip the screenshot; the XML gives you structure, the image gives
you intent.

**Implementing a frame? Read `behind-the-scenes/skills/figma-implement.md`
first, in full.** It is the step-by-step procedure — read order, token diff,
component reuse, the motion ceiling, and the checks that make a page done. It
lives in `behind-the-scenes/` rather than `.claude/skills/`, so this pointer is
what loads it. Not optional.

The two documents behind it: `docs/design-to-code.md` is the contract (token
sync, the Figma collections, the three things Figma cannot express faithfully),
and `docs/design-system.md` is the rule book for what the tokens are _for_ —
read it before choosing any colour. The short version of the read order:
`get_metadata` to orient, `get_screenshot` to actually look at it,
`get_variable_defs` to get the tokens, `get_design_context` last and one frame at
a time. Never skip the screenshot — the XML tells you structure, the image tells
you intent.

Before any `use_figma` call, load the `figma-use` skill. It is a hard
prerequisite, not a recommendation.

## Conventions

- Commit messages: `<area>: <what changed>` — e.g. `tokens: add status colours`,
  `content: add lesekiste case study`. Present tense, lowercase.
- Work on a branch, open a PR, let CI run. `main` deploys straight to production.