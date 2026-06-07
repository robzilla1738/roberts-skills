# Stack Scaffold

Greenfield **web** (Next.js 16 + tRPC + Neon/Drizzle + Vercel) and **native** (iOS/macOS SwiftUI) with product-driven intake, **recommended integrations**, typed config, tests, and build-green verification.

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Hub — platform + product intake, phase order |
| `platform-router.md` | **Start here** — web vs iOS vs macOS |
| `intake-product-profiles.md` | Web profiles + add-ons |
| `intake-native-profiles.md` | iOS/macOS profiles + RevenueCat, Sparkle, … |
| `foundation-macos-shell.md` | macOS Settings, commands, MenuBarExtra |
| `distribution-macos.md` | Sandbox, notarization, Sparkle |
| `production-habits-native.md` | CI, TestFlight, shipping checklists |
| `phases-greenfield.md` / `phases-native-greenfield.md` | Ordered phases |
| `phase-integrations.md` / `phase-native-integrations.md` | Install confirmed add-ons |
| + security, testing, file-tree, iOS shell spokes |

---

## Install

Copy `scaffold/` to `~/.cursor/skills/scaffold/` (or Claude/Codex paths in hub).

---

## Use it

```text
/scaffold — Mac menu bar utility with direct download and auto-update
/scaffold — B2B SaaS dashboard for Acme with teams
```

The agent should ask **platform**, then **what you are building**, recommend add-ons, then run the matching phase bundle.

---

## Platform families

| Family | Examples |
| --- | --- |
| `web-next` | SaaS dashboard, internal tool, API-first |
| `ios` | iPhone/iPad apps, subscriptions |
| `macos` | Mac apps, menu bar, direct download + Sparkle |
| `multi` | Web API + native clients |

---

## Related skills

- **autoreview** (`/review`) — after scaffold
- **web-marketing-landing** — marketing-only web
- **ios-design** / **macos-design** — native UI polish
- **macos-notch** — notch-style Mac apps
- **clerk-auth** — advanced Clerk (web)

---

## Version

`2026-06-04.2` — see `SKILL.md` front matter.

`disable-model-invocation: true` — invoke with `/scaffold`.
