---
name: scaffold
description: >
  Greenfield or extend a Next.js app with Tailwind v4, tRPC, TanStack Query,
  optional Clerk, Neon/Drizzle, and Vercel. Use for /scaffold or new project setup.
disable-model-invocation: true
version: 2026-06-03.1
platforms: [Next.js, TypeScript, Vercel]
primary_use_cases:
  - Bootstrap a new full-stack Next.js app on Robert's default stack
  - Add missing tRPC, Drizzle, or Clerk layers to an existing repo
  - Produce a build-green repo before feature work begins
---

# Stack Scaffold

Workflow skill for greenfielding or extending a **Next.js + Tailwind v4 + tRPC + TanStack Query + Neon/Drizzle + Vercel** app, with **optional Clerk** auth.

Read this hub first, run **intake**, then open only the spokes for your variant.

## Mission

The first commit should be **boring infrastructure**. No product features until plumbing is green: install, types, lint, build, database, API route, and (if chosen) auth.

## Non-negotiables

1. **App Router only** — no Pages Router for new apps.
2. **`pnpm`** — pin Node `22.x` and pnpm `>=10 <11` in `package.json` engines.
3. **Environment** — secrets in `.env.local` (gitignored); committed `.env.example` with comments.
4. **Server boundary** — DB and tRPC routers are server-only; use `import "server-only"` where appropriate.
5. **Safe tRPC errors** — never leak stack traces to clients; map Zod and domain errors in the formatter.
6. **Clerk on Next 16** — use `proxy.ts` + `clerkMiddleware` when auth is enabled (not legacy-only middleware patterns).
7. **Lazy database** — `getDb()` must not throw at import time when `DATABASE_URL` is missing (build safety).

## When to use

- Starting a new SaaS or internal app on the default stack
- Adding tRPC + Drizzle + Clerk to an empty Next.js repo
- User invokes `/scaffold` or asks to “set up the stack”

## When not to use

- **Marketing-only site** (no API DB) → [web-marketing-landing](../../design-skills/web-marketing-landing/SKILL.md)
- **macOS / mobile / non-Next** projects
- **Turborepo monorepo** as default — see intake note; v1 optimizes single-app greenfield

## Intake router

**Do not write code until intake is complete.** See [intake-and-variants.md](intake-and-variants.md).

| Variant | Spokes to run |
|---------|----------------|
| `full-app` (default) | All phases + auth spoke |
| `app-no-auth` | Skip [auth-clerk-optional.md](auth-clerk-optional.md); `publicProcedure` only |
| `marketing-only` | Redirect to [web-marketing-landing](../../design-skills/web-marketing-landing/SKILL.md) |
| `extend-existing` | Gap analysis; only missing spokes |

## Phase bundle (full-app)

Execute in order; do not skip exit criteria. Details: [phases-greenfield.md](phases-greenfield.md).

| Step | Spoke |
|------|--------|
| 0 | [intake-and-variants.md](intake-and-variants.md) |
| 1–3 | [stack-and-tooling.md](stack-and-tooling.md), [file-tree-and-conventions.md](file-tree-and-conventions.md) |
| 4 | [database-neon-drizzle.md](database-neon-drizzle.md) |
| 5 | [trpc-and-query.md](trpc-and-query.md) |
| 6 | [auth-clerk-optional.md](auth-clerk-optional.md) (if auth) |
| 7 | [file-tree-and-conventions.md](file-tree-and-conventions.md) (app shell) |
| 8 | [vercel-and-env.md](vercel-and-env.md) |
| 9 | [verification-checklist.md](verification-checklist.md) |

After verification, recommend **`/review`** via [autoreview](../autoreview/SKILL.md).

## Spoke index

| File | Contents |
|------|----------|
| [intake-and-variants.md](intake-and-variants.md) | Questions, variants, monorepo note |
| [stack-and-tooling.md](stack-and-tooling.md) | Versions, `create-next-app`, scripts, `cn()` |
| [phases-greenfield.md](phases-greenfield.md) | Phases 0–9 with exit criteria |
| [file-tree-and-conventions.md](file-tree-and-conventions.md) | Canonical tree, `@/*` paths |
| [database-neon-drizzle.md](database-neon-drizzle.md) | Neon, Drizzle, schema stub, migrations |
| [trpc-and-query.md](trpc-and-query.md) | Server, context, procedures, route, provider |
| [auth-clerk-optional.md](auth-clerk-optional.md) | Clerk proxy, sign-in, webhook sync |
| [vercel-and-env.md](vercel-and-env.md) | Env template, Vercel + Neon |
| [verification-checklist.md](verification-checklist.md) | Build gate, deliverables |

## Related skills

- [autoreview](../autoreview/SKILL.md) — production acceptance after scaffold
- [web-marketing-landing](../../design-skills/web-marketing-landing/SKILL.md) — marketing-only Next sites
- **clerk-auth** (global skill) — deep Clerk patterns; do not duplicate here

## Default stack (pinned at scaffold time)

| Layer | Package / tool |
|-------|----------------|
| Runtime | Node 22.x, pnpm 10.x |
| Framework | Next.js 16, React 19, TypeScript 5.9+ |
| CSS | Tailwind CSS 4, `@tailwindcss/postcss` |
| API | tRPC 11, TanStack Query 5, superjson, zod |
| Auth | `@clerk/nextjs` 7 (optional) |
| DB | Neon Postgres, Drizzle ORM, `@neondatabase/serverless` |
| Deploy | Vercel |

Verify latest minors on npm when scaffolding; update [stack-and-tooling.md](stack-and-tooling.md) if defaults drift.
