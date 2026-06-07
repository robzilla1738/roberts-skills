# Scaffold

Product-driven greenfield for **web** and **native Apple** apps:

- **Web:** Next.js, intake profiles (SaaS, internal tool, API-first), tRPC, Neon/Drizzle, Clerk, Vercel
- **iOS / macOS:** SwiftUI, SwiftData, XCTest, SPM integrations (RevenueCat, Sparkle, Sentry, …)

Intake **recommends** integrations from what you're building; you confirm before install.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install scaffold@roberts-skills
```

Then use `/scaffold`.

### Cursor / Codex

```bash
cp -R plugins/scaffold/skills/scaffold ~/.agents/skills/   # Cursor + Codex (global)
cp -R plugins/scaffold/skills/scaffold ~/.cursor/skills/   # Cursor (global)
```

## Use it

```text
/scaffold a Mac subscription app sold from my website
/scaffold a SaaS dashboard with auth and Postgres
/scaffold an iPhone app with premium unlock
```

See [`skills/scaffold/`](skills/scaffold/) for the hub and all reference spokes.
