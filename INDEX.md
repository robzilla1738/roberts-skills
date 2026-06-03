# Skills Library Index

> Portable replication guides. Search here before rebuilding a pattern from scratch.

| Doc | Category | Summary | Tags | Updated |
|-----|----------|---------|------|---------|
| design-skills/iOS/liquidglass-animation.md | design / iOS | Expanding Liquid Glass composer shell with + menu and slash-command panels | swiftui, ios, liquid-glass, animation, composer, chat-input | 2026-05-28 |
| design-skills/iOS/ios-sidebar-slide.md | design / iOS | Mobile sidebar underlay with foreground card slide, gesture-driven open/close | swiftui, ios, sidebar, drawer, gesture, navigation | 2026-05-28 |
| design-skills/macos-design/macos_immersive_onboarding_guide.md | design / macOS | Immersive first-launch onboarding wizard with blur, motion, and permission steps | swiftui, macos, onboarding, appkit, animation, permissions | 2026-05-30 |
| workflow-skills/autoreview/SKILL.md | workflow | Hard acceptance gate — review all session changes for production quality before marking work complete | autoreview, review, production-quality, acceptance-gate, workflow | 2026-05-28 |
| workflow-skills/macos-sandbox/SKILL.md | workflow | Smoke-test macOS .app/.pkg in disposable Tart VMs via macbox CLI or MCP — upload, launch, logs, screenshots, crashes, guest automation | macbox, macos, tart, vm, sandbox, smoke-test, mcp | 2026-06-03 |
| workflow-skills/scaffold/SKILL.md | workflow | Greenfield Next.js stack — Tailwind v4, tRPC, TanStack Query, optional Clerk, Neon/Drizzle, Vercel | scaffold, nextjs, trpc, clerk, neon, drizzle, vercel, tanstack | 2026-06-03.1 |
| design-skills/web-marketing-landing/SKILL.md | design / Web | Premium SaaS marketing home — aurora hero, glass nav, connector hub, bento grid, CSS motion (Next.js + Tailwind v4) | nextjs, react, tailwind, marketing, landing-page, css-animation | 2026-06-02 |
| design-skills/macos-notch/SKILL.md | design / macOS | Dynamic Island notch apps — NSPanel, geometry, state machine, module widgets (media, HUD, shelf, agents) | macos, notch, nspanel, dynamic-island, swiftui, appkit, menubar | 2026-06-03.2 |

## By category

### design / iOS

- [liquidglass-animation.md](design-skills/iOS/liquidglass-animation.md) — Expanding Liquid Glass composer shell
- [ios-sidebar-slide.md](design-skills/iOS/ios-sidebar-slide.md) — Sidebar underlay with sliding foreground card

### design / macOS

- [macos_immersive_onboarding_guide.md](design-skills/macos-design/macos_immersive_onboarding_guide.md) — Immersive first-launch onboarding wizard
- [macos-notch/SKILL.md](design-skills/macos-notch/SKILL.md) — Dynamic Island / notch-style macOS apps

### design / Web

- [web-marketing-landing/SKILL.md](design-skills/web-marketing-landing/SKILL.md) — Premium SaaS marketing home page pattern

### workflow

- [autoreview/SKILL.md](workflow-skills/autoreview/SKILL.md) — Hard acceptance gate for session changes (invoke with `/review`)
- [macos-sandbox/SKILL.md](workflow-skills/macos-sandbox/SKILL.md) — macOS app smoke testing in Tart VMs via macbox
- [scaffold/SKILL.md](workflow-skills/scaffold/SKILL.md) — Greenfield full-stack Next.js app (`/scaffold`)

## How to add entries

After `/documenter` writes or refreshes a doc:

1. Append or update the table row (Doc, Category, Summary, Tags, Updated).
2. Add or refresh the link under **By category**.
3. Use category format `{bucket} / {subfolder}` per `~/.agents/skills/documenter/references/taxonomy.md`.
