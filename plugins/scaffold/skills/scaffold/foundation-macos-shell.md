# macOS app shell (SwiftUI)

> Phase 3 for **`macos`** — native structure before feature work. Back to [SKILL.md](SKILL.md).

Aligns with **macos-design** — read hub + [swiftui-patterns.md](https://github.com/robzilla1738/roberts-skills/tree/main/plugins/macos-design/skills/macos-design/swiftui-patterns.md) for polish; this spoke is **scaffold infrastructure**.

---

## Non-negotiables (macOS)

1. **Real Mac app structure** — menu commands, Settings scene (`⌘,`), keyboard shortcuts, standard window chrome. Not a web page in a window.
2. **`Settings { }` scene** — never bury preferences only inside a custom modal.
3. **Commands in `.commands { }`** — File/Edit/View defaults + app-specific `CommandMenu`.
4. **Empty states** — `ContentUnavailableView` in list/detail panes.
5. **Minimum window size** — set on `WindowGroup` or root view; test at smallest size.
6. **Accessibility** — every interactive control has a label; support keyboard navigation to Settings.

---

## App style (from intake)

| Intake value | Scene model | Spoke section |
|--------------|-------------|---------------|
| `windowed` (default) | `WindowGroup` + optional `NavigationSplitView` | [Windowed productivity](#windowed-productivity) |
| `menu-bar` | `MenuBarExtra` + optional `WindowGroup` | [Menu bar utility](#menu-bar-utility) |
| `document` | `DocumentGroup` | [Document-based](#document-based) |
| `notch` | Stop UI here — hand off to **macos-notch** after shell | — |

Record app style in README and intake output.

---

## Shared `AppModel` (Swift 6)

Prefer `@Observable` over `ObservableObject` for new scaffold code:

```swift
import Observation

@Observable
@MainActor
final class AppModel {
    var selectedItemID: UUID?
    var searchText = ""
    var showUpgrade = false

    func openSettings() {
        NSApp.sendAction(Selector(("showSettingsWindow:")), to: nil, from: nil)
    }
}
```

Inject via `.environment(appModel)` (SwiftUI observation), not `environmentObject`.

---

## Windowed productivity

Default for `macos-productivity` and `macos-direct`.

```swift
import SwiftUI

@main
struct MyMacApp: App {
    @State private var appModel = AppModel()
    private let config = AppConfig.load()

    init() {
        SentryService.startIfNeeded(config)
        RevenueCatService.configureIfNeeded(config)
    }

    var body: some Scene {
        WindowGroup {
            MainWindowView()
                .environment(appModel)
                .frame(minWidth: 900, minHeight: 560)
        }
        .commands {
            SidebarCommands()
            ToolbarCommands()
            TextEditingCommands()

            CommandGroup(replacing: .appInfo) {
                Button("About \(Bundle.main.displayName)") {
                    NSApp.orderFrontStandardAboutPanel(options: [:])
                }
            }

            CommandMenu("Account") {
                Button("Upgrade…") { appModel.showUpgrade = true }
                    .disabled(!config.isRevenueCatConfigured)
            }
        }
        .defaultSize(width: 1100, height: 720)

        Settings {
            SettingsRootView(config: config)
                .environment(appModel)
        }
    }
}
```

### `MainWindowView` — `NavigationSplitView`

Three-column when data warrants it; two-column for simpler tools:

```swift
struct MainWindowView: View {
    @Environment(AppModel.self) private var appModel

    var body: some View {
        NavigationSplitView {
            SidebarView()
        } content: {
            ContentListView()
        } detail: {
            DetailPlaceholderView()
        }
        .searchable(text: Bindable(appModel).searchText, placement: .toolbar)
        .navigationTitle("My App")
    }
}
```

### Settings tabs

```swift
struct SettingsRootView: View {
    let config: AppConfig

    var body: some View {
        TabView {
            GeneralSettingsView()
                .tabItem { Label("General", systemImage: "gearshape") }
            IntegrationsStatusView(config: config)
                .tabItem { Label("Integrations", systemImage: "puzzlepiece.extension") }
            AdvancedSettingsView()
                .tabItem { Label("Advanced", systemImage: "slider.horizontal.3") }
        }
        .frame(width: 480, height: 320)
    }
}
```

`IntegrationsStatusView` — non-secret configured flags (Phase 6).

---

## Menu bar utility

For `macos-utility` when intake app style = `menu-bar`:

```swift
@main
struct UtilityApp: App {
    @State private var model = UtilityModel()

    var body: some Scene {
        MenuBarExtra("My Utility", systemImage: model.statusSymbol) {
            Text(model.statusLine)
            Divider()
            Button("Open…") { model.openMainWindow() }
            Button("Settings…") { model.openSettings() }
                .keyboardShortcut(",", modifiers: [.command])
            Divider()
            Button("Quit") { NSApplication.shared.terminate(nil) }
                .keyboardShortcut("q", modifiers: [.command])
        }
        .menuBarExtraStyle(.window) // or .menu per design

        WindowGroup(id: "main") {
            MainUtilityView()
                .environment(model)
        }
        .defaultLaunchBehavior(.suppressed) // menu-bar-first

        Settings {
            SettingsRootView(config: AppConfig.load())
        }
    }
}
```

**Best practice:** menu bar extra width should stay stable — avoid rapid title changes that resize the status item (see **macos-design** `layout-and-windowing.md`).

---

## Document-based

When intake app style = `document`:

```swift
@main
struct MyDocApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MyDocument()) { file in
            DocumentEditorView(document: file.$document)
        }
        Settings {
            SettingsRootView(config: AppConfig.load())
        }
    }
}
```

Enable sandbox **user-selected file** read/write entitlements per [distribution-macos.md](distribution-macos.md).

---

## Sparkle entry (direct distribution)

Wire updater from `@main` only when `sparkle` add-on confirmed — see [phase-native-integrations.md](phase-native-integrations.md#sparkle-macos-direct). Do not init Sparkle for Mac App Store builds.

---

## Phase exit

- [ ] App launches with correct scene model for intake app style
- [ ] `⌘,` opens Settings
- [ ] At least one app-specific command with keyboard shortcut
- [ ] Empty state visible in primary content area
- [ ] README notes **macos-design** for visual iteration

Next: Phase 4 — [stack-native-swiftui.md](stack-native-swiftui.md#data-layer).
