import { Data, demoData, validDay } from "./model";
export const STORAGE_KEY = "pocketplan.v1";
export interface Storage {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
}
function validate(value: unknown): asserts value is Data {
  const d = value as Data;
  if (
    !d ||
    d.version !== 1 ||
    !["system", "light", "dark"].includes(d.theme) ||
    !Array.isArray(d.tasks) ||
    !Array.isArray(d.projects)
  )
    throw new Error("Stored data is not compatible.");
  if (
    d.projects.some(
      (p) =>
        !p ||
        typeof p.id !== "string" ||
        typeof p.name !== "string" ||
        !/^#[0-9a-f]{6}$/i.test(p.color),
    )
  )
    throw new Error("Invalid stored project.");
  if (
    d.tasks.some(
      (t) =>
        !t ||
        typeof t.id !== "string" ||
        typeof t.title !== "string" ||
        !t.title.trim() ||
        typeof t.notes !== "string" ||
        !["normal", "high"].includes(t.priority) ||
        !(
          t.projectId === null || d.projects.some((p) => p.id === t.projectId)
        ) ||
        !(
          t.dueDate === null ||
          (typeof t.dueDate === "string" && validDay(t.dueDate))
        ) ||
        !(
          t.completedOn === null ||
          (typeof t.completedOn === "string" && validDay(t.completedOn))
        ),
    )
  )
    throw new Error("Invalid stored task.");
}
export function repository(storage: Storage) {
  return {
    async load(): Promise<Data> {
      const raw = await storage.getItem(STORAGE_KEY);
      if (raw !== null) {
        const data: unknown = JSON.parse(raw);
        validate(data);
        return data;
      }
      const data = demoData();
      await storage.setItem(STORAGE_KEY, JSON.stringify(data));
      return data;
    },
    async save(data: Data) {
      validate(data);
      await storage.setItem(STORAGE_KEY, JSON.stringify(data));
    },
  };
}
