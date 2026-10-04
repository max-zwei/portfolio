import { satteri } from '@astrojs/markdown-satteri';

/**
 * Markdown held in frontmatter — the release-note categories, and the case
 * sections when they land. Astro's render() only renders an entry's body.
 * Renderers are shared across the build by heading offset.
 */
interface FrontmatterMarkdownRenderer {
  render(source: string): Promise<{ code: string }>;
}

const renderers = new Map<0 | 2, Promise<FrontmatterMarkdownRenderer>>();

export async function renderFrontmatterMarkdown(
  source: string,
  headingOffset: 0 | 2 = 0,
): Promise<string> {
  let renderer = renderers.get(headingOffset);
  if (!renderer) {
    renderer = satteri({
      mdastPlugins: headingOffset
        ? [
            {
              name: 'heading-offset',
              heading(node, ctx) {
                ctx.setProperty(
                  node,
                  'depth',
                  Math.min(6, node.depth + headingOffset) as typeof node.depth,
                );
              },
            },
          ]
        : [],
    }).createRenderer({ syntaxHighlight: false });
    renderers.set(headingOffset, renderer);
  }
  const { code } = await (await renderer).render(source);
  return code;
}
