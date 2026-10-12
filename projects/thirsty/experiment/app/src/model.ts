export type Theme = "system" | "light" | "dark";
export type Task = {
  id: string;
  title: string;
  notes: string;
  projectId: string | null;
  dueDate: string | null;
  priority: "normal" | "high";
  completedOn: string | null;
};
export type Project = { id: string; name: string; color: string };
export type Data = {
  version: 1;
  tasks: Task[];
  projects: Project[];
  theme: Theme;
};
export const colors = [
  "#497C69",
  "#5B73B9",
  "#B36B49",
  "#9869A8",
  "#B08A32",
  "#BB5873",
];
export function localDay(date = new Date()): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}
export function dayOffset(day: string, offset: number): string {
  const [y, m, d] = day.split("-").map(Number);
  return localDay(new Date(y, m - 1, d + offset, 12));
}
export function validDay(day: string): boolean {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return false;
  const [y, m, d] = day.split("-").map(Number);
  return y >= 1900 && y <= 9999 && localDay(new Date(y, m - 1, d, 12)) === day;
}
export function todayGroups(tasks: Task[], day = localDay()) {
  return {
    overdue: tasks.filter((t) => t.dueDate && t.dueDate < day),
    today: tasks.filter((t) => t.dueDate === day),
  };
}
export function toggleTask(data: Data, id: string, day = localDay()): Data {
  return {
    ...data,
    tasks: data.tasks.map((t) =>
      t.id === id ? { ...t, completedOn: t.completedOn ? null : day } : t,
    ),
  };
}
export function deleteProject(data: Data, id: string): Data {
  return {
    ...data,
    projects: data.projects.filter((p) => p.id !== id),
    tasks: data.tasks.map((t) =>
      t.projectId === id ? { ...t, projectId: null } : t,
    ),
  };
}
export function progress(data: Data, day = localDay()) {
  const completed = data.tasks.filter((t) => t.completedOn).length;
  return {
    completed,
    remaining: data.tasks.length - completed,
    days: Array.from({ length: 7 }, (_, i) => {
      const date = dayOffset(day, i - 6);
      return {
        date,
        count: data.tasks.filter((t) => t.completedOn === date).length,
      };
    }),
  };
}
export function taskError(
  task: Pick<Task, "title" | "dueDate">,
): string | null {
  if (!task.title.trim()) return "Give your task a title.";
  if (task.dueDate && !validDay(task.dueDate))
    return "Use a real date in YYYY-MM-DD format (1900–9999).";
  return null;
}
export function demoData(day = localDay()): Data {
  return {
    version: 1,
    theme: "system",
    projects: [
      { id: "personal", name: "Personal", color: colors[0] },
      { id: "work", name: "Work", color: colors[1] },
    ],
    tasks: [
      {
        id: "a",
        title: "Plan a little time for yourself",
        notes: "A walk, a book, or a quiet cup of coffee.",
        projectId: "personal",
        dueDate: day,
        priority: "normal",
        completedOn: null,
      },
      {
        id: "b",
        title: "Write down this week’s priorities",
        notes: "Keep the list short and achievable.",
        projectId: "work",
        dueDate: day,
        priority: "high",
        completedOn: null,
      },
      {
        id: "c",
        title: "Book a dentist appointment",
        notes: "",
        projectId: "personal",
        dueDate: dayOffset(day, -1),
        priority: "normal",
        completedOn: null,
      },
      {
        id: "d",
        title: "Tidy up the desk",
        notes: "",
        projectId: "work",
        dueDate: null,
        priority: "normal",
        completedOn: dayOffset(day, -2),
      },
      {
        id: "e",
        title: "Pick a recipe for the weekend",
        notes: "",
        projectId: "personal",
        dueDate: dayOffset(day, 2),
        priority: "normal",
        completedOn: null,
      },
    ],
  };
}
