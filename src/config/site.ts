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

export const PORTFOLIO_SOURCE = {
  repository: 'https://github.com/max-zwei/portfolio',
  figma: 'https://www.figma.com/design/8SQOIPl0teOTvoFH1EffaB/Portfolio',
} as const;

/**
 * The paragraph at the top of the CV. The one piece of prose on /resume the
 * timeline can't tell you, so it is written by hand rather than derived — and
 * it stays here rather than in the resume collection because it is bio copy,
 * not a position. Verbatim from Figma 477:2483.
 */
export const CV_INTRO =
  'Thirteen years across Berlin startups, founding and running my own company, ' +
  'and two Mittelstand employers taught me how organisations create value and, ' +
  'more often, where they quietly leave it on the table: unused potential, ' +
  'unaddressed demographic shifts, processes drifting away from the core ' +
  'offer. When I stepped back from the founder role to prioritise being a ' +
  'father, it became clear that what I kept reaching for in every position ' +
  'was the curiosity and creative problem framing that sits at the centre of ' +
  'design. Design & Innovation at CODE University of Applied Sciences matches ' +
  'how I thrive, project based, hands on and learning by burning. I am now ' +
  'always looking for a working student position where I can put that into ' +
  'practice, test the designer role from the inside, and sharpen my focus, ' +
  'currently pulling strongest toward User Experience and Brand Design.';

/** The two lines the /resume header draws under the name (Figma 251:2563). */
export const CV_STUDY = {
  field: 'Design & Innovation',
  institution: '@ CODE University of Applied Sciences',
} as const;

/** The printed CV's contact column (Figma 492:2528). */
export const CV_CONTACT = {
  email: SITE.email,
  phone: '+49\u00A0174\u00A0186\u00A03130',
  phoneHref: 'tel:+491741863130',
  website: 'https://zwei.berlin',
} as const;

/**
 * The profiles the printed CV lists, in the order Figma 477:1918 draws them.
 * Each entry names a SOCIALS label; the href and the mark come from there, so
 * a URL is never written twice.
 */
export const CV_PROFILES = ['GitHub', 'Behance', 'LinkedIn'] as const;

/**
 * Tool tiles for Tech & Tools, on both résumé surfaces. Placeholder until the
 * logos exist (Figma /resume Handoff §12).
 */
export const CV_TOOLS = Array.from({ length: 18 }, () => ({
  name: '[tool]',
  icon: '/icons/figma.svg',
}));

/**
 * The footer's own navigation, from the Figma NavBar. Labels retain the
 * component's hashtag convention while hrefs map to the implemented routes.
 */
export const NAV = {
  impressum: { label: '#impressum', href: withBase('/impressum') },
  sections: [
    { label: '#projects', href: withBase('/projects') },
    { label: '#playground', href: withBase('/playground') },
    { label: '#curiosity', href: withBase('/curious') },
    { label: '#inspiration', href: withBase('/inspiration') },
  ],
  about: [
    { label: '#aboutme', href: withBase('/aboutme') },
    { label: '#behindthescenes', href: withBase('/behind-the-scenes') },
  ],
} as const;

/**
 * Social marks the footer draws, and the same row on /resume.
 *
 * `width` is each mark's own drawn width at a 16 height, so the asset is never
 * stretched. `iconDark` is the same artwork as Figma's `Mode=Dark` NavBar
 * paints it — neutral-white instead of neutral-800.
 */
export const SOCIALS = [
  {
    label: 'Figma',
    href: 'https://www.figma.com/@maxpinkert',
    icon: '/icons/figma.svg',
    iconDark: '/icons/dark/figma.svg',
    width: 12,
    height: 16,
  },
  {
    label: 'GitHub',
    href: 'https://github.com/max-zwei',
    icon: '/icons/github.svg',
    iconDark: '/icons/dark/github.svg',
    width: 17,
    height: 16,
  },
  {
    label: 'Dribbble',
    href: 'https://dribbble.com/maxzwei',
    icon: '/icons/dribbble.svg',
    iconDark: '/icons/dark/dribbble.svg',
    width: 16,
    height: 16,
  },
  {
    label: 'Behance',
    href: 'https://www.behance.net/maxpinkert',
    icon: '/icons/behance.svg',
    iconDark: '/icons/dark/behance.svg',
    width: 19,
    height: 16,
  },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/max-pinkert/',
    icon: '/icons/linkedin.svg',
    iconDark: '/icons/dark/linkedin.svg',
    width: 17,
    height: 16,
  },
] as const;

/** The three marks beside "explore with". */
export const EXPLORE_WITH = [
  {
    label: 'Claude',
    href: 'https://claude.ai/',
    icon: '/icons/explore-claude.svg',
    iconDark: '/icons/dark/explore-claude.svg',
  },
  {
    label: 'OpenAI',
    href: 'https://openai.com/',
    icon: '/icons/explore-openai.svg',
    iconDark: '/icons/dark/explore-openai.svg',
  },
  {
    label: '3',
    href: '#',
    icon: '/icons/explore-3.svg',
    iconDark: '/icons/dark/explore-3.svg',
  },
] as const;
