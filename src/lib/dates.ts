/*
 * Shared formatting for year and year-month values used by the CV surfaces.
 *
 * Keeping this here means the page and the Figma CV-section component cannot
 * drift into two different date formats.
 */

const MONTHS = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
];

/** `2024-09` → `Sep 2024`. A bare year passes through untouched. */
export function formatMonth(value: string): string {
  const [year, month] = value.split('-');
  return month ? `${MONTHS[Number(month) - 1]} ${year}` : year;
}

/**
 * Formats a CV date span, writing a shared year only once.
 *
 * The spaced hyphen-minus in `Mar - Oct 2026` is the glyph drawn by the
 * Figma `CV section`, rather than an en dash chosen by code.
 */
export function formatRange(start: string, end?: string): string {
  if (!end) return `${formatMonth(start)} - present`;
  const startFormatted = formatMonth(start);
  const endFormatted = formatMonth(end);
  if (startFormatted === endFormatted) return startFormatted;

  const [startYear, startMonth] = start.split('-');
  const [endYear, endMonth] = end.split('-');

  if (startYear === endYear && startMonth && endMonth) {
    const startLabel = MONTHS[Number(startMonth) - 1];
    const endLabel = MONTHS[Number(endMonth) - 1];
    return `${startLabel} - ${endLabel} ${startYear}`;
  }

  return `${startFormatted} - ${endFormatted}`;
}
