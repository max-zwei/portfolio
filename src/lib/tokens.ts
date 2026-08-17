import tokens from '../../design/tokens.json';

/**
 * Reads design/tokens.json and resolves it into something renderable.
 *
 * The styleguide page reads from here rather than from a hand-written list, so
 * it cannot drift from the token file. If a value changes in tokens.json, the
 * styleguide reflects it on the next build — including the contrast maths.
 */

type TokenLeaf = { $value: string | number | string[] | number[] };

const isLeaf = (v: unknown): v is TokenLeaf =>
  typeof v === 'object' && v !== null && '$value' in v;

/** Flattens a token group into [path, value] pairs. */
function flatten(group: Record<string, unknown>, prefix: string[] = []) {
  const out: Array<{ path: string[]; value: string }> = [];
  for (const [key, node] of Object.entries(group)) {
    if (key.startsWith('$')) continue;
    if (isLeaf(node)) {
      const raw = node.$value;
      out.push({
        path: [...prefix, key],
        value: String(Array.isArray(raw) ? raw[0] : raw),
      });
    } else if (typeof node === 'object' && node !== null) {
      out.push(...flatten(node as Record<string, unknown>, [...prefix, key]));
    }
  }
  return out;
}

// --- Colour -----------------------------------------------------------------

export const colorScales = Object.entries(tokens.color)
  .filter(([key]) => !key.startsWith('$'))
  .map(([scale, steps]) => ({
    name: scale,
    steps: flatten(steps as Record<string, unknown>).map(({ path, value }) => ({
      step: path[0],
      name: `${scale}/${path[0]}`,
      value,
      cssVar: `--color-${scale}-${path[0]}`,
    })),
  }));

const allColors = colorScales.flatMap((scale) => scale.steps);

// --- Contrast ---------------------------------------------------------------

const channel = (hex: string, i: number) =>
  parseInt(hex.slice(i, i + 2), 16) / 255;
const linearise = (c: number) =>
  c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;

function luminance(hex: string): number {
  const [r, g, b] = [1, 3, 5].map((i) => linearise(channel(hex, i)));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** WCAG 2.1 contrast ratio, 1–21. */
export function contrast(a: string, b: string): number {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

export type Verdict = 'AAA' | 'AA' | 'AA Large' | 'Decorative only';

/**
 * What a foreground/background pair is actually safe for.
 *
 * 4.5 — body text (WCAG AA, 1.4.3)
 * 3.0 — large text (≥24px, or ≥18.66px bold) and meaningful non-text UI (1.4.11)
 * below 3.0 — decoration only; it cannot carry meaning on its own
 */
export function verdict(ratio: number): Verdict {
  if (ratio >= 7) return 'AAA';
  if (ratio >= 4.5) return 'AA';
  if (ratio >= 3) return 'AA Large';
  return 'Decorative only';
}

/**
 * The colours that actually sit behind content. With one token tier there is no
 * `surface/*` role to enumerate, so this is the honest substitute: the four
 * neutrals the pages use as backgrounds. Every other colour is checked against
 * them.
 */
const GROUND_NAMES = [
  'neutral/white',
  'neutral/100',
  'neutral/200',
  'neutral/black',
];

export const grounds = GROUND_NAMES.map((name) => {
  const found = allColors.find((c) => c.name === name);
  if (!found) throw new Error(`Ground colour "${name}" is not in tokens.json`);
  return found;
});

/** Every colour against every ground, grouped by ramp. */
export const contrastMatrix = colorScales.map((scale) => ({
  name: scale.name,
  rows: scale.steps.map((step) => ({
    ...step,
    cells: grounds.map((ground) => {
      const ratio = contrast(step.value, ground.value);
      return { ground: ground.name, ratio, verdict: verdict(ratio) };
    }),
  })),
}));

/** Colours that can carry body text on at least one light ground. */
export const bodySafeOnLight = contrastMatrix
  .flatMap((scale) => scale.rows)
  .filter((row) =>
    row.cells.some(
      (cell) => cell.ground !== 'neutral/black' && cell.ratio >= 4.5,
    ),
  );

// --- Everything else --------------------------------------------------------

export const fontSizes = flatten(tokens.font.size).map(({ path, value }) => ({
  name: `font/size/${path[0]}`,
  cssVar: `--font-size-${path[0]}`,
  value,
}));

export const spacing = flatten(tokens.space).map(({ path, value }) => ({
  name: `space/${path[0]}`,
  cssVar: `--space-${path[0]}`,
  value,
}));

export const radii = flatten(tokens.radius).map(({ path, value }) => ({
  name: `radius/${path[0]}`,
  cssVar: `--radius-${path[0]}`,
  value,
}));
