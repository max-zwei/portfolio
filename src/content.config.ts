import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'zod';

/**
 * Project content schema.
 *
 * Every field here also lives in public/admin/config.yml (the CMS form) and
 * docs/content-schema.md (the explanation). Change one, change all three, or
 * the CMS will write frontmatter the build rejects.
 *
 * Deliberately small. Add a field when a design actually needs it — each one
 * costs three files to maintain, so speculative fields are expensive.
 */

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z
      .object({
        /** Project name. Used as the page <h1> and in listings. */
        title: z.string().min(1),

        /**
         * The "How might we ..." framing that opens the case study, written
         * without the prefix — the UI adds it.
         * e.g. hmw: "make reading practice feel like play?"
         */
        hmw: z.string().min(1),

        /** One or two sentences. Used on cards and as the meta description. */
        summary: z.string().min(1).max(280),

        /** Year the work was done, or started for ongoing work. */
        year: z.number().int().min(2015).max(2100),

        /** Free-form tags, e.g. ["UX Research", "EdTech"]. */
        tags: z.array(z.string().min(1)).default([]),

        /** Cover image, relative to the entry file. Optimised at build. */
        cover: image().optional(),

        /** Alt text for the cover. Required whenever a cover is set. */
        coverAlt: z.string().optional(),

        /** Link to the Figma file or frame the work was designed in. */
        figmaUrl: z.url().optional(),

        /** Link to the GitHub repository, where the project has one. */
        repoUrl: z.url().optional(),

        /**
         * Supporting images — sketches, flows, screens, photos of the thing.
         * Alt text is required on every one; there is no cover-style escape.
         */
        artefacts: z
          .array(
            z.object({
              src: image(),
              alt: z.string().min(1),
            }),
          )
          .default([]),
      })
      // A cover without alt text is an accessibility bug, so fail the build.
      .refine((data) => !data.cover || Boolean(data.coverAlt), {
        message: 'coverAlt is required when a cover image is set',
        path: ['coverAlt'],
      }),
});

export const collections = { projects };
