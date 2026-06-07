# Production habits (native — post-scaffold)

> Read after Phase 9; document in project README. Back to [SKILL.md](SKILL.md).

Scaffold delivers **build-green** with integrations stubbed. These habits ship to real users — document in README; implement when the product needs them.

---

## When to add what

| Habit | Why | When |
|-------|-----|------|
| **GitHub Actions** — `xcodebuild test` on macOS runner | CI gate every PR | First PR |
| **Xcode Cloud** or **fastlane** | Archive, TestFlight, notarize | Team Apple dev accounts |
| **TestFlight** (iOS) / **MAS TestFlight** (macOS) | Beta distribution | Before public launch |
| **Notarization pipeline** (`notarytool` + staple) | Direct Mac download works on Gatekeeper | Before shipping direct build |
| **Sparkle appcast + EdDSA keys** | Safe auto-updates | Direct Mac with `sparkle` |
| **App Store Connect** products | IAP / subscriptions | `revenuecat` / `storekit2` |
| **RevenueCat dashboard** | Entitlements, offerings, paywalls | After `revenuecat` installed |
| **Sentry releases + dSYM upload** | Symbolicated crashes | Production builds |
| **PostHog** project + feature flags | Analytics | After `posthog` installed |
| **Privacy Nutrition Labels** | App Store requirement | MAS submission |
| **App Privacy manifest** (`PrivacyInfo.xcprivacy`) | Required for common SDKs | MAS + many SDKs |
| **Localization** (`String Catalog`) | Ship beyond English | Before v1.0 public |
| **XCUITest** smoke | Launch, Settings, one core flow | After shell stable |
| **macos-sandbox** skill | VM smoke `.app` before release | Direct Mac builds |

---

## macOS direct-download checklist

```markdown
## Shipping (direct download)

- [ ] Developer ID Application certificate
- [ ] Hardened Runtime + App Sandbox entitlements finalized
- [ ] Archive → Export signed .app
- [ ] `notarytool submit` + `stapler staple`
- [ ] Sparkle: generate EdDSA keys (private key in secrets vault)
- [ ] Host HTTPS `appcast.xml` + release notes
- [ ] DMG or zip with instructions (optional: create-dmg)
- [ ] Smoke test on clean Mac (macos-sandbox or spare machine)
```

---

## Mac App Store checklist

```markdown
## Shipping (Mac App Store)

- [ ] Apple Distribution certificate + provisioning
- [ ] Sandbox entitlements match App Review expectations
- [ ] No Sparkle / outside update mechanisms in binary
- [ ] IAP products linked in App Store Connect
- [ ] Privacy manifest + App Privacy questionnaire
- [ ] Screenshots + description + review notes
```

---

## iOS App Store checklist

```markdown
## Shipping (iOS)

- [ ] App Store Connect app record + bundle ID
- [ ] TestFlight internal → external beta
- [ ] Sign in with Apple (if other social logins exist — Apple rule)
- [ ] Push capability + APNs key (if `apns`)
- [ ] RevenueCat ↔ App Store Connect product sync
```

---

## CI template (GitHub Actions)

```yaml
name: macOS CI
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Unit tests
        run: |
          xcodebuild test \
            -project MyMacApp.xcodeproj \
            -scheme MyMacApp \
            -destination 'platform=macOS' \
            CODE_SIGNING_ALLOWED=NO
```

Adjust project/scheme names. Add `swift test` for SPM-only repos.

---

## SDK stubs to harden later

| Stub | Harden when |
|------|-------------|
| RevenueCat paywall placeholder | Real offerings + Customer Center |
| Sparkle feed URL empty | Production appcast + delta updates |
| Sign in with Apple stub | Server token exchange if backend exists |
| `APIClient` health check | Auth headers, refresh, offline cache |
| In-memory SwiftData | CloudKit sync if `cloudkit` selected |

---

## README section template

```markdown
## Production checklist (after scaffold)

Platform: macos · Profile: macos-direct
Installed: sparkle, revenuecat, sentry

- [ ] CI: GitHub Actions xcodebuild
- [ ] Notarization + staple (direct)
- [ ] Sparkle appcast live
- [ ] RevenueCat products + offerings
- [ ] Sentry dSYM upload on release
- [ ] Product features (replace placeholders)
```

---

## Related

- [distribution-macos.md](distribution-macos.md) — entitlements, signing
- [phase-native-integrations.md](phase-native-integrations.md) — installed add-ons
- **macos-sandbox** — VM smoke tests
- **autoreview** (`/review`) — before merge
