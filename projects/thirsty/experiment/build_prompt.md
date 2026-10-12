Build PocketPlan, a complete but modest personal task-planning mobile app.

This is a recorded software-development case study. The deliverable is a working
MVP, not a design mockup. Work autonomously in the provided project directory
until the acceptance criteria below pass or a concrete environment limitation
prevents further progress. Make sensible implementation decisions without
asking follow-up questions. Keep the scope exactly as specified.

TECHNOLOGY AND SCOPE

- Use Expo, React Native and TypeScript. Support iOS and Android through the same
  codebase, and provide an Expo web preview for inspection in this environment.
- Use stable, mutually compatible dependencies and retain the package lockfile.
- Store data locally using a persistence library that supports the chosen native
  and web targets. No backend, login, API keys, paid services or cloud accounts.
- Use a simple, polished interface with clear typography, consistent spacing,
  accessible controls, empty states and sensible keyboard behavior.
- Use five main screens: Today, Tasks, Projects, Progress and Settings. Task and
  project editors may be modals or additional navigation screens.
- Do not add collaboration, payments, AI features, push notifications, recurring
  tasks, marketing pages, analytics, app-store publishing or unrelated features.

FUNCTIONAL REQUIREMENTS

1. Today
   Show tasks due today and overdue tasks, with separate labels. Let the user
   mark tasks complete or reopen them. Date-only due dates must be interpreted
   consistently in the user's local calendar, without accidental UTC shifts.

2. Tasks
   List all tasks with search and filters for status, project and priority.
   Support creating, viewing, editing and deleting tasks. Each task has a title,
   optional notes, optional project, optional due date, and normal or high
   priority. A title is required. Confirm destructive deletion.

3. Projects
   Create, rename and delete projects; let the user choose a project color.
   Display the number of incomplete tasks per project. Deleting a project must
   preserve its tasks by removing their project assignment, with confirmation.

4. Progress
   Show completed versus remaining task counts and completions for the past
   seven local calendar days. A simple bar chart is enough. Reopening a task
   must update the numbers correctly. Define the completion-date behavior in
   the README so the calculation is reproducible.

5. Settings
   Provide system/light/dark theme selection, persist the preference, and offer
   a confirmed reset to demo data. Seed a small synthetic demo dataset on first
   launch only. Normal relaunches must preserve edits and completed tasks.

ACCEPTANCE CRITERIA

- All five screens are implemented and connected by usable navigation.
- Task and project CRUD operations work, including validation and confirmations.
- Task data, project data and theme settings survive an app reload.
- Today/overdue filtering and progress counts follow the specified behavior.
- Loading and empty states are usable, and no unfinished placeholder feature
  is presented as complete.
- Type checking passes. Run meaningful automated tests covering date filtering,
  completion/reopening, project deletion without task loss, and persistence.
- Produce a successful Expo web build. If browser automation is available, run
  a smoke test that creates, edits and completes a task, reloads the app and
  confirms persistence. Save a screenshot if possible. Clearly distinguish web
  verification from actual iOS/Android device or simulator verification.
- If a native build or browser check cannot be run in this environment, report
  the exact limitation and what was verified instead. Never invent a passing
  check or screenshot.

WORKFLOW AND RESEARCH RECORD

- Use this one agent only. Do not spawn subagents, invoke another coding agent,
  or make separate model/API calls. Do not change model or reasoning settings.
- Start with a short implementation plan, then implement, test, inspect and fix
  the app. Stop once the acceptance criteria are met; do not expand the scope or
  continue polishing indefinitely. Do not aim for a predetermined token total.
- Use terminal and file tools for the work. Consult official package/framework
  documentation when needed. Install project dependencies locally; do not
  change system-wide configuration or global installations.
- A separate recorder captures emitted Codex events. Do not fabricate token
  counts or write a retrospective transcript and call it a raw execution log.
- Save the complete stdout/stderr of dependency installation, test, typecheck
  and build commands under artifacts/command-logs/, even if the tool's displayed
  output is truncated. Preserve the original exit status when using pipes or
  redirection. Give each attempt a distinct filename so failed attempts remain.
- Record material decisions and encountered errors briefly as progress messages.
  Operational explanations are enough; do not supply private internal reasoning.
- Keep generated logs and caches out of source control. Keep all app source,
  configuration, tests and the lockfile in the project. Do not create git commits
  or delete the repository metadata. Stop temporary development servers at the
  end of verification.

DELIVERABLES

1. Complete runnable app source, dependency lockfile and automated tests.
2. README.md with installation/start commands, architecture, data model,
   verification commands, supported targets and known limitations.
3. artifacts/acceptance-report.txt listing each acceptance criterion as PASS,
   FAIL or NOT VERIFIED, with evidence and commands used. Distinguish automated
   checks from manual inspection and native checks from web checks.
4. Full command logs in artifacts/command-logs/ and any available UI screenshots.
5. A concise final message describing the implemented features, checks actually
   run, outstanding limitations and how to launch the app. Do not estimate the
   session's token, energy or water consumption; that analysis happens outside
   this build.
