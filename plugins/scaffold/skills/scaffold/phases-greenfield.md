# Phases — greenfield

> Ordered execution with exit criteria. Back to [SKILL.md](SKILL.md).

**Rule:** Do not start phase N+1 until phase N’s exit criterion passes. Skip phases per [intake-product-profiles.md](intake-product-profiles.md).

---

## Phase 0 — Product intake

| | |
|--|--|
| **Actions** | [intake-product-profiles.md](intake-product-profiles.md) — ask what you are building; post scaffold plan |
| **Exit** | Profile ID + secondary picks written; user confirmed |

---

## Phase 1 — Bootstrap

| | |
|--|--|
| **Actions** | `pnpm create next-app@latest` (or `npm` per intake) |
| **Spoke** | [stack-and-tooling.md](stack-and-tooling.md) |
| **Exit** | `pnpm dev` loads |

```bash
pnpm create next-app@latest {{project-name}} \
  --typescript --eslint --app --no-src-dir --tailwind \
  --import-alias "@/*" --turbopack --use-pnpm
```

---

## Phase 2 — Tooling

| | |
|--|--|
| **Actions** | `engines`, `typecheck`, `tsx`, core deps |
| **Spoke** | [stack-and-tooling.md](stack-and-tooling.md) |
| **Exit** | `pnpm lint` and `pnpm typecheck` pass |

---

## Phase 2b — Env and errors

| | |
|--|--|
| **Actions** | `lib/env.ts`, `lib/errors.ts` |
| **Spoke** | [foundation-env-and-errors.md](foundation-env-and-errors.md) |
| **Skip** | Never — all full-stack profiles |
| **Exit** | Files exist; rule documented in README |

---

## Phase 2c — Testing

| | |
|--|--|
| **Actions** | Vitest config + sample test |
| **Spoke** | [foundation-testing.md](foundation-testing.md) |
| **Skip** | Never for full-stack profiles |
| **Exit** | `pnpm test:run` passes |

---

## Phase 3 — UI base

| | |
|--|--|
| **Actions** | `globals.css`, `lib/cn.ts`, layout; shadcn if profile says so |
| **Spoke** | [foundation-ui.md](foundation-ui.md), [file-tree-and-conventions.md](file-tree-and-conventions.md) |
| **Skip** | `api-first` with `minimal` UI |
| **Exit** | Home renders |

---

## Phase 4 — Database

| | |
|--|--|
| **Actions** | Neon, Drizzle, schema, lazy `getDb()`, push or migrate per intake |
| **Spoke** | [database-neon-drizzle.md](database-neon-drizzle.md) |
| **Exit** | `pnpm db:push` or migrate succeeds |

---

## Phase 5 — tRPC

| | |
|--|--|
| **Actions** | Full tRPC layer + AppError formatter + rate-limit stub |
| **Spoke** | [trpc-and-query.md](trpc-and-query.md) |
| **Exit** | `health.check` works |

---

## Phase 6 — Auth (optional)

| | |
|--|--|
| **Actions** | Clerk proxy, pages, webhook |
| **Spoke** | [auth-clerk-optional.md](auth-clerk-optional.md) |
| **Skip** | `api-first` / profile with `auth: none` |
| **Exit** | `/app` auth flow works when enabled |

---

## Phase 7 — App shell

| | |
|--|--|
| **Actions** | `/` + `/app` demos |
| **Spoke** | [file-tree-and-conventions.md](file-tree-and-conventions.md) |
| **Exit** | Client + server tRPC demos work |

---

## Phase 8 — Vercel

| | |
|--|--|
| **Actions** | `.env.example` aligned with `lib/env.ts`; deploy notes |
| **Spoke** | [vercel-and-env.md](vercel-and-env.md) |
| **Exit** | Preview checklist documented |

---

## Phase 9 — Integrations (intake add-ons)

| | |
|--|--|
| **Actions** | Install and wire every add-on from intake (#8): packages, `lib/env.ts`, routes, demos |
| **Spoke** | [phase-integrations.md](phase-integrations.md), [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md) |
| **Skip** | Add-ons = `none` only |
| **Exit** | All selected add-ons in `package.json` + code; ready for Phase 10 build gate |

---

## Phase 10 — Verify

| | |
|--|--|
| **Actions** | [verification-checklist.md](verification-checklist.md); README with profile, **installed add-ons**, [production-habits.md](production-habits.md) |
| **Exit** | All automated checks green; integration smoke tests for selected add-ons |

---

## Handoff

Scaffold is **complete** only after Phase 10 passes. Suggest **`/review`** (the **autoreview** skill). Tell the user which env keys activate each installed integration (AI, Resend, Stripe, etc.).
