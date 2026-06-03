# Phases — greenfield

> Ordered execution with exit criteria. Back to [SKILL.md](SKILL.md).

**Rule:** Do not start phase N+1 until phase N’s exit criterion passes.

---

## Phase 0 — Intake

| | |
|--|--|
| **Actions** | Complete [intake-and-variants.md](intake-and-variants.md); post scaffold plan |
| **Exit** | Variant and auth decision written; user confirmed or defaults applied |

---

## Phase 1 — Bootstrap

| | |
|--|--|
| **Actions** | `pnpm create next-app@latest` — TypeScript, ESLint, App Router, **no `src/` directory**, Tailwind, import alias `@/*` → `./*` |
| **Spoke** | [stack-and-tooling.md](stack-and-tooling.md) |
| **Exit** | `pnpm dev` serves default page without errors |

```bash
pnpm create next-app@latest {{project-name}} \
  --typescript \
  --eslint \
  --app \
  --no-src-dir \
  --tailwind \
  --import-alias "@/*" \
  --turbopack \
  --use-pnpm
```

Adjust flags if `create-next-app` CLI changed; prefer **no `src/`** for consistency with spoke file tree.

---

## Phase 2 — Tooling

| | |
|--|--|
| **Actions** | `engines`, `typecheck`, `tsx`, Drizzle/tRPC deps (or split: DB phase 4, tRPC phase 5), `server-only` |
| **Spoke** | [stack-and-tooling.md](stack-and-tooling.md) |
| **Exit** | `pnpm lint` passes; `pnpm typecheck` passes (add script if missing) |

---

## Phase 3 — UI base

| | |
|--|--|
| **Actions** | `app/globals.css` (Tailwind v4), `lib/cn.ts`, minimal `app/layout.tsx` + `app/page.tsx` |
| **Spoke** | [file-tree-and-conventions.md](file-tree-and-conventions.md) |
| **Exit** | Home page renders with Tailwind utility visible |

---

## Phase 4 — Database

| | |
|--|--|
| **Actions** | Neon project, `DATABASE_URL`, Drizzle config, `users` table, lazy `getDb()`, `db:push` or migrate |
| **Spoke** | [database-neon-drizzle.md](database-neon-drizzle.md) |
| **Exit** | `pnpm db:push` (or migrate) succeeds against Neon |

---

## Phase 5 — tRPC

| | |
|--|--|
| **Actions** | `lib/trpc/*`, `app/api/trpc/[trpc]/route.ts`, `TrpcProvider`, `health` router |
| **Spoke** | [trpc-and-query.md](trpc-and-query.md) |
| **Exit** | `health.check` returns `{ ok: true, db: boolean }` from client or curl |

---

## Phase 6 — Auth (optional)

| | |
|--|--|
| **Actions** | Clerk env, `proxy.ts`, sign-in/up routes, `ClerkProvider`, `getCurrentUser`, webhook sync |
| **Spoke** | [auth-clerk-optional.md](auth-clerk-optional.md) |
| **Skip when** | `app-no-auth` |
| **Exit** | Logged-out visit to `/app` redirects to `/sign-in`; logged-in user reaches `/app` |

---

## Phase 7 — App shell

| | |
|--|--|
| **Actions** | Public `/`, protected `/app` with layout; one `protectedProcedure` demo + one client `useQuery` demo |
| **Spoke** | [file-tree-and-conventions.md](file-tree-and-conventions.md), [trpc-and-query.md](trpc-and-query.md) |
| **Exit** | Demo pages call tRPC successfully |

---

## Phase 8 — Vercel

| | |
|--|--|
| **Actions** | `.env.example` complete; Vercel project; Neon integration; production env checklist |
| **Spoke** | [vercel-and-env.md](vercel-and-env.md) |
| **Exit** | Preview deploy checklist documented (deploy may be manual) |

---

## Phase 9 — Verify

| | |
|--|--|
| **Actions** | Run [verification-checklist.md](verification-checklist.md); write project `README.md` |
| **Exit** | All automated checks green; deliverables listed |

---

## Handoff

Scaffold is complete when Phase 9 passes. Suggest **`/review`** ([autoreview](../autoreview/SKILL.md)) before first feature PR.

**Intentionally empty next steps** (document in README):

- First domain router (e.g. `projects`, `billing`)
- Design system / component library
- E2E tests (Playwright)
- CI workflow
