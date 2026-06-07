# Native stack and tooling (Swift / SwiftUI)

> Read when: Phase 1–2 bootstrap. Back to [SKILL.md](SKILL.md).

---

## Pinned targets (verify at scaffold time)

| Layer | Target | Role |
|-------|--------|------|
| Language | Swift 6.x | Strict concurrency enabled |
| UI | SwiftUI (primary) | `@Observable` over `ObservableObject` for new code |
| Apple SDK | iOS 18+ / macOS 15+ default | Deployment target from intake |
| Data | SwiftData (default) | Local persistence |
| Tests | XCTest | Unit tests |
| Package manager | SPM (in Xcode) | Dependencies |

---

## Project layout (`xcodeproj`)

**macOS:** canonical tree in [file-tree-macos.md](file-tree-macos.md) (xcconfig, entitlements, Services/).

**iOS:** same structure minus Sparkle; use tab/split shell from [foundation-ios-shell.md](foundation-ios-shell.md).

Use **one module** for scaffold; split targets later. Commit `.gitignore` from file-tree spoke.

---

## Bootstrap commands

**Xcode (preferred):** create via GUI or `xcodegen` if user already uses it — do not add xcodegen unless asked.

**SPM executable** (CLI tools / minimal Mac utilities):

```bash
mkdir MyApp && cd MyApp
swift package init --type executable
```

Add platform in `Package.swift`:

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [.macOS(.v15)],
    targets: [
        .executableTarget(name: "MyApp"),
        .testTarget(name: "MyAppTests", dependencies: ["MyApp"]),
    ]
)
```

---

## Testing

See [foundation-native-testing.md](foundation-native-testing.md) for XCTest layout, Swift 6 `@MainActor` tests, and CI commands.

---

## Data layer

### SwiftData (default)

```swift
import SwiftData

@Model
final class Item {
    var title: String
    var createdAt: Date

    init(title: String, createdAt: Date = .now) {
        self.title = title
        self.createdAt = createdAt
    }
}
```

Attach `.modelContainer(for: Item.self)` in `@main` App.

### Remote-only (`api-client`)

- `Services/APIClient.swift` — `URLSession`, typed `Decodable` responses
- Base URL from `AppConfig.apiBaseURL` (no secrets in repo)

---

## Capabilities checklist (README)

| Capability | When |
|------------|------|
| Sign in with Apple | Auth intake |
| Push Notifications | `apns` add-on |
| iCloud / CloudKit | `cloudkit` add-on |
| App Groups | widgets / extensions later |
| Hardened Runtime + Notarization | macOS direct |
| In-App Purchase | `revenuecat` / `storekit2` |

---

## Xcode project settings (best practice)

| Setting | Value |
|---------|--------|
| Swift Language Version | Swift 6 |
| Strict Concurrency | Complete |
| User Script Sandboxing | Enabled (Xcode 15+) |
| Generate Info.plist | Prefer generated + `INFOPLIST_KEY_*` from xcconfig |

Link **entitlements** file on macOS — [distribution-macos.md](distribution-macos.md).

---

## Pitfalls

- Hard-coding API keys — use [foundation-native-security.md](foundation-native-security.md)
- Sparkle in Mac App Store build — guard with `DIRECT_DISTRIBUTION` flag
- Missing `-ObjC` linker flag for some SDKs — follow SPM package README
- Fake macOS chrome (custom traffic lights) — use system window; see **macos-design**
- Skipping **ios-design** / **macos-design** for consumer UI — scaffold builds shell; design skills polish

Next: [foundation-native-config.md](foundation-native-config.md) (Phase 2).
