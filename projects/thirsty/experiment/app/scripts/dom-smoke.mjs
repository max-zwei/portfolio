// Executes the actual Expo web export in JSDOM. This is NOT a real browser or layout test.
import { JSDOM, VirtualConsole } from "jsdom";
import { readFile } from "node:fs/promises";
import {
  getByRole,
  queryByRole,
  getByText,
  waitFor,
} from "@testing-library/dom";
import userEvent from "@testing-library/user-event";
import assert from "node:assert/strict";
const html = await readFile("dist/index.html", "utf8");
const bundlePath = html.match(/<script[^>]+src="([^"]+)"/)[1];
const bundle = await readFile(`dist/${bundlePath.replace(/^\//, "")}`, "utf8");
const windows = [];
const errors = [];
function launch(persisted) {
  const virtualConsole = new VirtualConsole();
  virtualConsole.on("jsdomError", (error) => errors.push(error.message));
  const dom = new JSDOM(html.replace(/<script[^>]*>[\s\S]*?<\/script>/g, ""), {
    url: "http://localhost:8081",
    runScripts: "outside-only",
    pretendToBeVisual: true,
    virtualConsole,
  });
  const { window } = dom;
  globalThis.window = window;
  globalThis.document = window.document;
  window.matchMedia = (query) => ({
    matches: false,
    media: query,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
  });
  window.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
  window.scrollTo = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
  if (persisted) window.localStorage.setItem("pocketplan.v1", persisted);
  window.eval(bundle);
  windows.push(window);
  const user = userEvent.setup({ document: window.document });
  const body = window.document.body;
  return {
    window,
    body,
    user,
    button: (name) => getByRole(body, "button", { name, exact: true }),
    tab: (name) => getByRole(body, "tab", { name, exact: true }),
    input: (name) => getByRole(body, "textbox", { name, exact: true }),
    data: () => JSON.parse(window.localStorage.getItem("pocketplan.v1")),
  };
}
try {
  let app = launch();
  await waitFor(() => assert.ok(app.tab("Today")));
  assert.ok(getByText(app.body, "Overdue", { exact: true }));
  assert.ok(getByText(app.body, "Due today", { exact: true }));
  console.log(
    "PASS (DOM): actual Expo export renders Today with seeded local data.",
  );
  await app.user.click(app.tab("Projects"));
  await app.user.click(app.button("+ Project"));
  await app.user.click(app.button("Save project"));
  assert.ok(getByText(app.body, "Give your project a name.", { exact: true }));
  await app.user.type(app.input("Project name"), "DOM project");
  await app.user.click(
    getByRole(app.body, "radio", { name: "Blue", exact: true }),
  );
  await app.user.click(app.button("Save project"));
  await waitFor(() => assert.ok(app.button("Edit project DOM project")));
  await app.user.click(app.button("Edit project DOM project"));
  await app.user.clear(app.input("Project name"));
  await app.user.type(app.input("Project name"), "Renamed DOM project");
  await app.user.click(app.button("Save project"));
  await waitFor(() =>
    assert.ok(app.button("Edit project Renamed DOM project")),
  );
  await app.user.click(app.tab("Tasks"));
  await app.user.click(app.button("+ New task"));
  await app.user.click(app.button("Save task"));
  assert.ok(getByText(app.body, "Give your task a title.", { exact: true }));
  await app.user.type(app.input("Title"), "DOM task");
  await app.user.type(app.input("Notes"), "Remember these notes");
  await app.user.type(app.input("Due date"), "2026-02-30");
  await app.user.click(app.button("Save task"));
  assert.ok(
    getByText(app.body, "Use a real date in YYYY-MM-DD format (1900–9999).", {
      exact: true,
    }),
  );
  await app.user.click(app.button("Due today"));
  // The filter and editor both contain the project name; the editor is the last matching button.
  const projectButtons = [
    ...app.body.querySelectorAll('[role="button"]'),
  ].filter((e) => e.getAttribute("aria-label") === "Renamed DOM project");
  await app.user.click(projectButtons.at(-1));
  await app.user.click(app.button("High priority"));
  await app.user.click(app.button("Save task"));
  await waitFor(() => assert.ok(app.button("Edit DOM task")));
  await app.user.click(app.button("Edit DOM task"));
  await app.user.clear(app.input("Title"));
  await app.user.type(app.input("Title"), "Edited DOM task");
  await app.user.click(app.button("Save task"));
  await waitFor(() => assert.ok(app.button("Edit Edited DOM task")));
  await app.user.click(
    getByRole(app.body, "checkbox", {
      name: "Complete Edited DOM task",
      exact: true,
    }),
  );
  await waitFor(() =>
    assert.ok(
      getByRole(app.body, "checkbox", {
        name: "Reopen Edited DOM task",
        exact: true,
      }),
    ),
  );
  await app.user.click(app.tab("Settings"));
  await app.user.click(app.button("Dark"));
  await waitFor(() => assert.equal(app.data().theme, "dark"));
  const persisted = app.window.localStorage.getItem("pocketplan.v1");
  app.window.close();
  app = launch(persisted);
  await waitFor(() =>
    assert.ok(
      getByRole(app.body, "checkbox", {
        name: "Reopen Edited DOM task",
        exact: true,
      }),
    ),
  );
  const task = app.data().tasks.find((t) => t.title === "Edited DOM task");
  assert.equal(task.notes, "Remember these notes");
  assert.equal(task.priority, "high");
  assert.equal(task.completedOn, task.dueDate);
  assert.equal(app.data().theme, "dark");
  assert.equal(
    app.data().projects.find((p) => p.id === task.projectId).name,
    "Renamed DOM project",
  );
  console.log(
    "PASS (DOM): task/project creation and edits, validation, completion and theme preserved on remount using real AsyncStorage web adapter.",
  );
  await app.user.click(app.tab("Progress"));
  assert.ok(getByText(app.body, "The last seven days", { exact: true }));
  await app.user.click(app.tab("Today"));
  await app.user.click(
    getByRole(app.body, "checkbox", {
      name: "Reopen Edited DOM task",
      exact: true,
    }),
  );
  await waitFor(() =>
    assert.equal(
      app.data().tasks.find((t) => t.id === task.id).completedOn,
      null,
    ),
  );
  await app.user.click(app.tab("Projects"));
  await app.user.click(app.button("Edit project Renamed DOM project"));
  await app.user.click(app.button("Delete project"));
  await app.user.click(app.button("Cancel"));
  assert.ok(app.button("Edit project Renamed DOM project"));
  await app.user.click(app.button("Edit project Renamed DOM project"));
  await app.user.click(app.button("Delete project"));
  await app.user.click(app.button("Confirm deletion"));
  await waitFor(() =>
    assert.equal(
      queryByRole(app.body, "button", {
        name: "Edit project Renamed DOM project",
        exact: true,
      }),
      null,
    ),
  );
  assert.equal(app.data().tasks.length, 6);
  assert.equal(app.data().tasks.find((t) => t.id === task.id).projectId, null);
  console.log(
    "PASS (DOM): Progress renders, reopening clears completion, project deletion/cancel preserve tasks.",
  );
  await app.user.click(app.tab("Tasks"));
  await app.user.type(app.input("Search tasks"), "Edited DOM");
  assert.ok(app.button("Edit Edited DOM task"));
  assert.equal(
    queryByRole(app.body, "button", {
      name: "Edit Book a dentist appointment",
      exact: true,
    }),
    null,
  );
  await app.user.click(app.button("Completed"));
  assert.ok(getByText(app.body, "No tasks here", { exact: true }));
  await app.user.click(app.button("Incomplete"));
  await app.user.click(app.button("High"));
  await app.user.click(app.button("No project"));
  assert.ok(app.button("Edit Edited DOM task"));
  await app.user.click(app.button("Edit Edited DOM task"));
  await app.user.click(app.button("Delete task"));
  await app.user.click(app.button("Cancel"));
  assert.ok(app.button("Edit Edited DOM task"));
  await app.user.click(app.button("Edit Edited DOM task"));
  await app.user.click(app.button("Delete task"));
  await app.user.click(app.button("Confirm deletion"));
  await waitFor(() => assert.equal(app.data().tasks.length, 5));
  assert.ok(getByText(app.body, "No tasks here", { exact: true }));
  await app.user.click(app.tab("Settings"));
  await app.user.click(app.button("Reset to demo data"));
  await app.user.click(app.button("Cancel"));
  assert.equal(app.data().theme, "dark");
  await app.user.click(app.button("Reset to demo data"));
  await app.user.click(app.button("Confirm reset"));
  await waitFor(() => assert.equal(app.data().theme, "system"));
  assert.equal(app.data().tasks.length, 5);
  await app.user.click(app.button("Light"));
  await waitFor(() => assert.equal(app.data().theme, "light"));
  console.log(
    "PASS (DOM): combined filters, task deletion/cancel, confirmed reset, system/light/dark preferences.",
  );
  app.window.close();
  app = launch("{corrupt");
  await waitFor(() => assert.ok(app.button("Retry loading")));
  assert.equal(app.window.localStorage.getItem("pocketplan.v1"), "{corrupt");
  await app.user.click(app.button("Reset to demo data"));
  await app.user.click(app.button("Cancel"));
  assert.equal(app.window.localStorage.getItem("pocketplan.v1"), "{corrupt");
  await app.user.click(app.button("Reset to demo data"));
  await app.user.click(app.button("Confirm reset"));
  await waitFor(() => assert.ok(app.tab("Today")));
  assert.equal(app.data().tasks.length, 5);
  console.log(
    "PASS (DOM): unreadable storage shows recovery controls, preserves data until confirmed reset.",
  );
  assert.deepEqual(errors, []);
  console.log(
    "DOM integration passed. No browser rendering, screenshots, device or simulator verification is claimed.",
  );
} catch (error) {
  console.error(error);
  process.exitCode = 1;
} finally {
  for (const window of windows) window.close();
}
