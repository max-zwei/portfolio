// @ts-check
import { rm } from 'node:fs/promises';
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

/**
 * Keeps the CMS shell out of the production build.
 *
 * `/admin` cannot log in on the live site — GitHub Pages has no server to run
 * Decap's OAuth exchange (see docs/cms.md). Publishing it anyway would put a
 * 5 MB third-party script from unpkg on the public domain in exchange for
 * nothing. Editing happens locally, where `npm run dev` serves public/ as-is,
 * so this costs the actual workflow nothing.
 *
 * Delete this integration if an OAuth relay is ever added.
 */
const excludeAdminFromBuild = {
  name: 'exclude-admin-from-build',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      await rm(new URL('admin/', dir), { recursive: true, force: true });
    },
  },
};

// `site` drives canonical URLs, OG tags and the sitemap — update it when the
// custom domain is attached (see docs/deployment.md).
export default defineConfig({
  site: 'https://max-zwei.github.io',
  output: 'static',
  integrations: [
    // Tools, not content. /admin isn't even deployed (see below); the
    // styleguide is, but shouldn't compete in search.
    sitemap({ filter: (page) => !/\/(admin|styleguide)/.test(page) }),
    excludeAdminFromBuild,
  ],
});
