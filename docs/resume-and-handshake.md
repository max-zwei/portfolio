# CV and handshake

Two documents the site hosts alongside the portfolio itself. They are not case
studies, so neither goes through the content collection or the CMS — each is one
file you edit directly.

| Document  | URL          | Source                                                | Also                     |
| --------- | ------------ | ----------------------------------------------------- | ------------------------ |
| CV        | `/resume`    | [`src/config/resume.ts`](../src/config/resume.ts)     | `/cv/max-pinkert-cv.pdf` |
| Handshake | `/handshake` | [`src/pages/handshake.md`](../src/pages/handshake.md) | —                        |

## The CV

`/resume` is the CV. The PDF is not a second document — it is that page, printed
to A4 by the same `@media print` rules that style it on screen. So a position is
written down exactly once, in `src/config/resume.ts`, and the two can't disagree.

### Editing it

Everything lives in `src/config/resume.ts`:

- **`intro`** — the paragraph at the top. The only prose on the CV the timeline
  can't tell you, so it's written by hand rather than derived.
- **`timeline`** — one array of positions _and_ qualifications. `kind` is
  `'work'` or `'education'`; the page sorts newest first on `start`, so the order
  in the file is a convenience, not the contract.

Dates are `YYYY-MM` strings. Leave `end` out for anything still running and the
entry renders as "present".

The file ships full of `[bracketed placeholders]`. That is deliberate — an
unfinished CV should be obvious in the PDF, not subtle.

### Regenerating the PDF

```bash
npm run cv     # builds the site, then prints /resume to public/cv/
```

The PDF is committed, because GitHub Pages serves `public/` as-is and a build
can't produce a file that the same build needs to deploy. **Re-run `npm run cv`
whenever `resume.ts` changes, and commit the result** — nothing checks this for
you, and a stale PDF is worse than no PDF.

[`scripts/render-cv.mjs`](../scripts/render-cv.mjs) serves `dist/` on a random
port and prints `/resume` with Chromium via `playwright-core`. It needs a browser
to print with:

```bash
npx playwright install chromium     # once
CHROME_PATH=/path/to/chrome npm run cv   # or point it at a Chrome you already have
```

`playwright-core` is a devDependency and is never shipped — CI doesn't run this
script, it only builds the site the PDF was already made from.

### Changing how it looks

Screen and print styles both live in `src/pages/resume.astro`. Two things to know
before touching them:

- **`@page` can't read custom properties.** The sheet size and margins are
  literal `mm` values, and that is the one place in this repo where a raw value is
  correct. Everything else in the print block uses tokens like the rest of the
  site.
- **`printBackground: true` is on**, so the timeline dots survive the print. They
  also carry `print-color-adjust: exact`, and the "Position"/"Education" label
  means the colour never carries the meaning on its own.

## The handshake

`/handshake` is the agreement used on pro bono projects: what's in scope, what
each side commits to, what happens to the work afterwards. It is a full markdown
page — frontmatter for the title and standfirst, `##` headings down from there —
rendered by [`ProseLayout.astro`](../src/layouts/ProseLayout.astro).

It isn't linked from anywhere on the site, on purpose. It's a URL to send to a
specific client, not a thing to browse to. The blanks stay as `[Client name]`
placeholders in the repo; fill them in per project wherever the conversation
happens, or print the page and fill them in there.

Section headings read `Section 1 — Project` rather than `1. Project` for two
reasons: the document refers to its own sections by number, and heading IDs
generated from a leading digit fail `npm run lint:html`.

`ProseLayout` is a plain markdown-page layout — anything else that is a document
rather than a case study can use it.
