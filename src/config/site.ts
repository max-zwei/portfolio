/**
 * Site-wide constants. Anything that appears in more than one place —
 * or that you would otherwise be tempted to retype — belongs here.
 */

/**
 * Prefixes a path in public/ with the deploy base.
 *
 * GitHub Pages serves this as a project page, so everything sits under
 * /portfolio. Astro rewrites the URLs it generates itself, but not the ones
 * written by hand in a template — those come through here. When a custom
 * domain lands and `base` goes away, this quietly becomes a no-op.
 */
export const withBase = (path: string) =>
  `${import.meta.env.BASE_URL.replace(/\/$/, '')}${path}`;

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
  { label: 'Résumé', href: withBase('/resume') },
];

/**
 * The footer's own navigation, from the Figma NavBar. The href is the label
 * with its `#` stripped — the same mechanical transform the token names use.
 * None of these routes exists yet; Max supplies the real map.
 */
export const NAV = {
  impressum: { label: '#impressum', href: withBase('/impressum') },
  sections: [
    { label: '#projects', href: withBase('/projects') },
    { label: '#playground', href: withBase('/playground') },
    { label: '#curiosity', href: withBase('/curiosity') },
    { label: '#inspiration', href: withBase('/inspiration') },
  ],
  about: [
    { label: '#aboutme', href: withBase('/aboutme') },
    { label: '#behindthescenes', href: withBase('/behindthescenes') },
  ],
} as const;

/** Social marks the footer draws. Only the GitHub URL is known. */
export const SOCIALS = [
  {
    label: 'Figma',
    href: '#',
    icon: '/icons/figma.svg',
    width: 16,
    height: 16,
  },
  {
    label: 'GitHub',
    href: 'https://github.com/max-zwei',
    icon: '/icons/github.svg',
    width: 16,
    height: 16,
  },
  {
    label: 'Dribbble',
    href: '#',
    icon: '/icons/dribbble.svg',
    width: 16,
    height: 16,
  },
  {
    label: 'Behance',
    href: '#',
    icon: '/icons/behance.svg',
    width: 16,
    height: 16,
  },
  {
    label: 'LinkedIn',
    href: '#',
    icon: '/icons/linkedin.svg',
    width: 16,
    height: 16,
  },
] as const;

/** The three marks beside "explore with". Decorative: the design draws no link. */
export const EXPLORE_WITH = [
  {
    label: 'Claude',
    href: 'https://claude.ai/',
    icon: '/icons/explore-claude.svg',
  },
  {
    label: 'OpenAI',
    href: 'https://openai.com/',
    icon: '/icons/explore-openai.svg',
  },
  { label: '3', href: '#', icon: '/icons/explore-3.svg' },
] as const;
