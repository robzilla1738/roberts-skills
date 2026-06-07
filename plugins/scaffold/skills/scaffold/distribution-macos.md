# macOS distribution and entitlements

> Phase 7 for **`macos`**. Back to [SKILL.md](SKILL.md).

---

## Distribution matrix

| Path | Updates | Payments | Sandbox | Sparkle |
|------|---------|----------|---------|---------|
| **Mac App Store** | Apple | IAP / StoreKit / RevenueCat | Required | **No** |
| **Direct download** | Sparkle (recommended) | Stripe on web + license key, or IAP via Mac StoreKit outside MAS | Recommended | **Yes** |
| **Both** | Separate builds or unified with feature flags | Plan per channel | MAS build sandboxed; direct may differ | Direct build only |

Record choice in intake (#6 distribution) and README.

---

## App Sandbox (default: ON)

Enable **App Sandbox** for new Mac apps unless user explicitly opts out (rare, non-sandboxed legacy tools).

| Entitlement | When |
|-------------|------|
| Outgoing network | API clients, RevenueCat, Sentry, PostHog, Sparkle |
| Incoming network (server) | Only if app hosts a local server |
| User-selected read-only / read-write | Document apps, export/import |
| Keychain access groups | Sign in with Apple, license tokens |
| Push notifications | N/A on macOS for most apps |
| Apple Events | Automation apps only — justify in README |

**Rule:** add the **minimum** entitlements; document each in README.

### `MyApp.entitlements` starter (network + keychain)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>keychain-access-groups</key>
    <array>
        <string>$(AppIdentifierPrefix)$(CFBundleIdentifier)</string>
    </array>
</dict>
</plist>
```

Add file-access entitlements for document-based apps.

---

## Code signing and hardened runtime

| Step | Direct download | Mac App Store |
|------|-----------------|---------------|
| Developer ID Application cert | Required | N/A (use Apple Distribution) |
| Hardened Runtime | Required | Automatic |
| Notarization (`notarytool`) | Required before shipping | Apple notarizes on upload |
| Staple ticket to `.app` | Required for offline Gatekeeper | N/A |

Document in README — do not automate notarization in scaffold; provide checklist in [production-habits-native.md](production-habits-native.md).

```bash
# Verify local build (after signing)
codesign --verify --deep --strict --verbose=2 MyApp.app
spctl -a -vv MyApp.app
```

---

## Sparkle (direct only)

Prerequisites when `sparkle` add-on is confirmed:

1. **HTTPS appcast** — host `appcast.xml` on your CDN/site
2. **EdDSA keys** — generate with Sparkle's `generate_keys` tool; **private key never in repo**
3. **Sandbox** — `com.apple.security.network.client` for update checks
4. **User-facing update menu** — `Check for Updates…` under Application menu

Feed URL lives in `AppConfig.sparkleFeedURL` (xcconfig). See [phase-native-integrations.md](phase-native-integrations.md#sparkle-macos-direct).

**MAS builds:** remove Sparkle dependency target or `#if` guard with `DIRECT_DISTRIBUTION` build flag.

---

## RevenueCat / StoreKit on Mac

- **MAS:** configure products in App Store Connect; use RevenueCat Apple platform key or StoreKit 2
- **Direct:** subscriptions often pair **web Stripe checkout** + license validation, or Mac IAP outside MAS (less common) — clarify in intake; document in README

---

## Bundle ID and versioning

- Bundle ID: `com.yourcompany.appname` — set in intake; never `com.example` in shipped README
- `CFBundleShortVersionString` — marketing version (1.0.0)
- `CFBundleVersion` — build number (monotonic integer for MAS)

Add **About** panel via standard command (see [foundation-macos-shell.md](foundation-macos-shell.md)).

---

## Phase 7 exit

- [ ] Entitlements file matches app style and add-ons
- [ ] README: distribution path + signing/notarization checklist
- [ ] Sparkle feed placeholder or "N/A (MAS)" documented
- [ ] Sandbox on unless user opted out with written reason in README

Next: Phase 8 — [phase-native-integrations.md](phase-native-integrations.md).
