---
version: alpha
name: thirsty
description: 'Visual specification and QML implementation contract for a staged app-building agent and water-dependent artwork. Implementation pending.'
colors:
  primary: '#000000'
  surface: '#FFFFFF'
  secondary: '#E1E1E1'
  water: '#0000FF'
  error: '#FF0000'
  action: '#FF00FF'
typography:
  heading:
    fontFamily: JetBrains Mono
    fontSize: '{size.xl}'
    fontWeight: 400
    letterSpacing: 0em
  body:
    fontFamily: JetBrains Mono
    fontSize: '{size.l}'
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0em
  task:
    fontFamily: JetBrains Mono
    fontSize: '{size.l}'
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0em
  warning:
    fontFamily: JetBrains Mono
    fontSize: 20px
    fontWeight: 400
    letterSpacing: 0em
rounded:
  none: 0px
size:
  s: 4px
  m: 8px
  l: 16px
  xl: 40px
  xxl: 96px
components:
  water_level:
    width: 94px
    height: 94px
    padding: 2px
    rounded: '{rounded.none}'
    borderColor: '{colors.primary}'
    borderWidth: 2px
    activeColor: '{colors.water}'
    emptyColor: '{colors.error}'
  agent_icon:
    width: '{size.l}'
    height: '{size.l}'
    activeColor: '{colors.primary}'
    inactiveColor: '{colors.secondary}'
    errorColor: '{colors.error}'
  agent-task:
    typography: '{typography.task}'
    textColor: '{colors.primary}'
    fontStyle: italic
  agent-action:
    typography: '{typography.task}'
    fontStyle: italic
    gap: '{size.l}'
  agent-error:
    typography: '{typography.warning}'
    textColor: '{colors.error}'
    gap: '{size.m}'
  agent-output:
    typography: '{typography.body}'
    textColor: '{colors.primary}'
  user-text:
    width: 931px
    height: 62px
    typography: '{typography.body}'
    padding: '{size.l}'
    rounded: '{rounded.none}'
    borderColor: '{colors.primary}'
    borderWidth: 2px
  user-button:
    width: 46px
    height: 62px
    typography: '{typography.body}'
    backgroundColor: '{colors.action}'
    textColor: '{colors.primary}'
    padding: '{size.l}'
    rounded: '{rounded.none}'
    borderColor: '{colors.primary}'
    borderWidth: 2px
  avatar:
    width: 208px
    height: 149px
    color: '{colors.primary}'
  qr_code:
    width: 208px
    height: 208px
---

# thirsty — Design System

This document follows the DESIGN.md template: token frontmatter followed by its eight ordered design sections. It is a project specification, not the template's format reference or a generated file.

## Overview

thirsty is an artwork presented as an app-building chat agent connected to a fake water-cooled server. Five physical sensors measure its water level as water drips away. The development process is theatrical: the interface performs work rather than generating code. See [README.md](README.md) for the project concept and visitor journey.

**Visual source:** [Figma · thirsty · Design System, node 9:214](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=9-214)

**Interface source:** [Figma · Interface, page 0:1](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=0-1) supplies the Start (`2:7`), Input (`2:16`), and Running (`2:31`) 1280 × 720 screen compositions. The component sheet supplies reusable defaults; Interface instances may override layout dimensions as scoped below.

**Implementation contract:** this YAML is the canonical token authority. The selected interface is native Qt Quick / QML through Python / PySide6, running fullscreen on an HDMI screen with Bluetooth keyboard input. Map tokens into the planned `app/ui/Theme.qml` and reusable QML components; behavior and sensor decisions live in [PRODUCT.md](PRODUCT.md). TH-04 owns theme/components, TH-07 owns screens, and TH-11 verifies the installed result. Application paths are planned, not existing implementation.

The visual language is sparse and terminal-like: monospaced text, square edges, pixel-based symbols, `{colors.primary}` outlines, `{colors.water}` water, `{colors.error}` interruption, and a `{colors.action}` submission button. Preserve the distinction between italic simulated work and regular-weight output.

**Evidence boundary:** `size/*` is the desired documentation naming convention for the source size scale, not a claim that live Figma variables have been renamed. Slash labels such as `size/l` identify documentation names; brace-wrapped dot paths such as `{size.l}` reference the tokens defined in the frontmatter. Color and typography token names above are documentation aliases derived from swatches and text properties, not claims of published Figma variables. Component aliases map to the source variants below. Product behavior comes from the project brief; recommendations and unresolved choices are explicitly marked. The component sheet establishes shared visual treatments; the Interface page establishes the three screen compositions. Implementation defaults added below are not claims about additional Figma variants.

## Colors

| Token                | Value     | Intended use                                 |
| -------------------- | --------- | -------------------------------------------- |
| `{colors.primary}`   | `#000000` | text, outlines, active icon elements, avatar |
| `{colors.surface}`   | `#FFFFFF` | background                                   |
| `{colors.secondary}` | `#E1E1E1` | inactive icon elements, secondary color      |
| `{colors.water}`     | `#0000FF` | everything related to water                  |
| `{colors.error}`     | `#FF0000` | everything related to errors                 |
| `{colors.action}`    | `#FF00FF` | user interactions                            |

## Typography

| Role                   | Family / style              | Size | Line height |
| ---------------------- | --------------------------- | ---- | ----------- |
| `{typography.heading}` | JetBrains Mono Regular, 400 | 40px | Auto        |
| `{typography.body}`    | JetBrains Mono Regular, 400 | 16px | 160%        |
| `{typography.task}`    | JetBrains Mono Italic, 400  | 16px | 160%        |
| `{typography.warning}` | JetBrains Mono Regular, 400 | 20px | Auto        |

All text uses zero letter spacing. Auto line heights are intentionally omitted from the numeric frontmatter; do not reinterpret them as a measured pixel value.

The `H1` variant name in `agent_messages` does **not** mean `{typography.heading}` display text: task headings use `{typography.task}` and output headings use `{typography.body}`, both with a leading `#`. Task headings and task/action bodies use the italic style defined by `{components.agent-task.fontStyle}` and `{components.agent-action.fontStyle}`; output headings and bodies are regular. The water-error headline uses `{typography.warning}` and `{colors.error}`, with `{typography.body}` and `{colors.primary}` supporting text. Do not introduce bold weights absent from the source.

**QML implementation:** bundle JetBrains Mono regular and italic faces under the planned `app/assets/fonts/`, with their license notices; load locally at weight 400 and retain a monospace fallback. Use explicit pixel sizes from the tokens. Preserve 1.6 proportional line height for body/task text and natural font metrics for Auto line heights. Italic comes from component `fontStyle`. TH-04 verifies font provenance and distribution permission; TH-11 verifies actual screen rendering.

## Layout

| Documentation label | Token reference | Value |
| ------------------- | --------------- | ----- |
| `size/s`            | `{size.s}`      | 4px   |
| `size/m`            | `{size.m}`      | 8px   |
| `size/l`            | `{size.l}`      | 16px  |
| `size/xl`           | `{size.xl}`     | 40px  |
| `size/xxl`          | `{size.xxl}`    | 96px  |

These five values are the source scale; do not replace them with a generic 8px progression.

Observed bindings: message-heading gaps use `{size.m}`; the water-error vertical gap uses `{components.agent-error.gap}`; action icon/text gaps use `{components.agent-action.gap}`; user-input/button padding uses `{components.user-text.padding}` and `{components.user-button.padding}`. The water indicator has a separate fixed inset, `{components.water_level.padding}`. Component-set presentation spacing (including its 20px padding and 40px variant separation) is not a screen-layout requirement.

**Default screen layout:** a 1280 × 720 reference canvas, 16:9, with `{size.xxl}` padding by default. Prefer 1280 × 720 HDMI output. If the screen requires another mode, scale uniformly and letterbox; do not stretch or independently reflow the composition. Validate pixel geometry, font rendering and QR scanning at the installed resolution.

**Scoped Interface exceptions:** Running's transcript begins at y0, so its top padding is 0 rather than the default `{size.xxl}`; the fixed water indicator remains at x1088/y96. That instance is 96 × 96, overriding the component-sheet 94 × 94 default. Input's field is 1026px wide, overriding the 931px component default; its button remains 46px wide, with a 16px gap for 1088px combined width. Apply these instance dimensions in the relevant QML screen, never by changing frontmatter defaults or shared theme values. Reference-frame coordinates and transcript geometry are screen layout, not additions to the five-value size scale; the canvas surface and shared visual treatments still use canonical tokens.

## Elevation & Depth

Inspected component roots and variants have no effects. Hierarchy comes from spacing, type, color, and outlines, not shadows or gradients. User controls use `{components.user-text.borderWidth}` and `{components.user-button.borderWidth}` borders in `{colors.primary}`; water indicators use `{components.water_level.borderWidth}` borders in `{colors.primary}`.

## Shapes

Visible product components use square corners (`{rounded.none}`). Preserve the crisp pixel geometry of the avatar, agent icons, and water grid.

Use the source geometry for icon assets instead of substituting unrelated symbols. Preserve square QR modules and avoid distortion or smoothing that harms scanning. Avatar reference dimensions are `{components.avatar.width}` × `{components.avatar.height}`; QR reference dimensions are `{components.qr_code.width}` × `{components.qr_code.height}`.

## Components

Names and variants below match Figma. Frontmatter component keys such as `agent-task` and `user-button` are local documentation aliases, not renamed Figma assets.

### QML component mapping

| Figma source     | Planned QML component               | Responsibility                                         |
| ---------------- | ----------------------------------- | ------------------------------------------------------ |
| `water_level`    | `WaterLevel.qml`                    | Levels 0–5 plus explicit unknown/fault fallback        |
| `agent_icon`     | `AgentIcon.qml`                     | Source running/error pixel patterns                    |
| `agent_messages` | `AgentMessage.qml`                  | Select visual treatment by source `type` and `variant` |
| `avatar`         | `Avatar.qml`                        | Display source artwork at the reference aspect ratio   |
| `user_messages`  | `UserInput.qml`, `SubmitButton.qml` | Styled text entry, validation and keyboard focus       |
| `qr_code`        | `RepositoryHandoff.qml`             | Locally generated QR and readable repository URL       |

- `Theme.qml`: manually map every YAML token to a named QML property; record the source token beside it, including resolved aliases.
- Convert `px` values to numeric reference-canvas pixels; preserve exact colors, weights and spacing. YAML stays the visual authority.
- Screen-specific geometry belongs in `Start.qml`, `Input.qml` and `Running.qml`; component defaults remain shared.
- Running: clipped, vertically scrolling transcript; auto-scroll on insertion; water indicator outside the scrolling container at x1088/y96.
- Keep long messages wrapped within transcript width; preserve the 96px gap below its reference viewport.
- Compare 1280 × 720 captures to Figma; check fonts, line wraps, fixed indicator and all water/error states.

### Water level — `water_level` (`9:391`)

Six variants: `Level=0`, `Level=1`, `Level=2`, `Level=3`, `Level=4`, `Level=5`. Each uses `{components.water_level.width}` × `{components.water_level.height}`, with a `{components.water_level.borderWidth}` border in `{colors.primary}`, `{components.water_level.rounded}` corners, and `{components.water_level.padding}` inset. The screenshot shows a five-by-five grid: levels 1–5 fill successive rows from the bottom in `{colors.water}`. Level 0 is a fully `{colors.error}` grid, **not** a `{colors.water}` full tank or a blank grid.

Five passive switches are the working hardware assumption. The controller normalizes them bottom → top into levels 0–5; the UI never interprets raw GPIO. Initial polarity is wet=1, configurable after testing. Level 0 means below the lowest switch, operationally empty; level 5 means the highest switch is wet. Only contiguous wet patterns are valid. Wiring, filtering, fault handling and calibration are defined in [PRODUCT.md §4](PRODUCT.md#4-sensor-assumptions-and-calibration); refill behavior is in [§3](PRODUCT.md#3-interaction-defaults).

**Unknown/fault default:** keep the water indicator footprint and outline, hide the last numeric fill, and show a black `?` on white. Pair it with a red sensor-status message. Do not display unknown as level 0. This is an implementation fallback, not a Figma variant.

### Agent icon — `agent_icon` (`9:469`)

Variants `State=running` (`9:468`) and `State=error` (`9:467`), both `{components.agent_icon.width}` × `{components.agent_icon.height}`. Running is a simulation of 3 active dots colored `{colors.primary}` and 5 inactive dots `{colors.secondary}`; error is `{colors.error}`. Preserve the pixel patterns, not just a color swap. Pair icons with status text. Default: use the source static running pattern; no animation behavior is established by Figma. Water/sensor pauses use the error pattern alongside the relevant status message.

### Agent messages — `agent_messages` (`9:558`)

| Source variant                    | Node    | Treatment                                                                                                                                                          |
| --------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Type=task, Variant=H1`           | `9:578` | `{components.agent-task.typography}` with `{components.agent-task.fontStyle}` style and `{colors.primary}` text; heading with `#`; `{size.m}` horizontal gap       |
| `Type=task, Variant=body`         | `9:557` | `{components.agent-task.typography}` with `{components.agent-task.fontStyle}` style and `{colors.primary}` narrative                                               |
| `Type=action, Variant=running`    | `9:553` | Running icon and `{components.agent-action.typography}` progress text with `{components.agent-action.fontStyle}` style; `{components.agent-action.gap}` gap        |
| `Type=action, Variant=error`      | `9:559` | Error icon and `{components.agent-action.typography}` progress text with `{components.agent-action.fontStyle}` style; `{components.agent-action.gap}` gap          |
| `Type=error, Variant=water_level` | `9:556` | `{components.agent-error.typography}` headline in `{colors.error}` and `{typography.body}` body in `{colors.primary}`; `{components.agent-error.gap}` vertical gap |
| `Type=output, Variant=H1`         | `9:554` | `{components.agent-output.typography}` heading in `{colors.primary}` with `#`; `{size.m}` horizontal gap                                                           |
| `Type=output, Variant=body`       | `9:555` | `{components.agent-output.typography}` completion narrative in `{colors.primary}`                                                                                  |

Progress copy such as “Working on creating the backend” represents simulated activity only. The final output must summarize what the performance presented as tackled and accompany a QR code to the app repository; it must not imply an actual coding pipeline in project documentation.

### Avatar — `avatar` (`16:105`)

A `{components.avatar.width}` × `{components.avatar.height}` pixel-wave motif in `{colors.primary}`, built from square cells. Keep the source artwork and aspect ratio. No responsive size or animation is defined.

### User controls — `user_messages` (`16:185`)

- `Type=text` (`16:183`): source size `{components.user-text.width}` × `{components.user-text.height}`, `{components.user-text.borderWidth}` border in `{colors.primary}`, `{components.user-text.rounded}` corners, `{components.user-text.padding}` padding, and `{components.user-text.typography}` text. Its `...` is sample content, not a sufficient accessible label.
- `Type=button` (`16:184`): source size `{components.user-button.width}` × `{components.user-button.height}`, filled with `{colors.action}`, `{components.user-button.borderWidth}` border in `{colors.primary}`, `{components.user-button.rounded}` corners, `{components.user-button.padding}` padding, and `{components.user-button.typography}` `>` glyph in `{colors.primary}`.

**Keyboard defaults:** use QML text-entry and button behavior with custom visuals; no platform-default skin. Focus the field on entry; ENTER submits; Tab reaches the button; Space/ENTER activates the focused button. Provide accessible names. Input is single-line; validation and length limits are in PRODUCT.md.

**Additional control states:** implementation defaults, not existing Figma variants. Use a 2px external `{colors.action}` focus outline without changing layout dimensions. Keep the button fill unchanged on hover/press; prevent duplicate activation. For empty input, disable submission and use `{colors.secondary}` button fill. Place validation text in `{colors.error}` above the input row. Restore the defined action fill when valid.

### Repository handoff — `qr_code` (`16:608`)

QR artwork in `{colors.primary}` and `{colors.surface}` at `{components.qr_code.width}` × `{components.qr_code.height}`. This draft does not verify its encoded destination. The final QR must lead to the approved app repository, not be copied as an arbitrary decorative image.

**QML implementation:** generate the QR locally from the configured, owner-approved repository URL and display it with a readable link. Keep square modules and a four-module quiet zone within the reserved footprint; use integer module sizes and centered whitespace rather than interpolation. TH-09 owns generation; TH-11 verifies phone scanning on the HDMI screen. Repository selection remains open; the staged agent does not generate repositories.

## Do's and Don'ts

- **Do** retain exact source component names and variant values in the mapping to QML components.
- **Do** keep content in local JSON and all runtime fonts/assets local.
- **Do** keep visual rendering in QML and experience/sensor state in the Python controller.
- **Don't** add generic rounded cards, shadows, gradients, or unobserved font weights.
- **Don't** describe staged backend creation, code execution, deployment, or repository generation as implemented capabilities in project documentation. This does not require visitor-facing disclosure of the performance's staged nature.
