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

The filename becomes the URL slug where a collection has a page. Most
collections ship one `[bracketed placeholder]` entry as a worked example —
copy it, or create an entry through `/admin`. `projects` does not: every entry
there is a real case study.

## projects

The case study has two optional Markdown introductions and six optional narrative
sections. Metadata, colors, and image slots are top-level fields.

| Field      | Type                    | Required | Purpose                                                    |
| ---------- | ----------------------- | -------- | ---------------------------------------------------------- |
| `title`    | string                  | yes      | Project name and accessible listing link label.            |
| `summary`  | string (≤ 280)          | yes      | Metadata description, not visible project card copy.       |
| `company`  | string                  | yes      | Who the work was for.                                      |
| `year`     | number                  | yes      | Year the work was done, or started for ongoing work.       |
| `tags`     | string[]                | no       | Discipline and domain tags; defaults to `[]`.              |
| `figmaUrl` | URL                     | no       | The Figma file or frame the work was designed in.          |
| `repoUrl`  | URL                     | no       | The GitHub repository, where the project has one.          |
| `match`    | object of four id lists | no       | What the /home questionnaire matches this entry on.        |
| `context`  | Markdown string         | no       | The project's context, directly in frontmatter.            |
| `hmw`      | Markdown string         | no       | The question guiding the project, directly in frontmatter. |

### Colors

`color1`, `color2`, `color3`, `color4`, `color5`, `color6`, `color7`, and `color8`
are independent optional strings. Each supplied value must be exactly `#RRGGBB`
(six hexadecimal digits, either case). Quote hex values in YAML so `#` is not
treated as a comment. No palette or default values are supplied; unused colors
remain absent. The CMS uses string controls with the same hex pattern rather
than a color picker that would introduce an initial color.

Clearing a previously saved optional scalar in Decap writes `""`, rather than
removing its YAML key. The project schema treats that exact empty string as
absence for colors, image slots, `context`, and `hmw`; it supplies no replacement
value. Nonempty colors still must match the full six-digit pattern, and an image
still requires nonblank alt text. This normalization is limited to these project
fields, not required summaries or other collections.

### Images

Seven independent, optional image slots live directly in frontmatter:

| Image key    | Companion alt-text key |
| ------------ | ---------------------- |
| `img_0.8h`   | `img_0.8h_alt`         |
| `img_0.6h_l` | `img_0.6h_l_alt`       |
| `img_0.6h_s` | `img_0.6h_s_alt`       |
| `img_1_2_l`  | `img_1_2_l_alt`        |
| `img_1_2_s`  | `img_1_2_s_alt`        |
| `img_1_1`    | `img_1_1_alt`          |
| `img_1_2`    | `img_1_2_alt`          |

Each image requires its companion **nonblank alt text** when supplied. Both
controls are optional in Decap so an unused pair can remain absent; the schema
enforces the conditional requirement. Slots have no defaults. Do not populate
them with old teasers or section artefacts automatically.

The dots are **literal characters in top-level keys**, not object paths. Write
`'img_0.8h': ./_media/example.jpg`, not an `img_0` object. The admin shell in
[`src/pages/admin/index.astro`](../src/pages/admin/index.astro) pins Decap **3.15.1**.
In that version, the
[editor's `getFieldValue`](https://github.com/decaporg/decap-cms/blob/decap-cms%403.15.1/packages/decap-cms-core/src/components/Editor/EditorControlPane/EditorControlPane.js)
reads `['data', field.get('name')]`, and the
[draft reducer](https://github.com/decaporg/decap-cms/blob/decap-cms%403.15.1/packages/decap-cms-core/src/reducers/entryDraft.js)
writes `['entry', ...dataPath, name]`. Neither splits the field name.
The [frontmatter formatter](https://github.com/decaporg/decap-cms/blob/decap-cms%403.15.1/packages/decap-cms-core/src/formats/frontmatter.ts)
passes metadata to the [YAML formatter](https://github.com/decaporg/decap-cms/blob/decap-cms%403.15.1/packages/decap-cms-core/src/formats/yaml.ts),
which uses `yaml.createNode(data)` and `doc.toJSON()`: dotted keys stay literal
through serialization. This is a source-level finding, not a claim that every
dot-aware CMS feature treats names literally: the editor's `focus(path)` splits
on dots, so automatic error-focus navigation can fail for these fields.

### Narrative sections

`exploration`, `definition`, `development`, `feedback`, `learning`, and
`behindTheScenes` are optional objects with exactly these fields:

| Field       | Type            | Required              | Purpose                                 |
| ----------- | --------------- | --------------------- | --------------------------------------- |
| `summary`   | Markdown string | yes, if object exists | The section itself; must be nonempty.   |
| `keyPoints` | string[]        | no                    | Takeaways in bullets; defaults to `[]`. |

The section summary is rich text, unlike the short top-level metadata `summary`.
The CMS retains the established optional-object pattern: `required: false` on
the object and its child controls, with a hint explaining the schema-enforced
summary requirement. This is deliberate:
[Decap's object control](https://github.com/decaporg/decap-cms/blob/decap-cms%403.15.1/packages/decap-cms-widget-object/src/ObjectControl.js)
validates every child even when an optional parent is absent, and
[widget presence validation](https://github.com/decaporg/decap-cms/blob/decap-cms%403.15.1/packages/decap-cms-core/src/components/Editor/EditorControlPane/Widget.js)
does not condition a child's `required` flag on the parent. Making the CMS
summary control unconditionally required would also require omitted sections.
The build therefore rejects any existing section object without a nonempty
summary, including `{}` or an object containing only key points. Collapsing a
section does not remove it; remove the whole object from frontmatter to omit it.

The CMS `keyPoints` control deliberately has **no default**. Giving it `[]`
materializes all six otherwise untouched section objects on a new entry, which
then fail the summary requirement. The schema supplies `[]` only after an
included section has a valid summary.

There is no Markdown body. The migration preserves former `context.description`
and `hmw.description` as their top-level strings, and the six other section
descriptions as `summary`. Subtitles, artefacts, legacy aliases, and project
teaser fields are no longer part of the contract.

### Page rendering

`/projects` cycles through the six `ProjectBento` variants. Its only visible
project copy is `hmw`; `title` names the link for assistive technology. Hover or
keyboard focus expands the active bento to the page width on a black ground,
while the other bentos become invisible and noninteractive.

All seven image keys map directly to their matching bento slots (without the
`img_` prefix); `color1`–`color8` retain their numbered palette positions.
Missing images and colors are hidden, with no fallback palette, production
placeholder or automatic old-media mapping. The three current projects supply
all seven slots with local WebP artwork and descriptive companion alt text.

Project detail opens with the back/“SHOW ME” chat choice. “SHOW ME” reveals the
full case study, whose sections are inline page markup, not selection buttons
or a `ProjectSection` component. Deep section anchors and the no-JavaScript
baseline keep the content reachable. The sticky 180px image strip loops
horizontally at 40px/s, even when the original artwork fits the viewport.
Its scrollbar is hidden without disabling native touch or keyboard scrolling.
Hover, focus, and active pointer/touch gestures pause it temporarily; it resumes
from the current scroll position afterward. Reduced motion stops the loop and
removes cloned images while preserving native scrolling. `summary`, `year` and
`tags` remain metadata rather than visible case-study copy.

Optional `figmaUrl` and `repoUrl` links appear as 32px icons in the final
“Behind the scenes” row, even when that narrative section is absent.
Résumé project previews use `img_1_1`, `img_1_2_s` and the first four colors;
unprovided artwork stays absent. Unrelated styleguide image fixtures remain
in use.

### Verified editor roundtrip

The local Decap 3.15.1 editor was exercised against an isolated filesystem
backend with a disposable entry and image. Publishing and reopening preserved
all three dotted image keys and their dotted alt keys as literal top-level YAML
keys; Astro loaded the uploaded image metadata from each. The same roundtrip
preserved Markdown in `context`, `hmw`, and all six section summaries, together
with their key-point lists. An untouched new entry omitted all optional sections
and image slots. No fixture or image was added to the real project content.

The editor rejected `#abc` and saved `#AaBb09`. Runtime schema probes covered all
eight color fields, all seven image/alt pairs (including omitted, empty, and
whitespace-only alt text), optional fields, and missing section summaries.
Clearing a saved color and image was also saved through Decap and loaded as
absent values. Saving whitespace-only alt text for a populated dotted image
produced the expected Astro loader error naming that literal alt key; restoring
alt text allowed the entry to load again.
Existing projects and release notes loaded successfully, and the release form
had no screenshots control. This focused smoke does not imply that unrelated
page-component type errors or the résumé icon build error are resolved.

## playground

| Field           | Type                    | Required    | Purpose                                               |
| --------------- | ----------------------- | ----------- | ----------------------------------------------------- |
| `title`         | string                  | yes         | Name of the experiment.                               |
| `summary`       | string (≤ 400)          | yes         | One or two sentences — this is the whole description. |
| `teaser`        | image                   | no          | Card image.                                           |
| `teaserAlt`     | string                  | conditional | **Required whenever `teaser` is set.**                |
| `githubUrl`     | URL                     | no          | Where the code lives.                                 |
| `figmaUrl`      | URL                     | no          | Where it was designed.                                |
| `additionalUrl` | URL                     | no          | Anything else — a demo, a write-up, a video.          |
| `match`         | object of four id lists | No          | What the /home questionnaire matches this entry on.   |

Playground entries are placed automatically; adding a card needs no coordinates
or layout changes. The desktop canvas uses three intrinsic columns and staggered
rows with 96px gaps. A larger card widens its column or increases its row height,
so adjacent cards remain separate. Mobile and no-JavaScript views use one column.
Each filename still supplies the `/playground#<slug>` target; collection order is
preserved, with no new ordering field.

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
| `company`     | string                                   | no          | Employer, client or institution. Blank hides the company line.                                  |
| `kind`        | `work` \| `education`                    | yes         | Tells the two apart on the printed CV.                                                          |
| `start`       | `YYYY-MM`                                | yes         | The timeline sorts on this, so the format matters.                                              |
| `end`         | `YYYY-MM`                                | no          | Leave it out for anything still active.                                                         |
| `summary`     | string                                   | no          | One or two sentences: what the work was, and what came of it. Blank hides the summary.          |
| `logo`        | image                                    | no          | Company or institution mark.                                                                    |
| `logoAlt`     | string                                   | conditional | **Required whenever `logo` is set.**                                                            |
| `projects`    | project reference[] (max 3)              | no          | Existing portfolio projects connected to this entry. Shown as linked previews on /resume.       |
| `documentUrl` | path (`/letters/…` or `/certificates/…`) | no          | The Arbeitszeugnis or certificate scan for this entry. Shown on /resume, not on the printed CV. |
| `match`       | object of four id lists                  | No          | What the /home questionnaire matches this entry on.                                             |

The CV's opening paragraph is _not_ here. It is bio copy rather than a position,
so it lives in [`src/config/site.ts`](../src/config/site.ts) as `CV_INTRO`.

## releaseNotes

| Field            | Type        | Required | Purpose                                                        |
| ---------------- | ----------- | -------- | -------------------------------------------------------------- |
| `date`           | date        | yes      | When the release happened.                                     |
| `description`    | string      | no       | One sentence under the date.                                   |
| `userExperience` | markdown    | no       | What changed in how the site behaves.                          |
| `userInterface`  | markdown    | no       | What changed in how it looks.                                  |
| `tech`           | markdown    | no       | What changed under it — build, CMS, tokens, workflow.          |
| `file`           | path or URL | no       | An optional attachment, under `/releases`, or an absolute URL. |

All three category fields are optional because a release rarely moves all three
at once. `file` is the **one upload that does not live in `src/`** — an uploaded
file is served as-is for download rather than optimised, so it goes to
`public/releases/`. An absolute `http(s)://` URL is also allowed and is passed
through untouched; Decap's `file` widget only uploads, so an external URL has
to be written into the entry's markdown by hand.

## match

The `projects`, `playground`, `inspiration`, `curiosity`, and `resume`
collections can describe the evidence they provide for the `/home`
questionnaire. The object has four axes; every value is a list of ids:

- `teams`: `corporate`, `startup`, `individual`, `pre-company`, `ngo`,
  `association`
- `fields`: `web-design`, `branding`, `ux-review`, `ui-review`, `ux-concept`,
  `product-management`
- `roles`: `volunteer`, `freelancer`, `employee`, `founding-designer`
- `tech`: `solely design`, `css-html`, `wordpress`, `no-code`, `python`, `javascript`, `julia`

An entry may leave any axis empty or omit it. These ids are stable keys:
rewording a questionnaire chip does not re-tag the content. The `Other …`
answer carries no id and matches nothing.

## Conventions

- **Every image needs alt text.** Optional images pair with an optional alt
  field and the schema fails the build if an image is set without nonblank alt
  text. Project slots use the exact companion keys listed above.
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

Project `context`, `hmw`, the six section `summary` fields, and the three
release-note categories are Markdown held in **frontmatter**, not in the entry
body. Astro's `render()` only renders a body, so these fields need an explicit
build-time Markdown pass rather than `<Content />`. This stays build-time only,
with no Markdown-rendering JavaScript sent to the client.

This is the price of a project having eight rich-text sections instead of one
body, and it is worth knowing before you go looking for `<Content />`.

## Example

```markdown
---
title: '[Project name]'
company: '[Company]'
summary: '[One or two sentences about the project.]'
year: 2026
tags: []
context: |
  [The project's context, with **Markdown** if needed.]
hmw: |
  [The question guiding the project.]
exploration:
  summary: |
    [What was explored and why.]
  keyPoints:
    - '[A takeaway from exploration.]'
---
```

Unused colors, image slots, and narrative sections are intentionally absent.

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

- A case-study section's `summary`. Decap validates `required` sub-fields
  inside an object widget even when the object is optional and untouched, so
  marking it required would make all six section objects mandatory. It is
  `required: false` in the CMS; zod rejects a section that exists without one.
- Alt text (the seven project `img_*_alt` fields, `teaserAlt`, and `logoAlt`).
  The CMS cannot express "required only when the image is set", so schema
  refinements in `src/content.config.ts` enforce it. The CMS lets you save;
  the build then fails.

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
