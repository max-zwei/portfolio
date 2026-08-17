# Max Pinkert — portfolio

A designer's portfolio, built in the open.

This is the source for my personal site: my work, myself, and whatever I'm in
the middle of. The focus is **UX and product design**, heading towards
**children's and education technology**.

The repo is public on purpose. Most of what's interesting about a design
project happens before the finished screen exists, and this is where that
lives — the token system, the decisions, the arguments with myself, and an
honest record of how much of the code an AI agent wrote.

> **Status:** infrastructure done, no case studies yet. The site is a
> deliberate v0.1 placeholder. Come back for the work; stay for the process.

## Start here

Depending on why you're here:

**👋 You want to know how I work**
→ [`behind-the-scenes/`](behind-the-scenes/) — the honest version. Includes
[what the AI agent actually did](behind-the-scenes/agent-runs/) and
[the instruction sets I write to keep it in line](behind-the-scenes/skills/).

**🎨 You're a designer**
→ [`src/styles/tokens.css`](src/styles/tokens.css) — the whole design system on
one screen. Nature-inspired palette, one flat tier.
→ [`docs/design-to-code.md`](docs/design-to-code.md) — how a Figma frame becomes
a page without the values drifting apart.

**⚙️ You're an engineer**
→ [Quick start](#quick-start), then
[`docs/content-schema.md`](docs/content-schema.md) for the content model.
→ [`CLAUDE.md`](CLAUDE.md) is the real style guide — it's written for agents,
but it's the most direct statement of how this codebase wants to be treated.

**🤖 You're an agent**
→ [`CLAUDE.md`](CLAUDE.md). Read it before touching anything.

## The idea

Three things the site has to do: show the work, show the person, and show
what's currently being worked on. That third one is the one most portfolios
skip — work in progress is meant to be visible here, not hidden until it's
polished. Case studies can link straight to the Figma file and the repo, so a
project can be shown mid-flight rather than only once it's been tidied up.

**The tone: professional, but not plain.** Restrained isn't the same as boring.
One or two confident gestures, not a page competing with itself for attention.

Every case study opens with a **"How might we …"** framing, so the portfolio
reads as one point of view rather than a pile of deliverables.

### How work flows through this repo

```
Figma (design)  ──MCP──▶  this repo (implementation)  ──Actions──▶  GitHub Pages
                              ▲
                   Decap CMS ─┘  (case studies, written as markdown)
```

All visual design is done by me in Figma and handed to an agent as a Figma URL.
**Agents implement designs; they do not invent them.** Where there's no design
yet, the rule is: build restrained and token-driven, so the real design drops in
cleanly later.

## Stack

| Concern    | Choice                                               | Why                                                                                           |
| ---------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Framework  | [Astro](https://astro.build) 7, static output        | Ships HTML, no client JS by default. A portfolio doesn't need a runtime.                      |
| Styling    | Plain CSS + custom properties                        | Tokens map 1:1 to Figma Variables. No build-tool indirection between design and code.         |
| Content    | Astro content collections                            | Markdown + a zod schema that fails the build on bad data.                                     |
| CMS        | [Decap CMS](https://decapcms.org)                    | Writes markdown back into the repo. No database, no vendor.                                   |
| Fonts      | JetBrains Mono, self-hosted; Satoshi + Erode pending | Self-hosted, no third-party requests. The two Fontshare faces still fall back to system type. |
| Hosting    | GitHub Pages via GitHub Actions                      | Free, static, already where the code lives.                                                   |
| Design I/O | Figma MCP server                                     | Lets an agent read the actual design instead of guessing from a screenshot.                   |

## Quick start

```bash
npm install
npm run dev        # http://localhost:4321
```

| Command             | What it does                                                        |
| ------------------- | ------------------------------------------------------------------- |
| `npm run dev`       | Dev server with hot reload                                          |
| `npm run cv`        | Re-prints `/resume` to `public/cv/max-pinkert-cv.pdf`               |
| `npm run verify`    | **The one to run before pushing** — check, build, HTML lint, format |
| `npm run check`     | `astro check` — 0 errors, 0 warnings                                |
| `npm run build`     | Static build into `dist/`                                           |
| `npm run preview`   | Serve the built output                                              |
| `npm run format`    | Prettier, write mode                                                |
| `npm run lint:html` | Accessibility + HTML validation against `dist/`                     |
| `npx decap-server`  | Local CMS backend so `/admin` works without OAuth                   |

CI runs the same chain on every pull request, plus `npm audit`.

## Repository layout

```
behind-the-scenes/      ★ The process, in public
  skills/               Instruction sets that shape how the agent works
  agent-runs/           What was delegated, what came back, what I decided
coding/                 Coding challenges, one folder each. Not type-checked.
.github/workflows/
  deploy.yml            Build + deploy to GitHub Pages on push to main
  ci.yml                Type-check + build on every PR
design/
  tokens.json           DTCG token export — the Figma ⇄ code exchange format
docs/
  content-schema.md     Every project field, what it's for, how to add one
  deployment.md         Pages setup, custom domain, DNS, rollback
  design-to-code.md     Figma MCP workflow and the token sync rules
  cms.md                Decap CMS: local editing, and the OAuth caveat
  resume-and-handshake.md   The CV pipeline and the pro bono agreement
public/
  admin/config.yml      Decap CMS config (the shell is src/pages/admin/)
  cv/                   The CV as PDF — a build artefact of /resume, committed
  og/default.png        Social share image
scripts/
  render-cv.mjs         Prints the built /resume page to that PDF
src/
  config/site.ts        Name, slogan, links — site-wide constants
  config/resume.ts      CV intro + timeline. The only place a position is written
  content.config.ts     Project schema (zod). The enforcer.
  content/projects/     Case studies as markdown; images in _media/
  layouts/BaseLayout.astro   <head>, meta, OG tags, skip link
  layouts/ProseLayout.astro  Markdown document pages (the handshake)
  pages/                File-based routes; admin/ is local-only, never deployed
  styles/
    tokens.css          Design tokens — one flat tier. Start here.
    global.css          Reset, type defaults, a11y helpers, .container
CLAUDE.md               Working rules for agents. Read before changing anything.
.mcp.json               Figma MCP server declaration
```

## The design system in one screen

Tokens live in [`src/styles/tokens.css`](src/styles/tokens.css) as **one flat
tier**, named after the thing: `--color-lemon-500`, `--space-md`,
`--font-size-lg`. Components use those names directly.

There is no role layer (`--text-secondary`, `--surface-raised`). There was one;
it was removed on purpose. I design in terms of the palette, not in terms of
roles, so a second set of names for the same values just meant translating in
both directions — Figma to code, and back again in my head.

The palette is nature-inspired: **Lemon** (citrus yellow, the signature accent),
**Pickled** (a sharp pink-red counterweight), **Tomato** (used sparingly as a
signal), **Herbs** (a grounded green), plus warm-tinted neutrals so nothing sits
coldly against them. The neutral ends are named rather than numbered —
`--color-neutral-white` is `#fdfcf8` and `--color-neutral-black` is `#040302`,
because neither is a pure white or black.

**The one rule that matters:** never hardcode a value that has a token. The
trade this makes is explicit — with no role layer, changing a colour is a real
decision at every place it appears rather than a one-line remap, and nothing
checks contrast for you. [`/styleguide`](src/pages/styleguide.astro) renders
every colour against every background it actually sits on, which is the check.
A dark mode would be a genuine refactor rather than a remap, should it
ever be wanted.

These tokens also exist as **Figma Variables** in the portfolio file — 74 of
them across 6 collections, with names that match the CSS one-for-one
(`color/lemon/500` in Figma is `--color-lemon-500` in code, and Dev Mode reports
it that way). Tune the values in Figma; the names don't move. **The token
_names_ are the stable contract, not the hexes.**

## Adding a case study

Either through the CMS (`/admin`, see [docs/cms.md](docs/cms.md)) or by hand:
create `src/content/projects/<slug>.md` with the frontmatter documented in
[docs/content-schema.md](docs/content-schema.md).

Every project opens with a **"How might we …"** framing (the `hmw` field) so the
portfolio reads as one point of view rather than a pile of deliverables. Each
can also carry `figmaUrl`, `repoUrl` and a list of `artefacts` — the working
files behind the retelling.

A field lives in three places and all three must agree, or the CMS will save
frontmatter that the build then rejects:

1. `src/content.config.ts` — the zod schema
2. `public/admin/config.yml` — the CMS form
3. `docs/content-schema.md` — the explanation

## Current state

Infrastructure is in place; the site is a v0.1 placeholder with no case studies
yet.

**Done**

- Astro project, static output, type-checking clean
- Design tokens (CSS custom properties + DTCG JSON), one scheme
- Project content schema + documentation
- Decap CMS wired to the schema, editorial workflow on
- v0.1 homepage — name, role, slogan, one brand gesture
- `/resume` — the CV as a timeline, and `npm run cv` to print it to PDF
- `/handshake` — the pro bono agreement, as a page I can send a client
- GitHub Actions: deploy on `main`, CI on PRs
- Figma MCP connection verified, handoff workflow documented
- Design tokens written into Figma as Variables, names matched to the CSS

**Needs a human (can't be done from code)**

- Custom domain: DNS records, then `public/CNAME` and `site` in `astro.config.mjs`
  ([docs/deployment.md](docs/deployment.md))
- Tuning the palette in Figma — the hexes there are a working set, not final
- The actual CV: positions, education and the intro paragraph are
  `[placeholders]` in [`src/config/resume.ts`](src/config/resume.ts) until I write
  them ([docs/resume-and-handshake.md](docs/resume-and-handshake.md))

**Decided, so don't "fix" it**

- **No dark mode.** One colour scheme. Don't add `prefers-color-scheme` blocks.
- **`/admin` is local-only and is stripped from the production build.** It can't
  log in without an OAuth relay, so shipping it would put a 5 MB third-party
  script on the live domain for nothing. Editing happens via `npx decap-server`.
  See [docs/cms.md](docs/cms.md).
- **The content schema is deliberately small.** Ten fields. Adding one costs
  three files to keep in sync, so add them when a design needs them — not in
  advance.

**Next**

- Real case studies
- `/work` index and project detail pages, built from the Figma designs
- An about page

## For agents

Read [CLAUDE.md](CLAUDE.md) before making changes. The short version:

1. **Never hardcode a value that has a token.** One flat tier — use the token
   names directly, and don't reintroduce a role layer.
2. **Accessibility is part of "done"** — semantic HTML, visible focus states, alt
   text, reduced-motion, and contrast that holds up.
3. **Don't invent content.** Placeholder copy must read as placeholder.
4. **Static and fast.** Adding client-side JS needs a reason and an ask.
5. **Run `npm run check` before committing.** Zero warnings.

For Figma work, read [docs/design-to-code.md](docs/design-to-code.md) first:
`get_metadata` to orient → `get_screenshot` to actually look at it →
`get_variable_defs` for tokens → `get_design_context` last, one frame at a time.
Never skip the screenshot; the XML gives you structure, the image gives you
intent.

## On the AI question

A good chunk of the code in here was written by an AI agent working from my
direction. I'd rather tell you that up front than have you find out.

The short version: I decide _what_ and _why_, the agent handles a lot of _how_,
and I stay close enough to catch it when the _how_ starts quietly changing the
_what_. Every design decision on this site is mine. Most of the lines aren't.

The long version, with the mistakes left in, is in
[`behind-the-scenes/`](behind-the-scenes/).

## Licence

Split, because the code and the work aren't the same thing:

- **[MIT](LICENSE)** — the site code, the config, the build tooling, and the
  agent skills in `behind-the-scenes/skills/`. Take them and use them.
- **[All rights reserved](LICENSE-CONTENT)** — the case studies, images, written
  copy, and the specific visual identity. Read it, link to it, quote it with
  attribution; don't republish it as your own.

The structure is fair game. The specific expression isn't.

---

**Max Pinkert** · UX & Product Design · [max.pinkert@code.berlin](mailto:max.pinkert@code.berlin)
