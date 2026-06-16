# Platform router

> Phase 0a — run **before** product profile intake. Back to [SKILL.md](SKILL.md).

Scaffold supports multiple **platform families**. Pick one first; each family has its own profile table, phase bundle, and add-on matrix.

---

## Opening question (required)

Ask the user:

> **What platform are you building for?** e.g. web (Next.js), iOS, macOS, Expo/React Native, or a combo (web + mobile).

Map the answer to a **platform family** below. If unclear, ask one follow-up: *"Is this a browser app, a native Apple app, or cross-platform mobile?"*

---

## Platform families

| Family ID | When | Phase bundle | Profile intake |
|-----------|------|--------------|----------------|
| `web-next` | SaaS, dashboard, API-first web app | [phases-greenfield.md](phases-greenfield.md) | [intake-product-profiles.md](intake-product-profiles.md) |
| `ios` | iPhone / iPad native app | [phases-native-greenfield.md](phases-native-greenfield.md) | [intake-native-profiles.md](intake-native-profiles.md) |
| `macos` | macOS native app (windowed, utility, menu bar) | [phases-native-greenfield.md](phases-native-greenfield.md) | [intake-native-profiles.md](intake-native-profiles.md) |
| `expo` | React Native / Expo mobile | — | **Out of scope** — custom plan; link Expo docs |
| `multi` | Web + native clients sharing backend | Both bundles | Split intake per target; see [Multi-platform](#multi-platform) |

### Default routing rules

- Mentions **Next.js**, **tRPC**, **Vercel**, **dashboard**, **SaaS web** → `web-next`
- Mentions **iPhone**, **iPad**, **iOS**, **App Store (mobile)** → `ios`
- Mentions **macOS**, **Mac app**, **menu bar app**, **notch app**, **Sparkle** → `macos`
- Mentions **Expo**, **React Native** only → `expo` (stop scaffold; agree custom plan)
- Mentions **Rhema-style** full stack (web + iOS) → `multi`

---

## Integration recommendations (all families)

After the product one-liner, **propose add-ons with rationale** — do not silently default.

1. Scan the product sentence for triggers in [intake-native-profiles.md](intake-native-profiles.md#integration-triggers) (native) or [intake-product-profiles.md](intake-product-profiles.md) add-on table (web).
2. Present a short **Recommended** list and an **Optional** list.
3. Ask: *"Use these add-ons, or change anything?"*
4. Record confirmed IDs in intake output; install in Phase 9 (web) or Phase 8 (native).

**Examples**

| Product | Platform | Recommend |
|---------|----------|-----------|
| "Bible app with premium subscription" | `ios` | `revenuecat`, `sign-in-with-apple`, `sentry` |
| "Mac utility sold on my website" | `macos` | `sparkle`, `revenuecat` or `storekit2`, `sentry` |
| "B2B SaaS dashboard" | `web-next` | `stripe`, `clerk` (profile default), `sentry`, `posthog` |
| "Mac menu bar notch HUD" | `macos` | `sentry`; skip `sparkle` if MAS-only |

User can accept, reject, or swap (e.g. `storekit2` instead of `revenuecat`).

---

## Multi-platform

When `multi` is selected:

1. **Shared backend** — usually `web-next` `api-first` or existing API; scaffold web API first unless API already exists.
2. **Native client** — run native intake for `ios` and/or `macos` with `client-only` profile (see [intake-native-profiles.md](intake-native-profiles.md)).
3. **Monorepo** — optional Turborepo (`apps/web`, `apps/ios` as separate Xcode project); document in README. No full monorepo generator — same rule as [intake-and-variants.md](intake-and-variants.md).
4. **Billing** — prefer **one** source of truth: Stripe (web) + RevenueCat (mobile) with shared entitlements, or RevenueCat everywhere for Apple platforms.

Post a **split intake plan** (web phases + native phases) before coding.

---

## Out of scope → route elsewhere

| Request | Route to |
|---------|----------|
| Marketing-only web | **web-marketing-landing** skill |
| macOS UI design / HIG audit only | **macos-design** skill |
| iOS UI design / HIG audit only | **ios-design** skill (global) |
| macOS notch / Dynamic Island shell | **macos-notch** skill |
| Supabase / Prisma-first web | Custom plan — do not force Neon/Drizzle |
| Expo / RN-only | Custom plan — not this skill's default |

---

## Intake output prefix (all platforms)

Include in every scaffold plan:

```text
Platform family: ios
Product: {{one-liner}}
Recommended add-ons: revenuecat, sign-in-with-apple, sentry
Add-ons (confirmed): revenuecat, sentry
...
```

Proceed to the family-specific profile file, then that family's phase bundle.
