# Decap CMS

The CMS lives at `/admin` and is configured in
[`public/admin/config.yml`](../public/admin/config.yml). It edits the markdown in
`src/content/projects/` and commits straight back to this repo — there is no
database and no separate content API.

`publish_mode: editorial_workflow` is on, so saving a project opens a **draft pull
request** rather than committing to `main`. Nothing goes live until that PR is
merged, at which point the deploy workflow rebuilds the site.

## Editing locally (no setup needed)

```bash
npx decap-server      # terminal 1 — proxy that writes to your local files
npm run dev           # terminal 2
```

Then open <http://localhost:4321/admin/>. `local_backend: true` makes the CMS talk
to the proxy instead of GitHub, so there is no login step and no OAuth. Changes
land in your working tree as ordinary file edits for you to commit.

This is the fastest path and the one to use while the schema is still moving.

## The CMS is not deployed

**Decision: `/admin` works locally only, and is stripped from the production
build.** This is a choice, not a gap.

`astro.config.mjs` carries a small `astro:build:done` integration that deletes
`dist/admin` after every build. Two reasons:

1. It couldn't log in anyway (see below), so a deployed copy is dead weight.
2. It loads a ~5 MB third-party script from unpkg. Publishing that on the live
   domain in exchange for a page nobody can use is a bad trade.

`npm run dev` still serves it, so local editing is unaffected. Delete the
integration if an OAuth relay is ever added.

**Why it's an Astro route and not a file in `public/`:** Astro's dev server
serves `public/` by exact path and does not resolve directory indexes, so
`public/admin/index.html` was only ever reachable at `/admin/index.html` —
never at `/admin`. As a route it works at both. The `is:inline` on the script
tag is load-bearing: without it Astro bundles the script and drops the
`integrity` and `crossorigin` attributes, silently undoing the SRI pinning.

### Pinning and integrity

`src/pages/admin/index.astro` loads Decap from unpkg at an **exact** version with an
SRI `integrity` hash — not a `^range`. A range means the browser runs whatever
the CDN resolves it to, and makes SRI impossible.

Bumping the version means recomputing the hash:

```bash
npm pack decap-cms@<version> && tar -xzf decap-cms-<version>.tgz
openssl dgst -sha384 -binary package/dist/decap-cms.js | openssl base64 -A
```

(unpkg serves the npm tarball byte-for-byte, so this is the same file.)

One honest caveat: Decap is code-split into ~93 lazy-loaded chunks, and SRI only
covers the entry file. Those chunks aren't integrity-checked. **Not deploying
this page is what actually contains that risk** — the pinning protects the local
editing session, where you're the only one loading it.

Everything the CMS does, it does through the local backend above. Wiring up the
live site would buy exactly one thing: writing case studies from a machine that
isn't Max's. That isn't worth a permanently deployed service and a rotating
secret today. Revisit it if and when writing from a phone or a borrowed laptop
actually comes up.

The rest of this section is the map for that day. Nothing below is required now.

### Why the live site can't just work

Decap authenticates you against GitHub so the commits it makes are genuinely
yours. GitHub hands back a temporary code that has to be exchanged for a token,
and that exchange needs a client secret — which cannot live in the browser
without being handed to everyone who views the page. So the exchange needs a
server, and **GitHub Pages serves static files only**. One small piece has to
live somewhere else.

Note this is only ever about _Max logging in to write_. The portfolio itself is
fully static and public; no visitor authenticates against anything.

### Option A — a hosted OAuth relay

Deploy one of the ready-made Decap OAuth clients (Netlify Function, Vercel
serverless function, Cloudflare Worker — all are a few lines and free at this
scale), then:

1. GitHub → **Settings → Developer settings → OAuth Apps → New OAuth App**
   - Homepage URL: your site's URL
   - Authorization callback URL: `https://<your-relay>/callback`
2. Put the client ID and secret in the relay's environment. **Never commit the
   secret** — it is not a build-time value and does not belong in this repo.
3. Uncomment `base_url` and `auth_endpoint` in `config.yml` and point `base_url`
   at the relay.

### Option B — move to a host with built-in auth

Netlify ships the OAuth endpoint itself (Decap started life as Netlify CMS), so
there is no relay, no OAuth app and no secret to rotate — connect the repo and
it works. It is the least machinery by some distance. The cost is that it drops
GitHub Pages and [`docs/deployment.md`](./deployment.md) stops applying. The
Astro build itself is host-agnostic, so the move is mostly deleting a workflow.

If browser editing ever becomes the priority, start here rather than with
Option A.

### What happens meanwhile

`/admin` returns a 404 on the live site, because it isn't deployed at all. That
is expected — see "The CMS is not deployed" above. Local editing is unaffected.

## Keeping the CMS and the schema in step

`config.yml` and `src/content.config.ts` describe the same fields, and nothing
enforces that automatically. When they drift, the CMS saves happily and the build
fails afterwards — the error surfaces in Actions, not in the CMS.

Field reference and the change checklist: [`docs/content-schema.md`](./content-schema.md).

## Media

Cover images upload to `src/content/projects/_media/` and are referenced as
`./_media/<name>`, which keeps them inside `src/` where Astro can optimise and
hash them. Images in `public/` are served as-is with no optimisation, which is why
they don't go there.
