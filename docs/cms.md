# Content and the CMS

`src/content/` is the content; Decap is the editing surface over it. It writes
markdown straight back into the repo — no database, no content API.

Both halves are here: **what every field means**, and **how to run the editor**.
The single source of truth for the fields themselves is
[`src/content.config.ts`](../src/content.config.ts); the Decap forms in
[`public/admin/config.yml`](../public/admin/config.yml) must mirror it. This
document explains what each field is _for_, which the code cannot.

## Collections

Seven, configured in [`public/admin/config.yml`](../public/admin/config.yml) and
served by [`src/pages/admin/index.astro`](../src/pages/admin/index.astro).

| Collection     | Lives in                     | What it is                                |
| -------------- | ---------------------------- | ----------------------------------------- |
| `projects`     | `src/content/projects/`      | The case studies                          |
| `playground`   | `src/content/playground/`    | Small self-directed builds                |
| `inspiration`  | `src/content/inspiration/`   | Other people's work worth pointing at     |
| `questions`    | `src/content/questions/`     | The open questions thoughts hang off      |
| `curiosity`    | `src/content/curiosity/`     | A thought, and the question it belongs to |
| `resume`       | `src/content/resume/`        | The CV, one entry per position            |
| `releaseNotes` | `src/content/release-notes/` | What changed on the site, and when        |

The filename becomes the URL slug where a collection has a page. Every
collection ships one `[bracketed placeholder]` entry as a worked example —
copy it, or create an entry through `/admin`.

## projects

The case study, told in eight sections. Everything above them is card and
listing data.

| Field                 | Type                    | Required    | Purpose                                                      |
| --------------------- | ----------------------- | ----------- | ------------------------------------------------------------ |
| `title`               | string                  | yes         | Project name. Used as the page `<h1>` and in listings.       |
| `summary`             | string (≤ 280)          | yes         | Card copy and meta description. One or two sentences.        |
| `company`             | string                  | yes         | Who the work was for.                                        |
| `year`                | number                  | yes         | Year the work was done, or started for ongoing work.         |
| `tags`                | string[]                | no          | Discipline and domain tags, e.g. `["uxresearch", "edtech"]`. |
| `teaserVertical`      | image                   | no          | Portrait teaser, for tall cards.                             |
| `teaserVerticalAlt`   | string                  | conditional | **Required whenever `teaserVertical` is set.**               |
| `teaserHorizontal`    | image                   | no          | Landscape teaser, for wide cards.                            |
| `teaserHorizontalAlt` | string                  | conditional | **Required whenever `teaserHorizontal` is set.**             |
| `figmaUrl`            | URL                     | no          | The Figma file or frame the work was designed in.            |
| `repoUrl`             | URL                     | no          | The GitHub repository, where the project has one.            |
| `match`               | object of four id lists | No          | What the /home questionnaire matches this entry on.          |

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

| Field           | Type                    | Required    | Purpose                                               |
| --------------- | ----------------------- | ----------- | ----------------------------------------------------- |
| `title`         | string                  | yes         | Name of the experiment.                               |
| `summary`       | string (≤ 280)          | yes         | One or two sentences — this is the whole description. |
| `teaser`        | image                   | no          | Card image.                                           |
| `teaserAlt`     | string                  | conditional | **Required whenever `teaser` is set.**                |
| `githubUrl`     | URL                     | no          | Where the code lives.                                 |
| `figmaUrl`      | URL                     | no          | Where it was designed.                                |
| `additionalUrl` | URL                     | no          | Anything else — a demo, a write-up, a video.          |
| `match`         | object of four id lists | No          | What the /home questionnaire matches this entry on.   |

## inspiration

| Field       | Type                    | Required    | Purpose                                                |
| ----------- | ----------------------- | ----------- | ------------------------------------------------------ |
| `title`     | string                  | yes         | Name of the thing.                                     |
| `url`       | URL                     | yes         | Where it lives. The point of the entry.                |
| `summary`   | string (≤ 280)          | yes         | Why it's here — what you took from it, not what it is. |
| `teaser`    | image                   | no          | Card image.                                            |
| `teaserAlt` | string                  | conditional | **Required whenever `teaser` is set.**                 |
| `match`     | object of four id lists | No          | What the /home questionnaire matches this entry on.    |

## questions

| Field      | Type   | Required | Purpose                             |
| ---------- | ------ | -------- | ----------------------------------- |
| `question` | string | yes      | The open question, as you'd ask it. |

One field, because a question _is_ its text. The **filename is the identity** —
that is the whole point of the collection: reword the question and every
thought under it still points at the same file.

## curiosity

| Field      | Type                    | Required | Purpose                                             |
| ---------- | ----------------------- | -------- | --------------------------------------------------- |
| `thought`  | string                  | yes      | The observation.                                    |
| `question` | reference → `questions` | yes      | The one question this thought belongs under.        |
| `match`    | object of four id lists | No       | What the /home questionnaire matches this entry on. |

Both halves, always. A thought without its question is a status update.

`question` holds a **filename**, not a sentence — `example-question`, not
`[And the question it leaves open?]`. In the CMS it is a dropdown of existing
questions; by hand, it is the question file's name without `.md`. Name one that
does not exist and the build fails with the name you typed, which is the point:
matching on the question _string_ meant one typo split a question into two, and
a reword orphaned everything under it.

That failure is a `.refine()` in `src/content.config.ts`, not `reference()`
itself. Astro's `reference()` resolves a dangling id to `undefined` and only
warns on the page that renders it — no page renders curiosity yet, so the check
has to be in the schema to be worth anything.

A thought belongs to **exactly one** question. That makes the set a tree, not a
graph — worth knowing before anything tries to draw it.

## resume

One entry per position or qualification. **This is the CV** — see
[`docs/resume.md`](./resume.md), and re-run `npm run pdf` after editing or the
committed PDF goes stale.

| Field         | Type                                     | Required    | Purpose                                                                                         |
| ------------- | ---------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------- |
| `role`        | string                                   | yes         | Job title, or the degree for an education entry.                                                |
| `company`     | string                                   | yes         | Employer, client or institution.                                                                |
| `kind`        | `work` \| `education`                    | yes         | Tells the two apart on the printed CV.                                                          |
| `start`       | `YYYY-MM`                                | yes         | The timeline sorts on this, so the format matters.                                              |
| `end`         | `YYYY-MM`                                | no          | Leave it out for anything still active.                                                         |
| `summary`     | string                                   | yes         | One or two sentences: what the work was, and what came of it.                                   |
| `logo`        | image                                    | no          | Company or institution mark.                                                                    |
| `logoAlt`     | string                                   | conditional | **Required whenever `logo` is set.**                                                            |
| `projectUrls` | URL[] (max 3)                            | no          | Up to three things to point at. Ordered — the first one leads.                                  |
| `documentUrl` | path (`/letters/…` or `/certificates/…`) | no          | The Arbeitszeugnis or certificate scan for this entry. Shown on /resume, not on the printed CV. |
| `match`       | object of four id lists                  | No          | What the /home questionnaire matches this entry on.                                             |

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

## match

The `projects`, `playground`, `inspiration`, `curiosity`, and `resume`
collections can describe the evidence they provide for the `/home`
questionnaire. The object has four axes; every value is a list of ids:

- `teams`: `corporate`, `startup`, `individual`, `pre-company`, `ngo`,
  `association`
- `fields`: `web-design`, `branding`, `ux-review`, `ui-review`, `ux-concept`,
  `product-management`
- `roles`: `volunteer`, `freelancer`, `employee`, `founding-designer`
- `tech`: `css-html`, `wordpress`, `no-code`, `python`, `javascript`, `julia`

An entry may leave any axis empty or omit it. These ids are stable keys:
rewording a questionnaire chip does not re-tag the content. The `Other …`
answer carries no id and matches nothing.

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

A `match` option is the exception: it lives in **four** places. Update
`src/config/match.ts` (the source of truth), then `src/content.config.ts`,
`public/admin/config.yml`, and this file, in that order.

1. Add it to the zod schema in `src/content.config.ts` (with a doc comment).
2. Add the matching widget to `public/admin/config.yml`.
3. Add a row to the right table above.
4. Render it wherever it belongs.

## Running the editor

```bash
npx decap-server   # terminal 1 — proxy that writes to your local files
npm run dev        # terminal 2
```

Open <http://localhost:4321/admin/>. `local_backend: true` points the CMS at the
proxy instead of GitHub, so there is no OAuth — the Login button asks for
nothing, just click it. Edits land in the working tree as ordinary file changes
for you to commit.

`publish_mode: editorial_workflow` is on, so against the GitHub backend a save
opens a draft pull request rather than committing to `main`.

## /admin is local-only, by decision

`astro.config.mjs` deletes `dist/admin` after every build. Two reasons:

1. It could not log in on the live site anyway. Decap exchanges a GitHub code
   for a token, that exchange needs a client secret, and GitHub Pages serves
   static files only — so it would need a relay that does not exist.
2. It pulls a ~5 MB third-party script from unpkg. Publishing that for a page
   nobody can use is a bad trade.

`npm run dev` still serves it, so local editing is unaffected. If an OAuth relay
is ever added, delete the integration and uncomment `base_url` /
`auth_endpoint` in `config.yml`.

Two details that look incidental and are not:

- **It is an Astro route, not a file in `public/`.** Astro's dev server serves
  `public/` by exact path and does not resolve directory indexes, so
  `public/admin/index.html` was only ever reachable at `/admin/index.html`.
- **`is:inline` on the script tag is load-bearing.** Without it Astro bundles
  the script and drops `integrity` and `crossorigin`, silently undoing the SRI
  pinning.

Decap is loaded at an **exact** version with an SRI hash, never a `^range` — a
range means the browser runs whatever the CDN resolves to, which makes SRI
impossible. Bumping the version means recomputing the hash:

```bash
npm pack decap-cms@<version> && tar -xzf decap-cms-<version>.tgz
openssl dgst -sha384 -binary package/dist/decap-cms.js | openssl base64 -A
```

SRI only covers the entry file; Decap lazy-loads ~93 further chunks that are not
integrity-checked. Not deploying the page is what contains that.

## Three things the CMS cannot enforce

**`required` is deliberately not symmetric with the zod schema. Don't "fix" it.**

- A case-study section's `description`. Decap validates `required` sub-fields
  inside an object widget even when the object is optional and untouched, so
  marking it required made all eight sections mandatory. It is `required: false`
  in the CMS; zod rejects a section that exists without one.
- Alt text (`teaserVerticalAlt`, `teaserHorizontalAlt`, `teaserAlt`, `logoAlt`).
  The CMS cannot express "required only when the image is set", so the
  `.refine()` calls in `src/content.config.ts` are the enforcement. The CMS lets
  you save; the build then fails.

The CMS blocks what it can express. zod is the backstop for anything
conditional.

**A curiosity entry's `question` must point at a question that exists.** The
relation widget only offers questions that are already saved, so the CMS side is
safe — but it also means a new question has to be created under **Questions**
before a thought can be filed under it. A hand-written entry naming a missing
file is caught by the schema at build time, not before.

**Saving a résumé entry stales the committed PDF.**
`public/cv/max-pinkert-cv.pdf` is printed from `/resume`. Re-run `npm run pdf`
and commit the result — nothing checks this for you. See
[`docs/resume.md`](./resume.md).
