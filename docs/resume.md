# Printed documents

Two pages are also downloadable PDFs. Neither PDF is a second document — each is
its page printed to A4 by the same `@media print` rules that style it on screen,
so nothing is written down twice and the two cannot disagree.

| Document  | URL          | Source                                                     | PDF                                    |
| --------- | ------------ | ---------------------------------------------------------- | -------------------------------------- |
| CV        | `/resume`    | `src/content/resume/` + `CV_INTRO` in `src/config/site.ts` | `/cv/max-pinkert-cv.pdf`               |
| Handshake | `/handshake` | `src/pages/handshake.md`                                   | `/handshake/max-pinkert-handshake.pdf` |

Both are produced by one command, `npm run pdf`. The rest of this file is about
the CV, which is the one with moving parts; the handshake is a single markdown
file and needs nothing explained.

## Editing it

Positions and qualifications are a **content collection**, one markdown file per
entry in `src/content/resume/`, editable in the CMS under **Résumé**. Fields are
documented in [`docs/content-schema.md`](./content-schema.md).

The **opening paragraph** is the exception. It is bio copy rather than a position,
so it stays in code as `CV_INTRO` in [`src/config/site.ts`](../src/config/site.ts).

Everything ships as `[bracketed placeholders]`. That is deliberate — an unfinished
CV should be obvious in the PDF, not subtle.

## Regenerating the PDF

```bash
npm run pdf    # builds the site, then prints both PDFs into public/
```

Both PDFs are committed, because GitHub Pages serves `public/` as-is and a build
can't produce a file that the same build needs to deploy. Re-run `npm run pdf`
whenever a résumé entry or the handshake changes, and commit the result.

Always run `npm run pdf` before merging.

[`scripts/render-pdf.mjs`](../scripts/render-pdf.mjs) serves `dist/` on a random
port and prints `/resume` and `/handshake` with Chromium via `playwright-core`. It needs a browser
to print with:

```bash
npx playwright install chromium     # once
CHROME_PATH=/path/to/chrome npm run pdf   # or point it at a Chrome you already have
```

`playwright-core` is a devDependency and is never shipped — CI doesn't run this
script, it only builds the site the PDFs were already made from.

The handshake's print rules live in `src/layouts/ProseLayout.astro`, so any
markdown page using that layout prints the same way.

## Changing how it looks

Screen and print styles both live in `src/pages/resume.astro`. Two things to know
before touching them:

- **`@page` can't read custom properties.** The sheet size and margins are
  literal `mm` values, and that is the one place in this repo where a raw value is
  correct. Everything else in the print block uses tokens like the rest of the
  site.
- **`printBackground: true` is on**, so the timeline dots survive the print. They
  also carry `print-color-adjust: exact`, and the "Position"/"Education" label
  means the colour never carries the meaning on its own.
