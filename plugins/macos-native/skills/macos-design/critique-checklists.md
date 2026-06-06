# Critique Checklists

> Read when: design review, anti-patterns, output templates, or launch checklist. Back to [SKILL.md](SKILL.md).

## 1. Design critique checklist

Use this checklist to review a generated macOS design.

### 1.1 Native structure

- Does the app have a complete menu bar command model?
- Does it use standard window behavior?
- Does it support Settings with Command-Comma if appropriate?
- Are standard File/Edit/View/Window/Help expectations met?
- Are toolbar and context-menu commands mirrored in menus where needed?

### 1.2 Layout

- Is the primary content visually dominant?
- Are sidebar, content, and inspector roles clear?
- Does the layout resize gracefully?
- Are minimum sizes defined?
- Does the app avoid hard-coded toolbar/control heights?
- Are empty states useful?

### 1.3 Liquid Glass/materials

- Is glass used only for suitable chrome/top-level controls?
- Are content cards/tables free of unnecessary glass?
- Are nested glass layers avoided?
- Is tint meaningful and restrained?
- Does the design work with Reduce Transparency and Increase Contrast?

### 1.4 Menus and shortcuts

- Are standard shortcuts preserved?
- Are frequent commands accelerated?
- Are unavailable commands disabled instead of mysteriously hidden?
- Are command names consistent across UI locations?
- Are context menus contextual?

### 1.5 Safe areas and camera housing

- Are top-aligned controls safe in full screen?
- Does the design avoid the camera housing?
- Does full-screen media/canvas content use safe areas correctly?
- Has the design been tested on notched and non-notched displays?

### 1.6 Accessibility

- Can the app be used without a mouse?
- Are icon-only controls labeled?
- Are custom controls accessible?
- Is reading order logical?
- Is contrast sufficient over materials?
- Are motion/transparency settings respected?

### 1.7 Visual polish

- Are typography, spacing, and alignment consistent?
- Are icons from SF Symbols where possible?
- Is the app icon direction appropriate for modern layered icons?
- Are colors semantic and adaptive?
- Does the app avoid web-app chrome and fake macOS elements?


## 2. Anti-patterns to reject

Reject or revise these:

- A macOS app with no menu bar command design.
- A custom top navigation bar pretending to replace the system menu bar.
- Fake traffic-light buttons.
- Fake notch/camera housing inside standard app window content (does not apply to intentional notch-style utility apps built per [macos-notch](../macos-notch/SKILL.md)]).
- A single fixed-size window for a complex productivity app.
- Toolbars with every command crammed into one row.
- Sidebars used as command menus.
- Inspectors used as primary navigation.
- Context menus as the only place for important commands.
- Icon-only controls without accessibility labels.
- Nonstandard keyboard shortcuts for standard commands.
- Custom text editing that lacks standard Edit menu behavior.
- Hard-coded control heights that break in current macOS.
- Glass applied to every card, row, form, and panel.
- Multiple nested translucent layers with unreadable text.
- Brand color overwhelming system accent and semantic colors.
- Hover-only essential actions.
- Confirmation alerts for every harmless action.
- Permanent deletion without undo or confirmation.
- Empty states that only say “No data.”
- Progress indicators with no explanation or cancel path.
- Charts without accessible summaries or data alternatives.
- Layouts that break with localized text.
- Menu bar extras that exist only for branding.
- Constantly animated menu bar items.


## 3. Output templates for LLMs

### 3.1 Full design specification template

```md
# App Design Specification: [App Name]

## Product intent
- Primary users:
- Primary task:
- Secondary tasks:
- Session length:
- Data/document model:

## Native macOS architecture
- App type:
- Window model:
- Navigation model:
- Main menu structure:
- Settings model:
- Multiwindow behavior:
- Full-screen behavior:

## Layout
- Window regions:
- Sidebar:
- Main content:
- Inspector:
- Toolbar:
- Search:
- Empty states:
- Minimum size:
- Wide/narrow behavior:

## Commands
- App menu:
- File menu:
- Edit menu:
- View menu:
- Domain-specific menus:
- Window menu:
- Help menu:
- Keyboard shortcuts:
- Context menus:

## Visual design
- Typography:
- Color/materials:
- Liquid Glass usage:
- Icons/SF Symbols:
- App icon direction:
- Motion:

## Accessibility
- Keyboard flows:
- VoiceOver structure:
- Custom control semantics:
- Contrast/transparency/motion:
- Localization:

## Implementation plan
- SwiftUI components:
- AppKit components:
- OS availability:
- Data/state model:
- Testing plan:

## Launch checklist
- Menu bar complete:
- Keyboard shortcuts tested:
- Safe areas tested:
- Accessibility tested:
- Light/dark/high contrast tested:
- Localization expansion tested:
- Performance tested:
```

### 3.2 Quick design review template

```md
# macOS Design Review

## Summary
- Native fit:
- Main strengths:
- Highest-risk issues:

## Required fixes
1.
2.
3.

## Recommended improvements
1.
2.
3.

## Menu/command audit
- Missing commands:
- Shortcut conflicts:
- Context menu issues:

## Layout audit
- Resize behavior:
- Sidebar/content/inspector hierarchy:
- Empty/error states:

## Visual audit
- Liquid Glass use:
- Typography:
- Color/materials:
- Icons:

## Accessibility audit
- Keyboard:
- VoiceOver:
- Contrast/motion/transparency:

## Implementation notes
- SwiftUI/AppKit changes:
- Availability/fallbacks:
```

### 3.3 Prompting pattern for generating native macOS UI

When generating code, ask the model to produce:

```text
Design a native macOS [app type] using SwiftUI first, AppKit only where needed.
Include: WindowGroup/Settings scenes, NavigationSplitView layout, toolbar, searchable, menu commands, keyboard shortcuts, context menus, accessibility labels, empty states, safe-area/full-screen notes, and Liquid Glass usage only where appropriate. Avoid custom fake macOS chrome. Use semantic colors and SF Symbols. Include availability checks for macOS 26-era APIs and fallbacks for earlier macOS versions.
```


## 4. Source map for ongoing verification

Use these Apple resources to verify current details before shipping:

- Apple Human Interface Guidelines: Designing for macOS
- Apple Human Interface Guidelines: Layout, Windows, Toolbars, Menus, The Menu Bar, Sidebars, Search fields, Context menus, Going full screen, Color, Materials, Typography, SF Symbols, App icons, Accessibility
- Apple Design: current design resources and “new design” overview
- Apple Design Resources: macOS UI kits, app icon templates, color resources, fonts
- SF Symbols app and documentation
- Icon Composer documentation
- WWDC: Meet Liquid Glass
- WWDC: Get to know the new design system
- WWDC: Build a SwiftUI app with the new design
- WWDC: Build an AppKit app with the new design
- WWDC: Make your Mac app more accessible to everyone
- AppKit documentation: `NSScreen.safeAreaInsets`, `NSScreen.auxiliaryTopLeftArea`, `NSScreen.auxiliaryTopRightArea`, `NSScreen.visibleFrame`, `NSPrefersDisplaySafeAreaCompatibilityMode`
- SwiftUI documentation: `NavigationSplitView`, `ToolbarItem`, `ToolbarItemGroup`, `ToolbarSpacer`, `searchable`, `inspector`, `MenuBarExtra`, `commands`, `GlassEffectContainer`, `glassEffect`, `GlassButtonStyle`
- AppKit documentation: `NSToolbar`, `NSMenu`, `NSMenuItemValidation`, `NSSplitViewController`, `NSGlassEffectView`, `NSGlassEffectContainerView`, `NSBackgroundExtensionView`


## 5. Final generation checklist

Before delivering a macOS app design or code scaffold, confirm:

- The app has a native menu bar command model.
- Standard menu items and shortcuts are preserved.
- The toolbar contains only high-frequency commands and is logically grouped.
- Sidebars, inspectors, and split views use standard platform containers.
- The main content remains visually dominant.
- Liquid Glass is used sparingly and only for appropriate chrome.
- Text over materials remains readable.
- The design handles full screen, safe areas, and camera housing.
- The layout resizes gracefully and avoids fixed control heights.
- Every icon-only control has an accessibility label.
- Every critical action has keyboard access.
- Context menus supplement rather than replace primary commands.
- Empty, loading, error, permission, and no-results states are designed.
- Light mode, dark mode, high contrast, Reduce Transparency, and Reduce Motion are considered.
- Localization and text expansion are considered.
- Performance is considered for large lists, tables, previews, effects, and scrolling.
- OS availability checks and fallbacks are included for current-design APIs.
## Related topics

- [foundations.md](foundations.md) — design principles and anti-pattern context
- [accessibility.md](accessibility.md) — detailed accessibility requirements
- [toolbars-and-menus.md](toolbars-and-menus.md) — menu and command completeness
