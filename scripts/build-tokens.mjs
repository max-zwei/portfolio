/**
 * Generates src/styles/tokens.css and design/tokens.json from DESIGN.md.
 *
 *   node scripts/build-tokens.mjs           writes both outputs
 *   node scripts/build-tokens.mjs --check   writes nothing, exits 1 on drift
 *
 * DESIGN.md's front matter is the one human-edited token source; it carries the
 * value the CSS ships. The export is derived from it — rem converted to px for
 * Figma, the fluid `clamp()` steps reduced to their desktop end. Where the two
 * media genuinely cannot hold the same value, EXCHANGE_OVERRIDES below names
 * the one case, with the reason.
 *
 * `--check` is what `npm run verify` and CI run, so it deliberately depends on
 * nothing but Node and the `yaml` parser: no prettier, no Astro.
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { parse } from 'yaml';
import { parseArgs } from 'node:util';

const ROOT = new URL('../', import.meta.url);
const SOURCE = new URL('DESIGN.md', ROOT);
const CSS_OUT = new URL('src/styles/tokens.css', ROOT);
const JSON_OUT = new URL('design/tokens.json', ROOT);

/** rem → px. Nothing in global.css changes the root font size. */
const ROOT_FONT_SIZE = 16;

// --- The contract between the front matter and the two outputs --------------

/** A numbered section banner, and the blank line that always follows it. */
const banner = (...body) => [
  '/* ---------------------------------------------------------------',
  ...body.map((line) => ` * ${line}`),
  ' * ------------------------------------------------------------- */',
  '',
];

const block = (...body) => ['/*', ...body.map((line) => ` * ${line}`), ' */'];

/**
 * One entry per front-matter group, in CSS emission order.
 *
 * `yaml`      dotted path in the front matter
 * `css`       custom property prefix, `--<key>` when empty
 * `json`      slash path in the export; absent means CSS-only
 * `type`      DTCG `$type` for the exported group
 * `px`        export the value in px rather than rem
 * `annotate`  trail each declaration with its pixel value
 * `ramps`     split `<ramp>-<step>` keys into nested export groups
 * `tight`     continue the previous group rather than opening a new block
 */
const GROUPS = [
  {
    yaml: 'colors',
    css: '--color-',
    json: 'color',
    type: 'color',
    ramps: true,
  },
  {
    yaml: 'fontFamily',
    css: '--font-',
    json: 'font/family',
    type: 'fontFamily',
  },
  {
    yaml: 'fontSize',
    css: '--font-size-',
    json: 'font/size',
    type: 'dimension',
    px: true,
    annotate: true,
  },
  {
    yaml: 'fontWeight',
    css: '--font-weight-',
    json: 'font/weight',
    type: 'fontWeight',
  },
  {
    yaml: 'lineHeight',
    css: '--line-height-',
    json: 'font/lineHeight',
    type: 'number',
  },
  {
    yaml: 'letterSpacing',
    css: '--letter-spacing-',
    json: 'font/letterSpacing',
    type: 'dimension',
  },
  {
    yaml: 'spacing',
    css: '--space-',
    json: 'space',
    type: 'dimension',
    px: true,
    annotate: true,
  },
  {
    yaml: 'rounded',
    css: '--radius-',
    json: 'radius',
    type: 'dimension',
    px: true,
  },
  { yaml: 'shadows', css: '--shadow-', json: 'shadow', type: 'shadow' },
  {
    yaml: 'motion.duration',
    css: '--duration-',
    json: 'motion/duration',
    type: 'duration',
  },
  {
    yaml: 'motion.easing',
    css: '--easing-',
    json: 'motion/easing',
    type: 'cubicBezier',
    tight: true,
  },
  { yaml: 'layout', css: '--' },
  {
    yaml: 'sizes',
    css: '--size-',
    json: 'size',
    type: 'dimension',
    px: true,
    annotate: true,
  },
  { yaml: 'focus', css: '--focus-' },
];

/** Front-matter keys that are not token groups. */
const META_KEYS = new Set([
  'version',
  'name',
  'description',
  'omitted',
  'typography',
]);

/** Export order of the top-level keys, `text` last. */
const JSON_TOP_ORDER = [
  'color',
  'font',
  'space',
  'radius',
  'size',
  'motion',
  'shadow',
  'text',
];

/**
 * The rationale that has to survive generation: `css` is a comment block above
 * the group, the ramp or the declaration; `json` becomes a `$description`;
 * `inline` is a trailing annotation where the pixel value alone will not do.
 */
const NOTES = {
  colors: {
    css: banner(
      '1. PRIMITIVES — Colour',
      'Nature-inspired palette. Named after the thing, not the usage.',
    ),
  },
  'colors.lemon': {
    css: ['/* Lemon — citrus yellow. The signature accent. */'],
  },
  'colors.pickled': {
    css: ['/* Pickled — pink-red. Sharp counterweight to Lemon. */'],
  },
  'colors.herbs': { css: ['/* Herbs — calm, grounded green. */'] },
  'colors.tomato': {
    css: ['/* Tomato — warm signal colour, used sparingly. */'],
  },
  'colors.neutral': {
    css: [
      '/* Neutrals — the ends are named, not numbered: neither is pure. */',
    ],
    json: 'The ends are named, not numbered — neither is a pure white or black.',
  },
  fontFamily: {
    css: [
      ...banner('2. PRIMITIVES — Typography'),
      ...block(
        'The "Variable" suffix is what the files actually register. Drop it and',
        'every visitor silently gets a system face, with no error anywhere. All',
        'three are declared in fonts.css; the generic behind each is what shows',
        'while they load.',
      ),
    ],
    json: "Satoshi and Erode are self-hosted in public/fonts/ and declared in src/styles/fonts.css; JetBrains Mono comes from @fontsource-variable/jetbrains-mono. The family names carry the 'Variable' suffix the woff2 files register — drop it and every visitor silently gets a system face, with no error anywhere.",
  },
  fontSize: {
    css: block(
      'Figma carries the desktop end of each step. Only the display steps are',
      'fluid: shrinking 16px body copy on a phone costs more than it buys.',
    ),
    json: 'Max value of the fluid clamp() in the CSS. Figma is a fixed-size medium, so it carries the desktop end of the scale. xs/sm/base are fixed in CSS rather than fluid.',
  },
  'lineHeight.none': {
    css: [
      '/* Set solid — the Figma heading styles H1–H5 all bind line-height 1. */',
    ],
    json: 'Set solid. The Figma heading styles H1–H5 all bind it.',
  },
  'lineHeight.loose': {
    css: [
      '/* Airy enough for wide-tracked mono. Chat bubbles, per the Figma text style. */',
    ],
    json: 'Airy enough for wide-tracked mono. The chat bubbles on /home.',
  },
  letterSpacing: {
    json: 'Figma applies FLOAT letter-spacing in px and cannot hold an em value. These are the em equivalents that ship.',
  },
  spacing: {
    css: banner(
      '3. PRIMITIVES — Space, radius, elevation, motion',
      '4px base grid.',
    ),
    json: '4px base grid.',
  },
  shadows: {
    json: 'Figma variables have no shadow type, so these are STRING variables paired with matching `Elevation / sm|md|lg` effect styles. Change one, change both.',
  },
  layout: {
    css: block(
      'Page grid — transcribed from the layout grid on every 1280 Figma desktop',
      'frame (`home - chat` 103:1102, `/projects` 128:638 and the rest): COLUMNS',
      '×10, gutter 24, margin 96, so 1088 of content and an 87.2 column. A layout',
      'grid is not a Figma variable, so unlike every other token here these have',
      "no entry in design/tokens.json — DESIGN.md's `layout` group is CSS-only,",
      'as is `focus`. The 375 `Mobile` frames draw ×5, gutter 16, margin 24; that',
      '24 is --space-md, which global.css already uses below 48rem.',
    ),
  },
  'layout.grid-frame': { inline: '1280px — the drawn frame' },
  'layout.grid-margin': { inline: '96px' },
  'layout.grid-gutter': { inline: '24px' },
  'layout.grid-column': {
    css: [
      '/* One column: 5.45rem / 87.2px. Computed, so changing the frame or the',
      '   gutter cannot leave a stale derived value behind. */',
    ],
  },
  'layout.measure': { blankBefore: true, inline: 'readable line length' },
  sizes: {
    json: 'Widths read off the /home chat frames. chat-choice is the only one the site ships as a token: the message column and bubble are computed as 8- and 5-column spans of the page grid. size/chat-column and size/chat-bubble remain in the Figma Size collection pending deletion (design/components.json outstanding.variableWrites).',
  },
  'sizes.chat-choice': {
    css: block(
      "The one width that is a component's own. 400px is not a column span — four",
      "columns is 420.8 — and the design's own chip instances exceed it.",
      '`size/chat-choice` in Figma.',
    ),
    json: 'Maximum width of a reply chip before its text wraps.',
  },
  focus: {
    css: banner('4. FOCUS RING — defined once, applied in global.css.'),
  },
};

/**
 * Values the export cannot take from the CSS. `--radius-full` ships `999rem`
 * and the Figma variable holds `9999px`: both are a pill, and neither is
 * derived from the other, so both are stated rather than computed.
 */
const EXCHANGE_OVERRIDES = { 'rounded.full': '9999px' };

const CSS_HEADER = `/*
 * Generated from DESIGN.md by scripts/build-tokens.mjs. Do not edit.
 * Run \`npm run tokens\` after changing DESIGN.md's front matter.
 *
 * Every name here is its Figma variable name with \`/\` swapped for \`-\` and \`--\`
 * in front: \`color/lemon/500\` is \`--color-lemon-500\`. That correspondence is
 * the anti-drift mechanism — keep it mechanical.
 *
 * Values come from Figma, through DESIGN.md. One tier, no role layer. The
 * three things Figma cannot express faithfully are in
 * behind-the-scenes/skills/figma-to-astro.md.
 */`;

const JSON_DESCRIPTION =
  'W3C DTCG-shaped token export, generated from DESIGN.md by scripts/build-tokens.mjs — do not hand-edit. This is the exchange format between Figma Variables and the design system. Collection names here map 1:1 to Figma Variable collections; token paths map to Figma variable names (e.g. color/lemon/500 -> `color/lemon/500`). One tier only — there is no role/semantic layer, by decision. src/styles/tokens.css is generated from the same source and is what ships.';

const TEXT_DESCRIPTION =
  'The twelve named Figma text styles. Each leg holds a CSS custom property name — text styles are Figma *styles*, not variables, so there is nothing here for a variable importer to read.';

// --- Conversions ------------------------------------------------------------

const fail = (message) => {
  throw new Error(message);
};

/** '1.5rem' → '24px'. Throws on anything that is not a rem number. */
function remToPx(value, path) {
  const match = /^(-?\d*\.?\d+)rem$/.exec(String(value).trim());
  if (!match)
    fail(`${path}: expected a rem value for the px export, got "${value}"`);
  const px = Number(match[1]) * ROOT_FONT_SIZE;
  if (!Number.isFinite(px)) fail(`${path}: "${value}" is not a number`);
  return `${trimZero(px)}px`;
}

const trimZero = (n) => String(Number(n.toFixed(4)));

/** Splits a clamp()'s top-level arguments. */
function clampArgs(value) {
  const inner = /^clamp\((.*)\)$/s.exec(String(value).trim());
  if (!inner) return null;
  const args = [];
  let depth = 0;
  let current = '';
  for (const char of inner[1]) {
    if (char === '(') depth += 1;
    if (char === ')') depth -= 1;
    if (char === ',' && depth === 0) {
      args.push(current.trim());
      current = '';
      continue;
    }
    current += char;
  }
  args.push(current.trim());
  return args;
}

/** The desktop end of a fluid step; a fixed value passes through. */
function clampMax(value) {
  const args = clampArgs(value);
  return args ? args[args.length - 1] : String(value);
}

/** `'Satoshi Variable', system-ui, sans-serif` — quote only what needs it. */
const cssFamily = (stack) =>
  stack
    .map((name) => (/^[A-Za-z0-9-]+$/.test(name) ? name : `'${name}'`))
    .join(', ');

const cssEasing = (points) => `cubic-bezier(${points.join(', ')})`;

/** Right-aligns single digits, the way the hand-written file did. */
const padPx = (px) => (px.replace('px', '').length === 1 ? ` ${px}` : px);

/** '1.5rem' → '24px'; a clamp() annotates both ends. */
function pxAnnotation(value, path) {
  const args = clampArgs(value);
  if (!args) return padPx(remToPx(value, path));
  const min = remToPx(args[0], path).replace('px', '');
  return `${min} → ${remToPx(args[args.length - 1], path)}`;
}

// --- Front matter -----------------------------------------------------------

function readFrontMatter() {
  const text = readFileSync(SOURCE, 'utf8');
  const match = /^---\n([\s\S]*?)\n---(?:\n|$)/.exec(text);
  if (!match)
    fail('DESIGN.md: no YAML front matter — the token source is missing');
  let front;
  try {
    front = parse(match[1]);
  } catch (error) {
    fail(`DESIGN.md front matter: ${error.message}`);
  }
  if (!front || typeof front !== 'object')
    fail('DESIGN.md front matter: not a mapping');

  const known = new Set([
    ...META_KEYS,
    ...GROUPS.map((g) => g.yaml.split('.')[0]),
  ]);
  for (const key of Object.keys(front)) {
    if (!known.has(key)) fail(`DESIGN.md front matter: unknown group "${key}"`);
  }
  return front;
}

function group(front, dotted) {
  const value = dotted.split('.').reduce((node, key) => node?.[key], front);
  if (!value || typeof value !== 'object')
    fail(`DESIGN.md front matter: missing group "${dotted}"`);
  return value;
}

// --- CSS --------------------------------------------------------------------

const rampOf = (key) => key.slice(0, key.indexOf('-'));

function buildCss(front) {
  const lines = [CSS_HEADER, '', ':root {'];
  const blank = () => {
    const last = lines[lines.length - 1];
    if (last !== '' && last !== ':root {') lines.push('');
  };
  const comment = (raw) =>
    lines.push(...raw.map((line) => (line === '' ? '' : `  ${line}`)));

  for (const spec of GROUPS) {
    const entries = Object.entries(group(front, spec.yaml));
    if (!spec.tight) blank();
    if (NOTES[spec.yaml]?.css) comment(NOTES[spec.yaml].css);

    let ramp = null;
    for (const [key, raw] of entries) {
      const path = `${spec.yaml}.${key}`;
      if (spec.ramps) {
        const current = rampOf(key);
        if (current !== ramp) {
          blank();
          if (NOTES[`${spec.yaml}.${current}`]?.css)
            comment(NOTES[`${spec.yaml}.${current}`].css);
          ramp = current;
        }
      }
      const note = NOTES[path];
      if (note?.blankBefore) blank();
      if (note?.css) comment(note.css);

      let value = raw;
      if (Array.isArray(raw))
        value = spec.yaml === 'fontFamily' ? cssFamily(raw) : cssEasing(raw);

      let annotation = '';
      if (note?.inline) annotation = ` /* ${note.inline} */`;
      else if (spec.annotate) annotation = ` /* ${pxAnnotation(raw, path)} */`;

      lines.push(`  ${spec.css}${key}: ${value};${annotation}`);
    }
  }

  lines.push('}');
  return `${lines.join('\n')}\n`;
}

// --- JSON -------------------------------------------------------------------

function exportValue(spec, key, raw) {
  const path = `${spec.yaml}.${key}`;
  if (path in EXCHANGE_OVERRIDES) return EXCHANGE_OVERRIDES[path];
  return spec.px ? remToPx(clampMax(raw), path) : raw;
}

/**
 * Groups are Maps, not objects: `color/neutral/100` is an integer-like key,
 * and a plain object would hoist it above `white` no matter what order it was
 * written in. A Map keeps the front matter's order, which is the ramp's order.
 */
function node(parent, key) {
  if (!parent.has(key)) parent.set(key, new Map());
  return parent.get(key);
}

function placeGroup(tree, spec, front) {
  const target = spec.json.split('/').reduce(node, tree);

  if (spec.type) target.set('$type', spec.type);
  if (NOTES[spec.yaml]?.json) target.set('$description', NOTES[spec.yaml].json);

  for (const [key, raw] of Object.entries(group(front, spec.yaml))) {
    let parent = target;
    let leafKey = key;
    if (spec.ramps) {
      const ramp = rampOf(key);
      parent = node(target, ramp);
      const rampNote = NOTES[`${spec.yaml}.${ramp}`]?.json;
      if (rampNote && !parent.has('$description'))
        parent.set('$description', rampNote);
      leafKey = key.slice(ramp.length + 1);
    }
    const leaf = new Map([['$value', exportValue(spec, key, raw)]]);
    const description = NOTES[`${spec.yaml}.${key}`]?.json;
    if (description) leaf.set('$description', description);
    parent.set(leafKey, leaf);
  }
}

/** Resolves `{fontSize.3xl}` to the CSS custom property name it stands for. */
function resolveReference(reference, front, path) {
  const match = /^\{([^.}]+)\.([^}]+)\}$/.exec(String(reference));
  if (!match) fail(`${path}: "${reference}" is not a token reference`);
  const [, groupName, key] = match;
  const spec = GROUPS.find((entry) => entry.yaml === groupName);
  if (!spec) fail(`${path}: "${reference}" points at no front-matter group`);
  if (!(key in group(front, spec.yaml)))
    fail(`${path}: "${reference}" has no such token`);
  return `${spec.css}${key}`;
}

function buildText(front) {
  const styles = front.typography;
  if (!styles || typeof styles !== 'object') {
    fail('DESIGN.md front matter: missing group "typography"');
  }
  const out = new Map([['$description', TEXT_DESCRIPTION]]);
  for (const [name, legs] of Object.entries(styles)) {
    const value = new Map();
    for (const [leg, reference] of Object.entries(legs)) {
      value.set(
        leg,
        resolveReference(reference, front, `typography.${name}.${leg}`),
      );
    }
    out.set(
      name,
      new Map([
        ['$type', 'typography'],
        ['$value', value],
      ]),
    );
  }
  return out;
}

/** JSON.stringify with 2-space indent, except arrays, which stay inline. */
function serialise(value, indent = '') {
  if (Array.isArray(value))
    return `[${value.map((item) => JSON.stringify(item)).join(', ')}]`;
  if (value instanceof Map) {
    const inner = `${indent}  `;
    const body = [...value]
      .map(
        ([key, child]) =>
          `${inner}${JSON.stringify(key)}: ${serialise(child, inner)}`,
      )
      .join(',\n');
    return `{\n${body}\n${indent}}`;
  }
  return JSON.stringify(value);
}

function buildJson(front) {
  const tree = new Map([
    ['$schema', 'https://design-tokens.org/schema.json'],
    ['$description', JSON_DESCRIPTION],
  ]);
  const exported = GROUPS.filter((spec) => spec.json);
  for (const top of JSON_TOP_ORDER) {
    if (top === 'text') {
      tree.set('text', buildText(front));
      continue;
    }
    for (const spec of exported.filter(
      (entry) => entry.json.split('/')[0] === top,
    )) {
      placeGroup(tree, spec, front);
    }
  }
  return `${serialise(tree)}\n`;
}

// --- CLI --------------------------------------------------------------------

const { values } = parseArgs({
  options: { check: { type: 'boolean', default: false } },
});

const front = readFrontMatter();
const outputs = [
  { url: CSS_OUT, label: 'src/styles/tokens.css', text: buildCss(front) },
  { url: JSON_OUT, label: 'design/tokens.json', text: buildJson(front) },
];

if (values.check) {
  const stale = outputs.filter((output) => {
    let current = null;
    try {
      current = readFileSync(output.url, 'utf8');
    } catch {
      return true;
    }
    return current !== output.text;
  });
  if (stale.length) {
    console.error('Generated tokens are out of date with DESIGN.md:');
    for (const output of stale) console.error(`  ${output.label}`);
    console.error('Run `npm run tokens`.');
    process.exit(1);
  }
  console.log('Generated tokens match DESIGN.md.');
} else {
  for (const output of outputs) writeFileSync(output.url, output.text);
  console.log(
    `Wrote ${outputs.map((output) => output.label).join(' and ')} from DESIGN.md.`,
  );
}
