import { defineCollection, reference } from 'astro:content';
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

/** `YYYY` or `YYYY-MM`. Sorted as a string, so the zero padding is load-bearing. */
const yearMonth = z
  .string()
  .regex(/^\d{4}(?:-(0[1-9]|1[0-2]))?$/, 'Use YYYY or YYYY-MM, e.g. 2025-03');

/** Markdown held in frontmatter needs a build-time markdown pass. */
const caseSection = z
  .object({
    summary: z.string().min(1),
    keyPoints: z.array(z.string().min(1)).default([]),
  })
  .optional();

/** Decap writes an empty string when an optional scalar field is cleared. */
const optionalProjectField = <T extends z.ZodType>(schema: T) =>
  z.preprocess(
    (value) => (value === '' ? undefined : value),
    schema.optional(),
  );

const projectColor = optionalProjectField(
  z
    .string()
    .regex(/^#[0-9a-fA-F]{6}$/, 'Use a six-digit hex color, e.g. #AABBCC'),
);

const projectImageSlots = [
  'img_0.8h',
  'img_0.6h_l',
  'img_0.6h_s',
  'img_1_2_l',
  'img_1_2_s',
  'img_1_1',
  'img_1_2',
] as const;

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

        color1: projectColor,
        color2: projectColor,
        color3: projectColor,
        color4: projectColor,
        color5: projectColor,
        color6: projectColor,
        color7: projectColor,
        color8: projectColor,

        /** Literal top-level keys; image paths are relative to the entry. */
        'img_0.8h': optionalProjectField(image()),
        'img_0.8h_alt': z.string().optional(),
        'img_0.6h_l': optionalProjectField(image()),
        'img_0.6h_l_alt': z.string().optional(),
        'img_0.6h_s': optionalProjectField(image()),
        'img_0.6h_s_alt': z.string().optional(),
        img_1_2_l: optionalProjectField(image()),
        img_1_2_l_alt: z.string().optional(),
        img_1_2_s: optionalProjectField(image()),
        img_1_2_s_alt: z.string().optional(),
        img_1_1: optionalProjectField(image()),
        img_1_1_alt: z.string().optional(),
        img_1_2: optionalProjectField(image()),
        img_1_2_alt: z.string().optional(),

        /** Link to the Figma file or frame the work was designed in. */
        figmaUrl: z.url().optional(),

        /** Link to the GitHub repository, where the project has one. */
        repoUrl: z.url().optional(),

        context: optionalProjectField(z.string().min(1)),
        hmw: optionalProjectField(z.string().min(1)),

        /** Sections are optional, but each included section needs a summary. */
        exploration: caseSection,
        definition: caseSection,
        development: caseSection,
        feedback: caseSection,
        learning: caseSection,
        behindTheScenes: caseSection,
        match,
      })
      .superRefine((data, ctx) => {
        for (const slot of projectImageSlots) {
          const alt = `${slot}_alt` as const;
          if (data[slot] && !data[alt]?.trim()) {
            ctx.addIssue({
              code: 'custom',
              message: `${alt} is required when ${slot} is set`,
              path: [alt],
            });
          }
        }
      }),
});

/** Small self-directed builds. Shown as a grid of cards that link out. */
const playground = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/playground' }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string().min(1),

        /** One or two sentences — this is the whole description. */
        summary: z.string().min(1).max(400),

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

        /** Employer, client or institution. Omit to leave the entry unaffiliated — the page shows no company line. */
        company: z.string().optional(),

        /**
         * Work or study. Drives the "Position"/"Education" label the CV needs
         * to tell the two apart. Not a constraint on how /resume looks.
         */
        kind: z.enum(['work', 'education']),

        /** The timeline sorts on this, so keep the format. */
        start: yearMonth,

        /** Leave it out for anything still running — it renders as "present". */
        end: yearMonth.optional(),

        /** One or two sentences: what the work was, and what came of it. Omit to show no summary. */
        summary: z.string().optional(),

        /** Company or institution mark. */
        logo: image().optional(),
        logoAlt: z.string().optional(),

        /** Up to three portfolio projects connected to this entry. */
        projects: z.array(reference('projects')).max(3).default([]),

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
  schema: z.object({
    date: z.coerce.date(),
    /** The line under the date — one sentence on what this release was. */
    description: z.string().min(1).optional(),

    /* The three things a release can touch. Markdown, and all optional —
       a release rarely moves all three at once. */
    userExperience: z.string().min(1).optional(),
    userInterface: z.string().min(1).optional(),
    tech: z.string().min(1).optional(),

    /**
     * An optional attachment. A path under /releases, or an absolute
     * http(s) URL — not an `image()`, since this is served or linked as-is
     * rather than run through Astro's optimiser.
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
