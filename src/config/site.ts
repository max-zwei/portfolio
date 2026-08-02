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
 * Social / professional links rendered in the footer.
 * Add entries as the profiles go live; empty `href` entries are skipped.
 */
export const LINKS: ReadonlyArray<{ label: string; href: string }> = [
  { label: 'Email', href: `mailto:max.pinkert@code.berlin` },
  { label: 'GitHub', href: 'https://github.com/max-zwei' },
];
