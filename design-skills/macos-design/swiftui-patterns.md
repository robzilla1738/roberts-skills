# SwiftUI Patterns

> Read when: SwiftUI shells, NavigationSplitView, commands, or implementation scaffolding. Back to [SKILL.md](SKILL.md).

## 1. Implementation recipes

### 1.1 Standard SwiftUI Mac app shell

```swift
import SwiftUI

@main
struct NativeMacApp: App {
    @StateObject private var appModel = AppModel()

    var body: some Scene {
        WindowGroup("Projects") {
            MainWindowView()
                .environmentObject(appModel)
        }
        .commands {
            SidebarCommands()
            ToolbarCommands()
            TextEditingCommands()

            CommandMenu("Project") {
                Button("New Task…") { appModel.newTask() }
                    .keyboardShortcut("n", modifiers: [.command, .shift])

                Button("Archive") { appModel.archiveSelection() }
                    .disabled(!appModel.canArchiveSelection)
            }
        }

        Settings {
            SettingsRootView()
                .environmentObject(appModel)
        }
    }
}

final class AppModel: ObservableObject {
    @Published var canArchiveSelection = false

    func newTask() {}
    func archiveSelection() {}
}
```

### 1.2 NavigationSplitView shell

```swift
struct MainWindowView: View {
    @State private var selectedSection: SectionID? = .inbox
    @State private var selectedItem: ItemID?
    @State private var searchText = ""
    @State private var inspectorPresented = true

    var body: some View {
        NavigationSplitView {
            List(selection: $selectedSection) {
                Section("Library") {
                    Label("Inbox", systemImage: "tray").tag(SectionID.inbox)
                    Label("Projects", systemImage: "folder").tag(SectionID.projects)
                    Label("Archive", systemImage: "archivebox").tag(SectionID.archive)
                }
            }
            .navigationTitle("Library")
        } content: {
            ItemList(section: selectedSection, selection: $selectedItem, searchText: searchText)
                .navigationTitle(titleForSelectedSection)
        } detail: {
            if let selectedItem {
                DetailEditor(itemID: selectedItem)
                    .inspector(isPresented: $inspectorPresented) {
                        ItemInspector(itemID: selectedItem)
                    }
            } else {
                ContentUnavailableView(
                    "No Selection",
                    systemImage: "sidebar.right",
                    description: Text("Select an item to view its details.")
                )
            }
        }
        .searchable(text: $searchText, placement: .toolbar, prompt: "Search")
        .toolbar {
            ToolbarItemGroup {
                Button("Filter", systemImage: "line.3.horizontal.decrease.circle") {}
                Button("Sort", systemImage: "arrow.up.arrow.down") {}
            }

            ToolbarItem(placement: .primaryAction) {
                Button("New", systemImage: "plus") {}
            }
        }
    }

    private var titleForSelectedSection: String {
        switch selectedSection {
        case .inbox: return "Inbox"
        case .projects: return "Projects"
        case .archive: return "Archive"
        case nil: return "Library"
        }
    }
}

enum SectionID { case inbox, projects, archive }
struct ItemID: Hashable {}
```

### 1.3 Settings scene shell

```swift
struct SettingsRootView: View {
    var body: some View {
        TabView {
            GeneralSettingsView()
                .tabItem { Label("General", systemImage: "gearshape") }

            AppearanceSettingsView()
                .tabItem { Label("Appearance", systemImage: "paintbrush") }

            AccountSettingsView()
                .tabItem { Label("Account", systemImage: "person.crop.circle") }
        }
        .frame(width: 620, height: 420)
    }
}
```

### 1.4 Sheet pattern

```swift
struct RenameSheet: View {
    @Environment(\.dismiss) private var dismiss
    @State private var name: String
    let onRename: (String) -> Void

    init(currentName: String, onRename: @escaping (String) -> Void) {
        _name = State(initialValue: currentName)
        self.onRename = onRename
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Rename Project")
                .font(.title2)

            TextField("Project name", text: $name)
                .textFieldStyle(.roundedBorder)

            HStack {
                Spacer()
                Button("Cancel", role: .cancel) { dismiss() }
                    .keyboardShortcut(.cancelAction)

                Button("Rename") {
                    onRename(name)
                    dismiss()
                }
                .keyboardShortcut(.defaultAction)
                .disabled(name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
            }
        }
        .padding(24)
        .frame(width: 420)
    }
}
```

### 1.5 Accessible custom row

```swift
struct FileRow: View {
    let file: FileSummary

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: file.symbolName)
                .frame(width: 24)

            VStack(alignment: .leading) {
                Text(file.name)
                Text(file.detail)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Text(file.modifiedDate, style: .date)
                .foregroundStyle(.secondary)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(file.name), \(file.detail), modified \(file.modifiedDate.formatted(date: .abbreviated, time: .omitted))")
        .contextMenu {
            Button("Open") { open(file) }
            Button("Reveal in Finder") { reveal(file) }
            Divider()
            Button("Move to Trash", role: .destructive) { moveToTrash(file) }
        }
    }

    private func open(_ file: FileSummary) {}
    private func reveal(_ file: FileSummary) {}
    private func moveToTrash(_ file: FileSummary) {}
}

struct FileSummary {
    let name: String
    let detail: String
    let symbolName: String
    let modifiedDate: Date
}
```


### 1.4 SwiftUI searchable pattern

```swift
struct SearchableLibraryView: View {
    @State private var query = ""
    @State private var selectedScope: SearchScope = .currentProject

    var body: some View {
        NavigationSplitView {
            SidebarView()
        } detail: {
            ResultsView(query: query, scope: selectedScope)
        }
        .searchable(text: $query, placement: .toolbar, prompt: "Search")
        .searchScopes($selectedScope) {
            Text("Current Project").tag(SearchScope.currentProject)
            Text("All Projects").tag(SearchScope.allProjects)
        }
    }
}

enum SearchScope { case currentProject, allProjects }
```

### 1.5 SwiftUI toolbar pattern

```swift
import SwiftUI

struct ProjectWindow: View {
    @State private var searchText = ""
    @State private var inspectorPresented = true

    var body: some View {
        NavigationSplitView {
            SidebarView()
        } content: {
            ItemListView(searchText: searchText)
        } detail: {
            EditorView()
                .inspector(isPresented: $inspectorPresented) {
                    InspectorView()
                }
        }
        .searchable(text: $searchText, placement: .toolbar, prompt: "Search")
        .toolbar {
            ToolbarItemGroup(placement: .navigation) {
                Button("Back", systemImage: "chevron.left") { navigateBack() }
                Button("Forward", systemImage: "chevron.right") { navigateForward() }
            }

            ToolbarItemGroup {
                Button("Filter", systemImage: "line.3.horizontal.decrease.circle") { showFilters() }
                Button("Sort", systemImage: "arrow.up.arrow.down") { showSortOptions() }
            }

            ToolbarItem(placement: .primaryAction) {
                Button("New Item", systemImage: "plus") { createItem() }
            }
        }
    }

    private func navigateBack() {}
    private func navigateForward() {}
    private func showFilters() {}
    private func showSortOptions() {}
    private func createItem() {}
}
```

### 1.7 SwiftUI commands pattern

```swift
import SwiftUI

@main
struct ExampleMacApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            SidebarCommands()
            ToolbarCommands()

            CommandGroup(after: .newItem) {
                Button("New Project…") { newProject() }
                    .keyboardShortcut("n", modifiers: [.command, .shift])
            }

            CommandMenu("Project") {
                Button("Run") { runProject() }
                    .keyboardShortcut("r", modifiers: [.command])

                Button("Stop") { stopProject() }
                    .keyboardShortcut(".", modifiers: [.command])

                Divider()

                Button("Archive Project…") { archiveProject() }
            }
        }

        Settings {
            SettingsView()
        }
    }

    private func newProject() {}
    private func runProject() {}
    private func stopProject() {}
    private func archiveProject() {}
}
```

### 1.6 SwiftUI MenuBarExtra pattern

```swift
import SwiftUI

@main
struct UtilityApp: App {
    @StateObject private var model = UtilityModel()

    var body: some Scene {
        MenuBarExtra("Sync Status", systemImage: model.systemImageName) {
            Text(model.statusText)

            Divider()

            Button(model.isPaused ? "Resume Sync" : "Pause Sync") {
                model.togglePaused()
            }

            Button("Open Main Window") {
                model.openMainWindow()
            }

            Divider()

            Button("Settings…") {
                model.openSettings()
            }
            .keyboardShortcut(",", modifiers: [.command])

            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q", modifiers: [.command])
        }

        WindowGroup {
            MainUtilityWindow(model: model)
        }

        Settings {
            SettingsView(model: model)
        }
    }
}

final class UtilityModel: ObservableObject {
    @Published var isPaused = false
    var statusText: String { isPaused ? "Sync paused" : "Sync up to date" }
    var systemImageName: String { isPaused ? "pause.circle" : "checkmark.circle" }

    func togglePaused() { isPaused.toggle() }
    func openMainWindow() {}
    func openSettings() {}
}
```
## Related topics

- [appkit-patterns.md](appkit-patterns.md) — AppKit bridging and hybrid apps
- [toolbars-and-menus.md](toolbars-and-menus.md) — command and toolbar design rules
- [layout-and-windowing.md](layout-and-windowing.md) — window and split-view layout
- [liquid-glass.md](liquid-glass.md) — Liquid Glass usage rules
