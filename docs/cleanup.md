# Cleanup

Working list. Answers to the questions are at the bottom.

# Deleted files

/Users/max.pinkert/Documents/GitHub/portfolio/docs/design-system-audit.md
/Users/max.pinkert/Documents/GitHub/portfolio/behind-the-scenes/agent-runs
/Users/max.pinkert/Documents/GitHub/portfolio/docs/design-to-code.md — merged into the figma-implement skill
/Users/max.pinkert/Documents/GitHub/portfolio/docs/deployment.md — folded into CLAUDE.md

# Open tasks for Claude

| Task                                                                                    | Folder / File                                 | Status                                                                                                                                |
| --------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Clean up file names                                                                     | `public/certificates`, `public/letters`       | Done — `max-pinkert-<document>-<issuer>.pdf`, lowercase kebab                                                                         |
| AEO, what can we do here already in order to have my page appear in answers to prompts? | —                                             | Done — [`docs/aeo.md`](./aeo.md). Item 1 needs copy from Max before the rest pays off                                                 |
| I want to visualise thoughts as a kind of mind map to each question. Is the CMS ready?  | `src/content/curiosity`                       | Answered — **no**, see A1. Needs your decision before any change                                                                      |
| I want this as a page /handshake, plus a PDF download                                   | `src/pages/handshake.md`                      | Done — page already existed; PDF at `/handshake/max-pinkert-handshake.pdf`, download link in the header, `npm run pdf` regenerates it |
| It's confusing that the JetBrains font isn't listed in this file                        | `src/styles/fonts.css`                        | Done — all three faces are declared there now, see A2                                                                                 |
| From where did you derive `a:hover { color: … }`? Make it a rule                        | `src/styles/global.css`                       | Done — removed; rule added to `docs/design-system.md` ("No style without a design") and as R4 in CLAUDE.md                            |
| Why so many fallback fonts?                                                             | `src/styles/tokens.css`                       | Done — three names max per stack, see A3                                                                                              |
| Get rid of the prosa comments                                                           | `src/styles/tokens.css`                       | Done                                                                                                                                  |
| What is the "Prettier" plugin?                                                          | `.prettierrc.json`                            | Answered — A4                                                                                                                         |
| Reduce cms.md to the necessary requirements                                             | `docs/cms.md`                                 | Done — 8 kB → 3 kB, the speculative OAuth section is gone                                                                             |
| What is the purpose of cms.md? Can't it be in content-schema.md?                        | `docs/cms.md`                                 | Answered — A5. Kept, but scoped: cms.md is the tool, content-schema.md is the content                                                 |
| Shouldn't design-to-code.md be part of CLAUDE.md? Or solely a skill?                    | `docs/design-to-code.md`                      | Done — merged into the skill and deleted, see A6                                                                                      |
| Shouldn't deployment.md be in CLAUDE.md? Or irrelevant?                                 | `docs/deployment.md`                          | Done — one row in the CLAUDE.md stack table, rest deleted, see A7                                                                     |
| Review the figma-implement skill for reliability and reproducibility                    | `behind-the-scenes/skills/figma-implement.md` | Done — see A8. Named in CLAUDE.md §6 as the main skill                                                                                |
| Review CLAUDE.md — structured, written for Claude, not prose                            | `CLAUDE.md`                                   | Done — rules R1–R11, decided list, map, procedures. **Needs your approval (R1)**                                                      |

# Open questions

| Question                            | Folder / File  | Answer                                                  |
| ----------------------------------- | -------------- | ------------------------------------------------------- |
| What is this folder for? Temporary? | `public/og`    | A9 — in use, don't delete. But the image isn't on-brand |
| What are all the node modules for?  | `node_modules` | A10                                                     |

# Answers

## A1 — Curiosity as a mind map: not ready

Today a curiosity entry is one `thought` + one `question`, both free text. To
group thoughts under a question you would have to match on the **question
string**, which is why `docs/content-schema.md` currently says to watch for
misspellings. That is a fragile way to build a graph: one typo and a node
splits in two, and renaming a question orphans every thought under it.

What it would take:

1. A `questions` collection — one file per question, the filename becoming the
   stable id.
2. `curiosity` (the thoughts) gets a `question` field that is a Decap
   **relation** widget pointing at that collection. That gives a dropdown of
   existing questions instead of retyped text, and the id survives a reword.
3. A page that groups thoughts by that id and draws the map.

Three files each for steps 1 and 2, plus a migration of the existing entries.

**Not done, because two things are your call and I should not invent them:**
does a question carry anything besides its text (a status — open / answered? a
date? a colour?), and does a thought belong to exactly one question or several?
The second decides whether this is a tree or a graph, which decides the
visualisation. Say which, and it is a small change.

## A2 — Why JetBrains Mono was not in fonts.css

Half right, half not. It comes from npm
(`@fontsource-variable/jetbrains-mono`), which ships its own `@font-face` rules
already subset by `unicode-range` — hand-writing them would throw that away, so
not duplicating the declaration was correct. But the import sat in
`BaseLayout.astro`, which is a layout, not where typefaces belong. Your instinct
was right: one file should own the type.

Fixed. `fonts.css` now opens with `@import '@fontsource-variable/jetbrains-mono/wght.css';`
above the two `@font-face` blocks, so all three faces are declared in one place
and the package still supplies the subsetting. Verified in the built CSS: three
families, five `unicode-range` subsets shipped.

Unrelated find while testing this: `node_modules/` was stale — it still held
`@fontsource-variable/inter` from before the typeface change, so the build could
not have worked on this machine. `npm ci` fixed it. Worth knowing if a build
fails for no visible reason.

## A3 — The fallback stacks

They were long for a reason that does not apply here: long stacks are for sites
that might not load their webfonts at all. This site self-hosts all three with
`font-display: swap`, so the fallback is only ever visible for the few hundred
milliseconds before the file arrives, or if it 404s.

Cut to three names each — the real family, one sensible bridge, the generic:

```css
--font-sans: 'Satoshi Variable', system-ui, sans-serif;
--font-serif: 'Erode Variable', serif;
--font-mono: 'JetBrains Mono Variable', monospace;
```

The `Variable` suffix is the one part that cannot go: it is the family name the
files actually register, and dropping it silently falls through to a system
face.

## A4 — The Prettier plugin

Prettier formats JS, CSS, HTML, JSON and markdown out of the box. It does not
understand `.astro` files — the frontmatter fence, the template, the scoped
`<style>` block. `prettier-plugin-astro` teaches it that syntax.

Without it, `npm run format:check` would either skip `.astro` files or mangle
them, and `npm run verify` fails on formatting. The `overrides` block below it
is what routes `*.astro` to that plugin's parser. It is a devDependency; nothing
ships to the browser.

## A5 — cms.md vs content-schema.md

They answer different questions and merging them would make one long document
with two audiences:

- **content-schema.md** — what a field means, what is required, how to add one.
  Read when writing content or changing the schema.
- **cms.md** — how to run the editor, why `/admin` is not deployed, what is
  load-bearing in its setup. Read roughly once a year, when something breaks.

Still relevant, yes — the local-editing instructions are the only record of how
to edit without OAuth. But it was carrying about 4 kB of planning for an OAuth
relay that does not exist and is not planned, which is exactly the speculative
structure the repo rules forbid elsewhere. That is gone; one sentence records
that the option exists.

## A6 — design-to-code.md

Merged into [`behind-the-scenes/skills/figma-implement.md`](../behind-the-scenes/skills/figma-implement.md)
and deleted.

Not CLAUDE.md: that file loads in every session, including ones that never touch
Figma, and 13 kB of MCP detail there costs attention on every unrelated task.
Not a separate doc either: it and the skill described the same job in two files
that could disagree — and did, in two places. A skill is loaded exactly when the
work needs it, which is the right trigger.

`docs/design-system.md` stays a document, because it is yours: it records design
intent, not procedure.

## A7 — deployment.md

Deleted. Of its 700 bytes, one sentence was load-bearing (push to `main` →
`deploy.yml` → Pages) and now lives in the CLAUDE.md stack table. The rest was
generic advice — check the Actions tab, `curl` the URL, hard-refresh — which
neither you nor an agent needs written down.

## A8 — figma-implement review

What was weak for reproducibility: the rules were spread through the prose, so
two runs could legitimately read it differently; steps had no stated output, so
"done" was a judgement call; and it referenced a motion intent table in
`design-system.md` that does not exist.

Changed:

- A **Laws** table at the top, L1–L8, each with what a violation looks like. The
  laws hold for every step and can be cited in a report.
- Every step now states its **output** and whether it is a stop gate.
- The contract from `design-to-code.md` is inlined, so there is no second
  document to fall out of sync with.
- The new "no invented style" rule is L2, and the matching anti-pattern is
  listed.
- The dangling motion-table reference is gone; `design-system.md` now says
  plainly that motion intent is not defined in Figma yet.

## A9 — public/og

Not temporary. `default.png` is the social preview card — `SITE.defaultImage`
feeds it into the `og:image` and `twitter:image` of every page, so deleting it
means every shared link renders as a bare text box. Keep the folder.

One thing to know: the image does not use the site's typefaces or palette. It
is set in a system sans and serif, and the accent on _experiences_ is not a
palette colour. It is a placeholder that happens to look finished — worth
redrawing in Figma when you get to it.

## A10 — node_modules

The build tooling, downloaded from npm. It is not committed (`.gitignore`
excludes it) and `npm install` recreates it from `package-lock.json`, so nothing
in it is yours to maintain. Nothing in it ships to visitors except the JetBrains
Mono font files.

Twelve packages are declared in `package.json`; the ~239 folders are those
twelve plus everything they depend on.

| Package                               | What it does                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------- |
| `astro`                               | The framework. Builds `src/` into static HTML.                                  |
| `@astrojs/sitemap`                    | Generates `sitemap-index.xml` at build time.                                    |
| `@astrojs/check` + `typescript`       | `npm run check` — type-checks the `.astro` files.                               |
| `zod`                                 | The content schema validator. Turns a bad frontmatter field into a build error. |
| `@fontsource-variable/jetbrains-mono` | The mono typeface, self-hosted from npm. **The only one that ships.**           |
| `html-validate`                       | `npm run lint:html` — alt text, heading order, labels, against the built HTML.  |
| `prettier` + `prettier-plugin-astro`  | Formatting. See A4.                                                             |
| `playwright-core`                     | Drives Chromium to print the two PDFs. Never runs in CI.                        |
