import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
// Import zod directly — the `z` re-export from `astro:content` is deprecated.
import { z } from 'zod';

/**
 * Project content schema.
 *
 * This schema is the contract between three places:
 *   1. the markdown files in src/content/projects/
 *   2. the Decap CMS form in public/admin/config.yml
 *   3. the components that render a project
 *
 * If you change a field here, change it in config.yml too — otherwise the CMS
 * will happily write entries the build then rejects. Full field documentation
 * lives in docs/content-schema.md.
 */

export const PROJECT_STATUSES = ['in-progress', 'completed'] as const;

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      /** Project name as it appears in listings and as the page <h1>. */
      title: z.string().min(1),

      /** Where the work stands. Drives the status pill colour. */
      status: z.enum(PROJECT_STATUSES),

      /**
       * The "How might we ..." framing that opens the case study.
       * Written without the "How might we" prefix — the UI adds it.
       * e.g. hmw: "make reading practice feel like play?"
       */
      hmw: z.string().min(1),

      /** One- or two-sentence summary used on cards and in meta tags. */
      summary: z.string().min(1).max(280),

      /** Year the work was done (or started, for ongoing work). */
      year: z.number().int().min(2015).max(2100),

      /** Free-form tags, e.g. ["UX Research", "EdTech", "Mobile"]. */
      tags: z.array(z.string().min(1)).default([]),

      /** Cover image, relative to the entry file. Optimised by Astro at build. */
      cover: image().optional(),

      /** Alt text for the cover. Required whenever a cover is set. */
      coverAlt: z.string().optional(),

      /** Your part in it, e.g. "UX Design, User Research". */
      role: z.string().optional(),

      /** Client, course, or context the work happened in. */
      context: z.string().optional(),

      /** How long it ran, e.g. "6 weeks". */
      duration: z.string().optional(),

      /** Lower numbers sort first on the index. Ties fall back to year. */
      order: z.number().int().default(0),

      /** Featured projects can be surfaced on the homepage. */
      featured: z.boolean().default(false),

      /** Hidden from all listings and from the sitemap, but still builds. */
      draft: z.boolean().default(false),

      /** Optional external link (live product, repo, prototype). */
      link: z.url().optional(),
    })
      // A cover without alt text is an accessibility bug, so fail the build.
      .refine((data) => !data.cover || Boolean(data.coverAlt), {
        message: 'coverAlt is required when a cover image is set',
        path: ['coverAlt'],
      }),
});

export const collections = { projects };
