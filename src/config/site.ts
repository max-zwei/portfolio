import type { IconName } from '../components/Icon.astro';

/**
 * Site-wide constants. Anything that appears in more than one place —
 * or that you would otherwise be tempted to retype — belongs here.
 */

/**
 * Applies Astro's configured base to hand-authored paths.
 *
 * Astro rewrites the URLs it generates, but template paths come through here.
 * With the default / base, they remain root-relative.
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

/** Tool tiles for Tech & Tools, on both résumé surfaces. */
export const CV_TOOLS = [
  { name: 'Lucid', icon: '/icons/tools/lucid.svg' },
  { name: 'Figma', icon: '/icons/tools/figma.svg' },
  { name: 'Jira', icon: '/icons/tools/jira.svg' },
  { name: 'UserGuiding', icon: '/icons/tools/userguiding.png' },
  { name: 'Miro', icon: '/icons/tools/miro.svg' },
  { name: 'Notion', icon: '/icons/tools/notion.svg' },
  { name: 'Atlassian', icon: '/icons/tools/atlassian.svg' },
  { name: '[tool]', icon: '/icons/tools/tool-08.png' },
  { name: '[tool]', icon: '/icons/tools/tool-09.svg' },
  { name: '[tool]', icon: '/icons/tools/tool-10.png' },
  { name: 'Asana', icon: '/icons/tools/asana.svg' },
  { name: 'Webflow', icon: '/icons/tools/webflow.svg' },
  { name: '[tool]', icon: '/icons/tools/tool-13.svg' },
  { name: 'WordPress', icon: '/icons/tools/wordpress.png' },
  { name: 'Visio', icon: '/icons/tools/visio.png' },
  { name: 'Marvel', icon: '/icons/tools/marvel.png' },
  { name: 'GitHub', icon: '/icons/tools/github-tool.svg' },
  { name: 'Excel', icon: '/icons/tools/excel.png' },
  { name: '[tool]', icon: '/icons/tools/tool-19.svg' },
  { name: 'Canva', icon: '/icons/tools/canva.png' },
] as const;

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
    { label: '#aboutme', href: withBase('/resume') },
    { label: '#behindthescenes', href: withBase('/behind-the-scenes') },
  ],
} as const;

/** Social marks the footer draws, and the same row on /resume. */
export const SOCIALS = [
  {
    label: 'Figma',
    href: 'https://www.figma.com/@maxpinkert',
    icon: 'figma',
  },
  {
    label: 'GitHub',
    href: 'https://github.com/max-zwei',
    icon: 'github',
  },
  {
    label: 'Dribbble',
    href: 'https://dribbble.com/maxzwei',
    icon: 'dribbble',
  },
  {
    label: 'Behance',
    href: 'https://www.behance.net/maxpinkert',
    icon: 'behance',
  },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/max-pinkert/',
    icon: 'linkedin',
  },
] as const satisfies ReadonlyArray<{
  label: string;
  href: string;
  icon: IconName;
}>;

/** The three marks beside "explore with". */
export const EXPLORE_WITH = [
  {
    label: 'Claude',
    icon: 'anthropic',
    href: 'https://claude.ai/new?q=Summarise%20this%20page%20for%20me%3A%20https%3A%2F%2Fzwei.berlin%2Fsummary',
  },
  {
    label: 'OpenAI',
    icon: 'openai',
    href: 'https://chatgpt.com/?q=Summarise%20this%20page%20for%20me%3A%20https%3A%2F%2Fzwei.berlin%2Fsummary',
  },
  {
    label: 'Perplexity',
    icon: 'perplexity',
    href: 'https://www.perplexity.ai/search?q=Summarise%20this%20page%20for%20me%3A%20https%3A%2F%2Fzwei.berlin%2Fsummary',
  },
] as const satisfies ReadonlyArray<{
  label: string;
  href: string;
  icon: IconName;
}>;
