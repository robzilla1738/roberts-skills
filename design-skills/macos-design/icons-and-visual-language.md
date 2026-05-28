# Icons and Visual Language

> Read when: typography, color, SF Symbols, app icons, shape, or motion. Back to [SKILL.md](SKILL.md).

## 1. Shape, corner radius, and concentricity

Modern Apple design emphasizes harmonious shapes. Rounded forms should relate to each other rather than appearing arbitrary.

### 1.1 Shape vocabulary

Use these shape types:

- **Rectangle with rounded corners** for windows, panes, fields, lists, and many compact controls.
- **Capsule** for large buttons, pills, segmented controls, and floating control groups.
- **Circle** for icon-only buttons when the action is compact and recognizable.
- **Concentric rounded rectangles** when a child view sits inside a rounded parent.

### 1.2 Concentricity

Concentricity means nested rounded shapes share a visually consistent center and curvature.

Rules:

- A child shape inside a rounded parent should use a smaller radius that visually follows the parent’s curve.
- Avoid “pinched” corners where inner and outer radii clash.
- Avoid tiny radii inside highly rounded containers.
- Avoid mixing capsules and rounded rectangles randomly.
- Use system shape APIs where available.

### 1.3 Control size implications

Modern macOS controls can vary by control size. Avoid fixed heights.

Rules:

- Use `.controlSize(...)` in SwiftUI or `controlSize` in AppKit.
- Let the system determine control metrics.
- Audit hard-coded constraints after adopting current SDKs.
- Use compact controls only where density is appropriate.
- Use large or extra-large primary buttons only where they support the flow.


## 2. Typography

### 2.1 System fonts

Use the system font family by default. On Apple platforms, San Francisco is designed for system UI and adapts across sizes, weights, and contexts.

Rules:

- Use semantic text styles where possible.
- Use system font metrics instead of fixed line heights.
- Use SF Mono or monospaced digits for code, logs, tables, timers, and aligned numeric data.
- Avoid decorative fonts in productivity UI.
- Avoid all caps except for small section labels where the style is clearly appropriate.

### 2.2 Hierarchy

A common Mac hierarchy:

- Window/document title
- Section header
- Body/list/table text
- Secondary explanatory text
- Caption/status text

Rules:

- Use weight and size sparingly.
- Prefer left-aligned text in forms and content-heavy UI.
- Keep line lengths readable.
- Use truncation carefully; provide tooltips or expansion for important truncated content.

### 2.3 Writing style

Rules:

- Be direct.
- Use sentence case for most labels.
- Use title case only where the platform convention or product style calls for it.
- Avoid jargon unless the user audience expects it.
- Button labels should say what happens.
- Error messages should explain recovery.


## 3. Color and materials

### 3.1 Semantic color

Use system semantic colors rather than hard-coded values.

Rules:

- Use primary, secondary, tertiary label colors for text hierarchy.
- Use system background/material roles for surfaces.
- Use accent color for selection and meaningful emphasis.
- Use semantic red/yellow/green/blue only for meaning.
- Test light mode, dark mode, high contrast, increased contrast, and vibrant sidebars.

### 3.2 Brand color

A Mac app can have brand identity without overpowering the UI.

Rules:

- Use brand color in app icon, onboarding, key illustrations, or occasional primary accents.
- Do not tint the entire interface.
- Do not override the user’s accent color casually.
- Make sure brand colors meet contrast requirements.

### 3.3 Materials

Use materials when they provide platform-native layering.

Rules:

- Prefer system materials to custom blur.
- Avoid stacking translucent materials.
- Ensure text over material remains legible.
- Respect Reduce Transparency.
- Use solid backgrounds when content density or accessibility requires it.


## 4. Icons, symbols, and app icons

### 4.1 SF Symbols

Use SF Symbols for common actions and objects.

Rules:

- Choose symbols that match system meaning.
- Use the same symbol for the same concept across the app.
- Pair symbols with labels when meaning is not obvious.
- Match symbol weight and scale to the surrounding text/control.
- Avoid editing SF Symbols in ways that break recognizability.
- Use variable or animated symbols only when motion communicates state.

### 4.2 Custom symbols

Create custom symbols only when no standard symbol matches.

Rules:

- Match SF Symbols optical weight and alignment.
- Provide variants for different weights/scales where needed.
- Test at small sizes.
- Ensure the symbol works in monochrome.

### 4.3 App icons

A modern Mac app icon should be distinctive, layered, and recognizable at many sizes.

Rules:

- Use Apple’s current app icon templates/resources.
- Build layered icons with current tooling where possible.
- Test Default, Dark, and Mono appearances if supported by the target OS.
- Avoid text in the icon.
- Avoid tiny details that disappear in the Dock, Spotlight, or Settings.
- Keep the silhouette clear.
- Do not use a screenshot of the app as the icon.

### 4.4 Icon usage in menus and toolbars

Rules:

- Toolbars can use symbol-only items for familiar actions, but provide labels/accessibility labels.
- Menus may use symbols where they improve scanability.
- Do not icon-decorate every command.
- Avoid duplicate-looking icons for unrelated actions.


## 5. Motion and animation

Motion should clarify cause, continuity, and state. It should not slow expert users down.

Rules:

- Use animation for transitions, insertion/removal, disclosure, drag/drop, and focus changes.
- Keep durations short and purposeful.
- Preserve spatial continuity.
- Avoid bouncing, pulsing, or decorative motion in productivity UI.
- Respect Reduce Motion.
- Provide non-motion cues for state changes.
- Avoid continuous animation in menu bar extras.

Liquid Glass-specific rules:

- Use system-provided glass interactions where possible.
- Do not invent heavy custom refraction animations.
- Avoid glass motion that interferes with reading or pointing.
## Related topics

- [liquid-glass.md](liquid-glass.md) — glass hierarchy and tinting
- [toolbars-and-menus.md](toolbars-and-menus.md) — icons in menus and toolbars
- [accessibility.md](accessibility.md) — contrast and Reduce Motion
