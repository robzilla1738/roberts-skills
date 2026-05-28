# Toolbars and Menus

> Read when: toolbars, menus, shortcuts, context menus, or menu bar extras. Back to [SKILL.md](SKILL.md).

## 1. Toolbars

A toolbar is for high-frequency, window-level commands. It is not a place to dump every feature.

### 1.1 Toolbar principles

- Put high-frequency commands in the toolbar.
- Keep complete command access in the menu bar.
- Group related controls.
- Separate primary actions from utility actions.
- Use labels where icons are ambiguous.
- Avoid unnecessary backgrounds and custom dividers.
- Let the system manage toolbar materials and overflow.
- Keep noninteractive text/status out of glass controls when possible.

### 1.2 Toolbar item grouping

Group by function and frequency:

```text
Navigation       View controls        Document actions       Primary action
Back/Forward     Layout/Sort/Filter   Share/Export           New/Create/Run
```

Rules:

- Use spacing to separate groups.
- Avoid grouping unrelated actions only for visual symmetry.
- Do not mix text-only labels and symbol-only buttons in the same small glass group if it makes scanning harder.
- Put destructive actions outside the main toolbar unless they are core and safe.
- Use menu buttons for lower-frequency groups.

### 1.3 Search in toolbars

For many Mac apps, search belongs in the toolbar, usually toward the trailing side.

Rules:

- Use a standard search field.
- Search the current logical scope unless the UI says otherwise.
- Make search results cancelable and reversible.
- Use `Command-F` for find/search in content.
- Use suggestions only when helpful.
- Do not make search compete with the primary action.

### 1.4 Toolbar customization

For complex productivity apps, consider allowing toolbar customization.

Rules:

- Provide good defaults.
- Do not require customization for basic usability.
- Keep menu commands available even if toolbar items are removed.
- Preserve user customization.

### Implementation

See [swiftui-patterns.md](swiftui-patterns.md) for the SwiftUI toolbar pattern.
### Implementation

See [appkit-patterns.md](appkit-patterns.md) for the AppKit toolbar pattern.


## 2. Menus and the menu bar

The menu bar is a defining macOS feature. It is the complete, discoverable command model for the active app. Toolbars and context menus should accelerate commands, not replace the menu bar.

### 2.1 Core menu principles

- Provide a standard app menu, File, Edit, View, Window, and Help where relevant.
- Preserve standard commands and shortcuts.
- Use predictable command names.
- Put commands in the menu where users expect them.
- Disable unavailable commands instead of hiding them when discoverability matters.
- Show keyboard shortcuts in main menus.
- Avoid showing keyboard shortcuts in context menus unless there is a strong platform reason.
- Use ellipses for commands that require more input before completing.
- Use checkmarks for persistent toggles.
- Use separators sparingly to group commands.
- Include Help search/documentation.

### 2.2 Standard menu structure

Use this as the default command skeleton.

```text
App menu
  About AppName
  Settings…                         ⌘,
  Services
  Hide AppName                      ⌘H
  Hide Others                       ⌥⌘H
  Show All
  Quit AppName                      ⌘Q

File
  New                               ⌘N
  Open…                             ⌘O
  Open Recent
  Close                             ⌘W
  Save                              ⌘S
  Save As…                          ⇧⌘S or ⌥⇧⌘S depending app convention
  Duplicate
  Rename…
  Move To…
  Export…
  Page Setup…
  Print…                            ⌘P

Edit
  Undo                              ⌘Z
  Redo                              ⇧⌘Z
  Cut                               ⌘X
  Copy                              ⌘C
  Paste                             ⌘V
  Paste and Match Style             ⌥⇧⌘V
  Delete
  Select All                        ⌘A
  Find
    Find…                           ⌘F
    Find Next                       ⌘G
    Find Previous                   ⇧⌘G
  Spelling and Grammar
  Substitutions
  Transformations
  Speech

View
  Show/Hide Toolbar
  Customize Toolbar…
  Show/Hide Sidebar                 ⌥⌘S or app-specific if standard differs
  Show/Hide Inspector               ⌥⌘I
  Zoom In                           ⌘+
  Zoom Out                          ⌘-
  Actual Size                       ⌘0
  Enter Full Screen                 ⌃⌘F

Window
  Minimize                          ⌘M
  Zoom
  Move Window to Left/Right Side of Screen where supported
  Show Previous Tab / Show Next Tab if using window tabs
  Bring All to Front

Help
  AppName Help
  Search field integrated by system
  Contact Support / Release Notes where appropriate
```

Adapt this skeleton to the app. Do not include irrelevant commands just to fill menus, but do include standard commands when the app supports them.

### 2.3 Command naming

Rules:

- Use verbs for actions: `Export…`, `Duplicate`, `Archive`, `Mark as Done`.
- Use nouns for destinations: `Projects`, `Inbox`, `Library`.
- Use `Show`/`Hide` for visibility toggles.
- Use `Enable`/`Disable` for feature state toggles.
- Use `Start`/`Stop`, `Pause`/`Resume`, `Connect`/`Disconnect` for stateful actions.
- Use ellipses only when the command opens a dialog or requires more input before taking effect.
- Avoid vague labels like `Manage`, `More`, `Do It`, `Process`, or `Advanced` unless no better label exists.

### 2.4 Keyboard shortcuts

Shortcuts should accelerate frequent actions and match Mac conventions.

Rules:

- Use standard shortcuts for standard commands.
- Avoid overriding universal shortcuts such as Command-C, Command-V, Command-Q, Command-W, Command-Tab, Command-Space, Command-Comma, Command-H, Command-M.
- Use Command for app shortcuts, Option for alternate versions, Shift for reverse/variant actions, and Control sparingly.
- Do not assign shortcuts to every command.
- Show shortcuts in the main menu.
- Make shortcuts work even when a toolbar button is not visible.
- Ensure keyboard shortcuts do not conflict with text input.

### 2.5 Context menus

Context menus expose object-specific actions without cluttering the main UI.

Rules:

- Context menus should be contextual, not global command dumps.
- Include only commands relevant to the clicked/selected object.
- Keep destructive actions separated and clearly labeled.
- Do not hide essential commands only in context menus.
- Do not rely on right-click as the only way to complete a task.
- If a command also exists in the menu bar, use the same label.

### 2.6 Menu icons

Modern macOS menus can use symbols in a leading column where helpful. Use icons carefully.

Rules:

- Use icons for recognizable, high-scan commands.
- Avoid adding icons to every menu item.
- Avoid unrelated icons that clutter scanning.
- Do not use different icons for the same command in different places.
- Prefer SF Symbols that match system meaning.
- If icons are ambiguous, the text label must carry the meaning.

### Implementation

See [swiftui-patterns.md](swiftui-patterns.md) for the SwiftUI commands pattern.
### Implementation

See [appkit-patterns.md](appkit-patterns.md) for the AppKit menu validation pattern.


## 3. Menu bar extras and status items

A menu bar extra is the small icon or title that appears on the right side of the macOS menu bar while an app or agent is running. It is appropriate for status, quick controls, and persistent background utilities. It is not a replacement for a full app interface.

### 3.1 Use a menu bar extra when

- The app provides ongoing background status.
- The user benefits from quick access while another app is frontmost.
- The app monitors something: sync, VPN, timer, battery, clipboard, audio, calendar, build status, uploads, automation.
- The app can provide a useful compact menu or popover.

### 3.2 Avoid a menu bar extra when

- The app has no persistent status or quick action.
- The menu bar item only duplicates the Dock icon.
- The item is promotional branding.
- The app would become unusable if the menu bar item is hidden.
- The item frequently changes width and causes distracting menu bar movement.

### 3.3 Menu bar extra design rules

- Let the user decide whether the menu bar extra is shown when possible.
- Provide access to important functionality elsewhere, such as the main window or Dock menu.
- Use a simple, template-style monochrome icon unless color conveys essential status.
- Keep dynamic text short and stable.
- Provide an accessible title/label.
- Provide Settings and Quit where appropriate.
- Do not animate continuously.
- Do not use a menu bar extra for alerts that should be notifications.
- Test on light and dark menu bars, with desktop tinting, full-screen apps, different display scale settings, and notched displays.

### 3.4 Practical menu bar icon sizing

Treat this as practical craft guidance, not a hard platform contract:

- Design the symbol to read clearly around 16–18 pt high.
- Keep it optically centered in the menu bar item.
- Prefer a vector or template image that the system can tint.
- Avoid thin strokes that disappear on high-density displays.
- Avoid full app icons in the menu bar.
- Provide selected/active state only when it communicates real status.

### 3.5 Menu versus popover

Use a **menu** when:

- Actions are simple commands.
- Status is brief.
- There is no need for custom layout.
- Keyboard scanning matters.

Use a **popover/window** when:

- The user needs richer controls.
- The UI includes forms, sliders, previews, or a list.
- The user may interact for more than a few seconds.
- You need custom layout or persistent state.

### Implementation

See [swiftui-patterns.md](swiftui-patterns.md) for the SwiftUI MenuBarExtra pattern.
## Related topics

- [swiftui-patterns.md](swiftui-patterns.md) — SwiftUI toolbar, commands, MenuBarExtra code
- [appkit-patterns.md](appkit-patterns.md) — AppKit toolbar and menu validation code
- [liquid-glass.md](liquid-glass.md) — glass on toolbars and navigation chrome
- [critique-checklists.md](critique-checklists.md) — menu and toolbar audit checklist
