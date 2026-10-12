import { test } from "node:test";
import assert from "node:assert/strict";
import {
  dayOffset,
  deleteProject,
  demoData,
  localDay,
  progress,
  taskError,
  todayGroups,
  toggleTask,
  validDay,
} from "../src/model";
import { repository, STORAGE_KEY, Storage } from "../src/persistence";
const today = "2026-03-29";
test("today and overdue use date-only boundaries, preserving completed items for reopening", () => {
  const data = demoData(today);
  data.tasks.push({
    ...data.tasks[0],
    id: "old-done",
    dueDate: "2026-03-28",
    completedOn: today,
  });
  const groups = todayGroups(data.tasks, today);
  assert.deepEqual(
    groups.today.map((t) => t.id),
    ["a", "b"],
  );
  assert.deepEqual(
    groups.overdue.map((t) => t.id),
    ["c", "old-done"],
  );
  assert.ok(
    ![...groups.today, ...groups.overdue].some(
      (t) => t.id === "d" || t.id === "e",
    ),
  );
  assert.deepEqual(todayGroups([], today), { overdue: [], today: [] });
});
test("local calendar formatting and seven-day offsets handle DST, month and year boundaries", () => {
  const original = process.env.TZ;
  try {
    for (const zone of [
      "Europe/Berlin",
      "America/Los_Angeles",
      "Pacific/Auckland",
    ]) {
      process.env.TZ = zone;
      assert.equal(localDay(new Date(2026, 2, 29, 0, 5)), today);
      assert.equal(dayOffset(today, -1), "2026-03-28");
      assert.equal(dayOffset("2026-10-25", 1), "2026-10-26");
      assert.equal(dayOffset("2026-01-01", -1), "2025-12-31");
      assert.deepEqual(
        progress(demoData(today), today).days.map((d) => d.date),
        [
          "2026-03-23",
          "2026-03-24",
          "2026-03-25",
          "2026-03-26",
          "2026-03-27",
          "2026-03-28",
          today,
        ],
      );
    }
  } finally {
    if (original === undefined) delete process.env.TZ;
    else process.env.TZ = original;
  }
});
test("date and title validation reject invalid input and accept leap days", () => {
  for (const date of [
    "2026-02-29",
    "2026-04-31",
    "2026-13-01",
    "2026-00-10",
    "2026-1-01",
    "0001-01-01",
  ])
    assert.equal(validDay(date), false);
  assert.equal(validDay("2028-02-29"), true);
  assert.ok(taskError({ title: "   ", dueDate: null }));
  assert.ok(taskError({ title: "Task", dueDate: "2026-02-30" }));
  assert.equal(taskError({ title: "Task", dueDate: null }), null);
});
test("complete, reopen and recomplete update totals and completion calendar day", () => {
  const original = demoData(today);
  const completed = toggleTask(original, "a", today);
  assert.equal(original.tasks[0].completedOn, null);
  assert.equal(completed.tasks[0].completedOn, today);
  assert.equal(progress(completed, today).completed, 2);
  assert.equal(progress(completed, today).remaining, 3);
  assert.equal(progress(completed, today).days[6].count, 1);
  const reopened = toggleTask(completed, "a", "2026-03-30");
  assert.equal(reopened.tasks[0].completedOn, null);
  assert.equal(progress(reopened, today).days[6].count, 0);
  assert.equal(progress(reopened, today).completed, 1);
  const again = toggleTask(reopened, "a", "2026-03-30");
  assert.equal(progress(again, "2026-03-30").days[6].count, 1);
  assert.equal(progress(again, "2026-03-30").days[5].count, 0);
});
test("project deletion removes only assignment and preserves all tasks and their completion", () => {
  const original = demoData(today);
  const next = deleteProject(original, "work");
  assert.equal(next.projects.length, 1);
  assert.equal(next.tasks.length, original.tasks.length);
  assert.deepEqual(
    next.tasks,
    original.tasks.map((t) =>
      t.projectId === "work" ? { ...t, projectId: null } : t,
    ),
  );
  assert.equal(original.projects.length, 2);
});
test("progress excludes completions older than seven days and future completions from chart", () => {
  const data = demoData(today);
  data.tasks[0].completedOn = "2026-03-22";
  data.tasks[1].completedOn = "2026-03-30";
  const p = progress(data, today);
  assert.equal(p.completed, 3);
  assert.equal(
    p.days.reduce((sum, d) => sum + d.count, 0),
    1,
  );
});
class MemoryStorage implements Storage {
  values = new Map<string, string>();
  writes = 0;
  async getItem(key: string) {
    return this.values.get(key) ?? null;
  }
  async setItem(key: string, value: string) {
    this.values.set(key, value);
    this.writes++;
  }
}
test("persistence seeds once, roundtrips edits, completion, project deletion and theme across instances", async () => {
  const storage = new MemoryStorage();
  const first = repository(storage);
  let data = await first.load();
  assert.equal(storage.writes, 1);
  data = toggleTask(data, "a", today);
  data = deleteProject(data, "work");
  data.theme = "dark";
  data.tasks[0].title = "An edited title";
  data.tasks.push({
    ...data.tasks[0],
    id: "new",
    title: "A new task",
    completedOn: null,
  });
  await first.save(data);
  assert.deepEqual(await repository(storage).load(), data);
  assert.equal(storage.writes, 2);
  await first.save({ ...data, tasks: [], projects: [] });
  assert.deepEqual((await repository(storage).load()).tasks, []);
  assert.equal(storage.writes, 3, "empty user data must not trigger reseeding");
});
test("persistence surfaces read/write errors and never overwrites corrupt data with seeds", async () => {
  const storage = new MemoryStorage();
  storage.values.set(STORAGE_KEY, "{broken");
  await assert.rejects(repository(storage).load());
  assert.equal(storage.writes, 0);
  storage.values.set(STORAGE_KEY, JSON.stringify({ version: 2 }));
  await assert.rejects(repository(storage).load());
  assert.equal(storage.writes, 0);
  const failing: Storage = {
    async getItem() {
      throw new Error("blocked read");
    },
    async setItem() {
      throw new Error("quota exceeded");
    },
  };
  await assert.rejects(repository(failing).load(), /blocked read/);
  await assert.rejects(repository(failing).save(demoData()), /quota exceeded/);
});
