---
name: token-system
description: "Build, audit, or sync a W3C-compatible design token system in Figma variables. Covers 2-tier (Primitive → Semantic) token architecture across Color, Typography, Spacing, Radius, Motion, and Elevation. Light/Dark modes. One Figma variable collection per token category. Use when starting a token system from scratch, auditing/refactoring an existing one, or syncing tokens from a codebase (e.g. CSS variables, globals.css). Prerequisite: figma-use skill must also be loaded."
disable-model-invocation: false
---

# Token System — Figma Variable Skill

Build a W3C Design Tokens Community Group-compatible token system in Figma variables. Two tiers: **Primitive** (raw values) → **Semantic** (role-based aliases). One variable collection per token category. Light/Dark modes on semantic collections.

**Prerequisites**: The `figma-use` skill MUST also be loaded before any `use_figma` call. It provides Plugin API syntax rules (return pattern, page reset, font loading, color range 0–1, ID tracking).

**Always pass `skillNames: "token-system"` when calling `use_figma` as part of this skill.**

---

## 1. The One Rule That Matters Most

**Never batch everything into one `use_figma` call.** Token systems require many sequential steps with validation between them. One collection at a time. One tier at a time. Validate before proceeding.

---

## 2. Workflow

### Step 0 — Orient

Ask the user:

> **What are we doing?**
> 1. **Scratch** — build a new token system in an empty or fresh Figma file
> 2. **Audit** — inspect an existing token setup and produce a gap/drift report
> 3. **Sync** — import tokens from a codebase (CSS variables, `globals.css`, JSON) into Figma
>
> *(You can do all three in sequence — start with which is the primary goal.)*

Then ask:

> **Schema: W3C standard or custom?**
> - **W3C** (recommended) — names follow the W3C Design Tokens Community Group spec: `{category}/{scale}` for primitives, `{category}/{role}/{variant}` for semantics. `$type`, `$value`, `$description` metadata where Figma supports it. Compatible with Style Dictionary, Token Studio, Figma Variables.
> - **Custom** — you define the naming rules. I'll follow whatever conventions you specify.

Lock these two decisions before any `use_figma` write.

---

### Step 1 — Discovery (all modes)

Run a read-only `use_figma` to inspect the current file state:

```javascript
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const variables = await figma.variables.getLocalVariablesAsync();
const textStyles = figma.getLocalTextStyles();
const effectStyles = figma.getLocalEffectStyles();

return {
  collectionCount: collections.length,
  collections: collections.map(c => ({
    id: c.id,
    name: c.name,
    modes: c.modes.map(m => ({ id: m.modeId, name: m.name })),
    variableCount: variables.filter(v => v.variableCollectionId === c.id).length
  })),
  variableCount: variables.length,
  textStyleCount: textStyles.length,
  effectStyleCount: effectStyles.length,
  sampleVariables: variables.slice(0, 20).map(v => ({ name: v.name, type: v.resolvedType, id: v.id }))
};
```

**If Scratch**: note existing collections/variables — ask user whether to clear them or build alongside.
**If Audit**: this is your baseline. Proceed to Step 5 (Audit Path).
**If Sync**: ask the user to paste or upload their token source (CSS vars, JSON, or describe the file). Proceed to Step 6 (Sync Path).

---

### Step 2 — Agree on Scope (Scratch path)

Confirm which token categories to build. Default full set:

| Category | Collection name | Primitive scale | Modes |
|----------|----------------|-----------------|-------|
| Color | `Color` | `color/{hue}/{step}` (e.g. `color/blue/500`) | Primitives: 1 mode (`Value`). Semantic: 2 modes (`Light`, `Dark`) |
| Typography | `Typography` | `typography/{property}/{scale}` (e.g. `typography/size/sm`) | 1 mode (`Value`) |
| Spacing | `Spacing` | `spacing/{scale}` (e.g. `spacing/4`) | 1 mode (`Value`) |
| Radius | `Radius` | `radius/{scale}` (e.g. `radius/sm`) | 1 mode (`Value`) |
| Motion | `Motion` | `motion/{property}/{scale}` (e.g. `motion/duration/fast`) | 1 mode (`Value`) |
| Elevation | `Elevation` | `elevation/{level}` (e.g. `elevation/1`) | 1 mode (`Value`) |

Ask: "Which categories do you want? Default is all six. Drop any you don't need."

**Checkpoint ✋**: Present the agreed category list + naming schema. Get explicit approval before writing anything.

---

### Step 3 — Build Primitive Collections (one per category)

For each agreed category, in order: Color → Typography → Spacing → Radius → Motion → Elevation.

**Pattern per collection:**

```javascript
// 1. Create collection
const collection = figma.variables.createVariableCollection('Color');
const modeId = collection.modes[0].modeId;
await figma.variables.renameVariableModeAsync(collection, modeId, 'Value');

// 2. Create primitive variables
const primitives = [
  { name: 'color/blue/50',  value: { r: 0.937, g: 0.965, b: 1.0   } },
  { name: 'color/blue/100', value: { r: 0.859, g: 0.925, b: 0.996 } },
  { name: 'color/blue/200', value: { r: 0.749, g: 0.863, b: 0.992 } },
  { name: 'color/blue/300', value: { r: 0.576, g: 0.773, b: 0.984 } },
  { name: 'color/blue/400', value: { r: 0.384, g: 0.651, b: 0.969 } },
  { name: 'color/blue/500', value: { r: 0.231, g: 0.510, b: 0.965 } },
  { name: 'color/blue/600', value: { r: 0.145, g: 0.392, b: 0.922 } },
  { name: 'color/blue/700', value: { r: 0.110, g: 0.306, b: 0.847 } },
  { name: 'color/blue/800', value: { r: 0.118, g: 0.247, b: 0.702 } },
  { name: 'color/blue/900', value: { r: 0.118, g: 0.220, b: 0.569 } },
  { name: 'color/blue/950', value: { r: 0.071, g: 0.122, b: 0.380 } },
  // ... gray, red, green, yellow scales
];

const createdIds = [];
for (const { name, value } of primitives) {
  const v = figma.variables.createVariable(name, collection, 'COLOR');
  v.setValueForMode(modeId, value);
  v.scopes = [];  // Primitives hidden from property pickers
  v.description = `$type: color`;
  createdIds.push(v.id);
}

return { collectionId: collection.id, modeId, createdCount: createdIds.length, createdIds };
```

**Scope rules by category:**
- All primitive variables → `scopes: []` (hidden — only semantics are exposed in the UI)

**Default primitive scales (W3C-compatible naming):**

*Color* — per hue: steps 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950. Minimum hues: `gray`, `blue`. Add more as needed (`red`, `green`, `yellow`, `orange`, `purple`). Also: `color/white` (#FFFFFF), `color/black` (#000000).

*Typography*:
```
typography/size/xs = 12    typography/size/sm = 14    typography/size/md = 16
typography/size/lg = 18    typography/size/xl = 20    typography/size/2xl = 24
typography/size/3xl = 30   typography/size/4xl = 36   typography/size/5xl = 48
typography/weight/regular = 400    typography/weight/medium = 500
typography/weight/semibold = 600   typography/weight/bold = 700
typography/line-height/tight = 1.25    typography/line-height/normal = 1.5
typography/line-height/loose = 1.75
typography/letter-spacing/tight = -0.025    typography/letter-spacing/normal = 0
typography/letter-spacing/wide = 0.025
```

*Spacing* (4px base grid):
```
spacing/0=0  spacing/1=4   spacing/2=8   spacing/3=12  spacing/4=16
spacing/5=20 spacing/6=24  spacing/8=32  spacing/10=40 spacing/12=48
spacing/16=64 spacing/20=80 spacing/24=96
```

*Radius*:
```
radius/none=0  radius/sm=2   radius/md=4   radius/lg=8
radius/xl=12   radius/2xl=16 radius/3xl=24 radius/full=9999
```

*Motion*:
```
motion/duration/instant=0    motion/duration/fast=100
motion/duration/normal=200   motion/duration/slow=400   motion/duration/slower=600
motion/easing/linear="linear"
motion/easing/ease-in="cubic-bezier(0.4,0,1,1)"
motion/easing/ease-out="cubic-bezier(0,0,0.2,1)"
motion/easing/ease-in-out="cubic-bezier(0.4,0,0.2,1)"
motion/easing/spring="cubic-bezier(0.33,1,0.68,1)"
```

*Elevation* — store as STRING variables (Figma variables don't support shadow types natively); also create matching `figma.createEffectStyle()` entries:
```
elevation/0="none"
elevation/1="0 1px 2px rgba(0,0,0,0.05)"
elevation/2="0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)"
elevation/3="0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)"
elevation/4="0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)"
elevation/5="0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)"
```

**After each collection**: validate with a read call. Return created count + sample names. Report to user before proceeding to next category.

**Checkpoint ✋** after all primitives: list all collections + variable counts. Await approval before building semantics.

---

### Step 4 — Build Semantic Collections (one per category)

Add a **Light** and **Dark** mode to the Color collection. For non-color categories, semantics live in the same collection as primitives with semantic naming — Figma's alias system works most reliably within a single collection.

Use `VARIABLE_ALIAS` to reference primitives. Never duplicate raw values in the semantic tier.

```javascript
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const colorCollection = collections.find(c => c.name === 'Color');

// Add Light and Dark modes
const lightModeId = await figma.variables.addVariableModeAsync(colorCollection, 'Light');
const darkModeId  = await figma.variables.addVariableModeAsync(colorCollection, 'Dark');

const allVars = await figma.variables.getLocalVariablesAsync();
const prim = (name) => allVars.find(v => v.name === name && v.variableCollectionId === colorCollection.id);

const semantics = [
  // Surface
  { name: 'color/surface/default',      scopes: ['FRAME_FILL','SHAPE_FILL'],                          light: 'color/white',     dark: 'color/gray/950'  },
  { name: 'color/surface/subtle',       scopes: ['FRAME_FILL','SHAPE_FILL'],                          light: 'color/gray/50',   dark: 'color/gray/900'  },
  { name: 'color/surface/raised',       scopes: ['FRAME_FILL','SHAPE_FILL'],                          light: 'color/white',     dark: 'color/gray/800'  },
  // Text
  { name: 'color/text/primary',         scopes: ['TEXT_FILL'],                                        light: 'color/gray/900',  dark: 'color/gray/50'   },
  { name: 'color/text/secondary',       scopes: ['TEXT_FILL'],                                        light: 'color/gray/600',  dark: 'color/gray/400'  },
  { name: 'color/text/disabled',        scopes: ['TEXT_FILL'],                                        light: 'color/gray/400',  dark: 'color/gray/600'  },
  { name: 'color/text/inverse',         scopes: ['TEXT_FILL'],                                        light: 'color/white',     dark: 'color/gray/900'  },
  { name: 'color/text/brand',           scopes: ['TEXT_FILL'],                                        light: 'color/blue/600',  dark: 'color/blue/400'  },
  // Border
  { name: 'color/border/default',       scopes: ['STROKE_COLOR'],                                     light: 'color/gray/200',  dark: 'color/gray/700'  },
  { name: 'color/border/strong',        scopes: ['STROKE_COLOR'],                                     light: 'color/gray/400',  dark: 'color/gray/500'  },
  { name: 'color/border/focus',         scopes: ['STROKE_COLOR'],                                     light: 'color/blue/500',  dark: 'color/blue/400'  },
  // Action
  { name: 'color/action/primary',       scopes: ['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'], light: 'color/blue/600', dark: 'color/blue/500'  },
  { name: 'color/action/primary-hover', scopes: ['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'], light: 'color/blue/700', dark: 'color/blue/400'  },
  { name: 'color/action/secondary',     scopes: ['FRAME_FILL','SHAPE_FILL'],                          light: 'color/gray/100',  dark: 'color/gray/800'  },
  // Feedback
  { name: 'color/feedback/error',       scopes: ['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'], light: 'color/red/600',   dark: 'color/red/400'   },
  { name: 'color/feedback/success',     scopes: ['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'], light: 'color/green/600', dark: 'color/green/400' },
  { name: 'color/feedback/warning',     scopes: ['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'], light: 'color/yellow/500',dark: 'color/yellow/400'},
  { name: 'color/feedback/info',        scopes: ['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'], light: 'color/blue/600',  dark: 'color/blue/400'  },
];

const createdIds = [];
for (const { name, scopes, light, dark } of semantics) {
  const v = figma.variables.createVariable(name, colorCollection, 'COLOR');
  const lightPrim = prim(light);
  const darkPrim  = prim(dark);
  if (lightPrim) v.setValueForMode(lightModeId, { type: 'VARIABLE_ALIAS', id: lightPrim.id });
  if (darkPrim)  v.setValueForMode(darkModeId,  { type: 'VARIABLE_ALIAS', id: darkPrim.id  });
  v.scopes = scopes;
  createdIds.push(v.id);
}

return { createdCount: createdIds.length, createdIds };
```

**Semantic scope reference:**

| Variable group | Scopes |
|----------------|--------|
| `color/surface/*` | `['FRAME_FILL', 'SHAPE_FILL']` |
| `color/text/*` | `['TEXT_FILL']` |
| `color/border/*` | `['STROKE_COLOR']` |
| `color/action/*`, `color/feedback/*` | `['FRAME_FILL', 'SHAPE_FILL', 'TEXT_FILL', 'STROKE_COLOR']` |
| `typography/size/*` | `['FONT_SIZE']` |
| `typography/weight/*` | `['FONT_WEIGHT']` |
| `typography/line-height/*` | `['LINE_HEIGHT']` |
| `typography/letter-spacing/*` | `['LETTER_SPACING']` |
| `spacing/*` (semantic) | `['GAP', 'WIDTH_HEIGHT']` |
| `radius/*` (semantic) | `['CORNER_RADIUS']` |
| `motion/*` | `[]` (not UI-bindable — code syntax only) |
| `elevation/*` | `[]` (handled via effect styles) |

**Checkpoint ✋** after all semantics: spot-check one alias chain end-to-end (semantic → primitive → raw value). Await approval before code syntax step.

---

### Step 5 — Set Code Syntax

Required for Dev Mode and token export tools. Run once across all variables.

```javascript
const allVars = await figma.variables.getLocalVariablesAsync();

for (const v of allVars) {
  // "color/surface/default" → "--color-surface-default"
  const cssName = '--' + v.name.replace(/\//g, '-');
  v.setVariableCodeSyntax('WEB',     `var(${cssName})`);   // Always use var() wrapper
  v.setVariableCodeSyntax('ANDROID', v.name.replace(/\//g, '.'));
  v.setVariableCodeSyntax('IOS',     v.name.replace(/\//g, '.'));
}

return { updatedCount: allVars.length };
```

**Rules:**
- WEB: always `var(--token-name)` — never the bare property name
- Primitives get code syntax too (for direct use in code), even though their Figma scopes are hidden
- Path separator: `/` → `-` for WEB, `/` → `.` for ANDROID/IOS

**Token system is complete.** Present a final summary: collection count, variable count per collection, mode count, code syntax confirmed.

---

### Step 6 — Audit Path

Run discovery (Step 1) then execute these checks:

```javascript
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const variables = await figma.variables.getLocalVariablesAsync();
const issues = [];

for (const v of variables) {
  const collection = collections.find(c => c.id === v.variableCollectionId);
  const modes = collection?.modes ?? [];

  // 1. ALL_SCOPES — pollutes every property picker
  if (v.scopes.includes('ALL_SCOPES')) {
    issues.push({ type: 'ALL_SCOPES', name: v.name, id: v.id });
  }

  // 2. Missing code syntax
  if (!v.codeSyntax?.WEB) {
    issues.push({ type: 'MISSING_CODE_SYNTAX', name: v.name, id: v.id });
  }

  // 3. Raw value in semantic-looking name (should be alias)
  const looksLikeSemantic = v.name.includes('/') && !/\d{2,3}$/.test(v.name) && !/\/(xs|sm|md|lg|xl|2xl|3xl|4xl|5xl|full|none|fast|slow|normal|loose|tight|wide|regular|medium|semibold|bold|instant|slower|linear)$/.test(v.name);
  for (const mode of modes) {
    const val = v.getValueForMode(mode.modeId);
    if (looksLikeSemantic && val !== null && typeof val !== 'object') {
      issues.push({ type: 'RAW_IN_SEMANTIC', name: v.name, mode: mode.name, id: v.id });
    }
  }

  // 4. Broken alias
  for (const mode of modes) {
    const val = v.getValueForMode(mode.modeId);
    if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') {
      const target = variables.find(vv => vv.id === val.id);
      if (!target) issues.push({ type: 'BROKEN_ALIAS', name: v.name, aliasId: val.id, id: v.id });
    }
  }
}

return { totalVariables: variables.length, issueCount: issues.length, issues };
```

Present the report grouped by issue type. For each issue, explain what it means and propose a fix. Ask which issues to auto-fix vs. leave for manual review.

---

### Step 7 — Sync Path (from codebase)

1. Ask the user to provide their token source in one of:
   - **CSS custom properties** (paste from `globals.css` or similar)
   - **W3C JSON** (`{ "color": { "blue": { "500": { "$value": "#3B82F6", "$type": "color" } } } }`)
   - **Plain description** — Claude structures them

2. Parse into: `{ name, value, type, description }` list. Infer category from name prefix. Identify primitives (raw values) vs. semantics (references to other tokens via `var(--...)` or `{token.path}`).

3. Run Steps 3–5 using the parsed values instead of defaults. Show a mapping table (source name → Figma variable name → collection) before any write.

4. **Checkpoint ✋**: get approval on the mapping before writing to Figma.

---

## 3. State Management

Write state to disk after each step and re-read at the start of each session:

```
/tmp/token-system-{DATE}.json
```

```json
{
  "runId": "ts-2024-001",
  "mode": "scratch",
  "schema": "w3c",
  "categories": ["Color", "Typography", "Spacing", "Radius", "Motion", "Elevation"],
  "step": "step4-semantics",
  "collections": {
    "Color":      { "id": "...", "primitiveModeId": "...", "lightModeId": "...", "darkModeId": "..." },
    "Typography": { "id": "...", "modeId": "..." },
    "Spacing":    { "id": "...", "modeId": "..." },
    "Radius":     { "id": "...", "modeId": "..." },
    "Motion":     { "id": "...", "modeId": "..." },
    "Elevation":  { "id": "...", "modeId": "..." }
  },
  "variableCounts": {},
  "completedSteps": []
}
```

**Idempotency**: before creating any variable, check by name + collection ID. Skip if exists, update only if value differs and user approves.

**Resume**: at session start, run a read-only `use_figma` to reconstruct the `{ name → id }` map, then re-read the state file.

---

## 4. Naming Conventions (W3C)

**Primitives** — raw value, scale-indexed:
```
color/blue/500      typography/size/md      spacing/4
radius/lg           motion/duration/normal  elevation/2
```

**Semantics** — role-based, mode-aware:
```
color/surface/default     color/text/primary
color/action/primary-hover    color/feedback/error
```

**Rules:**
- All lowercase, slash-separated, hyphen for multi-word segments
- No camelCase, no underscores in token names
- Primitive names end with a scale indicator (number or t-shirt size: xs/sm/md/lg/xl/2xl…)
- Semantic names never end with a raw scale indicator
- Add `$description` on every variable: one sentence on intended use

---

## 5. Critical Rules

1. **Primitives always `scopes: []`** — never directly applied in Figma UI
2. **Semantics always alias primitives** — `{ type: 'VARIABLE_ALIAS', id }`. Never duplicate raw values in semantic tier
3. **Code syntax on every variable** — WEB uses `var(--token-name)`. No exceptions
4. **Light/Dark on Color semantics only** — all other categories use one mode (`Value`)
5. **No component tokens** — this skill stops at semantic tier
6. **No `ALL_SCOPES`** — always set specific scopes per variable
7. **Sequential `use_figma` calls** — never parallel
8. **Never guess variable IDs** — read from state ledger or live query
9. **Typography**: Figma Variables support individual numeric properties (size, weight, line-height, letter-spacing) but not composite tokens. Use individual variables + `figma.createTextStyle()` with `setBoundVariable` for full text styles
10. **Elevation**: Figma variables don't support shadow type — store as STRING variables and create matching effect styles via `figma.createEffectStyle()`

---

## 6. Anti-Patterns

- ❌ Batching all primitives + semantics into one `use_figma` call
- ❌ `scopes: ['ALL_SCOPES']` on any variable — ever
- ❌ Raw values in the semantic layer instead of `VARIABLE_ALIAS`
- ❌ Missing code syntax on any variable
- ❌ Component-tier tokens (out of scope)
- ❌ Building semantics before primitives are validated
- ❌ Using `getPluginData` / `setPluginData` (not supported — use `getSharedPluginData`)
- ❌ Parallelizing `use_figma` calls
- ❌ Hallucinating variable IDs from memory

---

## 7. Checkpoint Summary

| After | Show | Ask |
|-------|------|-----|
| Step 0 | Mode + schema decision | "Confirmed: [scratch/audit/sync], [W3C/custom]. Proceed?" |
| Step 2 | Category list + naming examples | "Here's the full plan. Approve before I write anything?" |
| Step 3 — each collection | Collection name + variable count | "Created [N] primitives for [Category]. Continue?" |
| Step 3 — all done | Summary table (all collections + counts) | "All primitives done. Review before semantics?" |
| Step 4 | Semantic count + alias spot-check | "Semantics done. Alias check: [example chain]. Proceed to code syntax?" |
| Step 5 | Updated count | "Code syntax set on all [N] variables. Token system complete." |
| Audit | Issue list grouped by type | "Found [N] issues. Which should I fix automatically?" |
| Sync | Source → Figma mapping table | "Mapped [N] tokens. Approve before writing to Figma?" |
