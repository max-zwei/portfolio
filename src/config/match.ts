/**
 * The /home questionnaire's four axes, and the vocabulary content is tagged
 * with. Source of truth for both sides of the match: the chips a visitor
 * clicks (src/pages/index.astro) and the tag options on every entry
 * (src/content.config.ts, public/admin/config.yml, docs/cms.md).
 */

/** Questionnaire order. Also the order answers are echoed and read back in. */
export const AXIS_IDS = ['team', 'field', 'role', 'tech'] as const;

export type AxisId = (typeof AXIS_IDS)[number];

type Axis = {
  /** The step id in index.astro whose chips answer this axis. */
  step: string;
  /** Taggable options, in the order the frame lists them. */
  tags: readonly { readonly id: string; readonly label: string }[];
  /** The escape chip. Carries no tag, so it can neither hit nor miss. */
  other: string;
};

export const AXES = {
  team: {
    step: 'questionnaire',
    tags: [
      { id: 'corporate', label: 'Coporate' },
      { id: 'startup', label: 'Startup' },
      { id: 'individual', label: 'Individual' },
      { id: 'pre-company', label: 'Pre-Company' },
      { id: 'ngo', label: 'NGO' },
      { id: 'association', label: 'Association' },
    ],
    other: 'Other ...',
  },
  field: {
    step: 'field',
    tags: [
      { id: 'web-design', label: 'Web Design' },
      { id: 'branding', label: 'Branding' },
      { id: 'ux-review', label: 'UX Review' },
      { id: 'ui-review', label: 'UI Review' },
      { id: 'ux-concept', label: 'UX Concept' },
      { id: 'product-management', label: 'Product Management' },
    ],
    other: 'Other ...',
  },
  role: {
    step: 'role',
    tags: [
      { id: 'volunteer', label: 'Volunteer' },
      { id: 'freelancer', label: 'Freelancer' },
      { id: 'employee', label: 'Employee' },
      { id: 'founding-designer', label: 'Founding Designer' },
    ],
    other: 'Other ...',
  },
  tech: {
    step: 'stack',
    tags: [
      { id: 'css-html', label: 'CSS / HTML' },
      { id: 'wordpress', label: 'Wordpress' },
      { id: 'no-code', label: 'Framer / Webflow / Wix..' },
      { id: 'python', label: 'Python' },
      { id: 'javascript', label: 'Javascript' },
      { id: 'julia', label: 'Julia' },
    ],
    other: 'Other ..',
  },
} as const satisfies Record<AxisId, Axis>;

/** One axis's tag ids — for `z.enum` and for the CMS select options. */
export const tagIds = <A extends AxisId>(axis: A) =>
  AXES[axis].tags.map((t) => t.id);
