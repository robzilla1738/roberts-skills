# Native verification checklist

> Phase 9 — hard gate before scaffold complete. Back to [SKILL.md](SKILL.md).

Run after Phase 8 (integrations) completes, or after Phase 7 when add-ons = `none`.

---

## Automated commands

From project directory:

```bash
# macOS app
xcodebuild -project MyMacApp.xcodeproj -scheme MyMacApp \
  -destination 'platform=macOS' \
  CODE_SIGNING_ALLOWED=NO \
  build test

# iOS app (adjust simulator name)
xcodebuild -project MyApp.xcodeproj -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  CODE_SIGNING_ALLOWED=NO \
  build test
```

All must exit **0**. Fix failures before claiming done.

For SPM-only projects: `swift build && swift test`.

---

## Manual smoke tests — core

| # | Test | Expected |
|---|------|----------|
| 1 | Launch in Simulator / Run on Mac | App opens to shell |
| 2 | Navigate primary structure | No crash |
| 3 | Open Settings | Integration flags visible |
| 4 | SwiftData or API demo | Create/read sample succeeds |
| 5 | Sign in with Apple (if enabled) | Sheet presents; cancel is safe |

---

## Manual smoke tests — macOS

| # | Test | Expected |
|---|------|----------|
| M1 | `⌘,` | Settings window opens |
| M2 | App menu → About | About panel appears |
| M3 | App-specific command shortcut | Action fires (or disabled state correct) |
| M4 | Resize to minimum window size | Layout does not clip critical controls |
| M5 | Menu bar app: click status item | Popover/window opens |
| M6 | Sparkle: Check for Updates (no feed) | Disabled or no crash |
| M7 | `codesign --verify --deep --strict MyApp.app` (signed local build) | Passes when user signs |

---

## Manual smoke tests — integrations

| Add-on | Test | Expected |
|--------|------|----------|
| `revenuecat` | Launch without key | No crash; upgrade shows not configured |
| `revenuecat` | Launch with sandbox key | Offerings load or clear SDK error |
| `sparkle` | Launch without feed URL | No crash; menu item disabled |
| `sentry` | Launch without DSN | No crash |
| `posthog` | Launch without key | No crash |
| `sign-in-with-apple` | Tap sign in | System sheet appears |
| `storekit2` | Products load (StoreKit config) | IDs resolve or empty state |
| `apns` | Simulator launch | Registration stub does not crash |

---

## README must include

- Platform family + native profile ID + macOS app style (if applicable)
- Confirmed add-ons + xcconfig / Info.plist keys
- Distribution path (MAS / direct / both) + sandbox on/off
- Entitlements summary
- Build/test commands
- [production-habits-native.md](production-habits-native.md) checklist (unchecked)
- Pointer to **ios-design** / **macos-design** for UI iteration

---

## Handoff

Suggest **`/review`** (autoreview). For direct Mac builds, mention **macos-sandbox** before first ship.
