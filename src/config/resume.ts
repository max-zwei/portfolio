/**
 * CV data — the single source of truth for /resume and for the PDF built from it.
 *
 * `npm run cv` renders the built /resume page to public/cv/max-pinkert-cv.pdf,
 * so a position is written down exactly once. Never edit the PDF by hand: it is
 * a build artefact of this file, and the two would silently drift apart.
 *
 * Everything below is placeholder. The square brackets are the tell — they are
 * meant to be impossible to miss in the rendered PDF, so an unfinished CV can't
 * be sent out by accident.
 */

export interface ResumeEntry {
  /** Work or study. Drives the label and the marker colour on the timeline. */
  kind: 'work' | 'education';
  /** Job title, or the degree for an education entry. */
  title: string;
  /** Employer, client or institution. */
  organisation: string;
  /** City, or "Remote". Leave it out when it adds nothing. */
  location?: string;
  /** Start, as `YYYY-MM`. The timeline sorts on this, so keep the format. */
  start: string;
  /** End, as `YYYY-MM`. Leave it out for anything still running. */
  end?: string;
  /** One or two sentences: what the work was, and what came of it. */
  summary: string;
}

export const RESUME: {
  /** The one part of the CV that isn't on the timeline. Written, not derived. */
  intro: string;
  timeline: ResumeEntry[];
} = {
  intro:
    '[Two or three sentences in your own voice: what you design, who for, and ' +
    'where you are heading. This is the only prose on the CV that the timeline ' +
    'below cannot tell — replace it before sending the PDF anywhere.]',

  // Newest first, matching how the page renders it.
  timeline: [
    {
      kind: 'work',
      title: '[Current role]',
      organisation: '[Organisation]',
      location: '[City]',
      start: '2025-03',
      summary:
        '[What you are responsible for, and what has changed because of it. ' +
        'Two sentences at most — the case studies carry the detail.]',
    },
    {
      kind: 'education',
      title: '[Degree or programme]',
      organisation: '[Institution]',
      location: '[City]',
      start: '2023-09',
      summary:
        '[Focus of the study, and anything worth knowing about it: thesis ' +
        'topic, specialisation, a project that mattered.]',
    },
    {
      kind: 'work',
      title: '[Previous role]',
      organisation: '[Organisation]',
      location: '[City]',
      start: '2022-01',
      end: '2023-08',
      summary: '[What the work was, and what came of it.]',
    },
    {
      kind: 'education',
      title: '[Earlier qualification]',
      organisation: '[Institution]',
      start: '2019-09',
      end: '2021-12',
      summary: '[One line. Older entries earn less space, not none.]',
    },
  ],
};
