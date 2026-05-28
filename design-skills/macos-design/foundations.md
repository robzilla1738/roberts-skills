# Foundations

> Read when: choosing app architecture, design principles, onboarding, privacy, or app-type patterns. Back to [SKILL.md](SKILL.md).

## 1. macOS mental model

macOS is a desktop productivity environment. People often use several apps at once, multiple windows, external displays, keyboard shortcuts, drag and drop, file workflows, and long-lived documents or projects. A Mac interface should support depth without feeling heavy.

Design implications:

- **Windows are workspace containers.** They can be moved, resized, tiled, minimized, restored, and used across displays.
- **The menu bar is global and persistent.** It exposes commands for the active app and supports keyboard discovery.
- **The Dock is an app-level affordance.** Users expect app launch, app switching, Dock menus, badges where appropriate, and persistent app identity.
- **Keyboard and pointer are primary.** Hover, right-click, drag, focus rings, shortcuts, and precise hit testing matter.
- **Users expect inspectability.** Toolbars, sidebars, inspectors, context menus, and settings help users understand and control complex tasks.
- **Users expect standard behaviors.** Undo, redo, copy, paste, find, print, save, export, preferences/settings, full screen, minimize, zoom, and help should behave predictably.
- **A Mac app can be dense without being cluttered.** Dense information is acceptable when hierarchy, alignment, typography, grouping, and spacing are clear.


## 2. Current macOS design direction

Modern Apple platforms share a more unified design foundation, with Liquid Glass used as an adaptive, translucent, dynamic material for controls and navigation. On macOS, this does not erase Mac-specific expectations: multiwindow productivity, keyboard acceleration, menu bars, precise pointer interaction, large canvases, and resizable layouts remain central.

Use the current direction like this:

- Let content occupy more of the canvas.
- Let toolbars, sidebars, inspectors, and floating controls feel lighter and more integrated.
- Use standard navigation containers so the system applies the new materials correctly.
- Remove legacy custom backgrounds, bevels, dividers, and decorative borders that fight the system.
- Keep hierarchy visible through layout, grouping, typography, and command structure.
- Use glass for top-level interactive chrome, not arbitrary content surfaces.
- Test in light and dark appearances, with varied desktop backgrounds, full-screen mode, external displays, and accessibility settings.


## 3. Design principles for beautiful macOS apps

### 3.1 Clarity

A Mac UI should make the next meaningful action obvious. Clarity comes from predictable placement, strong labels, system icons, consistent command names, readable typography, and correct menu organization.

Practical rules:

- Give primary views clear titles.
- Use noun labels for destinations and verb labels for actions.
- Use icons only when they are recognizable or paired with text.
- Keep related controls together and unrelated controls apart.
- Use disabled states instead of hiding commands when discoverability matters.
- Reserve destructive styling for truly destructive actions.

### 3.2 Deference to content

The app’s job is to help people work with their content. Avoid chrome that draws attention away from that content.

Practical rules:

- Prefer transparent or adaptive system chrome around content.
- Do not add decorative background panels unless they aid grouping or legibility.
- Avoid strong tints across the entire app.
- Use accent color for selection and meaningful emphasis, not branding wallpaper.
- In content-heavy apps, let the toolbar and sidebar recede.

### 3.3 Hierarchy

Hierarchy is not only visual weight; it is also command structure, keyboard focus, navigation depth, and window modality.

Practical rules:

- One primary action per context is usually enough.
- Primary actions can be prominent or tinted, but avoid making several actions compete.
- Secondary actions belong in menus, toolbar overflow, contextual menus, or inspectors.
- Use sidebars for primary navigation, inspectors for contextual properties, and sheets for window-modal decisions.

### 3.4 Consistency

Consistency lets users transfer knowledge from other Mac apps.

Practical rules:

- Follow standard menu order and shortcut conventions.
- Use system controls before custom controls.
- Use standard icons and symbols before custom glyphs.
- Use system color roles instead of fixed color values.
- Keep command names identical across menu, toolbar, context menu, and help.

### 3.5 Direct manipulation

Mac users expect to manipulate objects directly.

Practical rules:

- Support drag and drop for files, rows, cards, layers, and media where relevant.
- Show selection clearly.
- Provide resize handles, column resizing, split-view resizing, and reorder affordances where relevant.
- Use context menus for object-specific actions.
- Preserve undo for direct manipulation operations.

### 3.6 Forgiveness

Powerful apps should be safe to explore.

Practical rules:

- Implement undo and redo for editing, organizing, and destructive changes where feasible.
- Ask for confirmation only when undo is impossible or data loss is likely.
- Prefer reversible archive/remove flows over permanent deletion.
- Explain failures with clear recovery actions.

### 3.7 Accessibility

A beautiful Mac app works for users who rely on VoiceOver, keyboard navigation, Voice Control, Switch Control, increased contrast, reduced motion, larger text, reduced transparency, or custom accent colors.

Practical rules:

- Every interactive element needs a semantic role and accessible label.
- Every hover-only action needs a keyboard and VoiceOver-accessible alternative.
- Custom controls must expose values, actions, traits, and focus behavior.
- Group related content into meaningful accessibility containers.
- Test all critical flows without a mouse.


## 4. Choosing the app architecture

### 4.1 Common macOS app archetypes

#### Document editor

Use for writing, drawing, coding, design, spreadsheets, diagrams, project files, and media editing.

Recommended structure:

- Main document window
- Toolbar with document-level commands
- Optional left sidebar for navigator/library/layers
- Main editor/canvas
- Optional right inspector for properties
- File menu with New, Open, Close, Save, Duplicate, Export, Print where relevant
- Edit menu with Undo, Redo, Cut, Copy, Paste, Find, Select All
- View menu with Show/Hide Sidebar, Show/Hide Inspector, Zoom, Enter Full Screen
- Window menu with standard window commands
- Document state restoration and autosave if appropriate

#### Library/browser app

Use for mail, notes, bookmarks, photos, references, knowledge bases, tasks, inventory, and collections.

Recommended structure:

- Sidebar for accounts, folders, tags, or sources
- Content list, table, or grid
- Detail pane or preview pane
- Toolbar search at the top trailing area
- Filters and sort controls near the collection they affect
- Context menus on items
- Batch actions in toolbar or context menu
- Empty states for no items, no search results, no permission, and no connection

#### Dashboard/analytics app

Use for metrics, monitoring, finance, system status, operations, and reports.

Recommended structure:

- Sidebar or segmented scope selector
- Main content area with cards, tables, charts, and detail drill-downs
- Date range, filters, and export controls in toolbar or top content area
- Avoid excessive glass on data cards
- Use tables for dense numeric information
- Support copy/export and keyboard search

#### Utility app

Use for small tools, converters, timers, clipboard tools, screen utilities, VPN clients, launchers, sync tools, and lightweight automation.

Recommended structure:

- Small main window or menu bar extra
- Settings window for configuration
- Menu bar extra only when persistent background access is useful
- Clear status, start/stop, pause/resume, and quit commands
- Minimal, stable chrome

#### Media/canvas app

Use for maps, video, photo editing, design canvas, drawing, games, immersive content, and full-screen creative tools.

Recommended structure:

- Edge-to-edge content canvas
- Floating controls, tool palettes, or HUDs where useful
- Scroll edge effects for bars that overlap content
- Safe-area-aware full-screen behavior
- Keyboard shortcuts for tools and modes
- Clear separation between content and controls

#### Settings/control app

Use for preferences, device configuration, account setup, developer tools, and system-adjacent apps.

Recommended structure:

- Settings scene/window
- Sidebar or tabbed settings categories
- Form sections with clear labels and help text
- Restore defaults where relevant
- Inline validation
- No custom preferences layout that breaks standard keyboard navigation

### 4.2 SwiftUI versus AppKit

Prefer **SwiftUI** for new apps when:

- The app fits standard windows, split views, lists, forms, navigation, toolbars, menus, settings, and controls.
- You want fast adoption of current materials, appearance, accessibility, localization, and platform adaptation.
- You can express the interface declaratively.

Use **AppKit** when:

- You need mature document architecture, custom text editing, complex table/outline views, advanced window behavior, precise responder-chain control, custom drawing, menu bar extras with highly specific behavior, input event handling, or deep system integrations.
- You need to host legacy views or integrate with existing AppKit code.
- You need advanced full-screen, multiwindow, panel, or inspector behavior not yet exposed in SwiftUI.

Use **hybrid SwiftUI + AppKit** when:

- SwiftUI handles the app shell, menus, settings, simple panes, and standard controls.
- AppKit handles specialized editors, custom rendering, advanced text/table behavior, or complex window/panel interactions.

LLM rule: Choose SwiftUI by default for generated apps, then explicitly call out AppKit only for capabilities SwiftUI does not handle well.


## 5. Notifications, badges, and status

Rules:

- Use notifications only for timely, user-relevant events.
- Do not notify for routine success if the user is already watching the app.
- Provide notification settings.
- Use Dock badges only for counts/status the user expects.
- Use menu bar status only for ongoing background state.
- Make status text specific: `Uploading 3 files`, not `Working`.


## 6. App onboarding and first launch

Rules:

- Keep onboarding short.
- Teach by doing when possible.
- Ask for permissions at the moment of need.
- Let users skip nonessential setup.
- Provide a first useful empty state.
- Avoid modal tours that block exploration.
- Provide sample content only when it helps understanding.

Recommended first-launch sequence:

1. Welcome or empty state with one primary action.
2. Optional account/import/setup path.
3. Permission explanation only when needed.
4. Main app with sidebar/content visible.
5. Help or template links available but not intrusive.


## 7. Privacy and trust UI

Rules:

- Ask only for permissions the app truly needs.
- Explain the value before the system prompt.
- Keep privacy settings visible.
- Provide clear sign-out, disconnect, delete, and export-data paths where relevant.
- Avoid dark patterns around subscriptions, trials, or data sharing.
- Show local/remote/synced status clearly when data location matters.


## 8. Design patterns by app type

### 8.1 Notes or writing app

Recommended:

- Sidebar: folders/tags
- Content: note list
- Detail: editor
- Toolbar: new note, share/export, search, formatting toggle
- Menus: File New/Open/Export/Print, Edit text commands, Format menu if rich text
- Shortcuts: Command-N new note, Command-F find, Command-B/I/U formatting
- Inspector: metadata, tags, backlinks, document info
- Accessibility: editor headings, reading order, keyboard focus

Avoid:

- Hiding note creation only behind a floating button
- Custom text editor without standard editing commands
- Weak contrast over decorative backgrounds

### 8.2 Developer tool

Recommended:

- Sidebar: projects/files/runs
- Main: editor/log/table/canvas
- Inspector: diagnostics/properties
- Toolbar: run/stop, scheme/environment, search, filters
- Menus: Project/Run/Debug menus, standard Edit/View/Window/Help
- Keyboard: Command-R run, Command-. stop, Command-B build if appropriate
- Tables/logs: monospaced font, filtering, copy, export

Avoid:

- Hiding errors in transient toasts
- Ignoring keyboard shortcuts
- Overusing cards for dense logs

### 8.3 Finance/analytics app

Recommended:

- Sidebar: accounts/categories/reports
- Main: table + charts + detail drill-down
- Toolbar: date range, export, search, filters
- Menus: File import/export/print, Edit copy/find, View grouping/sort
- Tables: sortable columns, numeric alignment, copy/export
- Accessibility: chart summaries and data tables

Avoid:

- Color-only positive/negative distinctions
- Decorative translucent cards behind dense numbers
- Fixed-width layouts that fail with large numbers/locales

### 8.4 Media app

Recommended:

- Edge-to-edge media canvas
- Floating controls with system glass/material
- Sidebar/library optional
- Toolbar minimal and contextual
- Safe-area-aware full screen
- Keyboard shortcuts for playback/tools
- Clear focus and selection states

Avoid:

- Controls behind the camera housing
- Persistent opaque bars over media when floating controls work better
- Tiny unlabeled icon controls

### 8.5 Menu bar utility

Recommended:

- Template menu bar icon
- Short status menu or popover
- Main window or settings for deeper configuration
- Settings, Pause/Resume, Quit
- Notifications only for important events
- User control over launch at login and menu bar visibility

Avoid:

- Branding-only menu bar item
- Constant animation
- Requiring the menu bar extra as the only access path
## Related topics

- [layout-and-windowing.md](layout-and-windowing.md) — window models and layout regions
- [navigation.md](navigation.md) — navigation and interaction patterns
- [critique-checklists.md](critique-checklists.md) — output templates and launch checklist
