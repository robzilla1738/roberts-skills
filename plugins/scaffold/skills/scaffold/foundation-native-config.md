# Native config and errors

> Phase 2 — typed configuration (mirrors web `lib/env.ts`). Back to [SKILL.md](SKILL.md).

See also [foundation-native-security.md](foundation-native-security.md) for Keychain and xcconfig wiring.

---

## Principles

1. **No secrets in git** — keys via `Config/Secrets.xcconfig` (gitignored) → `INFOPLIST_KEY_*` — see security spoke.
2. **Launch-safe** — app runs in Simulator without production keys; integrations no-op until configured.
3. **Single loader** — `AppConfig.load()` is the only place that reads plist / env / xcconfig.
4. **Debug vs Release** — `Purchases.logLevel = .debug` only in `#if DEBUG`.

---

## `AppConfig.swift` pattern

```swift
import Foundation

struct AppConfig: Sendable {
    let bundleIdentifier: String
    let apiBaseURL: URL?
    let revenueCatAPIKey: String?
    let sentryDSN: String?
    let postHogAPIKey: String?
    let sparkleFeedURL: URL?

    static func load() -> AppConfig {
        let env = ProcessInfo.processInfo.environment
        let plist = Bundle.main.infoDictionary ?? [:]

        func str(_ key: String) -> String? {
            if let v = env[key], !v.isEmpty { return v }
            if let v = plist[key] as? String, !v.isEmpty { return v }
            return nil
        }

        return AppConfig(
            bundleIdentifier: Bundle.main.bundleIdentifier ?? "com.example.app",
            apiBaseURL: str("API_BASE_URL").flatMap(URL.init(string:)),
            revenueCatAPIKey: str("REVENUECAT_API_KEY"),
            sentryDSN: str("SENTRY_DSN"),
            postHogAPIKey: str("POSTHOG_API_KEY"),
            sparkleFeedURL: str("SPARKLE_FEED_URL").flatMap(URL.init(string:))
        )
    }

    var isRevenueCatConfigured: Bool { revenueCatAPIKey != nil }
    var isSentryConfigured: Bool { sentryDSN != nil }
    var isSparkleConfigured: Bool { sparkleFeedURL != nil }
    var isPostHogConfigured: Bool { postHogAPIKey != nil }
}
```

Commit **`Config/Secrets.example.xcconfig`** and wire via **`Config/Debug.xcconfig`** / **`Release.xcconfig`** — full pattern in [foundation-native-security.md](foundation-native-security.md#xcconfig--infoplist-preferred).

macOS tree: [file-tree-macos.md](file-tree-macos.md).

---

## `AppError.swift`

```swift
import Foundation

enum AppError: LocalizedError {
    case notConfigured(String)
    case network(underlying: Error)
    case authRequired
    case keychain(OSStatus)

    var errorDescription: String? {
        switch self {
        case .notConfigured(let service):
            return "\(service) is not configured."
        case .network(let underlying):
            return underlying.localizedDescription
        case .authRequired:
            return "Sign in required."
        case .keychain(let status):
            return "Keychain error (\(status))."
        }
    }
}
```

User-facing surfaces show `localizedDescription`; log details to Sentry when configured.

---

## Settings debug screen (Phase 6)

Show non-secret config status:

- RevenueCat: configured yes/no
- Sentry: configured yes/no
- API base URL: host only (no tokens)

---

## README section

Document every key from confirmed add-ons and how to set in Xcode schemes vs xcconfig.

Next: [phases-native-greenfield.md](phases-native-greenfield.md) Phase 2c onward.
