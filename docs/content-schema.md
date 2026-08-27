# Content schema

Six collections. The single source of truth is
[`src/content.config.ts`](../src/content.config.ts); the Decap CMS forms in
[`public/admin/config.yml`](../public/admin/config.yml) must mirror it. This
document explains what each field is _for_, which the code cannot.

| Collection     | Lives in                     | What it is                                |
| -------------- | ---------------------------- | ----------------------------------------- |
| `projects`     | `src/content/projects/`      | The case studies                          |
| `playground`   | `src/content/playground/`    | Small self-directed builds                |
| `inspiration`  | `src/content/inspiration/`   | Other people's work worth pointing at     |
| `curiosity`    | `src/content/curiosity/`     | A thought and the question it leaves open |
| `resume`       | `src/content/resume/`        | The CV, one entry per position            |
| `releaseNotes` | `src/content/release-notes/` | What changed on the site, and when        |

The filename becomes the URL slug where a collection has a page. Every
collection ships one `[bracketed placeholder]` entry as a worked example —
copy it, or create an entry through `/admin`.

## projects

The case study, told in eight sections. Everything above them is card and
listing data.

| Field                 | Type           | Required    | Purpose                                                      |
| --------------------- | -------------- | ----------- | ------------------------------------------------------------ |
| `title`               | string         | yes         | Project name. Used as the page `<h1>` and in listings.       |
| `summary`             | string (≤ 280) | yes         | Card copy and meta description. One or two sentences.        |
| `company`             | string         | yes         | Who the work was for.                                        |
| `year`                | number         | yes         | Year the work was done, or started for ongoing work.         |
| `tags`                | string[]       | no          | Discipline and domain tags, e.g. `["uxresearch", "edtech"]`. |
| `teaserVertical`      | image          | no          | Portrait teaser, for tall cards.                             |
| `teaserVerticalAlt`   | string         | conditional | **Required whenever `teaserVertical` is set.**               |
| `teaserHorizontal`    | image          | no          | Landscape teaser, for wide cards.                            |
| `teaserHorizontalAlt` | string         | conditional | **Required whenever `teaserHorizontal` is set.**             |
| `figmaUrl`            | URL            | no          | The Figma file or frame the work was designed in.            |
| `repoUrl`             | URL            | no          | The GitHub repository, where the project has one.            |

Then the eight sections, in narrative order — `context`, `hmw`, `exploration`,
`definition`, `development`, `feedback`, `learning`, `behindTheScenes`. Each is
**optional** (not every project earns all eight) and each has the same shape:

| Field         | Type           | Required | Purpose                                                 |
| ------------- | -------------- | -------- | ------------------------------------------------------- |
| `subtitle`    | string         | no       | Sits next to the section heading.                       |
| `description` | markdown       | no       | The section itself. Required once the section exists.   |
| `artefacts`   | list of images | no       | Each needs `src` and `alt`. Alt text is never optional. |
| `keyPoints`   | string[]       | no       | The section in bullets, for a reader in a hurry.        |

There is no markdown body — the eight sections _are_ the case study.

## playground

| Field           | Type           | Required    | Purpose                                               |
| --------------- | -------------- | ----------- | ----------------------------------------------------- |
| `title`         | string         | yes         | Name of the experiment.                               |
| `summary`       | string (≤ 280) | yes         | One or two sentences — this is the whole description. |
| `teaser`        | image          | no          | Card image.                                           |
| `teaserAlt`     | string         | conditional | **Required whenever `teaser` is set.**                |
| `githubUrl`     | URL            | no          | Where the code lives.                                 |
| `figmaUrl`      | URL            | no          | Where it was designed.                                |
| `additionalUrl` | URL            | no          | Anything else — a demo, a write-up, a video.          |

## inspiration

| Field       | Type           | Required    | Purpose                                                |
| ----------- | -------------- | ----------- | ------------------------------------------------------ |
| `title`     | string         | yes         | Name of the thing.                                     |
| `url`       | URL            | yes         | Where it lives. The point of the entry.                |
| `summary`   | string (≤ 280) | yes         | Why it's here — what you took from it, not what it is. |
| `teaser`    | image          | no          | Card image.                                            |
| `teaserAlt` | string         | conditional | **Required whenever `teaser` is set.**                 |

## curiosity

| Field      | Type   | Required | Purpose                             |
| ---------- | ------ | -------- | ----------------------------------- |
| `thought`  | string | yes      | The observation.                    |
| `question` | string | yes      | What it makes you want to find out. |

Both halves, always. A thought without its question is a status update. Always check the question for any mispells, as the thoughts will be matched to corresponding questions.

## resume

One entry per position or qualification. **This is the CV** — see
[`docs/resume.md`](./resume.md), and re-run `npm run pdf` after editing or the
committed PDF goes stale.

| Field         | Type                  | Required    | Purpose                                                        |
| ------------- | --------------------- | ----------- | -------------------------------------------------------------- |
| `role`        | string                | yes         | Job title, or the degree for an education entry.               |
| `company`     | string                | yes         | Employer, client or institution.                               |
| `kind`        | `work` \| `education` | yes         | Tells the two apart on the printed CV.                         |
| `start`       | `YYYY-MM`             | yes         | The timeline sorts on this, so the format matters.             |
| `end`         | `YYYY-MM`             | no          | Leave it out for anything still active.                        |
| `summary`     | string                | yes         | One or two sentences: what the work was, and what came of it.  |
| `logo`        | image                 | no          | Company or institution mark.                                   |
| `logoAlt`     | string                | conditional | **Required whenever `logo` is set.**                           |
| `projectUrls` | URL[] (max 3)         | no          | Up to three things to point at. Ordered — the first one leads. |

The CV's opening paragraph is _not_ here. It is bio copy rather than a position,
so it lives in [`src/config/site.ts`](../src/config/site.ts) as `CV_INTRO`.

## releaseNotes

| Field            | Type           | Required | Purpose                                               |
| ---------------- | -------------- | -------- | ----------------------------------------------------- |
| `date`           | date           | yes      | When the release happened.                            |
| `userExperience` | markdown       | no       | What changed in how the site behaves.                 |
| `userInterface`  | markdown       | no       | What changed in how it looks.                         |
| `tech`           | markdown       | no       | What changed under it — build, CMS, tokens, workflow. |
| `screenshots`    | list of images | no       | Each needs `src` and `alt`.                           |
| `file`           | path           | no       | An optional attachment, under `/releases`.            |

All three category fields are optional because a release rarely moves all three
at once. `file` is the **one upload that does not live in `src/`** — it is served
as-is for download rather than optimised, so it goes to `public/releases/`.

## Conventions

- **Every image needs alt text.** Optional images pair with an optional alt
  field and the schema fails the build if one is set without the other. Images
  inside a list (`artefacts`, `screenshots`) require `alt` outright — there is no
  escape there at all.
- **Images live next to the entry**, in the collection's `_media/` folder,
  referenced as `./_media/name.jpg`. That keeps them inside `src/` where Astro
  can optimise and hash them. `public/` is served as-is with no optimisation,
  which is why they don't go there — the release-note `file` is the deliberate
  exception, because a download should not be transformed.
- **Tags are a controlled vocabulary.** Reuse existing tags before inventing new
  ones; the CMS offers the existing set as suggestions.
- **`figmaUrl` and `repoUrl` are the receipts.** They let a case study point at
  the actual working file rather than only the polished retelling.

### Rich text in frontmatter

Section `description`s and the three release-note categories are markdown held in
**frontmatter**, not in the entry body. Astro's `render()` only renders a body, so
these need an explicit build-time markdown pass when the pages get built — use
`createMarkdownProcessor` from `@astrojs/markdown-remark` (already a transitive
Astro dependency; add it to `package.json` explicitly at that point). Build-time
only, so it stays zero client JS.

This is the price of a project having eight rich-text sections instead of one
body, and it is worth knowing before you go looking for `<Content />`.

## Example

```markdown
---
title: Lesekiste
company: Selbstständig
summary: A tangible reading companion that turns daily practice into a shared
  ritual between child and parent.
year: 2026
tags:
  - UX Research
  - EdTech
teaserVertical: ./_media/lesekiste-tall.jpg
teaserVerticalAlt: A wooden box with illustrated cards spread on a kitchen table
figmaUrl: https://figma.com/design/xxxx/Lesekiste
context:
  subtitle: Evening reading had become a fight
  description: |
    Six-year-olds are asked to read for ten minutes a day. **Most of that time
    is spent negotiating.**
  keyPoints:
    - Ten minutes is the target; nobody enjoys them
  artefacts:
    - src: ./_media/lesekiste-flow.png
      alt: Service blueprint showing the evening routine from box to bedtime
hmw:
  description: |
    How might we make reading practice feel like play?
---
```

## Adding a field

Use this file as source of truth for the fields. Update all others accordingly.

1. Add it to the zod schema in `src/content.config.ts` (with a doc comment).
2. Add the matching widget to `public/admin/config.yml`.
3. Add a row to the right table above.
4. Render it wherever it belongs.
