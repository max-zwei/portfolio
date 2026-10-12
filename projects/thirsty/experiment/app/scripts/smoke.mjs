import { chromium, expect } from "@playwright/test";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { resolve, extname } from "node:path";
import assert from "node:assert/strict";
const root = resolve("dist");
const types = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".json": "application/json",
  ".css": "text/css",
  ".png": "image/png",
  ".ico": "image/x-icon",
};
const server = createServer(async (req, res) => {
  try {
    const file = resolve(
      root,
      "." + decodeURIComponent(new URL(req.url, "http://localhost").pathname),
    );
    if (file !== root && !file.startsWith(root + "/")) {
      res.writeHead(403);
      res.end();
      return;
    }
    const path = file === root ? resolve(root, "index.html") : file;
    const bytes = await readFile(path);
    res.writeHead(200, {
      "Content-Type": types[extname(path)] || "application/octet-stream",
    });
    res.end(bytes);
  } catch {
    res.writeHead(404);
    res.end();
  }
});
await new Promise((done, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", done);
});
let browser;
let page;
try {
  browser = await chromium.launch({
    executablePath:
      process.env.CHROME_PATH ||
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless: true,
  });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    timezoneId: "Europe/Berlin",
  });
  page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const button = (name) => page.getByRole("button", { name, exact: true });
  const tab = (name) => page.getByRole("tab", { name, exact: true });
  const saved = async () => {
    await expect(page.getByText("Saving…", { exact: true })).toHaveCount(0);
  };
  const readData = () =>
    page.evaluate(() => JSON.parse(localStorage.getItem("pocketplan.v1")));
  await page.goto(`http://127.0.0.1:${server.address().port}`);
  await expect(tab("Today")).toBeVisible();
  await expect(
    page.getByText("Book a dentist appointment", { exact: true }),
  ).toBeVisible();
  await page.screenshot({ path: "artifacts/today-mobile.png", fullPage: true });
  console.log("PASS: demo launch, Today due/overdue groups, mobile viewport.");
  await tab("Projects").click();
  await button("+ Project").click();
  await button("Save project").click();
  await expect(
    page.getByText("Give your project a name.", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("textbox", { name: "Project name", exact: true })
    .fill("Smoke project");
  await page.getByRole("radio", { name: "Blue", exact: true }).click();
  await button("Save project").click();
  await expect(
    page.getByRole("textbox", { name: "Project name", exact: true }),
  ).toHaveCount(0);
  await button("Edit project Smoke project").click();
  await page
    .getByRole("textbox", { name: "Project name", exact: true })
    .fill("Renamed project");
  await button("Save project").click();
  await expect(button("Edit project Renamed project")).toBeVisible();
  console.log("PASS: project validation, creation, color and rename.");
  await tab("Tasks").click();
  await button("+ New task").click();
  await button("Save task").click();
  await expect(
    page.getByText("Give your task a title.", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("textbox", { name: "Title", exact: true })
    .fill("Browser smoke task");
  await page
    .getByRole("textbox", { name: "Notes", exact: true })
    .fill("Persistent notes");
  await page
    .getByRole("textbox", { name: "Due date", exact: true })
    .fill("2026-02-30");
  await button("Save task").click();
  await expect(
    page.getByText("Use a real date in YYYY-MM-DD format (1900–9999).", {
      exact: true,
    }),
  ).toBeVisible();
  await button("Due today").click();
  await button("Renamed project").last().click();
  await button("High priority").click();
  await button("Save task").click();
  await expect(
    page.getByRole("textbox", { name: "Title", exact: true }),
  ).toHaveCount(0);
  await button("Edit Browser smoke task").click();
  await page
    .getByRole("textbox", { name: "Title", exact: true })
    .fill("Edited smoke task");
  await button("Save task").click();
  await expect(button("Edit Edited smoke task")).toBeVisible();
  await page
    .getByRole("checkbox", { name: "Complete Edited smoke task", exact: true })
    .click();
  await expect(
    page.getByRole("checkbox", {
      name: "Reopen Edited smoke task",
      exact: true,
    }),
  ).toBeVisible();
  await tab("Settings").click();
  await button("Dark").click();
  await saved();
  await page.reload();
  await expect(tab("Today")).toBeVisible();
  await expect(
    page.getByRole("checkbox", {
      name: "Reopen Edited smoke task",
      exact: true,
    }),
  ).toBeVisible();
  let data = await readData();
  const task = data.tasks.find((t) => t.title === "Edited smoke task");
  assert.equal(task.notes, "Persistent notes");
  assert.equal(task.priority, "high");
  assert.equal(task.completedOn, task.dueDate);
  assert.equal(data.theme, "dark");
  assert.equal(
    data.projects.find((p) => p.id === task.projectId).name,
    "Renamed project",
  );
  await page.screenshot({
    path: "artifacts/persisted-dark-mobile.png",
    fullPage: true,
  });
  console.log(
    "PASS: create, edit, complete, project assignment and theme survive browser reload (real AsyncStorage web adapter).",
  );
  await tab("Progress").click();
  await expect(
    page.getByText("The last seven days", { exact: true }),
  ).toBeVisible();
  await expect(page.getByText("2", { exact: true }).first()).toBeVisible();
  await page.screenshot({
    path: "artifacts/progress-mobile.png",
    fullPage: true,
  });
  await tab("Today").click();
  await page
    .getByRole("checkbox", { name: "Reopen Edited smoke task", exact: true })
    .click();
  await expect(
    page.getByRole("checkbox", {
      name: "Complete Edited smoke task",
      exact: true,
    }),
  ).toBeVisible();
  assert.equal(
    (await readData()).tasks.find((t) => t.id === task.id).completedOn,
    null,
  );
  console.log("PASS: Progress renders and reopening clears completion.");
  await tab("Projects").click();
  await button("Edit project Renamed project").click();
  await button("Delete project").click();
  await button("Cancel").click();
  await expect(button("Edit project Renamed project")).toBeVisible();
  await button("Edit project Renamed project").click();
  await button("Delete project").click();
  await button("Confirm deletion").click();
  await expect(button("Edit project Renamed project")).toHaveCount(0);
  data = await readData();
  assert.equal(data.tasks.length, 6);
  assert.equal(data.tasks.find((t) => t.id === task.id).projectId, null);
  console.log(
    "PASS: project deletion confirmation/cancel, preserving all tasks without assignment.",
  );
  await tab("Tasks").click();
  await page
    .getByRole("textbox", { name: "Search tasks", exact: true })
    .fill("Edited smoke");
  await expect(button("Edit Edited smoke task")).toBeVisible();
  await expect(button("Edit Book a dentist appointment")).toHaveCount(0);
  await button("Completed").click();
  await expect(page.getByText("No tasks here", { exact: true })).toBeVisible();
  await button("Incomplete").click();
  await button("High").click();
  await button("No project").click();
  await expect(button("Edit Edited smoke task")).toBeVisible();
  await button("Edit Edited smoke task").click();
  await button("Delete task").click();
  await button("Cancel").click();
  await expect(button("Edit Edited smoke task")).toBeVisible();
  await button("Edit Edited smoke task").click();
  await button("Delete task").click();
  await button("Confirm deletion").click();
  await expect(button("Edit Edited smoke task")).toHaveCount(0);
  assert.equal((await readData()).tasks.length, 5);
  console.log(
    "PASS: combined search/status/project/priority filters and task deletion confirmation.",
  );
  await tab("Settings").click();
  await button("Reset to demo data").click();
  await button("Cancel").click();
  assert.equal((await readData()).theme, "dark");
  await button("Reset to demo data").click();
  await button("Confirm reset").click();
  await saved();
  assert.equal((await readData()).theme, "system");
  assert.equal((await readData()).tasks.length, 5);
  await button("Light").click();
  await saved();
  await page.reload();
  await expect(tab("Today")).toBeVisible();
  assert.equal((await readData()).theme, "light");
  await page.setViewportSize({ width: 1200, height: 900 });
  await page.screenshot({
    path: "artifacts/today-desktop.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 320, height: 700 });
  await button("+ New task").click();
  await expect(button("Save task")).toBeVisible();
  await page.screenshot({
    path: "artifacts/editor-small-mobile.png",
    fullPage: true,
  });
  await button("Cancel").click();
  assert.deepEqual(errors, [], "no uncaught browser errors");
  console.log(
    "PASS: reset confirmation, light preference persistence, narrow/desktop layout, no uncaught browser errors.",
  );
  console.log("Browser smoke test passed. Screenshots saved under artifacts/.");
} catch (error) {
  if (page)
    await page
      .screenshot({ path: "artifacts/smoke-failure.png", fullPage: true })
      .catch(() => {});
  console.error(error);
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  await new Promise((done) => server.close(done));
  console.log("Browser and temporary static server stopped.");
}
