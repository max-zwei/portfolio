import React, { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  AppState,
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  useColorScheme,
} from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  colors,
  Data,
  deleteProject,
  demoData,
  localDay,
  progress,
  Project,
  Task,
  taskError,
  Theme,
  todayGroups,
  toggleTask,
} from "./src/model";
import { repository } from "./src/persistence";
const repo = repository(AsyncStorage);
const tabs = ["Today", "Tasks", "Projects", "Progress", "Settings"] as const;
const icons = ["◷", "☷", "▦", "▥", "⚙"];
type Tab = (typeof tabs)[number];
const uid = () =>
  `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
export default function App() {
  return (
    <SafeAreaProvider>
      <PocketPlan />
    </SafeAreaProvider>
  );
}
function PocketPlan() {
  const system = useColorScheme();
  const [data, setData] = useState<Data | null>(null);
  const [loadError, setLoadError] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const saving = useRef(false);
  const [day, setDay] = useState(localDay());
  const [tab, setTab] = useState<Tab>("Today");
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("all");
  const [projectFilter, setProjectFilter] = useState("all");
  const [priority, setPriority] = useState("all");
  const [task, setTask] = useState<Task | null>(null);
  const [project, setProject] = useState<Project | null>(null);
  const [editorError, setEditorError] = useState("");
  const [confirm, setConfirm] = useState<{
    title: string;
    body: string;
    action: () => Promise<void>;
  } | null>(null);
  const dark =
    data?.theme === "dark" || (data?.theme !== "light" && system === "dark");
  const c = dark
    ? {
        bg: "#151E1B",
        card: "#202D27",
        text: "#F0F4EF",
        muted: "#ADBDB4",
        line: "#3D5045",
        accent: "#A9D9B7",
        tint: "#2E4839",
        red: "#FFAAA0",
      }
    : {
        bg: "#F6F7F2",
        card: "#FFFFFF",
        text: "#213C30",
        muted: "#617267",
        line: "#DCE4DB",
        accent: "#315F48",
        tint: "#E5EEDF",
        red: "#A23F35",
      };
  const load = async () => {
    setLoadError(false);
    setError("");
    try {
      setData(await repo.load());
    } catch {
      setLoadError(true);
      setError(
        "Could not read your saved plan. Retry, or reset it to demo data.",
      );
    }
  };
  useEffect(() => {
    void load();
    const timer = setInterval(() => setDay(localDay()), 30000);
    const subscription = AppState.addEventListener("change", () =>
      setDay(localDay()),
    );
    return () => {
      clearInterval(timer);
      subscription.remove();
    };
  }, []);
  async function commit(next: Data): Promise<boolean> {
    if (saving.current) return false;
    saving.current = true;
    setBusy(true);
    setError("");
    try {
      await repo.save(next);
      setData(next);
      return true;
    } catch {
      setError("Could not save your changes. Please try again.");
      return false;
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }
  const text = (value: string, style?: object) => (
    <Text style={[{ color: c.text }, style]}>{value}</Text>
  );
  const button = (
    label: string,
    onPress: () => void,
    selected = false,
    danger = false,
  ) => (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityState={{ selected, disabled: busy }}
      disabled={busy}
      onPress={onPress}
      style={({ pressed }) => [
        s.button,
        {
          backgroundColor: selected ? c.accent : c.card,
          borderColor: danger ? c.red : c.line,
          opacity: pressed || busy ? 0.6 : 1,
        },
      ]}
    >
      <Text
        style={{
          color: selected
            ? dark
              ? "#15251C"
              : "#FFFFFF"
            : danger
              ? c.red
              : c.text,
          fontWeight: "600",
        }}
      >
        {label}
      </Text>
    </Pressable>
  );
  const empty = (title: string, subtitle: string) => (
    <View style={[s.empty, { borderColor: c.line }]}>
      {text(title, s.emptyTitle)}
      {text(subtitle, { color: c.muted, textAlign: "center", lineHeight: 22 })}
    </View>
  );
  const startTask = (existing?: Task) => {
    setEditorError("");
    setTask(
      existing || {
        id: uid(),
        title: "",
        notes: "",
        dueDate: null,
        projectId: null,
        priority: "normal",
        completedOn: null,
      },
    );
  };
  const startProject = (existing?: Project) => {
    setEditorError("");
    setProject(existing || { id: uid(), name: "", color: colors[0] });
  };
  const field = (
    label: string,
    value: string,
    onChangeText: (v: string) => void,
    multiline = false,
    placeholder = "",
  ) => (
    <View style={s.field}>
      {text(label, s.label)}
      <TextInput
        accessibilityLabel={label}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={c.muted}
        multiline={multiline}
        style={[
          s.input,
          { color: c.text, backgroundColor: c.bg, borderColor: c.line },
          multiline && { minHeight: 100, textAlignVertical: "top" },
        ]}
        maxLength={multiline ? 5000 : 200}
        autoCapitalize={label === "Due date" ? "none" : "sentences"}
        returnKeyType={multiline ? "default" : "done"}
      />
    </View>
  );
  const modal = (
    visible: boolean,
    close: () => void,
    content: React.ReactNode,
  ) => (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={() => {
        if (!busy) close();
      }}
    >
      <SafeAreaView style={s.overlay}>
        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? "padding" : "height"}
          style={s.modalWrap}
        >
          <View style={[s.modalCard, { backgroundColor: c.card }]}>
            <ScrollView
              keyboardShouldPersistTaps="handled"
              contentContainerStyle={s.modalContent}
            >
              {content}
            </ScrollView>
          </View>
        </KeyboardAvoidingView>
      </SafeAreaView>
    </Modal>
  );
  const reset = () =>
    setConfirm({
      title: "Reset your plan?",
      body: "This removes all your tasks, projects and settings and restores the demo plan. This cannot be undone.",
      action: async () => {
        if (await commit(demoData())) {
          setLoadError(false);
          setProjectFilter("all");
          setStatus("all");
          setPriority("all");
          setSearch("");
          setConfirm(null);
        }
      },
    });
  if (!data)
    return (
      <SafeAreaView style={[s.root, { backgroundColor: c.bg }]}>
        <View style={s.empty}>
          {text("PocketPlan", s.title)}
          {loadError ? (
            <>
              {text(error)}
              {button("Retry loading", () => void load())}
              {button("Reset to demo data", reset, false, true)}
            </>
          ) : (
            <>
              <ActivityIndicator color={c.accent} />
              {text("Opening your plan…")}
            </>
          )}
        </View>
        {modal(
          !!confirm,
          () => setConfirm(null),
          <>
            {text(confirm?.title || "", s.section)}
            {text(confirm?.body || "")}
            <View style={s.row}>
              {button("Cancel", () => setConfirm(null))}
              {button(
                "Confirm reset",
                () => void confirm?.action(),
                false,
                true,
              )}
            </View>
            {!!error && text(error, { color: c.red })}
          </>,
        )}
      </SafeAreaView>
    );
  const row = (t: Task) => {
    const p = data.projects.find((p) => p.id === t.projectId);
    return (
      <View
        key={t.id}
        style={[s.taskRow, { backgroundColor: c.card, borderColor: c.line }]}
      >
        <Pressable
          accessibilityRole="checkbox"
          accessibilityLabel={`${t.completedOn ? "Reopen" : "Complete"} ${t.title}`}
          accessibilityState={{ checked: !!t.completedOn, disabled: busy }}
          disabled={busy}
          onPress={() => void commit(toggleTask(data, t.id))}
          style={s.checkTouch}
        >
          <View
            style={[
              s.check,
              {
                backgroundColor: t.completedOn ? c.accent : "transparent",
                borderColor: t.completedOn ? c.accent : c.muted,
              },
            ]}
          >
            {t.completedOn && (
              <Text style={{ color: dark ? "#15251C" : "white" }}>✓</Text>
            )}
          </View>
        </Pressable>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`Edit ${t.title}`}
          onPress={() => startTask(t)}
          style={s.taskBody}
        >
          {text(t.title, {
            fontSize: 16,
            fontWeight: "600",
            textDecorationLine: t.completedOn ? "line-through" : "none",
            color: t.completedOn ? c.muted : c.text,
          })}
          <View style={s.meta}>
            {p && (
              <View style={s.meta}>
                <View style={[s.dot, { backgroundColor: p.color }]} />
                {text(p.name, { color: c.muted, fontSize: 12 })}
              </View>
            )}
            {t.dueDate &&
              text(t.dueDate === day ? "Today" : t.dueDate, {
                color: c.muted,
                fontSize: 12,
              })}
            {t.priority === "high" &&
              text("↑ High priority", { color: c.red, fontSize: 12 })}
            {t.completedOn &&
              text("Completed", { color: c.muted, fontSize: 12 })}
          </View>
        </Pressable>
        <Text style={{ color: c.muted }}>›</Text>
      </View>
    );
  };
  const groups = todayGroups(data.tasks, day);
  const stats = progress(data, day);
  const filtered = data.tasks.filter(
    (t) =>
      (!search ||
        `${t.title} ${t.notes}`.toLowerCase().includes(search.toLowerCase())) &&
      (status === "all" ||
        (status === "done" ? !!t.completedOn : !t.completedOn)) &&
      (projectFilter === "all" ||
        t.projectId === (projectFilter === "none" ? null : projectFilter)) &&
      (priority === "all" || t.priority === priority),
  );
  return (
    <SafeAreaView
      style={[s.root, { backgroundColor: c.bg }]}
      edges={["top", "bottom"]}
    >
      <StatusBar style={dark ? "light" : "dark"} />
      <View style={s.shell}>
        <View style={[s.brand, { borderColor: c.line }]}>
          {text("◈  PocketPlan", { fontWeight: "700", fontSize: 19 })}
          {text("A little plan. A clearer day.", {
            color: c.muted,
            fontSize: 12,
          })}
        </View>
        <ScrollView
          style={s.content}
          keyboardShouldPersistTaps="handled"
          contentContainerStyle={s.contentInner}
        >
          <View style={s.heading}>
            <View style={{ flex: 1 }}>
              {text(tab, s.title)}
              {text(
                {
                  Today: new Date(`${day}T12:00:00`).toLocaleDateString(
                    undefined,
                    { weekday: "long", month: "long", day: "numeric" },
                  ),
                  Tasks: "Everything on your mind, in one place.",
                  Projects: "Make room for what matters.",
                  Progress: "Small steps add up.",
                  Settings: "Make PocketPlan feel like you.",
                }[tab],
                { color: c.muted, lineHeight: 22 },
              )}
            </View>
            {(tab === "Today" || tab === "Tasks") &&
              button("+ New task", () => startTask(), true)}
            {tab === "Projects" &&
              button("+ Project", () => startProject(), true)}
          </View>
          {!!error && (
            <View
              accessibilityRole="alert"
              style={[s.notice, { backgroundColor: c.tint }]}
            >
              {text(error, { color: c.red })}
            </View>
          )}
          {busy && text("Saving…", { color: c.muted })}
          {tab === "Today" && (
            <>
              <View style={[s.summary, { backgroundColor: c.tint }]}>
                {text("One thing at a time.", {
                  fontSize: 21,
                  fontWeight: "600",
                })}
                {text(
                  `${groups.today.filter((t) => !t.completedOn).length} to do today · ${groups.overdue.filter((t) => !t.completedOn).length} overdue`,
                  { color: c.muted },
                )}
              </View>
              {text("Overdue", s.section)}
              {groups.overdue.length
                ? groups.overdue.map(row)
                : empty(
                    "All caught up",
                    "No overdue tasks. Enjoy the breathing room.",
                  )}
              {text("Due today", s.section)}
              {groups.today.length
                ? groups.today.map(row)
                : empty(
                    "A clear day ahead",
                    "Add a task with today’s date to start your plan.",
                  )}
            </>
          )}
          {tab === "Tasks" && (
            <>
              {field(
                "Search tasks",
                search,
                setSearch,
                false,
                "Search titles and notes…",
              )}
              {text("Status", s.label)}
              <View style={s.row}>
                {button("All tasks", () => setStatus("all"), status === "all")}
                {button(
                  "Incomplete",
                  () => setStatus("open"),
                  status === "open",
                )}
                {button(
                  "Completed",
                  () => setStatus("done"),
                  status === "done",
                )}
              </View>
              {text("Project filter", s.label)}
              <View style={s.row}>
                {button(
                  "All projects",
                  () => setProjectFilter("all"),
                  projectFilter === "all",
                )}
                {button(
                  "No project",
                  () => setProjectFilter("none"),
                  projectFilter === "none",
                )}
                {data.projects.map((p) => (
                  <React.Fragment key={p.id}>
                    {button(
                      p.name,
                      () => setProjectFilter(p.id),
                      projectFilter === p.id,
                    )}
                  </React.Fragment>
                ))}
              </View>
              {text("Priority filter", s.label)}
              <View style={s.row}>
                {["all", "normal", "high"].map((p) => (
                  <React.Fragment key={p}>
                    {button(
                      p === "all"
                        ? "Any priority"
                        : p === "high"
                          ? "High"
                          : "Normal",
                      () => setPriority(p),
                      priority === p,
                    )}
                  </React.Fragment>
                ))}
              </View>
              {text(
                `${filtered.length} ${filtered.length === 1 ? "task" : "tasks"}`,
                s.section,
              )}
              {filtered.length
                ? filtered.map(row)
                : empty(
                    "No tasks here",
                    "Try a different filter, or add your first task.",
                  )}
            </>
          )}
          {tab === "Projects" && (
            <>
              {data.projects.length
                ? data.projects.map((p) => (
                    <Pressable
                      key={p.id}
                      accessibilityRole="button"
                      accessibilityLabel={`Edit project ${p.name}`}
                      onPress={() => startProject(p)}
                      style={[
                        s.projectCard,
                        { backgroundColor: c.card, borderColor: c.line },
                      ]}
                    >
                      <View
                        style={[s.projectIcon, { backgroundColor: p.color }]}
                      >
                        <Text style={{ color: "white", fontSize: 22 }}>▦</Text>
                      </View>
                      <View style={{ flex: 1 }}>
                        {text(p.name, { fontSize: 18, fontWeight: "600" })}
                        {text(
                          `${data.tasks.filter((t) => t.projectId === p.id && !t.completedOn).length} incomplete tasks`,
                          { color: c.muted, marginTop: 5 },
                        )}
                      </View>
                      {text("›")}
                    </Pressable>
                  ))
                : empty(
                    "Start with a project",
                    "Group related tasks with a name and a color.",
                  )}
              {text(
                "Deleting a project keeps its tasks. They become unassigned.",
                { color: c.muted, lineHeight: 22, marginTop: 16 },
              )}
            </>
          )}
          {tab === "Progress" && (
            <>
              <View style={s.row}>
                <View style={[s.stat, { backgroundColor: c.tint }]}>
                  {text(String(stats.completed), s.number)}
                  {text("Completed", { color: c.muted })}
                </View>
                <View style={[s.stat, { backgroundColor: c.card }]}>
                  {text(String(stats.remaining), s.number)}
                  {text("Remaining", { color: c.muted })}
                </View>
              </View>
              <View
                style={[
                  s.chartCard,
                  { backgroundColor: c.card, borderColor: c.line },
                ]}
              >
                {text("The last seven days", s.section)}
                {text("Tasks completed each local calendar day", {
                  color: c.muted,
                })}
                <View style={s.chart}>
                  {stats.days.map((d) => (
                    <View
                      key={d.date}
                      accessibilityLabel={`${d.date}: ${d.count} completed tasks`}
                      style={s.barColumn}
                    >
                      {text(String(d.count), { fontWeight: "600" })}
                      <View style={s.barTrack}>
                        <View
                          style={{
                            width: "70%",
                            height: d.count
                              ? Math.max(
                                  8,
                                  (d.count /
                                    Math.max(
                                      1,
                                      ...stats.days.map((v) => v.count),
                                    )) *
                                    100,
                                )
                              : 3,
                            backgroundColor: d.count ? c.accent : c.line,
                            borderRadius: 5,
                          }}
                        />
                      </View>
                      {text(
                        new Date(`${d.date}T12:00:00`).toLocaleDateString(
                          undefined,
                          { weekday: "short" },
                        ),
                        { fontSize: 11, color: c.muted },
                      )}
                      {text(d.date.slice(5), { fontSize: 10, color: c.muted })}
                    </View>
                  ))}
                </View>
              </View>
              {data.tasks.length === 0 &&
                empty(
                  "Your progress starts here",
                  "Add a task, then complete it to see your progress.",
                )}
              {text(
                "Completing a task records today. Reopening removes that completion; completing it again records the new day.",
                { color: c.muted, lineHeight: 22, marginTop: 20 },
              )}
            </>
          )}
          {tab === "Settings" && (
            <>
              <View
                style={[
                  s.chartCard,
                  { backgroundColor: c.card, borderColor: c.line },
                ]}
              >
                {text("Appearance", s.section)}
                {text("Choose the theme that feels right.", { color: c.muted })}
                <View style={s.row}>
                  {(["system", "light", "dark"] as Theme[]).map((theme) => (
                    <React.Fragment key={theme}>
                      {button(
                        theme[0].toUpperCase() + theme.slice(1),
                        () => void commit({ ...data, theme }),
                        data.theme === theme,
                      )}
                    </React.Fragment>
                  ))}
                </View>
              </View>
              <View
                style={[
                  s.chartCard,
                  {
                    backgroundColor: c.card,
                    borderColor: c.line,
                    marginTop: 20,
                  },
                ]}
              >
                {text("A fresh start", s.section)}
                {text(
                  "Restore the sample plan. Your current tasks, projects and theme preference will be replaced.",
                  { color: c.muted, lineHeight: 22 },
                )}
                <View style={s.row}>
                  {button("Reset to demo data", reset, false, true)}
                </View>
              </View>
              {text("Stored on this device", s.section)}
              {text(
                "Your plan is saved locally. No account needed. Web data stays in this browser; clearing its storage removes the plan.",
                { color: c.muted, lineHeight: 22 },
              )}
            </>
          )}
        </ScrollView>
        <View style={[s.nav, { backgroundColor: c.card, borderColor: c.line }]}>
          {tabs.map((t, i) => (
            <Pressable
              key={t}
              accessibilityRole="tab"
              accessibilityLabel={t}
              accessibilityState={{ selected: tab === t }}
              onPress={() => setTab(t)}
              style={[
                s.navItem,
                { backgroundColor: tab === t ? c.tint : "transparent" },
              ]}
            >
              {text(icons[i], {
                color: tab === t ? c.accent : c.muted,
                fontSize: 23,
              })}
              {text(t, {
                color: tab === t ? c.accent : c.muted,
                fontSize: 11,
                fontWeight: "600",
              })}
            </Pressable>
          ))}
        </View>
      </View>
      {modal(
        !!task,
        () => setTask(null),
        task && (
          <>
            {text(
              data.tasks.some((t) => t.id === task.id)
                ? "Edit task"
                : "New task",
              s.section,
            )}
            {field(
              "Title",
              task.title,
              (title) => setTask({ ...task, title }),
              false,
              "What would you like to do?",
            )}
            {field(
              "Notes",
              task.notes,
              (notes) => setTask({ ...task, notes }),
              true,
              "Optional details",
            )}
            {field(
              "Due date",
              task.dueDate || "",
              (dueDate) => setTask({ ...task, dueDate: dueDate || null }),
              false,
              "YYYY-MM-DD · optional",
            )}
            <View style={s.row}>
              {button("Due today", () => setTask({ ...task, dueDate: day }))}
              {button("Clear date", () => setTask({ ...task, dueDate: null }))}
            </View>
            {text("Project", s.label)}
            <View style={s.row}>
              {button(
                "Unassigned",
                () => setTask({ ...task, projectId: null }),
                task.projectId === null,
              )}
              {data.projects.map((p) => (
                <React.Fragment key={p.id}>
                  {button(
                    p.name,
                    () => setTask({ ...task, projectId: p.id }),
                    task.projectId === p.id,
                  )}
                </React.Fragment>
              ))}
            </View>
            {text("Priority", s.label)}
            <View style={s.row}>
              {button(
                "Normal priority",
                () => setTask({ ...task, priority: "normal" }),
                task.priority === "normal",
              )}
              {button(
                "High priority",
                () => setTask({ ...task, priority: "high" }),
                task.priority === "high",
              )}
            </View>
            {task.completedOn &&
              text(`Completed on ${task.completedOn}`, { color: c.muted })}
            {!!editorError && (
              <Text accessibilityRole="alert" style={{ color: c.red }}>
                {editorError}
              </Text>
            )}
            {!!error && text(error, { color: c.red })}
            <View style={s.row}>
              {button("Cancel", () => setTask(null))}
              {button(
                "Save task",
                () => {
                  const e = taskError(task);
                  if (e) {
                    setEditorError(e);
                    return;
                  }
                  const next = { ...task, title: task.title.trim() };
                  void commit({
                    ...data,
                    tasks: data.tasks.some((t) => t.id === task.id)
                      ? data.tasks.map((t) => (t.id === task.id ? next : t))
                      : [...data.tasks, next],
                  }).then((ok) => {
                    if (ok) setTask(null);
                  });
                },
                true,
              )}
            </View>
            {data.tasks.some((t) => t.id === task.id) &&
              button(
                "Delete task",
                () => {
                  const id = task.id;
                  setTask(null);
                  setConfirm({
                    title: "Delete this task?",
                    body: `“${task.title}” will be permanently removed.`,
                    action: async () => {
                      if (
                        await commit({
                          ...data,
                          tasks: data.tasks.filter((t) => t.id !== id),
                        })
                      )
                        setConfirm(null);
                    },
                  });
                },
                false,
                true,
              )}
          </>
        ),
      )}
      {modal(
        !!project,
        () => setProject(null),
        project && (
          <>
            {text(
              data.projects.some((p) => p.id === project.id)
                ? "Edit project"
                : "New project",
              s.section,
            )}
            {field(
              "Project name",
              project.name,
              (name) => setProject({ ...project, name }),
              false,
              "e.g. Personal",
            )}
            {text("Project color", s.label)}
            <View style={s.row}>
              {colors.map((color, i) => (
                <Pressable
                  key={color}
                  accessibilityRole="radio"
                  accessibilityLabel={
                    ["Green", "Blue", "Terracotta", "Purple", "Gold", "Rose"][i]
                  }
                  accessibilityState={{ checked: project.color === color }}
                  onPress={() => setProject({ ...project, color })}
                  style={[
                    s.swatch,
                    {
                      backgroundColor: color,
                      borderColor:
                        project.color === color ? c.text : "transparent",
                    },
                  ]}
                >
                  <Text style={{ color: "white" }}>
                    {project.color === color ? "✓" : ""}
                  </Text>
                </Pressable>
              ))}
            </View>
            {!!editorError && (
              <Text accessibilityRole="alert" style={{ color: c.red }}>
                {editorError}
              </Text>
            )}
            {!!error && text(error, { color: c.red })}
            <View style={s.row}>
              {button("Cancel", () => setProject(null))}
              {button(
                "Save project",
                () => {
                  if (!project.name.trim()) {
                    setEditorError("Give your project a name.");
                    return;
                  }
                  const next = { ...project, name: project.name.trim() };
                  void commit({
                    ...data,
                    projects: data.projects.some((p) => p.id === project.id)
                      ? data.projects.map((p) =>
                          p.id === project.id ? next : p,
                        )
                      : [...data.projects, next],
                  }).then((ok) => {
                    if (ok) setProject(null);
                  });
                },
                true,
              )}
            </View>
            {data.projects.some((p) => p.id === project.id) &&
              button(
                "Delete project",
                () => {
                  const id = project.id;
                  setProject(null);
                  setConfirm({
                    title: "Delete this project?",
                    body: `“${project.name}” will be removed. Its tasks will be kept with no project assignment.`,
                    action: async () => {
                      if (await commit(deleteProject(data, id))) {
                        setProjectFilter("all");
                        setConfirm(null);
                      }
                    },
                  });
                },
                false,
                true,
              )}
          </>
        ),
      )}
      {modal(
        !!confirm,
        () => setConfirm(null),
        <>
          {text(confirm?.title || "", s.section)}
          {text(confirm?.body || "", { lineHeight: 24 })}
          {!!error && text(error, { color: c.red })}
          <View style={s.row}>
            {button("Cancel", () => setConfirm(null))}
            {button(
              confirm?.title === "Reset your plan?"
                ? "Confirm reset"
                : "Confirm deletion",
              () => void confirm?.action(),
              false,
              true,
            )}
          </View>
        </>,
      )}
    </SafeAreaView>
  );
}
const s = StyleSheet.create({
  root: { flex: 1 },
  shell: { flex: 1, width: "100%", maxWidth: 760, alignSelf: "center" },
  brand: {
    paddingHorizontal: 22,
    paddingVertical: 18,
    borderBottomWidth: 1,
    gap: 5,
  },
  content: { flex: 1 },
  contentInner: { padding: 22, paddingBottom: 32 },
  heading: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    marginBottom: 24,
  },
  title: { fontSize: 34, fontWeight: "700", marginBottom: 5 },
  section: { fontSize: 18, fontWeight: "700", marginTop: 18, marginBottom: 12 },
  label: { fontSize: 13, fontWeight: "600", marginBottom: 8 },
  button: {
    minHeight: 44,
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderRadius: 12,
    borderWidth: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  row: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginVertical: 12 },
  summary: { borderRadius: 18, padding: 23, gap: 9 },
  taskRow: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderWidth: 1,
    borderRadius: 15,
    marginBottom: 10,
    gap: 8,
  },
  checkTouch: {
    minWidth: 44,
    minHeight: 48,
    justifyContent: "center",
    alignItems: "center",
  },
  check: {
    width: 25,
    height: 25,
    borderRadius: 8,
    borderWidth: 1.5,
    alignItems: "center",
    justifyContent: "center",
  },
  taskBody: { flex: 1, paddingVertical: 8, minHeight: 48 },
  meta: {
    flexDirection: "row",
    alignItems: "center",
    flexWrap: "wrap",
    gap: 8,
    marginTop: 5,
  },
  dot: { width: 7, height: 7, borderRadius: 4 },
  empty: {
    padding: 26,
    borderWidth: 1,
    borderStyle: "dashed",
    borderRadius: 15,
    gap: 10,
    alignItems: "center",
    marginVertical: 6,
  },
  emptyTitle: { fontSize: 18, fontWeight: "600" },
  nav: { flexDirection: "row", borderTopWidth: 1, padding: 8, gap: 3 },
  navItem: {
    flex: 1,
    minHeight: 58,
    alignItems: "center",
    justifyContent: "center",
    gap: 4,
    borderRadius: 12,
  },
  field: { marginBottom: 16 },
  input: {
    borderWidth: 1,
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    minHeight: 48,
  },
  projectCard: {
    flexDirection: "row",
    gap: 15,
    alignItems: "center",
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    marginBottom: 12,
  },
  projectIcon: {
    width: 48,
    height: 48,
    borderRadius: 13,
    alignItems: "center",
    justifyContent: "center",
  },
  stat: { flex: 1, minWidth: 120, padding: 24, borderRadius: 18, gap: 5 },
  number: { fontSize: 40, fontWeight: "700" },
  chartCard: { borderWidth: 1, borderRadius: 18, padding: 20 },
  chart: { flexDirection: "row", marginTop: 28 },
  barColumn: { flex: 1, alignItems: "center", gap: 6 },
  barTrack: {
    height: 105,
    width: "100%",
    alignItems: "center",
    justifyContent: "flex-end",
  },
  overlay: {
    flex: 1,
    backgroundColor: "#00000066",
    justifyContent: "center",
    padding: 16,
  },
  modalWrap: {
    width: "100%",
    maxWidth: 520,
    alignSelf: "center",
    maxHeight: "100%",
  },
  modalCard: { borderRadius: 22, overflow: "hidden", flexShrink: 1 },
  modalContent: { padding: 24 },
  swatch: {
    width: 44,
    height: 44,
    borderRadius: 22,
    borderWidth: 3,
    justifyContent: "center",
    alignItems: "center",
  },
  notice: { padding: 14, borderRadius: 10, marginBottom: 16 },
});
