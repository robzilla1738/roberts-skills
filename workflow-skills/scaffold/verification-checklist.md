# Verification checklist

> Read when: Phase 9 — hard gate before scaffold complete. Back to [SKILL.md](SKILL.md).

---

## Automated commands

Run from project root:

```bash
pnpm install
pnpm typecheck
pnpm lint
pnpm build
pnpm db:push    # or pnpm db:migrate
```

All must exit **0**. Fix failures before claiming done.

---

## Manual smoke tests

| # | Test | Expected |
|---|------|----------|
| 1 | `pnpm dev` → open `/` | Public home loads |
| 2 | Open `/api/trpc/health.check` or use client `HealthBadge` | `{ ok: true, db: true }` when DB configured |
| 3 | Visit `/app` logged out (auth variant) | Redirect to `/sign-in` |
| 4 | Sign in → `/app` | Protected page loads; tRPC demo works |
| 5 | Clerk webhook test event (optional) | User row upserted |

---

## Deliverables

- [ ] `.env.example` — commented, complete for chosen variant
- [ ] `README.md` — setup, env table, scripts, deploy notes
- [ ] No secrets in git diff
- [ ] No stray `console.log` / TODO from scaffold
- [ ] Migrations or push state documented if team uses migrate vs push

---

## Intentionally empty (list in README)

- Domain routers beyond `health`
- UI component library
- E2E tests
- GitHub Actions CI
- Error monitoring (Sentry, etc.)

---

## Optional: autoreview

If scaffold was done in one agent session, invoke **`/review`** using [autoreview](../autoreview/SKILL.md) before the first feature commit.

---

## Scaffold complete

When automated + manual checks pass, report to the user:

- Project path
- Variant (`full-app` / `app-no-auth`)
- Commands to run locally
- Vercel / Neon / Clerk dashboard steps remaining (if any)
