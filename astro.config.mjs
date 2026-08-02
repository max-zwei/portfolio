// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// `site` drives canonical URLs, OG tags and the sitemap — update it when the
// custom domain is attached (see docs/deployment.md).
// GitHub Pages serves this repo from the root of the domain, so `base` stays '/'.
export default defineConfig({
  site: 'https://max-zwei.github.io',
  base: '/',
  output: 'static',
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
  integrations: [
    sitemap({
      // The CMS admin shell is not content.
      filter: (page) => !page.includes('/admin'),
    }),
  ],
});
