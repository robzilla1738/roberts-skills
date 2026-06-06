---
name: scaffold
description: >
  Greenfield or extend a Next.js app with Tailwind v4, tRPC, TanStack Query,
  optional Clerk, Neon/Drizzle, Vercel, and intake-selected add-ons (AI SDK,
  Resend, Stripe, Sentry, PostHog) fully installed and build-green.
  Use for /scaffold or new project setup.
disable-model-invocation: true
version: 2026-06-03.4
platforms: [Next.js, TypeScript, Vercel]
primary_use_cases:
  - Bootstrap a new full-stack Next.js app on Robert's default stack
  - Add missing tRPC, Drizzle, or Clerk layers to an existing repo
  - Produce a build-green repo with intake integrations installed before feature work
---

# Stack Scaffold

Workflow skill for greenfielding a **Next.js + Tailwind v4 + tRPC + TanStack Query + Neon/Drizzle + Vercel** app, with **optional Clerk** auth — driven by **product intake** so the foundation matches what you are building.

Read this hub first, run **product intake**, then open only the spokes for your profile.

## Mission

Deliver a **fully configured repo** matching intake: core stack (Phases 0–8) plus every selected add-on installed and wired (Phase 9). No product business logic beyond integration **demos/stubs**. Phase 10 verification (`typecheck`, `lint`, `test`, `build`, smoke tests) must pass before the skill is complete.

## Non-negotiables

1. **Product intake first** — ask what you are building; record scaffold profile before `create-next-app`. See [intake-product-profiles.md](intake-product-profiles.md).
2. **App Router only** — no Pages Router for new apps.
3. **Package manager** — default `pnpm`; pin Node `22.x` and pnpm `>=10 <11` unless intake says `npm`.
4. **Environment** — `lib/env.ts` (Zod); secrets in `.env.local`; committed `.env.example`. No raw `process.env` in `lib/` elsewhere.
5. **Server boundary** — DB and tRPC routers are server-only; `import "server-only"` where appropriate.
6. **Safe tRPC errors** — `AppError` + Zod mapped in formatter; never leak stacks.
7. **Clerk on Next 16** — `proxy.ts` + `clerkMiddleware` when auth is enabled.
8. **Lazy database** — `getDb()` must not throw at import time when `DATABASE_URL` is missing.
9. **Scaffold profile in README** — record profile ID, stack choices, installed add-ons, and [production-habits.md](production-habits.md) checklist.
10. **Intake add-ons are installed** — when add-ons are not `none`, run Phase 9 ([phase-integrations.md](phase-integrations.md)); do not leave them README-only.

## When to use

- Starting a SaaS dashboard, internal tool, or API-first Next app
- Adding tRPC + Drizzle + Clerk to an empty Next.js repo
- User invokes `/scaffold`

## When not to use

- **Marketing-only** → the **web-marketing-landing** skill
- **Supabase / Prisma-first** → custom plan (not default spokes)
- **Expo / mobile-only** → separate skill
- **macOS / non-Next** → out of scope

## Intake router

| Profile | Summary |
|---------|---------|
| `saas-dashboard` | Default — Clerk, full stack, shadcn, foundations |
| `internal-tool` | Full stack; simpler shell; optional dev auth bypass |
| `api-first` | tRPC + DB; minimal UI; auth optional |
| `marketing-only` | Redirect web-marketing-landing |
| `extend-existing` | Gap-fill only |

Details: [intake-product-profiles.md](intake-product-profiles.md).

## Phase bundle

Execute in order. Details: [phases-greenfield.md](phases-greenfield.md).

| Step | Spoke |
|------|--------|
| 0 | [intake-product-profiles.md](intake-product-profiles.md) |
| 1–2 | [stack-and-tooling.md](stack-and-tooling.md) |
| 2b | [foundation-env-and-errors.md](foundation-env-and-errors.md) |
| 2c | [foundation-testing.md](foundation-testing.md) |
| 3 | [foundation-ui.md](foundation-ui.md) + [file-tree-and-conventions.md](file-tree-and-conventions.md) |
| 4 | [database-neon-drizzle.md](database-neon-drizzle.md) |
| 5 | [trpc-and-query.md](trpc-and-query.md) |
| 6 | [auth-clerk-optional.md](auth-clerk-optional.md) (if auth) |
| 7 | App shell — [file-tree-and-conventions.md](file-tree-and-conventions.md) |
| 8 | [vercel-and-env.md](vercel-and-env.md) |
| 9 | [phase-integrations.md](phase-integrations.md) + [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md) — skip only if add-ons = `none` |
| 10 | [verification-checklist.md](verification-checklist.md) |
| post | [production-habits.md](production-habits.md) — document remaining launch habits in README |

Skip phases per profile (e.g. `api-first` skips shadcn and often auth). **Never skip Phase 9** when intake lists add-ons.

After Phase 10, recommend **`/review`** via the **autoreview** skill (`/review`).

## Spoke index

| File | Contents |
|------|----------|
| [intake-product-profiles.md](intake-product-profiles.md) | Product question, profiles, intake template |
| [intake-and-variants.md](intake-and-variants.md) | Extend-existing, monorepo, out-of-scope |
| [stack-and-tooling.md](stack-and-tooling.md) | Versions, create-next-app, scripts |
| [foundation-env-and-errors.md](foundation-env-and-errors.md) | `lib/env.ts`, `lib/errors.ts` |
| [foundation-testing.md](foundation-testing.md) | Vitest |
| [foundation-ui.md](foundation-ui.md) | shadcn vs minimal |
| [phases-greenfield.md](phases-greenfield.md) | Phases 0–10 |
| [phase-integrations.md](phase-integrations.md) | Phase 9 — install intake add-ons |
| [file-tree-and-conventions.md](file-tree-and-conventions.md) | Canonical tree |
| [database-neon-drizzle.md](database-neon-drizzle.md) | Neon, Drizzle |
| [trpc-and-query.md](trpc-and-query.md) | tRPC server, client, route |
| [auth-clerk-optional.md](auth-clerk-optional.md) | Clerk |
| [vercel-and-env.md](vercel-and-env.md) | Deploy |
| [verification-checklist.md](verification-checklist.md) | Build gate |
| [production-habits.md](production-habits.md) | Post-scaffold checklist |
| [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md) | AI SDK streaming, Resend, Stripe, provider/env patterns |

## Related skills

- the **autoreview** skill (`/review`)
- the **web-marketing-landing** skill
- **clerk-auth** (global) — deep Clerk patterns

## Default stack

| Layer | Package / tool |
|-------|----------------|
| Runtime | Node 22.x, pnpm 10.x |
| Framework | Next.js 16, React 19, TypeScript 5.9+ |
| CSS | Tailwind CSS 4 |
| API | tRPC 11, `@trpc/tanstack-react-query`, TanStack Query 5, superjson, zod |
| Testing | Vitest |
| Auth | `@clerk/nextjs` 7 (profile-dependent) |
| DB | Neon, Drizzle |
| Deploy | Vercel |
| AI (intake) | `ai`, `@ai-sdk/react` — Phase 9 |
| Email / billing (intake) | `resend`, `stripe` — Phase 9 |
| Observability (intake) | `@sentry/nextjs`, `posthog-js` — Phase 9 |

Verify latest minors on npm when scaffolding.
