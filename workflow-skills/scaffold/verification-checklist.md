# Verification checklist

> Read when: Phase 9 — hard gate before scaffold complete. Back to [SKILL.md](SKILL.md).

---

## Automated commands

Run from project root:

```bash
pnpm install
pnpm typecheck
pnpm lint
pnpm test:run
pnpm build
pnpm db:push    # or pnpm db:migrate per intake
```

All must exit **0**. Fix failures before claiming done.

---

## Manual smoke tests

| # | Test | Expected |
|---|------|----------|
| 1 | `pnpm dev` → open `/` | Public home loads |
| 2 | `HealthBadge` or tRPC health query | `{ ok: true, db: true }` when DB configured |
| 3 | Visit `/app` logged out (auth profile) | Redirect to `/sign-in` |
| 4 | Sign in → `/app` | Protected page loads; tRPC demo works |
| 5 | Clerk webhook test event (optional) | User row upserted |

---

## Deliverables

- [ ] **README** — setup, env table, scripts, **scaffold profile ID**, package manager
- [ ] **Production habits** section — link checklist from [production-habits.md](production-habits.md)
- [ ] `.env.example` — matches `lib/env.ts`
- [ ] No secrets in git diff
- [ ] No stray `console.log` / scaffold TODOs
- [ ] DB workflow (`push` vs `migrate`) documented

---

## Intentionally empty (list in README)

Depends on profile:

| Profile | May still be empty |
|---------|-------------------|
| `saas-dashboard` | Domain routers, Stripe, CI, Playwright, Sentry |
| `api-first` | shadcn components, auth (if deferred) |
| All | GitHub Actions unless user asked |

Do not list “UI library” if shadcn profile was applied.

---

## Optional: autoreview

If scaffold was done in one agent session, invoke **`/review`** using [autoreview](../autoreview/SKILL.md) before the first feature commit.

---

## Scaffold complete

Report to the user:

- Project path and **scaffold profile**
- Commands to run locally
- Vercel / Neon / Clerk steps remaining
- Post-scaffold add-ons from intake (document only)
