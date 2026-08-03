# Content schema — projects

The single source of truth is [`src/content.config.ts`](../src/content.config.ts).
The Decap CMS form in [`public/admin/config.yml`](../public/admin/config.yml) must
mirror it. This document explains what each field is _for_, which the code cannot.

Entries live in `src/content/projects/<slug>.md`. The filename becomes the URL
slug (`src/content/projects/lesekiste.md` → `/work/lesekiste`).

## Fields

| Field       | Type                 | Required    | Purpose                                                                                                       |
| ----------- | -------------------- | ----------- | ------------------------------------------------------------------------------------------------------------- |
| `title`     | string               | yes         | Project name. Used as the page `<h1>` and in listings.                                                        |
| `hmw`       | string               | yes         | The "How might we …" framing, **without** the prefix — the UI adds it. Keep it as a question.                 |
| `summary`   | string (≤ 280 chars) | yes         | Card copy and meta description. One or two sentences.                                                         |
| `year`      | number               | yes         | Year the work was done, or started for ongoing work.                                                          |
| `tags`      | string[]             | no          | Discipline and domain tags, e.g. `["UX Research", "EdTech"]`. Defaults to `[]`.                               |
| `cover`     | image path           | no          | Cover image, path relative to the markdown file. Astro optimises it at build time.                            |
| `coverAlt`  | string               | conditional | **Required whenever `cover` is set** — the build fails otherwise. Describe the image, don't repeat the title. |
| `figmaUrl`  | URL                  | no          | The Figma file or frame the work was designed in.                                                             |
| `repoUrl`   | URL                  | no          | The GitHub repository, where the project has one.                                                             |
| `artefacts` | list of images       | no          | Supporting images — sketches, flows, screens, photos. Each needs `src` and `alt`. Defaults to `[]`.           |

The markdown body below the frontmatter is the case study itself.

**That's the whole schema, on purpose.** Every field costs three files to keep
in sync, so the set stays at what a case study genuinely can't be written
without. Things like `role`, `duration` or `featured` are
easy to add — see below — but they should be added when a design calls for
them, not in advance.

## Conventions

- **`hmw` is the hook.** Every project opens with the same framing, so the
  portfolio reads as one point of view rather than a list of deliverables.
- **Every artefact needs alt text.** Unlike `cover`, there is no way to add one
  without it — the schema requires `alt` on each. Describe what the image shows;
  a reader who can't see it should still follow the argument.
- **`figmaUrl` and `repoUrl` are the receipts.** They let a case study point at
  the actual working file rather than only the polished retelling.
- **Tags are a controlled vocabulary.** Reuse existing tags before inventing new
  ones; the CMS offers the existing set as suggestions.
- **Images live next to the entry.** Cover images go in
  `src/content/projects/_media/` and are referenced as `./_media/cover.jpg`, so
  Astro can optimise and hash them.

## Example

```markdown
---
title: Lesekiste
hmw: make reading practice feel like play for six-year-olds?
summary: A tangible reading companion that turns daily practice into a shared
  ritual between child and parent.
year: 2026
tags:
  - UX Research
  - EdTech
cover: ./_media/lesekiste-cover.jpg
coverAlt: A wooden box with illustrated cards spread out on a kitchen table
figmaUrl: https://figma.com/design/xxxx/Lesekiste
repoUrl: https://github.com/max-zwei/lesekiste
artefacts:
  - src: ./_media/lesekiste-flow.png
    alt: Service blueprint showing the evening routine from box to bedtime
  - src: ./_media/lesekiste-cards.jpg
    alt: Six prototype cards laid out, each with a single word and a drawing
---

## The starting point

…
```

## Adding a field

1. Add it to the zod schema in `src/content.config.ts` (with a doc comment).
2. Add the matching widget to `public/admin/config.yml`.
3. Add a row to the table above.
4. Render it wherever it belongs.

Skipping step 2 is the usual cause of "the CMS saved it but the build fails".
