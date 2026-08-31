# Max Pinkert — portfolio

Not the first try of creating a portfolio but hopefully a more long-term approach.

Me, myself and I, a source of my work, my profile, my skills, my random thoughts and anything in between and outside.

The repo (still not used to this lingo...) is public on purpose. My hope is to show you the behind the scenes of this design project in itself.

**Status:** trust the process

## Start here

Depending on why you're here:

**👋 You want to know how I code**
[`behind-the-scenes/`](behind-the-scenes/) which is fairly empty, as I'm still developing my coding skills and had to rely on Claude Code. Nonetheless I already included some skills I use on a regular basis and specifically for this project -> [skills](behind-the-scenes/skills/).

**🎨 You're a designer**
First of all, why are you here? You're probably looking for my Figma file:
https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio?node-id=29-39&t=TJXfA7cuqJFqoJID-1

I did also put down my thoughts on probably a heavily discussed topic on how to move from Design to Code. Honestly, I keep finding new inspiration on how to tackle this and very tough to keep up with all the updates regarding the infrastructure and tools of this process. It ended up as a skill rather than a document, because that is what actually gets read by the thing doing the work:
→ [`behind-the-scenes/skills/figma-to-astro.md`](behind-the-scenes/skills/figma-to-astro.md), and [`docs/design-system.md`](docs/design-system.md) for what the tokens are _for_.

**⚙️ You're an engineer**
Don't judge me and my beautiful repo. If you like my approach of trying to bridge Design and Code, feel free to get in touch and let's work on our next projects together!

**🤖 You're an agent**
→ [`CLAUDE.md`](CLAUDE.md). Read it before touching anything!!!

### How work flows through this repo

In my previous life I was a Quality Manager, so I can't write a document without including the word process in it. So here you go:

```
Figma (design)  ── Figma MCP // Claude CODE ──▶  repo (implementation)  ── Actions ──▶  GitHub Pages
                              ▲
                   Decap CMS ─┘  (.md)
```

All visual design is done by me in Figma and handed to Claude Code with Figma MCP as a Figma URL.
Where there's no design yet, the rule is: build restrained and token-driven, so the real design drops in cleanly later.

## Stack

| Concern   | Choice                            | Why                                                                                                                                                                 |
| --------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Framework | [Astro](https://astro.build)      | Seems like a solid choice. As long as I don't have any specific requirements, I'll stick to it                                                                      |
| Styling   | Plain CSS + custom properties     | Never really happy with how "Variables & Styles" work in Figma and how to translate this into CSS code. Know of any better solution?                                |
| CMS       | [Decap CMS](https://decapcms.org) | Writes markdown back into the repo. Looks like a nice minimalistic solution                                                                                         |
| Hosting   | GitHub Pages via GitHub Actions   | Honestly can't be bothered to use more and more tools so was hoping to find a solution within the existing tool stack and GitHub pages is also free for my use case |

## npm commands

```bash
npm install
npm run dev        # http://localhost:4321
```

| Command             | What it does                                                        |
| ------------------- | ------------------------------------------------------------------- |
| `npm run dev`       | Dev server with hot reload                                          |
| `npm run pdf`       | Re-prints `/resume` and `/handshake` to their PDFs in `public/`     |
| `npm run verify`    | **The one to run before pushing** — check, build, HTML lint, format |
| `npm run check`     | `astro check` — 0 errors, 0 warnings                                |
| `npm run build`     | Static build into `dist/`                                           |
| `npm run preview`   | Serve the built output                                              |
| `npm run format`    | Prettier, write mode                                                |
| `npm run lint:html` | Accessibility + HTML validation against `dist/`                     |
| `npx decap-server`  | Local CMS backend so `/admin` works without OAuth                   |

CI runs the same chain on every pull request, plus `npm audit`.

## The design system in one screen

Tokens live in [`src/styles/tokens.css`](src/styles/tokens.css) as **one flat
tier**, named after the thing: `--color-lemon-500`, `--space-md`,
`--font-size-lg`. Components use those names directly.

The kind of conflicts I have with Claude Code:
"There is no role layer (`--text-secondary`, `--surface-raised`). There was one;
it was removed on purpose. I design in terms of the palette, not in terms of
roles, so a second set of names for the same values just meant translating in
both directions — Figma to code, and back again in my head."

The kind of AI filler text no one needs:
"The palette is nature-inspired: **Lemon** (citrus yellow, the signature accent),
**Pickled** (a sharp pink-red counterweight), **Tomato** (used sparingly as a
signal), **Herbs** (a grounded green), plus warm-tinted neutrals so nothing sits
coldly against them. The neutral ends are named rather than numbered —
`--color-neutral-white` is `#fdfcf8` and `--color-neutral-black` is `#040302`,
because neither is a pure white or black."

I guess this should rather be in CLAUDE.md, right Claude?:
"**The one rule that matters:** never hardcode a value that has a token. The
trade this makes is explicit — with no role layer, changing a colour is a real
decision at every place it appears rather than a one-line remap, and nothing
checks contrast for you. [`/styleguide`](src/pages/styleguide.astro) renders
every colour against every background it actually sits on, which is the check.
A dark mode would be a genuine refactor rather than a remap, should it
ever be wanted."

## Note to myself: How to add content?

Either through the CMS (`/admin`) or by hand: create
`src/content/projects/<slug>.md` with the frontmatter documented in
[docs/cms.md](docs/cms.md) — one file for both the fields and the editor.

A field lives in three places and all three must agree, or shit will hit the fan:

1. `src/content.config.ts` — the zod schema
2. `public/admin/config.yml` — the CMS form
3. `docs/cms.md` — the explanation

## Licence

Split, because the code and the work aren't the same thing:

- **[MIT](LICENSE)** — the site code, the config, the build tooling, and the
  agent skills in `behind-the-scenes/skills/`. Take them and use them and build beautiful things with them!
- **[All rights reserved](LICENSE-CONTENT)** — the case studies, images, written
  copy, and the specific visual identity. Read it, link to it, quote it with
  attribution; don't republish it as your own, just looking no touching!
- **[Third-party fonts](public/fonts/LICENSE)** — neither of the above covers
  the typefaces. See below. I have a new kind of respect for typography after watching the Netflix Abstract Episode with Jonathan Hoefler, will for now and probably ever rely on professionals for typefaces.

### Typefaces

**Satoshi** (Deni Anggara) and **Erode** (Nikhil Ranganathan, Jeremie Hornus)
are © 2017–2021 [Indian Type Foundry](https://www.indiantypefoundry.com), both
trademarks of the Indian Type Foundry, obtained through
[Fontshare](https://www.fontshare.com) and self-hosted from `public/fonts/`
under the ITF Free Font Licence.

**JetBrains Mono** is © 2020 the JetBrains Mono Project Authors, under the SIL
Open Font License 1.1, installed from npm.

Terms and provenance for all three: [`public/fonts/LICENSE`](public/fonts/LICENSE).

---

**Max Pinkert** · [max.pinkert@code.berlin](mailto:max.pinkert@code.berlin)
