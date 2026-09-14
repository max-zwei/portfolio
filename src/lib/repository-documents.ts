import { satteri, satteriHeadingIdsPlugin } from '@astrojs/markdown-satteri';

const FRONT_MATTER = /^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/;
const FRONT_MATTER_OPEN = /^---(?:\r?\n|$)/;
const EXTERNAL_SCHEME = /^[a-zA-Z][a-zA-Z\d+.-]*:/;
const REPOSITORY_ROOT = 'https://repository.invalid/';

export async function renderRepositoryDocument(
  source: string,
  document: 'readme' | 'design',
  repositoryUrl: string,
): Promise<string> {
  const frontMatter = FRONT_MATTER.exec(source);
  if (!frontMatter && FRONT_MATTER_OPEN.test(source)) {
    throw new Error(`Invalid YAML front matter in ${document} document`);
  }

  const body = frontMatter ? source.slice(frontMatter[0].length) : source;
  if (!body.trim()) {
    throw new Error(`Empty repository document: ${document}`);
  }

  const renderer = await satteri({
    hastPlugins: [
      satteriHeadingIdsPlugin(),
      {
        name: 'repository-document',
        element: {
          filter: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'table'],
          visit(node, ctx) {
            if (/^h[1-6]$/.test(node.tagName)) {
              const oldRank = Number(node.tagName.slice(1));
              const oldId = String(node.properties.id);

              return {
                ...node,
                tagName: `h${Math.min(6, oldRank + 2)}`,
                properties: {
                  ...node.properties,
                  id: `${document}-${oldId}`,
                },
              };
            }

            if (node.tagName === 'a') {
              const href = node.properties.href;
              if (typeof href !== 'string') return;

              if (href.startsWith('#')) {
                ctx.setProperty(node, 'href', `#${document}-${href.slice(1)}`);
                return;
              }

              if (EXTERNAL_SCHEME.test(href) || href.startsWith('//')) return;

              const target = new URL(href, REPOSITORY_ROOT);
              const view = target.pathname.endsWith('/') ? 'tree' : 'blob';
              ctx.setProperty(
                node,
                'href',
                `${repositoryUrl}/${view}/main${target.pathname}${target.search}${target.hash}`,
              );
              return;
            }

            ctx.wrapNode(node, {
              type: 'element',
              tagName: 'div',
              properties: { className: ['table-wrap'] },
              children: [],
            });
          },
        },
      },
    ],
  }).createRenderer({ syntaxHighlight: false });

  const result = await renderer.render(body);
  return result.code;
}
