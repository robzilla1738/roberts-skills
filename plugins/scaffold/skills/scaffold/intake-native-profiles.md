# Native product intake (iOS / macOS)

> Phase 0b — after [platform-router.md](platform-router.md). Back to [SKILL.md](SKILL.md).

---

## Opening question (required)

Ask the user:

> **What are you building?** One sentence — e.g. "subscription Bible app for iPhone", "Mac menu bar timer", "direct-download productivity Mac app with auto-update".

Map to a **native profile** below. Default: **`ios-consumer`** or **`macos-productivity`** by platform family.

---

## Archetypes → native profile

| Archetype | When | Profile ID | Auth | Data | Distribution |
|-----------|------|------------|------|------|--------------|
| Consumer app | General iPhone/iPad app | `ios-consumer` | Sign in with Apple optional | SwiftData or API | App Store |
| Subscription app | Premium, IAP, paywall | `ios-subscription` | Sign in with Apple recommended | SwiftData + sync optional | App Store |
| Mac productivity | Windowed Mac app | `macos-productivity` | Optional | SwiftData or API | MAS or direct |
| Mac utility / menu bar | Small utility, menu bar extra | `macos-utility` | Rare | Local or light API | Often direct |
| Mac direct-download | Sold outside Mac App Store | `macos-direct` | Optional | Any | Direct + Sparkle |
| Native client only | API/backend exists elsewhere | `client-only` | Match backend | Remote API | Per platform |
| Extend existing | Xcode project started | `extend-existing-native` | Gap analysis | Partial | — |

### Profile notes

**`ios-subscription`**

- Recommend **`revenuecat`** (or `storekit2` if user wants zero third-party billing SDK)
- Recommend **`sign-in-with-apple`** when accounts matter
- Paywall stub screen; `Purchases.configure` guarded when API key missing
- README: App Store Connect products + RevenueCat dashboard checklist

**`macos-direct`**

- Recommend **`sparkle`** for auto-update (skip if user says Mac App Store only)
- Full distribution spoke: [distribution-macos.md](distribution-macos.md) — sandbox, signing, notarization
- App style usually `windowed` or `menu-bar`; entitlements per [file-tree-macos.md](file-tree-macos.md)
- Ship checklist: [production-habits-native.md](production-habits-native.md)

**`macos-utility`**

- Clarify: menu bar extra vs notch-style panel → if notch, route UI to **macos-notch** skill after scaffold shell
- Lighter test surface; still XCTest + build gate

**`client-only`**

- Skip backend scaffold; add typed API client + auth token storage
- Match env/config to existing API base URL

**`extend-existing-native`**

- Inventory: `.xcodeproj` / `.xcworkspace`, `Package.swift`, tests, entitlements
- Run only missing phases from [phases-native-greenfield.md](phases-native-greenfield.md)

---

## Integration triggers

Use these to build the **Recommended** add-ons list. User confirms before install.

| Trigger (product words) | Add-on ID | Platforms | Notes |
|-------------------------|-----------|-----------|-------|
| subscription, premium, paywall, IAP, in-app purchase | `revenuecat` | iOS, macOS | Default over raw StoreKit for cross-platform entitlements |
| subscription but no third-party SDK | `storekit2` | iOS, macOS | Native StoreKit 2 only |
| paywall UI experiments | `superwall` | iOS, macOS | Pairs with RevenueCat; optional |
| Mac direct download, outside App Store, auto-update | `sparkle` | macOS only | Not for Mac App Store builds |
| sign in, accounts, sync | `sign-in-with-apple` | iOS, macOS | Native auth |
| crash reporting, error monitoring | `sentry` | iOS, macOS | |
| analytics, funnels, feature flags | `posthog` | iOS, macOS | |
| push notifications, reminders | `apns` | iOS | Entitlements + stub registration |
| iCloud sync, CloudKit | `cloudkit` | iOS, macOS | SwiftData + CloudKit or CK API |
| backend API (you own server) | `api-client` | iOS, macOS | URLSession client + typed models (no SDK) |

Web-only add-ons (`stripe`, `resend`, `clerk`, `ai-sdk`) apply to **`web-next`** only — mention in `multi` plans when the backend is web.

---

## Secondary intake (required picks)

| # | Question | Options | Default |
|---|----------|---------|---------|
| 1 | Project name + directory | — | Ask |
| 2 | UI framework | `swiftui` \| `swiftui+appkit` | `swiftui` |
| 3 | Minimum OS | iOS `18` / `17` · macOS `15` / `14` | Latest minus one |
| 4 | **macOS app style** (macOS only) | `windowed` \| `menu-bar` \| `document` \| `notch` | `windowed` |
| 5 | Data layer | `swiftdata` \| `coredata` \| `remote-only` | `swiftdata` for local-first |
| 6 | Auth | `sign-in-with-apple` \| `none` \| `later` | Profile default |
| 7 | Distribution | `app-store` \| `direct` \| `both` | `app-store` (macOS direct → `direct` + Sparkle) |
| 8 | App Sandbox (macOS) | `on` \| `off` | `on` |
| 9 | **Add-ons** (Phase 8 install) | `none` or comma-separated IDs from triggers | **Recommend** then confirm |
| 10 | Xcode project shape | `xcodeproj` \| `spm-executable` | `xcodeproj` |

### macOS app style routing

| Style | Profile fit | Notes |
|-------|-------------|-------|
| `windowed` | `macos-productivity`, `macos-direct` | [foundation-macos-shell.md](foundation-macos-shell.md) |
| `menu-bar` | `macos-utility` | MenuBarExtra + suppressed default window |
| `document` | File-based tools | `DocumentGroup` + sandbox file entitlements |
| `notch` | HUD / island apps | Scaffold minimal shell → **macos-notch** skill |

**Add-ons rule:** every confirmed ID must be wired in [phase-native-integrations.md](phase-native-integrations.md) before verify. Do not README-only.

---

## Intake output template

```text
Platform family: macos
Native profile: macos-direct
Product: Productivity app sold from my website
Path: ./MyMacApp
UI: swiftui
Minimum macOS: 15
App style: windowed
Data: swiftdata
Auth: sign-in-with-apple
Distribution: direct
Sandbox: on
Recommended add-ons: sparkle, revenuecat, sentry
Add-ons (confirmed): sparkle, revenuecat, sentry
Project shape: xcodeproj

Phases: 0, 1, 2, 2b-security, 2c, 3, 4, 5, 6, 7, 8, 9
Skipped: —
Spokes: platform-router, intake-native-profiles, stack-native-swiftui,
  foundation-native-config, foundation-native-security, foundation-macos-shell,
  file-tree-macos, distribution-macos, phase-native-integrations,
  verification-native-checklist, production-habits-native (read)
Design reference: macos-design (visual polish after Phase 3)
```

Proceed to [phases-native-greenfield.md](phases-native-greenfield.md).
