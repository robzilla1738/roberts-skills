# Phases — native greenfield (iOS / macOS)

> Ordered execution with exit criteria. Back to [SKILL.md](SKILL.md).

**Rule:** Do not start phase N+1 until phase N's exit criterion passes. Skip phases per [intake-native-profiles.md](intake-native-profiles.md).

**macOS** phases reference additional spokes — open them when platform family is `macos`.

---

## Phase 0 — Platform + product intake

| | |
|--|--|
| **Actions** | [platform-router.md](platform-router.md) → [intake-native-profiles.md](intake-native-profiles.md) — recommend add-ons; post plan |
| **Exit** | Platform family, profile ID, macOS app style (if applicable), confirmed add-ons; user confirmed |

---

## Phase 1 — Bootstrap

| | |
|--|--|
| **Actions** | Create Xcode project or SPM executable; commit `.gitignore` |
| **Spoke** | [stack-native-swiftui.md](stack-native-swiftui.md), [file-tree-macos.md](file-tree-macos.md) (macOS) |
| **Exit** | Project opens in Xcode; app runs on Simulator / Mac |

**iOS:** File → New → App (SwiftUI, Swift). **macOS:** same with Mac target.

For `spm-executable`: `swift package init --type executable` + platform manifest in `Package.swift`.

---

## Phase 2 — Config and errors

| | |
|--|--|
| **Actions** | `AppConfig.swift`, `AppError.swift`, `Config/*.xcconfig` |
| **Spoke** | [foundation-native-config.md](foundation-native-config.md) |
| **Exit** | Config loads; missing secrets do not crash at launch |

---

## Phase 2b — Security (Keychain, ATS)

| | |
|--|--|
| **Actions** | `KeychainStore.swift`, xcconfig → Info.plist wiring, ATS defaults |
| **Spoke** | [foundation-native-security.md](foundation-native-security.md) |
| **Skip** | Never for apps with auth or any add-on |
| **Exit** | Secrets.example committed; Secrets.xcconfig gitignored |

---

## Phase 2c — Testing

| | |
|--|--|
| **Actions** | XCTest target + config/error tests |
| **Spoke** | [foundation-native-testing.md](foundation-native-testing.md) |
| **Skip** | Never |
| **Exit** | `xcodebuild test` or `swift test` passes |

---

## Phase 3 — UI shell

| | |
|--|--|
| **Actions** | Platform shell: navigation, Settings, commands (macOS), empty states |
| **Spoke** | [foundation-macos-shell.md](foundation-macos-shell.md) (macOS) · [foundation-ios-shell.md](foundation-ios-shell.md) (iOS) |
| **Design** | **macos-design** / **ios-design** — hub + 1–2 spokes for HIG alignment |
| **Skip** | `extend-existing-native` if shell exists |
| **Exit** | App launches to primary shell; `⌘,` Settings on macOS |

---

## Phase 4 — Data layer

| | |
|--|--|
| **Actions** | SwiftData model / Core Data stack / API client per intake |
| **Spoke** | [stack-native-swiftui.md](stack-native-swiftui.md#data-layer) |
| **Skip** | `remote-only` with `api-client` only |
| **Exit** | Sample read/write or API health call works |

---

## Phase 5 — Auth (optional)

| | |
|--|--|
| **Actions** | Sign in with Apple + Keychain persistence |
| **Spoke** | [phase-native-integrations.md](phase-native-integrations.md#step-6--sign-in-with-apple) |
| **Skip** | `auth: none` / `later` |
| **Exit** | Sign-in control present; cancel is safe |

---

## Phase 6 — App shell demos

| | |
|--|--|
| **Actions** | `IntegrationsStatusView`, About, Upgrade placeholder |
| **Exit** | Non-secret integration flags visible in Settings |

---

## Phase 7 — Distribution prep

| | |
|--|--|
| **Actions** | Entitlements, bundle ID, sandbox, signing/notarization README |
| **Spoke** | [distribution-macos.md](distribution-macos.md) (macOS) · iOS: App Store Connect notes in README |
| **Skip** | `extend-existing-native` if already configured |
| **Exit** | `.entitlements` committed; distribution checklist in README |

---

## Phase 8 — Integrations (intake add-ons)

| | |
|--|--|
| **Actions** | SPM packages; wire stubs per [phase-native-integrations.md](phase-native-integrations.md) |
| **Skip** | Add-ons = `none` only |
| **Exit** | Every confirmed add-on wired; launch safe without secrets |

---

## Phase 9 — Verify

| | |
|--|--|
| **Actions** | [verification-native-checklist.md](verification-native-checklist.md) |
| **Post** | [production-habits-native.md](production-habits-native.md) — document in README |
| **Exit** | Build + tests green; smoke table satisfied |

---

## Handoff

Scaffold complete after Phase 9. Suggest **`/review`** (autoreview).

| Platform | Next skill |
|----------|------------|
| macOS UI polish | **macos-design** |
| macOS notch | **macos-notch** |
| iOS UI polish | **ios-design** |
| Direct Mac smoke test | **macos-sandbox** |
