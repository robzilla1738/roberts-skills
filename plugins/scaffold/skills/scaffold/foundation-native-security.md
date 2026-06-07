# Native security foundations

> Phase 2b companion — Keychain, ATS, secrets. Back to [SKILL.md](SKILL.md).

---

## Principles

1. **Secrets never in source or UserDefaults** — API keys via xcconfig → Info.plist build settings; tokens in Keychain.
2. **Keychain for credentials** — Sign in with Apple user ID, auth tokens, license keys.
3. **App Transport Security** — HTTPS only; no arbitrary loads unless documented exception.
4. **Log redaction** — never `print()` API keys or DSNs; Sentry scrubs when configured.

---

## Keychain helper

```swift
import Foundation
import Security

enum KeychainStore {
    enum Key: String {
        case appleUserID = "apple_user_id"
        case authToken = "auth_token"
    }

    static func save(_ data: Data, for key: Key) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock,
            kSecValueData as String: data,
        ]
        SecItemDelete(query as CFDictionary)
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else { throw AppError.keychain(status) }
    }

    static func load(for key: Key) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne,
        ]
        var item: CFTypeRef?
        guard SecItemCopyMatching(query as CFDictionary, &item) == errSecSuccess else { return nil }
        return item as? Data
    }

    static func delete(for key: Key) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
        ]
        SecItemDelete(query as CFDictionary)
    }
}
```

Extend `AppError`:

```swift
case keychain(OSStatus)
```

Enable **Keychain Sharing** capability only when extensions need shared access.

---

## xcconfig → Info.plist (preferred)

`Config/Secrets.xcconfig` (gitignored):

```xcconfig
REVENUECAT_API_KEY = appl_xxx
SENTRY_DSN = https://example@o123.ingest.sentry.io/456
SPARKLE_FEED_URL = https://example.com/appcast.xml
API_BASE_URL = https:/$()/api.example.com
```

`Config/Debug.xcconfig`:

```xcconfig
#include? "Secrets.xcconfig"
INFOPLIST_KEY_REVENUECAT_API_KEY = $(REVENUECAT_API_KEY)
INFOPLIST_KEY_SENTRY_DSN = $(SENTRY_DSN)
INFOPLIST_KEY_SPARKLE_FEED_URL = $(SPARKLE_FEED_URL)
INFOPLIST_KEY_API_BASE_URL = $(API_BASE_URL)
```

In `AppConfig.load()`, read `INFOPLIST_KEY_*` via `Bundle.main.object(forInfoDictionaryKey:)`.

**Commit:** `Secrets.example.xcconfig` with empty values only.

---

## Info.plist ATS

Default (do not disable globally):

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
</dict>
```

For local dev API only, use **exception domains** in Debug xcconfig — not in Release.

---

## Sign in with Apple

- Store `userIdentifier` in Keychain, not UserDefaults
- Do not persist identity tokens long-term unless required for server refresh
- macOS: use `SignInWithAppleButton` or `ASAuthorizationController` with window anchor

---

## macOS sandbox file access

When reading user-picked files:

```swift
let started = url.startAccessingSecurityScopedResource()
defer { if started { url.stopAccessingSecurityScopedResource() } }
```

Document in README for document-based profiles.
