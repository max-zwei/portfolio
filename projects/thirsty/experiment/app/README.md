# PocketPlan

A modest local personal planner built with Expo, React Native and TypeScript. One codebase targets iOS, Android and web. It has five tabs: Today, Tasks, Projects, Progress and Settings. No backend, account or API keys are needed.

## Run

Use Node.js 22.22.2+, 24.15.0+, or 26+ and npm (the test harness follows JSDOM’s supported Node ranges). This environment used Node 26.10.0 and npm 11.19.1.

```sh
npm ci
npm run web
```

Expo prints the local web preview URL. For native development:

```sh
npm start
# Press i for an iOS simulator, or a for an Android emulator.
```

Use an Expo Go client compatible with SDK 55, or a local development build with `npx expo run:ios` / `npx expo run:android`. Native builds require Xcode and its simulator on macOS, or the Android SDK, emulator and Java toolchain. No cloud build service is configured or required. The committed package lockfile fixes the tested dependency tree. Expo's compatibility check selects React 19.2.0, React Native 0.83.10 and the SDK 55 packages.

In a filesystem sandbox that blocks Expo's usual home cache, use this project-local cache override:

```sh
EXPO_NO_TELEMETRY=1 __UNSAFE_EXPO_HOME_DIRECTORY="$PWD/.expo-user" npm run web
```

The override is an Expo CLI implementation option for this restricted environment, not an app setting. No system-wide setup was changed.

## Features and behavior

- **Today:** overdue and due-today sections; completion checkboxes also reopen tasks. Both sections retain completed tasks so reopening is available there. Summary counts include only incomplete tasks.
- **Tasks:** all tasks, title/notes search, and combined status, project and priority filters. Tap a task to view or edit its title, notes, project, optional due date and normal/high priority. Titles are required. Destructive deletion requires confirmation.
- **Projects:** create, rename, choose among six colors, and see incomplete task counts. Confirmed project deletion removes only the project assignment; every task is preserved.
- **Progress:** current completed/remaining counts and a seven-day completion bar chart, including today.
- **Settings:** persisted system/light/dark preference and a confirmed reset that replaces tasks, projects and theme with the sample plan.

The interface includes loading and empty states, save/read error messages, labeled controls, safe-area spacing and scrollable editors with keyboard avoidance. Fields support up to 200 characters for titles/project names and 5,000 for notes. Due dates use explicit `YYYY-MM-DD` entry with “Due today” and “Clear date” helpers.

## Architecture and storage

- `App.tsx`: application state, five-tab navigation, task/project editors, reusable confirmation modal and theme-aware React Native UI. Navigation is deliberately small and does not require a router.
- `src/model.ts`: task/project types, date validation and local-day arithmetic, seed data, completion/reopening, project deletion and progress calculations.
- `src/persistence.ts`: versioned repository with an injected storage interface, schema checks and first-launch-only seeding.
- `tests/model.test.ts`: eight tests for date boundaries/DST, validation, completion/reopening, chart bounds, project preservation, seed-once behavior, round-trip persistence and storage errors.
- `scripts/dom-smoke.mjs`: integration interactions against the actual exported Expo web bundle in JSDOM.
- `scripts/smoke.mjs`: real Playwright browser workflow with mobile/desktop screenshots and automatic temporary-server cleanup.

Data is stored as one JSON document under `pocketplan.v1` using `@react-native-async-storage/async-storage` (native storage on iOS/Android, localStorage on web). Its schema is:

```ts
type Task = {
  id: string;
  title: string;
  notes: string;
  projectId: string | null;
  dueDate: string | null; // YYYY-MM-DD, no timezone
  priority: "normal" | "high";
  completedOn: string | null; // local calendar day of latest completion
};
type Project = { id: string; name: string; color: string };
type Data = {
  version: 1;
  tasks: Task[];
  projects: Project[];
  theme: "system" | "light" | "dark";
};
```

Seeding happens only when the storage key is absent. An intentionally empty plan stays empty. A corrupt/unsupported saved document displays a retry/reset state instead of silently overwriting user data. Saves finish before the UI adopts changes; concurrent writes are blocked and failures are shown. Reset explicitly overwrites the document with newly date-relative demo data.

Storage is local to the app installation or browser origin. Reloading preserves edits; clearing browser/app storage or uninstalling can remove them. Changing the web hostname/port changes the storage origin. There is no multi-tab synchronization, cross-device sync or export.

## Reproducible date and completion rules

Due dates and completion dates are calendar strings, never UTC timestamps. Due-today uses equality with today's local `YYYY-MM-DD`; overdue means a non-null due date lexically precedes today. Null due dates appear only in Tasks. Validation accepts real dates from 1900 through 9999, including leap days. Local-day calculation reads year/month/day components; day offsets use local noon and calendar arithmetic to avoid DST duration assumptions. Date labels are formatted from local noon, not `new Date('YYYY-MM-DD')` UTC parsing.

Marking an incomplete task complete records the user's local calendar day **at the completion action**. Reopening sets `completedOn` to null, removing its contribution from completed totals and the seven-day chart. Completing it again records the new local day. There is one current completion per task, not a historical event log. Editing an already completed task retains its completion day. Deleting a task removes its completion contribution; deleting a project does not. Chart buckets span local today minus six calendar days through today, inclusive. Older/future recorded completions still count toward current completed totals but not the chart. The displayed local day refreshes every 30 seconds and when app activity changes. Existing recorded days are not reinterpreted after timezone changes.

## Verification

```sh
npm run typecheck
npm test
npx expo install --check
npm run build:web
npm run test:dom       # requires dist/ from build:web
npm run test:browser   # requires dist/ and a launchable browser
```

The browser script uses system Chrome on macOS by default. Set `CHROME_PATH` to a Chromium-compatible executable on another machine. To download a project-local browser:

```sh
PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/playwright" npx playwright install chromium --only-shell
# Set CHROME_PATH to the downloaded chrome-headless-shell executable.
CHROME_PATH=/absolute/path/to/chrome-headless-shell npm run test:browser
```

On success it creates mobile Today, dark-theme persistence, Progress, desktop Today and narrow-editor screenshots under `artifacts/`. It tests task and project CRUD, validation, combined filters, confirmations, completion/reopening, actual browser reload persistence and reset. The script always closes its browser and temporary HTTP server.

Actual results for this environment are in `artifacts/acceptance-report.txt`, with complete stdout/stderr (including failed attempts) in `artifacts/command-logs/`. Logs, caches and build output are ignored by Git; source, configuration, tests and lockfile are retained.

### Verified here

Type checking, all eight model/repository tests, Expo dependency compatibility, a successful production Expo web export, and JSDOM integration against that export. DOM integration tests use the real AsyncStorage web adapter, preserve its serialized data across a fresh app/window mount, and exercise all five tabs. JSDOM does not verify browser layout, keyboard rendering or device behavior.

### Environment limitations

Real browser verification and screenshots could not run. System Chrome aborted with `SIGABRT`; the separately downloaded project-local Chromium headless shell failed with `bootstrap_check_in ... Permission denied (1100)` in macOS Mach port registration and exited with `SIGTRAP`. The sandbox does not permit the required browser launch. No UI screenshot or real-browser pass is claimed.

No native build, simulator, physical iOS device or physical Android device was verified. `xcodebuild -version` reports that the active developer directory is CommandLineTools rather than Xcode; `xcrun simctl` is unavailable; `adb` is absent. Native source compatibility/type checking is not native execution evidence.

`npm audit` reported 32 transitive dependency advisories (11 moderate, 21 high) in the chosen SDK tree. The full report is retained. The suggested forced fixes would change the Expo/React Native SDK combination; they were not applied. Dependency compatibility checks pass, but an audit-clean tree is not claimed.

Official references used: [Expo SDK 55](https://expo.dev/changelog/sdk-55), [Expo SDK reference](https://docs.expo.dev/versions/latest/), and [AsyncStorage installation](https://react-native-async-storage.github.io/2.0/Installation/).
