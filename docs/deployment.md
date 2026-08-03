# Deployment

The site is a static build served by GitHub Pages. Every push to `main` triggers
[`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml), which
type-checks, builds, and publishes `dist/`. Pull requests run
[`ci.yml`](../.github/workflows/ci.yml), which does everything except publish.

```
push to main → npm ci → astro check → astro build → upload artifact → deploy-pages
```

## One-time setup in the GitHub UI

The workflow uses the Pages _deployment API_, not the legacy `gh-pages` branch.
That needs one setting flipped by hand — the workflow cannot do it for you:

1. **Settings → Pages → Build and deployment → Source: GitHub Actions.**

Until that is set, the deploy job fails with
`Error: Get Pages site failed`. That failure means exactly this step is missing;
nothing in the code needs changing.

## Custom domain

1. At your DNS provider, point the domain at GitHub Pages:
   - **Apex domain** (`example.com`) — four `A` records:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     (and the matching `AAAA` records if you want IPv6).
   - **Subdomain** (`www.example.com`) — one `CNAME` record pointing to
     `max-zwei.github.io`.
2. **Settings → Pages → Custom domain** — enter the domain and save. GitHub
   writes a `CNAME` file to the deployed site.
3. Because this repo deploys from an artifact rather than a branch, also commit
   the domain to **`public/CNAME`** (a single line, no protocol, no trailing
   slash) — otherwise the next deploy overwrites GitHub's copy and the domain
   detaches:
   ```
   maxpinkert.com
   ```
4. Wait for the DNS check to pass, then tick **Enforce HTTPS**. The certificate
   is issued by Let's Encrypt and can take up to an hour on first setup.
5. Update `site` in [`astro.config.mjs`](../astro.config.mjs) and the `Sitemap:`
   line in [`public/robots.txt`](../public/robots.txt) to the new domain.
   Canonical URLs, OG tags, and the sitemap all derive from `site`, so this step
   is not cosmetic.

## Verifying a deploy

- **Actions tab** → the run's `deploy` job prints the live URL.
- `curl -sI https://<domain> | head -1` → expect `HTTP/2 200`.
- `curl -s https://<domain>/sitemap-index.xml` → expect XML, not a 404.
- Hard-refresh once; Pages caches aggressively at the edge.

## Rollback

Re-run an older successful deploy from the Actions tab (**Re-run all jobs** on
that run), or revert the offending commit on `main` and let the workflow deploy
the revert. There is no separate deploy branch to untangle.
