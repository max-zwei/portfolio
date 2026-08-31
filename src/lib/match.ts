import type { AxisId } from '../config/match';

/** Tie-break order when two entries score the same. Strongest proof first. */
export const COLLECTIONS = [
  'projects',
  'playground',
  'resume',
  'inspiration',
  'curiosity',
] as const;

export type Collection = (typeof COLLECTIONS)[number];

/** A run of text, optionally a link. Shared with index.astro's message copy. */
export type Run = string | { text: string; href: string };

/** One matchable entry, flattened at build time. */
export type Entry = {
  collection: Collection;
  /** What the statement calls it. */
  label: string;
  /** Where to point, or null when nothing resolvable exists yet. */
  href: string | null;
  tags: Record<AxisId, readonly string[]>;
};

/** One answered question: the chip's tag id, and the words on the chip. */
export type Answer = { axis: AxisId; id?: string; label: string };

export type Verdict = {
  /** Answers the shown evidence backs up. */
  hits: Answer[];
  /** Answers with a real option that no shown evidence backs up. */
  gaps: Answer[];
  /** Up to three entries, strongest first. */
  evidence: Entry[];
};

/** Three links is what the panel can carry without turning into a list. */
const MAX_EVIDENCE = 3;

export const verdict = (entries: Entry[], answers: Answer[]): Verdict => {
  // An `Other …` answer carries no id: it constrains nothing, so it can
  // neither score an entry nor count as a gap.
  const asked = answers.filter((a) => a.id);

  const evidence = entries
    .map((entry) => ({
      entry,
      score: asked.filter((a) => entry.tags[a.axis].includes(a.id!)).length,
    }))
    .filter((s) => s.score > 0)
    .sort(
      (a, b) =>
        b.score - a.score ||
        COLLECTIONS.indexOf(a.entry.collection) -
          COLLECTIONS.indexOf(b.entry.collection) ||
        a.entry.label.localeCompare(b.entry.label),
    )
    .slice(0, MAX_EVIDENCE)
    .map((s) => s.entry);

  // Hits are measured against the evidence that is actually shown, so every
  // ticked box has a link next to it.
  const hit = (a: Answer) =>
    evidence.some((e) => e.tags[a.axis].includes(a.id!));

  return {
    hits: asked.filter(hit),
    gaps: asked.filter((a) => !hit(a)),
    evidence,
  };
};

/** "A", "A and B", "A, B and C". No Oxford comma — the design's copy has none. */
const list = (parts: Run[]): Run[] =>
  parts.flatMap((part, i) =>
    i === 0 ? [part] : [i === parts.length - 1 ? ' and ' : ', ', part],
  );

/**
 * The panel's paragraphs. The three sentence skeletons are the frame's own
 * copy with their `…` slots filled — the space that sat before the closing
 * `?` / `.` went with the ellipsis it belonged to. An empty array means: say
 * nothing, leave the design's placeholder standing.
 */
export const statement = (v: Verdict): Run[][] => {
  if (!v.evidence.length) return [];

  const paragraphs: Run[][] = [];

  if (v.gaps.length && v.hits.length) {
    paragraphs.push([
      'It depends, are you willing to trade off ',
      ...list(v.gaps.map((g) => g.label)),
      ' to gain ',
      ...list(v.hits.map((h) => h.label)),
      '?',
    ]);
  }

  const tech = v.hits.find((h) => h.axis === 'tech');
  if (tech) {
    paragraphs.push([
      `Skill-wise he ticks the boxes for your tool setup of ${tech.label}.`,
    ]);
  }

  paragraphs.push([
    'And maybe ',
    ...list(
      v.evidence.map((e) =>
        e.href ? { text: e.label, href: e.href } : e.label,
      ),
    ),
    ' can provide you a clearer understanding of a similar set of deliverables to what you are aiming for.',
  ]);

  return paragraphs;
};
