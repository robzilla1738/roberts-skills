# Stack Scaffold

Greenfield a **Next.js 16 + Tailwind v4 + tRPC + TanStack Query + Neon/Drizzle + Vercel** app with **product-driven intake** — typed env, Vitest, optional Clerk, and production-habits checklist.

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Hub — product intake, phase order |
| `intake-product-profiles.md` | **Start here** — what are you building? |
| `foundation-env-and-errors.md` | Zod env + AppError |
| `foundation-testing.md` | Vitest |
| `foundation-ui.md` | shadcn vs minimal |
| `production-habits.md` | Post-scaffold industry checklist |
| + stack, DB, tRPC, auth, Vercel, verify spokes |

---

## Install

Copy `scaffold/` to `~/.cursor/skills/scaffold/` (or Claude/Codex paths in hub).

---

## Use it

```text
/scaffold — B2B SaaS dashboard for Acme with teams and billing later
```

The agent should ask **what you are building**, pick a profile (`saas-dashboard`, `internal-tool`, `api-first`, etc.), then run phases 0–9.

---

## Profiles (summary)

| Profile | Use for |
| --- | --- |
| `saas-dashboard` | Default multi-user SaaS |
| `internal-tool` | Team tools |
| `api-first` | Backend-first, thin UI |
| `marketing-only` | Redirect to web-marketing-landing |
| `extend-existing` | Gap-fill only |

---

## Related skills

- the **autoreview** skill (`/review`) — `/review` after scaffold
- the **web-marketing-landing** skill — marketing-only
- **clerk-auth** — advanced Clerk

---

## Version

`2026-06-03.2` — see `SKILL.md` front matter.

`disable-model-invocation: true` — invoke with `/scaffold`.
