/**
 * Renders the built /resume page to public/cv/max-pinkert-cv.pdf.
 *
 * The CV is not a second document. It is the /resume page printed to A4 by the
 * same rules that style it on screen (the `@media print` block in
 * src/pages/resume.astro), so there is exactly one place where a position is
 * written down: the `resume` content collection in src/content/resume/.
 *
 * Run it with `npm run cv`, which builds first — this script only reads dist/.
 *
 * It needs a Chromium to print with, in this order:
 *   1. $CHROME_PATH, if set
 *   2. whatever Playwright has installed (`npx playwright install chromium`)
 */

import { createReadStream, existsSync } from 'node:fs';
import { mkdir, stat } from 'node:fs/promises';
import { createServer } from 'node:http';
import { dirname, extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));
const dist = join(root, 'dist');
const output = join(root, 'public', 'cv', 'max-pinkert-cv.pdf');
const route = '/resume';

const MIME = {
  '.css': 'text/css',
  '.html': 'text/html; charset=utf-8',
  '.jpg': 'image/jpeg',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
};

/**
 * Astro builds absolute asset paths, so file:// URLs load a page with no fonts
 * and no styles — which prints, silently, as the wrong document. Hence a real
 * server, small enough to not be worth a dependency.
 */
function createStaticServer(directory) {
  return createServer(async (request, response) => {
    const { pathname } = new URL(request.url ?? '/', 'http://localhost');
    const requested = join(directory, normalize(decodeURIComponent(pathname)));

    if (!requested.startsWith(directory)) {
      response.writeHead(403).end();
      return;
    }

    // Directory-style routes: /resume is really /resume/index.html.
    const isDirectory = await stat(requested)
      .then((entry) => entry.isDirectory())
      .catch(() => false);
    const file = isDirectory ? join(requested, 'index.html') : requested;

    if (!existsSync(file)) {
      response.writeHead(404).end();
      return;
    }

    response.writeHead(200, {
      'content-type': MIME[extname(file)] ?? 'application/octet-stream',
    });
    createReadStream(file).pipe(response);
  });
}

async function launchBrowser() {
  const executablePath = process.env.CHROME_PATH;
  try {
    return await chromium.launch(executablePath ? { executablePath } : {});
  } catch (error) {
    console.error(
      'Could not start Chromium. Install one with `npx playwright install ' +
        'chromium`, or point CHROME_PATH at an existing Chrome.\n',
    );
    throw error;
  }
}

if (!existsSync(join(dist, 'resume', 'index.html'))) {
  console.error(`No built ${route} page in dist/. Run \`npm run cv\` instead.`);
  process.exit(1);
}

const server = createStaticServer(dist);
await new Promise((ready) => server.listen(0, '127.0.0.1', ready));
const { port } = server.address();

const browser = await launchBrowser();
try {
  const page = await browser.newPage();
  await page.goto(`http://127.0.0.1:${port}${route}`, {
    waitUntil: 'networkidle',
  });
  // Self-hosted fonts load late enough to miss the print if we don't wait.
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });

  await mkdir(dirname(output), { recursive: true });
  await page.pdf({
    path: output,
    printBackground: true,
    // Honour the @page rule in resume.astro rather than restating A4 here.
    preferCSSPageSize: true,
  });
} finally {
  await browser.close();
  server.close();
}

const { size } = await stat(output);
console.log(
  `Wrote ${output.replace(`${root}/`, '')} (${Math.round(size / 1024)} kB)`,
);
