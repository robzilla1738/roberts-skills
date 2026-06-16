# iOS app shell (SwiftUI)

> Phase 3 for **`ios`**. Back to [SKILL.md](SKILL.md).

Aligns with **ios-design** — read hub + navigation/layout spokes for polish; this spoke is **scaffold infrastructure**.

---

## Non-negotiables (iOS)

1. **Native navigation** — `NavigationStack` (compact) or `NavigationSplitView` (iPad regular).
2. **Settings** — dedicated screen (not Mac `Settings` scene); link from toolbar or tab.
3. **Safe areas** — respect Dynamic Island, home indicator, keyboard.
4. **Empty states** — `ContentUnavailableView`.
5. **Touch targets** — minimum 44×44 pt.

---

## App entry

```swift
import SwiftUI
import SwiftData

@main
struct MyIOSApp: App {
    private let config = AppConfig.load()

    init() {
        SentryService.startIfNeeded(config)
        RevenueCatService.configureIfNeeded(config)
    }

    var body: some Scene {
        WindowGroup {
            RootTabView(config: config)
        }
        .modelContainer(for: Item.self)
    }
}
```

---

## Root layout

**iPhone:** `NavigationStack` + tab bar if 3+ top-level sections.

**iPad:** `NavigationSplitView` with sidebar list + detail.

```swift
struct RootTabView: View {
    let config: AppConfig

    var body: some View {
        TabView {
            NavigationStack {
                HomeView()
            }
            .tabItem { Label("Home", systemImage: "house") }

            NavigationStack {
                SettingsRootView(config: config)
            }
            .tabItem { Label("Settings", systemImage: "gearshape") }
        }
    }
}
```

---

## Upgrade / paywall stub

When `revenuecat` or `storekit2` confirmed — sheet from Settings:

```swift
.sheet(isPresented: $showUpgrade) {
    UpgradePlaceholderView(isConfigured: config.isRevenueCatConfigured)
}
```

---

## Phase exit

- [ ] Launches on iPhone simulator
- [ ] Settings shows integration status (non-secret)
- [ ] Empty state on primary list
- [ ] README points to **ios-design** for UI iteration

Next: Phase 4 — [stack-native-swiftui.md](stack-native-swiftui.md#data-layer).
