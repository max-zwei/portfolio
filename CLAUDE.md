# CLAUDE.md

Operating rules for any agent working in this repository. Read fully before the
first edit.

## 0. Context

Max Pinkert's personal portfolio. UX and product design, moving towards
children's and education technology.

**Design happens in Figma. This repo implements it.** You are never asked to
create a visual design or ideate an experience. Where no design exists yet,
build restrained and token-driven so the real one drops in cleanly.

## 1. Rules

Numbered so they can be cited. `MUST` / `NEVER` are literal.

| Rule | Statement                                                                                                                                                                                                                                                                                                                                                                                      |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1   | NEVER change this file without Max's explicit approval. Propose, then wait.                                                                                                                                                                                                                                                                                                                    |
| R2   | NEVER write a literal that has a token. No hex, no `px`, no `font-family` in a component. Use `var(--color-neutral-700)`, `var(--space-md)`. A needed value with no token → ask.                                                                                                                                                                                                               |
| R3   | NEVER introduce a role layer. `--text-secondary`, `--surface-default` and friends were tried and deliberately removed. One flat tier only.                                                                                                                                                                                                                                                     |
| R4   | NEVER author a style the design has not defined. Every declaration traces to a Figma frame, to `global.css`, or to an accessibility requirement. An invented hover colour is a bug.                                                                                                                                                                                                            |
| R5   | The Figma file is the decision, not a draft. You MAY report a contrast failure, an asymmetric ramp, an odd value. You MUST NOT resolve one by adding a token, darkening a value, extending a ramp or substituting a step.                                                                                                                                                                      |
| R6   | NEVER invent content. No case studies, testimonials, client names, metrics or bio copy. Placeholder copy MUST read as placeholder — `[bracketed]`.                                                                                                                                                                                                                                             |
| R7   | Accessibility is part of done. Semantic HTML, a visible `:focus-visible` on every interactive element, alt text on every image, `prefers-reduced-motion` respected (globally — do not re-add it per page), contrast measured and reported.                                                                                                                                                     |
| R8   | NEVER add speculative structure. No field, option or helper for a use case that does not exist. Components are the one exception, with a sharper test: a component set **published in the Figma library** MAY live in `src/components/` before its first page use, because the library is itself a design decision. Anything not in the library stays inline on the page until its second use. |
| R9   | Comments earn their place: complex code, or structure. NOT narration of the work. `tokens.css` and `fonts.css` are the exception — there the rationale is the useful part.                                                                                                                                                                                                                     |
| R10  | Run `npm run verify` before pushing. Zero warnings.                                                                                                                                                                                                                                                                                                                                            |
| R11  | Zero client JS unless a feature genuinely cannot work without it. Ask first.                                                                                                                                                                                                                                                                                                                   |

## 2. Decided — do not revisit

| Decision                                                        | Consequence                                                                                                                       |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| No dark mode.                                                   | NEVER add a `prefers-color-scheme` block. With no role tier a dark scheme is a refactor of every component, and that is accepted. |
| `/admin` is local-only, stripped from the production build.     | It cannot log in without an OAuth relay. Edit via `npx decap-server`. See [docs/cms.md](docs/cms.md).                             |
| The content schema is deliberately small.                       | A field costs three files to keep in sync. Add one when a design needs it.                                                        |
| Token names are Figma variable names, mechanically transformed. | `color/lemon/500` ↔ `--color-lemon-500`. This one-to-one mapping is the entire anti-drift mechanism. Do not break it.             |
| Fonts are self-hosted; the site makes no third-party requests.  | No CDN links, no `@import` from a font host.                                                                                      |

## 3. Stack

| Concern   | Choice                        | Constraint                                                                      |
| --------- | ----------------------------- | ------------------------------------------------------------------------------- |
| Framework | Astro, static output          | No SSR.                                                                         |
| Styling   | Plain CSS + custom properties | No Tailwind, no CSS-in-JS. Scoped `<style>` in `.astro` files.                  |
| Content   | Astro content collections     | Seven. Markdown in `src/content/`, schemas in `src/content.config.ts`.          |
| CMS       | Decap                         | `public/admin/`. Writes markdown back to the repo.                              |
| Hosting   | GitHub Pages via Actions      | `.github/workflows/deploy.yml`. Every push to `main` deploys. PRs run `ci.yml`. |
| Design    | Figma via MCP                 | `.mcp.json`. Procedure: `behind-the-scenes/skills/figma-implement.md`.          |

## 4. Map

```
src/
  components/            Ported Figma component sets, one file per set. Each names its set and node id.
  config/site.ts         Site-wide constants. Edit here, never inline.
  content.config.ts      Collection schemas (zod).
  content/projects/      Case studies. Eight sections each; images in _media/.
  content/playground/    Small self-directed builds.
  content/inspiration/   Other people's work worth pointing at.
  content/questions/     The open questions thoughts hang off. Filename is the id.
  content/curiosity/     A thought, and the question it belongs to.
  content/resume/        The CV, one entry per position.
  content/release-notes/ What changed on the site, and when.
  layouts/               BaseLayout — head, meta, OG, skip link.
                         ProseLayout — markdown document pages.
  lib/dates.ts           formatMonth / formatRange, shared by /resume and CvSection.
  lib/tokens.ts          Reads design/tokens.json for /styleguide.
  pages/                 File-based routes. handshake.md is a markdown page.
  styles/tokens.css      Design tokens. One flat tier. Start here.
  styles/fonts.css       All three typefaces.
  styles/global.css      Reset, typography defaults, a11y helpers, .container.
design/tokens.json       DTCG export — the Figma exchange format.
design/components.json   Figma component-set manifest. Read before porting a set twice.
public/admin/            Decap CMS config.
public/cv/               CV as PDF. Generated. NEVER hand-edit.
public/handshake/        Handshake as PDF. Generated. NEVER hand-edit.
public/fonts/            Satoshi + Erode woff2 + LICENSE. Third-party type.
public/avatars/          Chat avatars as SVG. One per speaker, plus everyone.svg.
public/icons/            Footer and Icons-set marks as SVG. Exported from Figma.
public/logo/             The chat-ground logo variants as SVG. Exported from Figma.
public/certificates/     Scanned qualifications. public/letters/ — references.
scripts/render-pdf.mjs   Prints /resume and /handshake to those PDFs.
behind-the-scenes/skills/ Agent skills. figma-implement.md is the main one.
docs/                    cms (fields + editor), design-system, resume, aeo.
```

## 5. Commands

```bash
npm run dev      # local dev server
npm run verify   # check + build + HTML lint + format check — before every push
npm run pdf      # rebuild, then re-print /resume and /handshake to public/
npm run format   # prettier, write mode
npx decap-server # local CMS backend, so /admin works without OAuth
```

`npm run verify` is the chain CI runs (CI adds `npm audit`).

## 6. Procedures

### Implementing a Figma frame

**Read [behind-the-scenes/skills/figma-implement.md](behind-the-scenes/skills/figma-implement.md)
in full first. Not optional.** It is the contract and the procedure: read order,
token diff, component reuse, the motion ceiling, the checks that make a page
done.

[docs/design-system.md](docs/design-system.md) is what the tokens are _for_.
Read it before choosing any colour.

Read order, short form: `get_metadata` → `get_screenshot` → `get_variable_defs`
→ `get_design_context` (one frame, last). NEVER skip the screenshot.

Before any `use_figma` call, load the `figma-use` skill. Hard prerequisite.

### Changing a content field

A field lives in three places. Change all three or the CMS writes frontmatter
the build rejects:

1. `src/content.config.ts` — the zod schema (the enforcer)
2. `public/admin/config.yml` — the CMS form
3. `docs/cms.md` — the explanation

### Adding a token

Three files, same commit: `design/tokens.json`, `src/styles/tokens.css`, and the
Figma variable collection. Two of three is a bug. The Figma variable needs WEB
code syntax set, or the MCP emits invalid CSS.

### Editing the résumé or the handshake

Both PDFs are printed from their pages. After editing either, run `npm run pdf`
and commit the result — nothing checks this for you.

## 7. Conventions

- Commits: `<area>: <what changed>`, present tense, lowercase. E.g.
  `tokens: add status colours`, `content: add lesekiste case study`.
- Work on a branch, open a PR, let CI run. `main` deploys straight to
  production.
