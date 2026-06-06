# Skills Library Index

> Catalog of skills and portable replication guides. Search here before rebuilding a pattern
> from scratch. Skills live under `plugins/<plugin>/skills/<name>/`; guides under `guides/`.

| Doc | Category | Summary | Tags | Updated |
|-----|----------|---------|------|---------|
| plugins/bughunt-suite/skills/bughunt/SKILL.md | workflow | Offensive whole-codebase hunter for bugs, pain points & inefficiencies — zero-dep toolkit ranks hotspots, parallel fan-out across 13 lenses × hotspots, mandatory skeptic-verify, fingerprint/dedupe/baseline-diff, markdown/HTML/SARIF + CI exit codes (report-only) | bughunt, bug-hunting, code-review, static-analysis, taint, concurrency, authz, performance, supply-chain, technical-debt, sarif, ci, fan-out, security, workflow | 2026-06-06 |
| plugins/bughunt-suite/skills/triage/SKILL.md | workflow | Triage a bug or findings into a ranked, evidence-backed report — severity × confidence + impact rubric, minimal repro, finding schema (markdown + JSON), baseline diff | triage, repro, severity, confidence, impact-rubric, bug-report, workflow | 2026-06-06 |
| plugins/bughunt-suite/skills/fuzz/SKILL.md | workflow | Flush out hidden bugs dynamically — discover, generate, and RUN property/fuzz/differential harnesses, shrink to regression test, emit confirmed findings | fuzz, property-based-testing, fuzzing, differential-testing, regression, workflow | 2026-06-06 |
| plugins/autoreview/skills/autoreview/SKILL.md | workflow | Hard acceptance gate — review all session changes for production quality before marking work complete | autoreview, review, production-quality, acceptance-gate, workflow | 2026-05-28 |
| plugins/macos-sandbox/skills/macos-sandbox/SKILL.md | workflow | Smoke-test macOS .app/.pkg in disposable Tart VMs via macbox CLI or MCP — upload, launch, logs, screenshots, crashes, guest automation | macbox, macos, tart, vm, sandbox, smoke-test, mcp | 2026-06-03 |
| plugins/scaffold/skills/scaffold/SKILL.md | workflow | Greenfield Next.js — product intake profiles, typed env, Vitest, tRPC, optional Clerk, Neon/Drizzle, Vercel, intake add-ons installed (AI SDK, Resend, Stripe, Sentry, PostHog) | scaffold, nextjs, trpc, clerk, neon, drizzle, vercel, vitest, zod, shadcn, ai-sdk, resend, stripe, sentry, posthog | 2026-06-03.4 |
| plugins/macos-design/skills/macos-design/SKILL.md | design / macOS | Design, critique, and scaffold native macOS apps — HIG, Liquid Glass, menus, toolbars, safe areas, accessibility, SwiftUI/AppKit | macos, swiftui, appkit, liquid-glass, hig, design | 2026-05-28 |
| plugins/macos-design/skills/macos-design/macos_immersive_onboarding_guide.md | design / macOS | Immersive first-launch onboarding wizard with blur, motion, and permission steps | swiftui, macos, onboarding, appkit, animation, permissions | 2026-05-30 |
| plugins/macos-notch/skills/macos-notch/SKILL.md | design / macOS | Dynamic Island notch apps — NSPanel, geometry, state machine, module widgets (media, HUD, shelf, agents) | macos, notch, nspanel, dynamic-island, swiftui, appkit, menubar | 2026-06-03.2 |
| plugins/web-marketing-landing/skills/web-marketing-landing/SKILL.md | design / Web | Premium SaaS marketing home — aurora hero, glass nav, connector hub, bento grid, CSS motion (Next.js + Tailwind v4) | nextjs, react, tailwind, marketing, landing-page, css-animation | 2026-06-02 |
| guides/ios/liquidglass-animation.md | guide / iOS | Expanding Liquid Glass composer shell with + menu and slash-command panels | swiftui, ios, liquid-glass, animation, composer, chat-input | 2026-05-28 |
| guides/ios/ios-sidebar-slide.md | guide / iOS | Mobile sidebar underlay with foreground card slide, gesture-driven open/close | swiftui, ios, sidebar, drawer, gesture, navigation | 2026-05-28 |

## By category

### workflow

- [bughunt-suite/skills/bughunt](plugins/bughunt-suite/skills/bughunt/SKILL.md) — Offensive whole-codebase hunter (bugs, pain points, inefficiencies): zero-dep toolkit + 13-lens fan-out + mandatory verify + baseline-diff/SARIF/CI (`/bughunt`)
- [bughunt-suite/skills/triage](plugins/bughunt-suite/skills/triage/SKILL.md) — Rank & reproduce findings: severity × confidence + impact rubric + repro (`/triage`)
- [bughunt-suite/skills/fuzz](plugins/bughunt-suite/skills/fuzz/SKILL.md) — Discover, generate, and RUN property/fuzz/differential harnesses to confirm bugs (`/fuzz`)
- [autoreview](plugins/autoreview/skills/autoreview/SKILL.md) — Hard acceptance gate for session changes (`/review`)
- [macos-sandbox](plugins/macos-sandbox/skills/macos-sandbox/SKILL.md) — macOS app smoke testing in Tart VMs via macbox (`/macos-sandbox`)
- [scaffold](plugins/scaffold/skills/scaffold/SKILL.md) — Greenfield full-stack Next.js app (`/scaffold`)

### design / macOS

- [macos-design](plugins/macos-design/skills/macos-design/SKILL.md) — Native macOS app design (`/macos-design`)
- [macos_immersive_onboarding_guide.md](plugins/macos-design/skills/macos-design/macos_immersive_onboarding_guide.md) — Immersive first-launch onboarding wizard
- [macos-notch](plugins/macos-notch/skills/macos-notch/SKILL.md) — Dynamic Island / notch-style macOS apps (`/macos-notch`)

### design / Web

- [web-marketing-landing](plugins/web-marketing-landing/skills/web-marketing-landing/SKILL.md) — Premium SaaS marketing home page pattern (`/landing-page`)

### guide / iOS

- [liquidglass-animation.md](guides/ios/liquidglass-animation.md) — Expanding Liquid Glass composer shell
- [ios-sidebar-slide.md](guides/ios/ios-sidebar-slide.md) — Sidebar underlay with sliding foreground card

## How to add entries

1. Append or update the table row (Doc, Category, Summary, Tags, Updated).
2. Add or refresh the link under **By category**.
3. Skills live under `plugins/<plugin>/skills/<name>/`; non-skill replication guides under `guides/`.
