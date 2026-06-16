# Native testing foundation

> Phase 2c. Back to [SKILL.md](SKILL.md).

XCTest is the default. UI tests are optional in scaffold — document in [production-habits-native.md](production-habits-native.md).

---

## Target layout

```text
MyAppTests/
├── AppConfigTests.swift
├── AppErrorTests.swift
├── KeychainStoreTests.swift      # if security spoke applied
└── Services/
    └── RevenueCatServiceTests.swift  # mock / config-only
```

---

## Sample tests

```swift
import XCTest
@testable import MyApp

final class AppConfigTests: XCTestCase {
    func testLoadsWithoutSecrets() {
        let config = AppConfig.load()
        XCTAssertFalse(config.bundleIdentifier.isEmpty)
        XCTAssertFalse(config.isRevenueCatConfigured) // no keys in CI
    }
}

final class AppErrorTests: XCTestCase {
    func testLocalizedDescription() {
        let error = AppError.notConfigured("RevenueCat")
        XCTAssertEqual(error.errorDescription, "RevenueCat is not configured.")
    }
}
```

---

## macOS test commands

```bash
# List schemes
xcodebuild -list -project MyApp.xcodeproj

# Build + unit tests (CI)
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=macOS' \
  -resultBundlePath TestResults.xcresult \
  CODE_SIGNING_ALLOWED=NO
```

`CODE_SIGNING_ALLOWED=NO` is acceptable for CI simulator-less macOS unit tests when no entitlements are required at test time.

---

## iOS test commands

```bash
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  CODE_SIGNING_ALLOWED=NO
```

Use `xcrun simctl list devices` to pick an available simulator.

---

## Swift 6 concurrency in tests

Mark test classes `@MainActor` when testing `@MainActor` types:

```swift
@MainActor
final class AppModelTests: XCTestCase {
    func testDefaults() {
        let model = AppModel()
        XCTAssertNil(model.selectedItemID)
    }
}
```

---

## StoreKit testing

When `storekit2` or `revenuecat` is installed:

- Add `Configuration.storekit` for local StoreKit Testing in Xcode
- Unit tests assert **configuration state**, not live purchases

---

## Pitfalls

- Tests that require secrets — must pass in CI without keys
- Flaky UI tests on menu bar apps — defer UI tests to production habits
- Missing test target membership for `Services/` files

Next: Phase 3 — platform shell spoke ([foundation-macos-shell.md](foundation-macos-shell.md) or ios-design).
