import { defineCollection, reference, type SchemaContext } from 'astro:content';
import { glob } from 'astro/loaders';
import { existsSync, readdirSync } from 'node:fs';
import { z } from 'zod';
import { tagIds } from './config/match';

/**
 * Content schemas.
 *
 * Every field here also lives in public/admin/config.yml (the CMS form) and
 * docs/cms.md (the explanation). Change one, change all three, or the CMS
 * will write frontmatter the build rejects.
 *
 * Deliberately small. Add a field when a design actually needs it — each one
 * costs three files to maintain, so speculative fields are expensive.
 */

/** The `image()` helper Astro hands to each schema. Named so helpers can take it. */
type ImageFn = SchemaContext['image'];

/** `YYYY` or `YYYY-MM`. Sorted as a string, so the zero padding is load-bearing. */
const yearMonth = z
  .string()
  .regex(/^\d{4}(?:-(0[1-9]|1[0-2]))?$/, 'Use YYYY or YYYY-MM, e.g. 2025-03');

/**
 * Supporting images — sketches, flows, screens, photos of the thing.
 * Alt text is required on every one; there is no optional-image escape here.
 */
const artefacts = (image: ImageFn) =>
  z
    .array(
      z.object({
        src: image(),
        alt: z.string().min(1),
      }),
    )
    .default([]);

/**
 * One movement of a case study. The eight below are the same shape — what
 * differs between them is the narrative position, not the fields, so the
 * shape is written once.
 *
 * `description` is markdown held in frontmatter. Astro's `render()` only
 * renders an entry's body, so this needs a build-time markdown pass whenever
 * the case-study page gets built. See docs/cms.md.
 */
const caseSection = (image: ImageFn) =>
  z
    .object({
      /** Sits next to the section heading. */
      subtitle: z.string().min(1).optional(),

      /** The section itself, as markdown. */
      description: z.string().min(1),

      artefacts: artefacts(image),

      /** The section in bullets — what a reader in a hurry should take away. */
      keyPoints: z.array(z.string().min(1)).default([]),
    })
    .optional();

/**
 * What the /home questionnaire matches an entry on. Every option comes from
 * src/config/match.ts, so a chip and a tag can never drift apart.
 *
 * `.prefault({})` lets an untagged entry omit the object entirely and still
 * parse to four empty arrays, which is what the matcher expects.
 */
const match = z
  .object({
    teams: z.array(z.enum(tagIds('team'))).default([]),
    fields: z.array(z.enum(tagIds('field'))).default([]),
    roles: z.array(z.enum(tagIds('role'))).default([]),
    tech: z.array(z.enum(tagIds('tech'))).default([]),
  })
  .prefault({});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z
      .object({
        /** Project name. Used as the page <h1> and in listings. */
        title: z.string().min(1),

        /** One or two sentences. Used on cards and as the meta description. */
        summary: z.string().min(1).max(280),

        /** Who the work was for. */
        company: z.string().min(1),

        /** Year the work was done, or started for ongoing work. */
        year: z.number().int().min(2015).max(2100),

        /** Free-form tags, e.g. ["UX Research", "EdTech"]. */
        tags: z.array(z.string().min(1)).default([]),

        /** Portrait teaser, for tall cards. Relative to the entry file. */
        teaserVertical: image().optional(),
        teaserVerticalAlt: z.string().optional(),

        /** Landscape teaser, for wide cards. Relative to the entry file. */
        teaserHorizontal: image().optional(),
        teaserHorizontalAlt: z.string().optional(),

        /** Link to the Figma file or frame the work was designed in. */
        figmaUrl: z.url().optional(),

        /** Link to the GitHub repository, where the project has one. */
        repoUrl: z.url().optional(),

        /* The case study, in narrative order. Every section is optional —
           not every project earns all eight — but a section that exists has
           something to say, so `description` is required inside it. */
        context: caseSection(image),
        hmw: caseSection(image),
        exploration: caseSection(image),
        definition: caseSection(image),
        development: caseSection(image),
        feedback: caseSection(image),
        learning: caseSection(image),
        behindTheScenes: caseSection(image),
        match,
      })
      // An image without alt text is an accessibility bug, so fail the build.
      .refine(
        (data) => !data.teaserVertical || Boolean(data.teaserVerticalAlt),
        {
          message: 'teaserVerticalAlt is required when teaserVertical is set',
          path: ['teaserVerticalAlt'],
        },
      )
      .refine(
        (data) => !data.teaserHorizontal || Boolean(data.teaserHorizontalAlt),
        {
          message:
            'teaserHorizontalAlt is required when teaserHorizontal is set',
          path: ['teaserHorizontalAlt'],
        },
      ),
});

/** Small self-directed builds. Shown as a grid of cards that link out. */
const playground = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/playground' }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string().min(1),

        /** One or two sentences — this is the whole description. */
        summary: z.string().min(1).max(280),

        teaser: image().optional(),
        teaserAlt: z.string().optional(),

        githubUrl: z.url().optional(),
        figmaUrl: z.url().optional(),

        /** Anything that isn't GitHub or Figma — a demo, a write-up, a video. */
        additionalUrl: z.url().optional(),

        match,
      })
      .refine((data) => !data.teaser || Boolean(data.teaserAlt), {
        message: 'teaserAlt is required when teaser is set',
        path: ['teaserAlt'],
      }),
});

/** Other people's work worth pointing at. Every entry links somewhere. */
const inspiration = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/inspiration' }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string().min(1),

        /** Where it lives. The point of the entry, so it isn't optional. */
        url: z.url(),

        /** Why it's here — what Max took from it. */
        summary: z.string().min(1).max(280),

        teaser: image().optional(),
        teaserAlt: z.string().optional(),

        match,
      })
      .refine((data) => !data.teaser || Boolean(data.teaserAlt), {
        message: 'teaserAlt is required when teaser is set',
        path: ['teaserAlt'],
      }),
});

/**
 * The question filenames, read fresh on every parse.
 *
 * `reference()` on its own does not fail a build on a dangling id — it
 * resolves to `undefined` and warns only on the page that renders it, which
 * for an unrendered collection is never. This makes the dangling id a schema
 * error instead, which is the whole reason the reference exists.
 */
const questionIds = () =>
  readdirSync('./src/content/questions')
    .filter((file) => file.endsWith('.md'))
    .map((file) => file.slice(0, -'.md'.length));

/**
 * The open questions thoughts hang off. One field, because a question is its
 * text — the *filename* is the identity, and that is the point: rewording a
 * question leaves every thought still pointing at it.
 */
const questions = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/questions' }),
  schema: z.object({
    /** The question itself. Keep it a question. */
    question: z.string().min(1),
  }),
});

/** A thought and the question it leaves open. Both halves, always. */
const curiosity = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/curiosity' }),
  schema: z.object({
    /** The observation. */
    thought: z.string().min(1),

    /* Exactly one question, by filename. A reference rather than free text so
       the build fails on a typo instead of silently splitting a question in
       two — which is what makes grouping thoughts by question possible. */
    question: reference('questions').refine(
      (ref) => questionIds().includes(ref.id),
      {
        error: (issue) =>
          `No question named "${(issue.input as { id: string }).id}". Add it under src/content/questions/, or point at one that exists.`,
      },
    ),

    match,
  }),
});

/**
 * The CV, one entry per position or qualification.
 *
 * This is the single source for /resume and for the PDF printed from it, so
 * editing here and re-running `npm run pdf` is the whole workflow. See
 * docs/resume.md.
 */
const resume = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/resume' }),
  schema: ({ image }) =>
    z
      .object({
        /** Job title, or the degree for an education entry. */
        role: z.string().min(1),

        /** Employer, client or institution. */
        company: z.string().min(1),

        /**
         * Work or study. Drives the "Position"/"Education" label the CV needs
         * to tell the two apart. Not a constraint on how /resume looks.
         */
        kind: z.enum(['work', 'education']),

        /** The timeline sorts on this, so keep the format. */
        start: yearMonth,

        /** Leave it out for anything still running — it renders as "present". */
        end: yearMonth.optional(),

        /** One or two sentences: what the work was, and what came of it. */
        summary: z.string().min(1),

        /** Company or institution mark. */
        logo: image().optional(),
        logoAlt: z.string().optional(),

        /** Up to three things to point at. Ordered — the first one leads. */
        projectUrls: z.array(z.url()).max(3).default([]),

        /**
         * The one scan behind this entry — an Arbeitszeugnis under /letters, or
         * a qualification under /certificates. A path into public/ rather than
         * an image(): it is served as-is for reading, not optimised, exactly
         * like `file` on releaseNotes. The folder carries the meaning, so there
         * is no separate label field to keep in step with it.
         */
        documentUrl: z
          .string()
          .regex(
            /^\/(letters|certificates)\/[a-z0-9._-]+\.pdf$/,
            'Use /letters/name.pdf or /certificates/name.pdf',
          )
          .optional(),

        match,
      })
      .refine((data) => !data.logo || Boolean(data.logoAlt), {
        message: 'logoAlt is required when logo is set',
        path: ['logoAlt'],
      })
      .refine(
        (data) =>
          !data.documentUrl || existsSync(`./public${data.documentUrl}`),
        {
          message: 'No such file under public/ — check the filename',
          path: ['documentUrl'],
        },
      ),
});

/** What changed on the site, and when. */
const releaseNotes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/release-notes' }),
  schema: ({ image }) =>
    z.object({
      date: z.coerce.date(),

      /* The three things a release can touch. Markdown, and all optional —
         a release rarely moves all three at once. */
      userExperience: z.string().min(1).optional(),
      userInterface: z.string().min(1).optional(),
      tech: z.string().min(1).optional(),

      screenshots: artefacts(image),

      /**
       * An optional attachment. A path under /releases, not an `image()` —
       * this is served as-is for download rather than optimised.
       */
      file: z.string().min(1).optional(),
    }),
});

export const collections = {
  projects,
  playground,
  inspiration,
  questions,
  curiosity,
  resume,
  releaseNotes,
};
