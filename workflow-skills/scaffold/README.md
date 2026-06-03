# Stack Scaffold

Greenfield a **Next.js 16 + Tailwind v4 + tRPC + TanStack Query + Neon/Drizzle + Vercel** app, with optional **Clerk** auth — in a build-green state before feature work.

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

Hub-and-spoke workflow:

| File | Role |
| --- | --- |
| `SKILL.md` | Hub — intake router, phase order, related skills |
| `intake-and-variants.md` | Questions and variant selection |
| `phases-greenfield.md` | Phases 0–9 with exit criteria |
| `stack-and-tooling.md` | Versions, create-next-app, scripts |
| `file-tree-and-conventions.md` | Canonical layout |
| `database-neon-drizzle.md` | Neon + Drizzle setup |
| `trpc-and-query.md` | tRPC server, client, route handler |
| `auth-clerk-optional.md` | Clerk proxy, webhook (optional) |
| `vercel-and-env.md` | Env template and deploy |
| `verification-checklist.md` | Final gate |

---

## Install

Copy the entire `scaffold` directory into your assistant's skills location.

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/scaffold/` |
| Codex | `~/.agents/skills/scaffold/` |
| Cursor | `~/.cursor/skills/scaffold/` |

---

## Use it

```text
/scaffold — new SaaS app called Acme with Clerk and Neon
```

```text
/scaffold extend-existing — add tRPC and Drizzle to this Next repo
```

The agent should run **intake first**, then phases in order.

---

## Variants

| Variant | Description |
| --- | --- |
| `full-app` | Default — DB, tRPC, Clerk, `/app` shell |
| `app-no-auth` | DB + tRPC, no Clerk |
| `marketing-only` | Redirects to web-marketing-landing skill |
| `extend-existing` | Gap-fill only |

---

## Related skills

- [autoreview](../autoreview/) — `/review` after scaffold
- [web-marketing-landing](../../design-skills/web-marketing-landing/) — marketing-only sites
- **clerk-auth** (global) — advanced Clerk patterns

---

## Version

See `version` in `SKILL.md` front matter. Current: `2026-06-03.1`.

`disable-model-invocation: true` — loads on explicit `/scaffold` or request.
