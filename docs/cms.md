# Decap CMS

The CMS is the editing surface for `src/content/`. It writes markdown straight
back into the repo — no database, no content API. What the fields mean is
[`docs/content-schema.md`](./content-schema.md); this file is only about running
the thing.

Configured in [`public/admin/config.yml`](../public/admin/config.yml), served by
[`src/pages/admin/index.astro`](../src/pages/admin/index.astro). Six collections:
Projects, Playground, Inspiration, Curiosity, Résumé, Release notes.

## Editing

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

## Two things the CMS cannot enforce

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

**Saving a résumé entry stales the committed PDF.**
`public/cv/max-pinkert-cv.pdf` is printed from `/resume`. Re-run `npm run pdf`
and commit the result — nothing checks this for you. See
[`docs/resume.md`](./resume.md).
