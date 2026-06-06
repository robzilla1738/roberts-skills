# Navigation

> Read when: sidebar/tab navigation, search, drill-down, or pointer/keyboard/gesture interaction. Back to [SKILL.md](SKILL.md).

## 1. Navigation patterns

### 1.1 Sidebar navigation

Best for:

- Source lists
- Folders
- Projects
- Accounts
- Major app sections
- Persistent collections

Avoid for:

- Short modal flows
- Object properties
- One-off filters
- Commands

### 1.2 Tab navigation

Use tabs when sections are peer destinations and the set is small and stable.

Rules:

- Keep tab labels short.
- Avoid tabs and sidebars competing for the same hierarchy.
- Do not put commands as tabs.
- If a tab is essentially a filter, consider a segmented control instead.

### 1.3 Segmented controls

Use segmented controls for compact switching among views or modes within a context.

Rules:

- Keep segment count low.
- Use text when icons are ambiguous.
- Do not use segmented controls for navigation with many destinations.
- Make selected state clear.

### 1.4 Breadcrumbs

Use breadcrumbs for deep hierarchical navigation where users need orientation.

Rules:

- Keep breadcrumbs compact.
- Make each segment clickable where possible.
- Do not duplicate a sidebar path unnecessarily.

### 1.5 Drill-down

Drill-down navigation is less central on Mac than on iPhone, but can work in inspectors, settings, and compact utility windows.

Rules:

- Preserve context.
- Provide clear back navigation.
- Avoid deep stacks inside a wide Mac window when a split view would be better.


## 2. Search and find

Search is often a primary Mac productivity accelerator.

### 2.1 Search types

- **Global app search**: searches across the app’s data.
- **Scoped search**: searches the current folder/project/account/view.
- **Find in document**: finds text or objects within the current document.
- **Command search/help search**: helps users find commands.
- **Spotlight/App Intents integration**: exposes app content/actions to system search where appropriate.

### 2.2 Search placement

- Put common search in the toolbar, often trailing.
- Put find-in-document in the Edit > Find menu and support Command-F.
- Use visible filters near the content they affect.
- Use advanced search only when simple search cannot cover the task.

### 2.3 Search behavior

Rules:

- Preserve user input until dismissed or reset.
- Show clear no-results states.
- Highlight matches where useful.
- Support keyboard navigation through results.
- Avoid surprising scope changes.
- Make search cancelable.
- Do not block typing with slow network calls; debounce or progressively load.

### Implementation

See [swiftui-patterns.md](swiftui-patterns.md) for the SwiftUI searchable pattern.


## 3. Input and interaction

### 3.1 Pointer

Rules:

- Use appropriate cursors for resize, text insertion, dragging, links, and unavailable actions.
- Provide clear hover feedback for interactive elements.
- Keep hit targets large enough for precise but comfortable pointing.
- Avoid tiny controls near window edges unless they are standard.

### 3.2 Keyboard

Rules:

- Support Tab/Shift-Tab navigation through forms and controls.
- Support arrow keys in collections.
- Support Command shortcuts for app commands.
- Support Escape to cancel or exit transient modes.
- Support Return/Enter for default actions where safe.
- Ensure shortcuts do not break text editing.

### 3.3 Trackpad gestures

Use gestures as accelerators, not requirements.

Examples:

- Pinch to zoom in canvas/media apps.
- Two-finger scroll in lists and canvases.
- Swipe navigation where conventional.
- Force click only as an optional enhancement.

### 3.4 Drag and drop

Rules:

- Support dragging files into document/library apps where useful.
- Support dragging rows/items to reorder or move when expected.
- Show clear insertion indicators.
- Support drag cancellation.
- Preserve undo for moves/reorders.
- Provide keyboard alternatives.

### 3.5 Multiwindow and multitasking

Rules:

- Do not assume only one window.
- Use document/window-specific state correctly.
- Keep commands targeted at the active window/selection.
- Support opening items in new windows where useful.
- Handle multiple displays.
- Restore windows and state thoughtfully.
## Related topics

- [toolbars-and-menus.md](toolbars-and-menus.md) — toolbar search placement and commands
- [swiftui-patterns.md](swiftui-patterns.md) — NavigationSplitView and searchable patterns
- [layout-and-windowing.md](layout-and-windowing.md) — sidebar and inspector layout
