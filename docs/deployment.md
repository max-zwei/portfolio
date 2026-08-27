# Deployment

The site is a static build served by GitHub Pages. Every push to `main` triggers
[`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml), which
type-checks, builds, and publishes `dist/`. Pull requests run
[`ci.yml`](../.github/workflows/ci.yml), which does everything except publish.

```
push to main → npm ci → astro check → astro build → upload artifact → deploy-pages
```

## Verifying a deploy

- **Actions tab** → the run's `deploy` job prints the live URL.
- `curl -sI https://<domain> | head -1` → expect `HTTP/2 200`.
- `curl -s https://<domain>/sitemap-index.xml` → expect XML, not a 404.
- Hard-refresh once; Pages caches aggressively at the edge.
