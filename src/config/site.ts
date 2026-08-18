/**
 * Site-wide constants. Anything that appears in more than one place —
 * or that you would otherwise be tempted to retype — belongs here.
 */
export const SITE = {
  name: 'Max Pinkert',
  role: 'UX & Product Design',
  slogan: "I care about experiences. And I'm curious to find them.",
  description:
    'Portfolio of Max Pinkert — UX and product designer working towards children and education technology.',
  lang: 'en',
  defaultImage: '/og/default.png',
  email: 'max.pinkert@code.berlin',
} as const;

/**
 * The paragraph at the top of the CV. The one piece of prose on /resume the
 * timeline can't tell you, so it is written by hand rather than derived — and
 * it stays here rather than in the resume collection because it is bio copy,
 * not a position.
 *
 * The square brackets are the tell: an unfinished CV should be impossible to
 * miss in the printed PDF, not subtle.
 */
export const CV_INTRO =
  '[Two or three sentences in your own voice: what you design, who for, and ' +
  'where you are heading. This is the only prose on the CV that the timeline ' +
  'below cannot tell — replace it before sending the PDF anywhere.]';

/** Social / professional links. Add entries as the profiles go live. */
export const LINKS: ReadonlyArray<{ label: string; href: string }> = [
  { label: 'Email', href: `mailto:${SITE.email}` },
  { label: 'GitHub', href: 'https://github.com/max-zwei' },
  { label: 'Résumé', href: '/resume' },
];
