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

| Concern    | Choice | Notes |
| ---------- | ------ | ----- |
| Framework  | Astro (static output) | No SSR. Zero client JS unless a feature genuinely needs it. |
| Styling    | Plain CSS + custom properties | No Tailwind, no CSS-in-JS. Scoped `<style>` blocks in `.astro` files. |
| Content    | Astro content collections | Markdown in `src/content/projects/`, schema in `src/content.config.ts`. |
| CMS        | Decap CMS | `public/admin/`. Writes markdown back to the repo. Local editing only, by decision — see `docs/cms.md`. |
| Hosting    | GitHub Pages via Actions | `.github/workflows/deploy.yml`, pushes to `main` only. |
| Design     | Figma via MCP | `.mcp.json`, workflow in `docs/design-to-code.md`. |

## Non-negotiables

**Tokens.** Never hardcode a value that exists as a token. No hex colours, no
`16px`, no `font-family` in components. Use the *semantic* layer
(`var(--text-secondary)`), never primitives (`var(--color-neutral-500)`) — the
semantic layer is the only place a value can be changed once and land
everywhere. If a design needs a value that has no token, add the token; don't
inline it.

**One colour scheme.** There is no dark mode, by decision. Don't add
`prefers-color-scheme` blocks or a theme toggle. If it's ever wanted, it's a
remap of the semantic tokens — not a change to any component.

**Accessibility is part of "done", not a follow-up.**
- Semantic HTML first. A `<div>` with a click handler is a bug.
- Every interactive element needs a visible `:focus-visible` state.
- Every image needs alt text — the content schema fails the build without it.
- Respect `prefers-reduced-motion`; the global stylesheet already does, so don't
  reintroduce unconditional animation.
- Check contrast. One scheme means no dark-mode escape hatch for a weak pairing.

**Static and fast.** This is a portfolio, not an app. Adding a client-side
framework, a state library, or an analytics script needs a reason and an ask.

**No invented content.** Do not write case studies, testimonials, client names,
metrics, or bio copy on Max's behalf. Placeholder copy must read as placeholder.
Real content comes from Max, through the CMS or a direct instruction.

## Layout

```
src/
  config/site.ts        Site-wide constants (name, slogan, links). Edit here, not inline.
  content.config.ts     Project schema (zod). Mirror changes in public/admin/config.yml.
  content/projects/     Case studies as markdown; images in _media/.
  layouts/              BaseLayout.astro — head, meta, OG tags, skip link.
  pages/                File-based routes.
  styles/
    tokens.css          Design tokens. Primitives, then semantics. Start here.
    global.css          Reset, typography defaults, a11y helpers, .container.
design/tokens.json      DTCG token export — the Figma exchange format.
public/admin/           Decap CMS shell + config.
docs/                   Deployment, content schema, design-to-code handoff, CMS.
```

## Commands

```bash
npm run dev      # local dev server
npm run check    # astro check — must be 0 errors, 0 warnings before committing
npm run build    # static build into dist/
npm run preview  # serve the built output
npx decap-server # local CMS backend, so /admin works without OAuth
```

`npm run check` and `npm run build` both run in CI on every PR. Run them locally
before pushing; they catch schema mismatches that are otherwise invisible.

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
- Comments explain *why*, not *what*. The token files are the exception — there,
  the naming rationale is the useful part.
