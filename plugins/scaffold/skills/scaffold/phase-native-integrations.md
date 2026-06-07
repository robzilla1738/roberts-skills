# Phase 8 — Native integrations (intake add-ons)

> Run after Phase 7, **before** Phase 9 verify. Back to [SKILL.md](SKILL.md).

**Skip** only when confirmed add-ons are exactly `none`.

Install SPM packages, extend `AppConfig`, add service stubs, and wire demo UI. Build and launch must succeed without secrets.

---

## Add-on matrix

| Add-on ID | SPM / SDK | Files to add / update |
|-----------|-----------|------------------------|
| `revenuecat` | [RevenueCat/purchases-ios](https://github.com/RevenueCat/purchases-ios) | `Services/RevenueCatService.swift`, paywall placeholder view |
| `storekit2` | Apple StoreKit | `Services/StoreKitService.swift`, product IDs in config |
| `superwall` | [Superwall/Superwall-iOS](https://github.com/superwall/Superwall-iOS) | `Services/SuperwallService.swift` — requires RevenueCat or StoreKit |
| `sparkle` | [sparkle-project/Sparkle](https://github.com/sparkle-project/Sparkle) | macOS only — `Services/SparkleUpdater.swift`, feed URL in config |
| `sentry` | [getsentry/sentry-cocoa](https://github.com/getsentry/sentry-cocoa) | `Services/SentryService.swift`, init in `@main` App |
| `posthog` | [PostHog/posthog-ios](https://github.com/PostHog/posthog-ios) | `Services/PostHogService.swift`, `.onAppear` identify stub |
| `sign-in-with-apple` | AuthenticationServices | `Services/AppleSignInService.swift`, capability + button |
| `apns` | UserNotifications | `Services/PushNotificationService.swift`, delegate stub |
| `cloudkit` | CloudKit / SwiftData | Model config + container identifier in entitlements |
| `api-client` | — (URLSession) | `Services/APIClient.swift`, health endpoint call |

Verify package URLs and versions in each project's README at scaffold time.

---

## Step 1 — Extend `AppConfig`

Add optional fields and `is*Configured` helpers for every selected add-on. Update `Secrets.example.xcconfig` in the same commit.

---

## Step 2 — `revenuecat`

Works on **iOS and macOS** via [purchases-ios](https://github.com/RevenueCat/purchases-ios) SPM.

```swift
import RevenueCat

enum RevenueCatService {
    static func configureIfNeeded(_ config: AppConfig) {
        guard let key = config.revenueCatAPIKey else { return }
        #if DEBUG
        Purchases.logLevel = .debug
        #endif
        Purchases.configure(withAPIKey: key)
    }

    static func offeringsConfigured() async -> Bool {
        guard AppConfig.load().isRevenueCatConfigured else { return false }
        _ = try? await Purchases.shared.offerings()
        return true
    }

    static var isPro: Bool {
        get async {
            guard let info = try? await Purchases.shared.customerInfo() else { return false }
            return info.entitlements.active["pro"] != nil
        }
    }
}
```

- Call `configureIfNeeded` from `@main` `init()` before UI appears
- **macOS:** add Upgrade command (see [foundation-macos-shell.md](foundation-macos-shell.md))
- **iOS:** `UpgradePlaceholderView` sheet from settings
- Add `Configuration.storekit` for local testing when StoreKit products exist
- README: RevenueCat project + App Store Connect / MAS product linking

---

## Step 3 — `sparkle` (macOS direct)

**Skip** when distribution = `app-store` only.

### SPM

Add [sparkle-project/Sparkle](https://github.com/sparkle-project/Sparkle) (2.x). Link `Sparkle.framework` to the app target.

### `Services/SparkleUpdaterController.swift`

Use Sparkle 2's standard controller — verify API against current Sparkle docs at scaffold time:

```swift
import Sparkle
import AppKit

@MainActor
final class SparkleUpdaterController: NSObject {
    private let updaterController: SPUStandardUpdaterController

    override init() {
        updaterController = SPUStandardUpdaterController(
            startingUpdater: false,
            updaterDelegate: nil,
            userDriverDelegate: nil
        )
        super.init()
    }

    func startIfConfigured(_ config: AppConfig) {
        guard let feedURL = config.sparkleFeedURL else { return }
        updaterController.updater.feedURL = feedURL
        try? updaterController.updater.start()
    }

    func checkForUpdates() {
        updaterController.checkForUpdates(nil)
    }
}
```

### Wire in `@main` App

```swift
@State private var sparkle = SparkleUpdaterController()

init() {
    // after config load
    sparkle.startIfConfigured(config)
}
```

### Commands menu

```swift
CommandGroup(after: .appInfo) {
    Button("Check for Updates…") {
        sparkle.checkForUpdates()
    }
    .disabled(!config.isSparkleConfigured)
}
```

### README (required)

- Generate EdDSA keys with Sparkle `generate_keys`; store private key in CI secrets
- Host HTTPS `appcast.xml`; never commit private key
- Entitlement: `com.apple.security.network.client`
- See [distribution-macos.md](distribution-macos.md)

---

## Step 4 — `sentry`

```swift
import Sentry

enum SentryService {
    static func startIfNeeded(_ config: AppConfig) {
        guard let dsn = config.sentryDSN else { return }
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

---

## Step 5 — `posthog`

Init only when `POSTHOG_API_KEY` set. Capture one `app_launched` event from root view `.onAppear` (debug log when not configured).

---

## Step 6 — `sign-in-with-apple`

- Enable **Sign in with Apple** capability (iOS + macOS targets)
- Use [foundation-native-security.md](foundation-native-security.md) `KeychainStore` for `userIdentifier`
- macOS: present `ASAuthorizationController` with `NSWindow` anchor or SwiftUI `SignInWithAppleButton`
- README: if you offer Google/email login on iOS, Apple requires Sign in with Apple too

---

## Step 7 — `storekit2`

- `Product.products(for:)` with IDs from config plist
- Purchase button stub; handle `.userCancelled` gracefully
- README: App Store Connect product ID checklist

---

## Step 8 — `apns`

- Request authorization on first launch (stub — can no-op in Simulator)
- Register for remote notifications in `AppDelegate` or `@UIApplicationDelegateAdaptor`
- README: APNs key + entitlement steps

---

## Phase exit criterion

- [ ] Every confirmed add-on has SPM dependency or system framework wired
- [ ] `AppConfig` + `Secrets.example.xcconfig` document all keys
- [ ] `xcodebuild build` + tests pass without secrets
- [ ] Settings/debug screen shows configured vs not for each integration
- [ ] No product business logic beyond **stubs/demos**

Next: [verification-native-checklist.md](verification-native-checklist.md) (Phase 9).
