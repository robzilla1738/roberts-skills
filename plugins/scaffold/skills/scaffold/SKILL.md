---
name: scaffold
description: >
  Greenfield or extend apps across web (Next.js + tRPC + Neon/Drizzle + Vercel)
  and native Apple (iOS/macOS SwiftUI) with product intake, recommended
  integrations (Stripe, RevenueCat, Sparkle, Sentry, PostHog, etc.), and
  build-green verification. Use for /scaffold or new project setup.
disable-model-invocation: true
version: 2026-06-04.2
platforms: [Next.js, iOS, macOS, SwiftUI, TypeScript, Vercel]
primary_use_cases:
  - Bootstrap a new full-stack Next.js app on Robert's default web stack
  - Scaffold native iOS or macOS apps with SwiftUI and SPM integrations
  - Recommend and install intake-selected add-ons (RevenueCat, Sparkle, etc.)
  - Add missing layers to an existing web or Xcode repo
  - Produce a build-green repo before feature work
---

# Stack Scaffold

Workflow skill for **product-driven greenfield** across platform families:

| Family | Stack |
|--------|--------|
| **`web-next`** | Next.js + Tailwind v4 + tRPC + TanStack Query + Neon/Drizzle + Vercel + optional Clerk |
| **`ios`** | SwiftUI + SwiftData + XCTest + SPM integrations |
| **`macos`** | SwiftUI + SwiftData + XCTest + SPM integrations (Sparkle when direct distribution) |

Read this hub first, run **platform + product intake**, then open only the spokes for your family.

## Mission

Deliver a **fully configured repo** matching intake: core phases plus every **confirmed** add-on installed and wired. No product business logic beyond integration **demos/stubs**. Verification must pass before the skill is complete.

**Recommend integrations** from the product sentence (RevenueCat for subscriptions, Sparkle for direct-download Mac apps, Stripe for web billing, etc.) — user confirms before install.

## Non-negotiables

1. **Platform intake first** — [platform-router.md](platform-router.md) before profiles or `create-next-app` / Xcode bootstrap.
2. **Recommend, then confirm** — propose add-ons with rationale; record confirmed IDs in the intake plan.
3. **Family-specific profiles** — web: [intake-product-profiles.md](intake-product-profiles.md); native: [intake-native-profiles.md](intake-native-profiles.md).
4. **Add-ons are installed** — web Phase 9 / native Phase 8; never README-only.
5. **Scaffold profile in README** — platform family, profile ID, stack choices, add-ons, production habits.
6. **Design skills for native UI polish** — **ios-design** / **macos-design** after native shell; **macos-notch** for notch apps.

### Web-only (when `web-next`)

- App Router only; `pnpm` default; `lib/env.ts` (Zod); lazy `getDb()`; Clerk `proxy.ts` on Next 16.
- See existing web spokes unchanged.

### Native-only (when `ios` / `macos`)

- `AppConfig.load()` + [foundation-native-security.md](foundation-native-security.md) — no secrets in git; Keychain for tokens.
- Launch-safe without API keys; `#if DEBUG` for verbose SDK logs.
- **macOS:** real app structure ([foundation-macos-shell.md](foundation-macos-shell.md)) — Settings scene, commands, sandbox, entitlements ([distribution-macos.md](distribution-macos.md)).
- **iOS:** [foundation-ios-shell.md](foundation-ios-shell.md) — NavigationStack / split, safe areas.
- Post-scaffold: [production-habits-native.md](production-habits-native.md) in README.

## When to use

- Starting a SaaS web app, iOS app, or Mac app
- Extending an empty Next.js or Xcode project
- User invokes `/scaffold`

## When not to use

- **Marketing-only web** → **web-marketing-landing** skill
- **UI design audit only** → **ios-design** / **macos-design**
- **Expo / RN-only** → custom plan (not default spokes)
- **Supabase / Prisma-first web** → custom plan

## Intake router

### Step 0a — Platform

[platform-router.md](platform-router.md) — `web-next` | `ios` | `macos` | `multi` | `expo` (out of scope)

### Step 0b — Product profile

| Family | Profiles |
|--------|----------|
| `web-next` | `saas-dashboard`, `internal-tool`, `api-first`, `marketing-only`, `extend-existing` |
| `ios` / `macos` | `ios-consumer`, `ios-subscription`, `macos-productivity`, `macos-utility`, `macos-direct`, `client-only`, `extend-existing-native` |

## Phase bundles

### Web (`web-next`)

[phases-greenfield.md](phases-greenfield.md) — Phases 0–10; integrations Phase 9.

### Native (`ios` / `macos`)

[phases-native-greenfield.md](phases-native-greenfield.md) — Phases 0–9; integrations Phase 8.

### Multi

Split plan per [platform-router.md](platform-router.md#multi-platform).

## Spoke index

| File | Contents |
|------|----------|
| [platform-router.md](platform-router.md) | Platform family, recommendations, multi |
| [intake-product-profiles.md](intake-product-profiles.md) | Web profiles + add-ons |
| [intake-native-profiles.md](intake-native-profiles.md) | iOS/macOS profiles + triggers |
| [intake-and-variants.md](intake-and-variants.md) | Extend-existing, monorepo |
| [phases-greenfield.md](phases-greenfield.md) | Web phases 0–10 |
| [phases-native-greenfield.md](phases-native-greenfield.md) | Native phases 0–9 |
| [phase-integrations.md](phase-integrations.md) | Web Phase 9 add-ons |
| [phase-native-integrations.md](phase-native-integrations.md) | Native Phase 8 add-ons |
| [stack-and-tooling.md](stack-and-tooling.md) | Web bootstrap |
| [stack-native-swiftui.md](stack-native-swiftui.md) | Xcode / SPM bootstrap |
| [foundation-native-config.md](foundation-native-config.md) | AppConfig + AppError |
| [foundation-native-security.md](foundation-native-security.md) | Keychain, xcconfig, ATS |
| [foundation-native-testing.md](foundation-native-testing.md) | XCTest + CI |
| [foundation-macos-shell.md](foundation-macos-shell.md) | macOS scenes, commands, split view |
| [foundation-ios-shell.md](foundation-ios-shell.md) | iOS navigation shell |
| [file-tree-macos.md](file-tree-macos.md) | macOS tree, .gitignore |
| [distribution-macos.md](distribution-macos.md) | Sandbox, signing, notarization, Sparkle |
| [production-habits-native.md](production-habits-native.md) | Post-scaffold native checklist |
| [verification-native-checklist.md](verification-native-checklist.md) | Native build gate |
| + web foundation, DB, tRPC, auth, Vercel, verify spokes | Unchanged |

## Related skills

- **autoreview** (`/review`)
- **web-marketing-landing** — marketing-only web
- **ios-design** / **macos-design** — native UI polish
- **macos-notch** — notch / Dynamic Island Mac apps
- **macos-sandbox** — VM smoke-test `.app` before ship
- **clerk-auth** — deep Clerk (web)

## Default stacks

### Web

| Layer | Package / tool |
|-------|----------------|
| Runtime | Node 22.x, pnpm 10.x |
| Framework | Next.js 16, React 19, TypeScript 5.9+ |
| API | tRPC 11, TanStack Query 5, Neon, Drizzle |
| Deploy | Vercel |
| Web add-ons | `ai-sdk`, `resend`, `stripe`, `sentry`, `posthog` |

### Native

| Layer | Package / tool |
|-------|----------------|
| Language | Swift 6, SwiftUI |
| Data | SwiftData (default) |
| Tests | XCTest |
| Native add-ons | `revenuecat`, `sparkle`, `sentry`, `posthog`, `sign-in-with-apple`, `storekit2`, `apns`, `cloudkit` |

Verify latest package versions when scaffolding.
