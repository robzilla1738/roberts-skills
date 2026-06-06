---
name: macos-design
description: >
  Design, critique, or scaffold native macOS applications using current HIG,
  Liquid Glass, menu/toolbar conventions, safe areas, accessibility, and
  SwiftUI/AppKit patterns. Use when the user invokes /macos-design or names
  this skill for macOS app design, UI review, native UI generation, or
  notch-style / Dynamic Island macOS apps.
disable-model-invocation: true
version: 2026-05-28.1
platforms: [macOS, SwiftUI, AppKit, Mac Catalyst]
primary_use_cases:
  - Generate a native macOS app design specification
  - Review a macOS UI for Apple-platform fit and polish
  - Produce SwiftUI or AppKit layout scaffolding
  - Design menu bars, toolbars, sidebars, inspectors, settings, menu bar extras, and full-screen experiences
  - Handle modern Liquid Glass, safe areas, camera housing, and accessibility responsibly
  - Design or implement notch-style apps with hardware-aligned top-center panels
---

# macOS Design

Hub skill for designing, critiquing, and scaffolding native macOS applications. Read this file first, then open only the spoke files relevant to the task.

## Mission

Create macOS applications that feel unmistakably native: powerful, spacious, precise, keyboard-friendly, accessible, and visually calm. Favor standard macOS structures and system components before custom UI. When custom UI is justified, make it harmonize with the system rather than compete with it.

This skill is written for an LLM. Use it as a design-generation and design-review checklist. It is not a substitute for Apple's Human Interface Guidelines, current SDK documentation, or testing in the latest Xcode/macOS, but it is structured to make generated macOS applications substantially more native and polished.

## Non-negotiable design stance

A generated macOS app should assume the following unless the user explicitly asks otherwise:

1. **Use native app structure.** A Mac app is not a web page in a resizable window. It has a menu bar, app menu, keyboard shortcuts, window management, settings, undo/redo where appropriate, contextual menus, help, accessibility, and standard system behaviors.
2. **Respect the content.** The interface should frame, organize, and accelerate the user's work. Avoid decorative chrome, gratuitous backgrounds, and UI effects that compete with content.
3. **Prefer system components.** SwiftUI and AppKit controls automatically adapt to appearance, accent color, accessibility settings, localization, input modes, and future OS updates. Custom controls inherit none of this unless you build it.
4. **Design for density and precision.** Mac users expect fast scanning, accurate selection, keyboard access, multiwindow workflows, drag and drop, resize behavior, and visible structure.
5. **Use Liquid Glass selectively.** In the current macOS design language, Liquid Glass belongs primarily to top-level controls, navigation, floating bars, and system-like chrome. Do not turn every card, table row, inspector, or content panel into glass.
6. **Treat the menu bar as part of the app.** Commands belong in predictable menus. Context menus and toolbars are accelerators, not replacements for the menu bar.
7. **Honor safe areas and the camera housing.** Never place essential content or controls where the menu bar, toolbar, rounded display corners, or camera housing can obscure them.
8. **Accessibility is part of the design, not a pass at the end.** Every generated design should include keyboard, VoiceOver, contrast, Reduce Transparency, Increase Contrast, Reduce Motion, and localization considerations.
9. **Target OS matters.** A design using macOS 26-era APIs should include availability checks and graceful fallbacks for earlier macOS versions.
10. **Do not imitate macOS superficially in standard app windows.** Fake traffic lights, fake title bars, fake menu bars, fake notches inside normal window content, and web-style side navigation usually make apps feel less native. Dedicated notch-style utility apps are a separate case — see the **macos-notch** skill (separate plugin).

## How to use this skill

### Read order

1. Read this hub (`SKILL.md`).
2. Use the topic router below to pick 1–3 spoke files (never all 11 unless doing a full audit).
3. Read those spoke files before producing output.
4. Finish design tasks with a template from [critique-checklists.md](critique-checklists.md).

### When creating a macOS app

Produce output in this order:

1. **Product intent.** Identify the app category, primary task, secondary tasks, user role, and expected session length.
2. **Native architecture.** Choose the window model, navigation pattern, menu structure, toolbar model, settings model, and document/data model.
3. **Layout blueprint.** Define regions, split views, sidebars, inspectors, content canvas/list/table, empty states, responsive behavior, minimum window size, and full-screen behavior.
4. **Interaction model.** Define menu commands, keyboard shortcuts, context menus, drag and drop, undo/redo, search, selection, focus, and pointer behavior.
5. **Visual system.** Define typography, system colors, materials, icons, Liquid Glass usage, spacing, shape, toolbar grouping, and app icon direction.
6. **Accessibility and localization.** Include semantic labels, keyboard-only flows, VoiceOver structure, contrast, motion, transparency, text expansion, and localized command names.
7. **Implementation plan.** Specify SwiftUI/AppKit components and API patterns, with OS availability checks.
8. **Quality checklist.** Include a launch-ready review checklist.

### When critiquing an existing macOS design

Inspect it against:

- Native structure
- Menu and command completeness
- Toolbar grouping and hierarchy
- Layout resilience
- Safe-area/camera-housing correctness
- Liquid Glass restraint
- Keyboard and accessibility support
- Icon, typography, color, and material consistency
- Empty, loading, error, and permission states
- Localization and scaling

Use [critique-checklists.md](critique-checklists.md) for the full audit sections and output templates.

## Topic router

| If the task involves… | Read |
|-----------------------|------|
| App archetypes, principles, mental model, privacy, onboarding, notifications, app-type patterns | [foundations.md](foundations.md) |
| Windows, split views, sidebars, inspectors, safe areas, camera housing, settings, controls, documents, performance | [layout-and-windowing.md](layout-and-windowing.md) |
| Sidebar/tab/segmented nav, search, drill-down, pointer/keyboard/gesture/drag-drop | [navigation.md](navigation.md) |
| Toolbars, menus, shortcuts, context menus, menu bar extras | [toolbars-and-menus.md](toolbars-and-menus.md) |
| Liquid Glass, glass hierarchy, materials restraint | [liquid-glass.md](liquid-glass.md) |
| Typography, semantic color, SF Symbols, app icons, shape/concentricity, motion | [icons-and-visual-language.md](icons-and-visual-language.md) |
| VoiceOver, keyboard, contrast, transparency, localization | [accessibility.md](accessibility.md) |
| SwiftUI shells, NavigationSplitView, commands, MenuBarExtra, code recipes | [swiftui-patterns.md](swiftui-patterns.md) |
| AppKit split views, responder chain, NSScreen safe areas, Mac Catalyst | [appkit-patterns.md](appkit-patterns.md) |
| Notch-style app, top-center panel, hardware-aligned notch UI, peek/HUD/shelf modules | the **macos-notch** skill (separate plugin) |
| Critique checklists, anti-patterns, output templates, source map, launch checklist | [critique-checklists.md](critique-checklists.md) |

### Common task bundles

| Task | Spokes to read |
|------|----------------|
| New app design spec | foundations → layout-and-windowing → navigation → toolbars-and-menus → icons-and-visual-language → accessibility → critique-checklists |
| Toolbar + menu review | toolbars-and-menus → critique-checklists |
| Liquid Glass audit | liquid-glass → icons-and-visual-language → critique-checklists |
| SwiftUI scaffold | foundations → layout-and-windowing → swiftui-patterns |
| AppKit / hybrid app | foundations → appkit-patterns → layout-and-windowing |
| Notch-style app | the **macos-notch** skill (foundations → module spokes → integration-shipping) + appkit-patterns → toolbars-and-menus → accessibility |
| Full design audit | All spokes + critique-checklists |

## Spoke index

| File | Contents |
|------|----------|
| [foundations.md](foundations.md) | Mental model, design principles, app archetypes, SwiftUI vs AppKit, onboarding, privacy, app-type patterns |
| [layout-and-windowing.md](layout-and-windowing.md) | Windows, layout regions, safe areas, controls, settings, errors, documents, performance |
| [navigation.md](navigation.md) | Sidebar/tab/segmented navigation, search, input and interaction |
| [toolbars-and-menus.md](toolbars-and-menus.md) | Toolbars, menus, shortcuts, context menus, menu bar extras |
| [liquid-glass.md](liquid-glass.md) | Liquid Glass placement, hierarchy, tinting, anti-patterns |
| [icons-and-visual-language.md](icons-and-visual-language.md) | Shape, typography, color, materials, icons, motion |
| [accessibility.md](accessibility.md) | VoiceOver, keyboard, contrast, transparency, localization |
| [swiftui-patterns.md](swiftui-patterns.md) | SwiftUI shells, NavigationSplitView, commands, searchable, MenuBarExtra |
| [appkit-patterns.md](appkit-patterns.md) | AppKit split views, responder chain, safe areas, Mac Catalyst |
| *(moved)* | Notch-style apps → the **macos-notch** hub skill (separate plugin) |
| [critique-checklists.md](critique-checklists.md) | Critique checklists, anti-patterns, output templates, source map, launch checklist |
