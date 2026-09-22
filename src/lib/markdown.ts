import { satteri } from '@astrojs/markdown-satteri';

/**
 * Markdown held in frontmatter — the release-note categories, and the case
 * sections when they land. Astro's render() only renders an entry's body.
 * One renderer for the whole build.
 */
interface FrontmatterMarkdownRenderer {
  render(source: string): Promise<{ code: string }>;
}

let renderer: Promise<FrontmatterMarkdownRenderer> | undefined;

export async function renderFrontmatterMarkdown(
  source: string,
): Promise<string> {
  renderer ??= satteri().createRenderer({ syntaxHighlight: false });
  const { code } = await (await renderer).render(source);
  return code;
}
