# Layout and Windowing

> Read when: windows, split views, sidebars, inspectors, safe areas, settings, controls, or performance. Back to [SKILL.md](SKILL.md).

## 1. Window design

### 1.1 Window anatomy

A standard macOS window has:

- A frame/titlebar area with traffic light controls
- Optional toolbar/titlebar-integrated controls
- Content body
- Optional sidebars, split views, inspectors, sheets, and popovers
- Resize behavior and minimum/maximum constraints

Design rules:

- Do not fake traffic lights.
- Do not replace the titlebar unless the app’s workflow genuinely requires a custom title area.
- Keep resize behavior stable; avoid layouts that collapse unpredictably.
- Define a sensible minimum window size.
- Preserve system window behaviors: minimize, zoom, full screen, tabbing where appropriate, and state restoration.
- Put document/project identity in the window title or title area when useful.
- Use accessory views carefully; they must not crowd the toolbar.

### 1.2 Window types

#### Main window

Use for the primary app workspace.

Must support:

- Resizing
- Keyboard focus
- Toolbar/menu commands
- State restoration where appropriate
- Full-screen support when useful

#### Document window

Use when each file/project deserves its own workspace.

Must support:

- Document title
- Edited state
- Save/autosave behavior
- File menu commands
- Undo manager
- Recent documents

#### Utility/palette panel

Use for transient tools, inspectors, color panels, or floating palettes.

Rules:

- Keep panels narrow and focused.
- Avoid using a panel as a dumping ground for preferences.
- Ensure the main workflow still works when the panel is closed.

#### Settings window

Use for app-wide preferences and account/configuration.

Rules:

- Use standard Settings scene where possible.
- Group settings into clear categories.
- Avoid modal settings unless the user must complete setup before using the app.

#### Popover

Use for lightweight, contextual controls.

Rules:

- Keep popovers small and focused.
- Dismiss when the user completes the action or clicks away.
- Do not use a popover for a complex multi-step workflow.

#### Sheet

Use for window-modal tasks tied to a specific window or document.

Rules:

- Use when the user must complete or cancel before continuing in that window.
- Keep the sheet focused on a single decision or task.
- Make default, cancel, and destructive actions clear.

#### Alert

Use only for interruption-worthy conditions.

Rules:

- Avoid alerts for routine confirmation.
- Make the message specific.
- Make the recovery action clear.
- Put the safest button in the default position unless the context demands otherwise.

### 1.3 Full-screen behavior

A full-screen Mac app should feel spacious, not cramped. Standard toolbar/sidebar behavior is usually better than hiding everything.

Rules:

- Let content expand naturally.
- Do not hide essential controls without a reliable way to reveal them.
- Respect safe areas and the camera housing.
- Use floating controls only when they improve content focus.
- Do not place critical content at the extreme top center of a full-screen display.
- Test full screen on notched and non-notched Mac displays, external displays, and multiple display arrangements.

### 1.4 Window layout responsiveness

Every generated macOS layout should define behavior for:

- Minimum width and height
- Narrow window
- Wide window
- Full screen
- Sidebar collapsed and expanded
- Inspector hidden and shown
- Toolbar item overflow
- Large text or longer localized labels
- External display with different scale factor

LLM checklist:

- Does the main content remain usable at the minimum window size?
- Does the toolbar overflow gracefully?
- Are split panes resizable?
- Is the sidebar optional when space is constrained?
- Can the inspector be hidden?
- Does search remain discoverable?
- Does the layout avoid fixed pixel assumptions?


## 2. Layout systems

### 2.1 Use points, not pixels

macOS layout uses points. A point can map to different pixel counts depending on display scale. Do not hard-code pixel-perfect assets or dimensions unless generating raster artwork for a known asset slot.

Rules:

- Use system spacing where possible.
- Avoid hard-coded control heights.
- Avoid hard-coded assumptions about toolbar, menu bar, or titlebar height.
- Use Auto Layout, SwiftUI layout, safe area guides, and system containers.
- Test at different display scaling settings.

### 2.2 Common layout regions

A polished Mac app usually composes these regions:

```text
┌─────────────────────────────────────────────────────────────┐
│ Window titlebar / toolbar / search / primary actions         │
├───────────────┬─────────────────────────────┬───────────────┤
│ Sidebar       │ Main content                │ Inspector     │
│ Navigation    │ List, table, canvas, editor │ Properties    │
│ Sources       │ Detail, preview, document   │ Context tools │
└───────────────┴─────────────────────────────┴───────────────┘
```

Use:

- **Sidebar** for primary destinations and sources.
- **Main content** for the user’s work.
- **Inspector** for contextual details and properties.
- **Toolbar** for high-frequency commands and navigation controls.
- **Menu bar** for complete command access.
- **Context menu** for object-specific commands.

### 2.3 Sidebar

Use a sidebar for stable navigation across major sections, accounts, folders, projects, tags, or sources.

Rules:

- Keep sidebar items short and scannable.
- Use recognizable SF Symbols sparingly.
- Group related items with section headers.
- Keep the selected destination obvious.
- Allow the sidebar to collapse if the app benefits from more canvas space.
- Avoid putting transient filters or object properties in the primary sidebar.
- Do not use the sidebar as a menu replacement for commands.

Current-design guidance:

- Prefer standard `NavigationSplitView` or `NSSplitViewController` sidebars.
- Let the system apply modern sidebar materials and safe-area behavior.
- Remove legacy custom visual-effect backgrounds that fight the current design.
- Use background extension effects for media or canvas content that visually continues behind a sidebar, while keeping text and controls in safe, readable regions.

### 2.4 Inspector

Use an inspector for contextual properties of the current selection.

Rules:

- Inspectors should be optional and hideable.
- They should reflect the current selection, not primary navigation.
- Put frequent, simple edits near the content if that is faster; use the inspector for deeper properties.
- Use clear section headings and form labels.
- Avoid deep navigation stacks inside inspectors.
- Preserve selection when showing/hiding the inspector.

### 2.5 Split views

Use split views when multiple panes must be visible and resizable.

Rules:

- Use standard split view components.
- Provide sensible default pane widths.
- Define minimum and maximum widths.
- Remember user-adjusted widths where appropriate.
- Avoid too many vertical dividers.
- Do not create four or five equally prominent panes; choose a primary content pane.

### 2.6 Lists, outlines, tables, and grids

Choose the structure that matches the data:

- **List**: simple collection, single column, optional details.
- **Outline**: hierarchical collection, folders/projects/groups.
- **Table**: dense structured data with sortable columns.
- **Grid**: visual browsing, media, templates, thumbnails.
- **Canvas**: spatial manipulation, drawing, maps, diagrams.

Rules:

- Make selection states clear.
- Support keyboard navigation.
- Provide context menus on rows/items.
- Use column sorting where useful.
- Preserve scroll position and selection across updates.
- Avoid card layouts for dense data better shown as a table.
- Provide empty states and no-results states.
- Use progressive loading for large datasets.

### 2.7 Forms

Forms are common in settings, inspectors, account setup, and configuration.

Rules:

- Align labels consistently.
- Group related settings into sections.
- Put explanatory help text near the setting it explains.
- Use checkboxes for independent booleans, radio buttons for mutually exclusive options, pop-up buttons/menus for compact choice lists, and text fields for typed input.
- Validate inline where possible.
- Avoid modal error alerts for form validation unless the user is leaving the form.
- Do not mix too many control styles in one group.

### 2.8 Empty states

A good empty state explains the situation and gives a next step.

Types:

- First launch/no data
- No selection
- No search results
- Permission missing
- Network unavailable
- Sync pending
- Filter excludes all results
- Error loading data

Rules:

- Use concise title text.
- Explain only what helps the user act.
- Provide one primary action where possible.
- Avoid blaming the user.
- Avoid decorative illustrations that dominate a productivity app.


## 3. Safe areas, camera housing, and the “top notch”

Apple generally refers to the physical top-center display cutout on some Mac notebooks as the **camera housing**. In design and code, treat it as a safe-area constraint, not as a decorative feature.

### 3.1 Core rules

- Do not place essential controls, text, search fields, menus, or status indicators where the camera housing can obscure them.
- Do not assume every Mac has the same menu bar height, titlebar height, toolbar height, display scale, or safe area.
- Do not fake a notch inside app content.
- In standard windowed apps, let system windows, toolbars, and safe areas handle the top region.
- In custom full-screen apps, explicitly account for safe-area insets and auxiliary top-left/top-right areas.
- For media/canvas apps that opt into content around the camera housing, keep meaningful UI out of the obscured region and use the visible top-left/top-right auxiliary areas carefully.

### 3.2 When the user asks for a “top notch effect”

Interpret this in one of four ways:

1. **Safe-area-aware MacBook design.** Design content so it avoids the camera housing and looks intentional in full screen.
2. **Marketing mockup.** Render a MacBook-like frame with a camera housing for screenshots or promotional images.
3. **Immersive full-screen content.** Extend background/media behind the menu bar/camera housing while keeping controls and readable text in safe areas.
4. **Dedicated notch-style utility app.** A borderless top-center panel that merges with the camera housing — a Dynamic Island for macOS. Read the **macos-notch** skill (separate plugin).

LLM response rule: For standard windowed apps, recommend safe-area-aware layout. Do not recommend adding a fake notch to normal app UI. Only route to the **macos-notch** skill when the user explicitly wants a notch-style or Dynamic Island macOS app.

### 3.3 Full-screen compatibility

Some Mac models have a camera housing at the top center of the display. The system can use a compatibility mode to avoid placing app content under that area. Apps that draw custom full-screen content may need to evaluate safe areas and choose whether to extend content.

Implementation guidance:

- Use standard system full-screen behavior unless the app is media, game, design-canvas, or immersive content.
- If opting out of safe-area compatibility, audit every top-aligned control.
- Use `NSScreen.safeAreaInsets` to understand the unobscured region.
- Use `NSScreen.auxiliaryTopLeftArea` and `NSScreen.auxiliaryTopRightArea` for visible regions beside the camera housing.
- Use `NSScreen.visibleFrame` for the visible desktop area excluding system UI such as the menu bar and Dock.
- Test on notched and non-notched displays.

### Implementation

See [appkit-patterns.md](appkit-patterns.md) for the AppKit safe-area helper.
### Implementation

See [appkit-patterns.md](appkit-patterns.md) for the Info.plist compatibility key.


## 4. Controls

### 4.1 General control rules

- Use standard controls.
- Use standard sizes and metrics.
- Do not hard-code heights.
- Keep labels clear.
- Preserve focus rings.
- Provide disabled states.
- Provide tooltips only for supplementary explanation, not essential meaning.
- Pair icon-only controls with accessibility labels.
- Do not rely on hover to reveal essential controls.

### 4.2 Buttons

Use buttons for immediate actions.

Rules:

- Use a verb label.
- Use one primary button in a context.
- Use destructive styling only for destructive actions.
- In dialogs, ensure default/cancel/destructive roles are correct.
- For icon-only buttons, use a symbol with a label exposed to accessibility.

SwiftUI:

```swift
Button("Export…", systemImage: "square.and.arrow.up") {
    exportDocument()
}
.keyboardShortcut("e", modifiers: [.command, .shift])
```

### 4.3 Toggle, checkbox, and switch

Use:

- **Checkbox** for independent on/off settings in Mac forms.
- **Toggle/switch** for immediate state changes, especially modern SwiftUI settings.
- **Radio buttons** for mutually exclusive choices where all options should be visible.
- **Pop-up button/menu** for compact mutually exclusive choices.

Rules:

- Labels should describe the enabled state.
- Avoid negative labels like `Disable Auto Save` when `Auto Save` is clearer.
- Put explanatory text below complex settings.

### 4.4 Sliders

Use sliders for continuous values.

Rules:

- Show min/max or meaningful labels when the scale is not obvious.
- Use tick marks for discrete values.
- Consider a neutral/default value marker when relevant.
- Pair sliders with numeric fields when precision matters.

### 4.5 Text fields

Rules:

- Use placeholder text as a hint, not a label replacement.
- Validate input inline.
- Preserve user input on validation errors.
- Use secure fields for secrets.
- Use monospaced fonts for code, tokens, and aligned numeric IDs where useful.

### 4.6 Progress

Rules:

- Use determinate progress when total work is knowable.
- Use indeterminate progress when it is not.
- Provide cancel when the operation is long and cancelable.
- Explain what is happening in plain language.
- Do not block the whole app for background work unless necessary.


## 5. Settings and preferences

### 5.1 Settings structure

Use a Settings window for app-wide preferences.

Common categories:

- General
- Accounts
- Appearance
- Notifications
- Shortcuts
- Sync
- Advanced
- Privacy
- Extensions/Integrations

Rules:

- Do not overuse Advanced as a junk drawer.
- Put dangerous settings behind clear explanations.
- Use search in settings for complex apps.
- Save changes immediately unless the setting requires Apply/Revert semantics.
- Provide reset/default actions where useful.

### 5.2 Account and permission flows

Rules:

- Explain why permission is needed before triggering system permission prompts.
- Provide recovery when permission is denied.
- Use system authentication and account flows where available.
- Do not bury sign-out or delete-account actions.
- Make privacy implications clear.


## 6. Error handling and destructive actions

### 6.1 Error messages

A good error message contains:

- What happened
- Why it matters
- What the user can do next
- Optional technical detail behind disclosure/copy button

Bad:

```text
Error 4009
```

Better:

```text
The project couldn’t be uploaded because the server rejected the file format. Export as PDF or choose a different file.
```

### 6.2 Destructive actions

Rules:

- Use undo where possible.
- Use confirmation when deletion is permanent, expensive, or surprising.
- Put destructive buttons in a destructive role.
- Clearly name the object being affected.
- Avoid vague `Are you sure?` alerts.
- Separate destructive actions from common actions in menus and toolbars.


## 7. File, document, and data workflows

Rules:

- Support Finder drag/drop where useful.
- Use standard open/save panels.
- Respect sandbox security-scoped resources when applicable.
- Support autosave only when it fits the user’s mental model.
- Expose export separately from save when formats differ.
- Use recent documents for document-based apps.
- Preserve metadata and user intent when importing/exporting.


## 8. Performance and rendering polish

Beautiful Mac apps feel fast and stable.

Rules:

- Avoid custom blur/shadow effects when system materials suffice.
- Avoid applying glass/material to large scrolling content unnecessarily.
- Virtualize large lists/tables.
- Keep scrolling smooth.
- Avoid layout thrashing from constantly changing toolbar/menu bar extra widths.
- Use vector assets where possible.
- Provide placeholders for slow content.
- Keep main-thread work minimal.
- Defer expensive previews until needed.
- Test on battery and lower-power Macs, not only high-end machines.
## Related topics

- [foundations.md](foundations.md) — app archetypes and architecture
- [navigation.md](navigation.md) — sidebar, split view, and search placement
- [appkit-patterns.md](appkit-patterns.md) — NSScreen safe-area helpers
- [accessibility.md](accessibility.md) — keyboard and resize accessibility
