# Verification checklist

> Read when: **Phase 10** — hard gate before scaffold complete. Back to [SKILL.md](SKILL.md).

Run Phase 10 only after Phase 9 (integrations) completes for all intake add-ons, or after Phase 8 when add-ons = `none`.

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

## Manual smoke tests — core

| # | Test | Expected |
|---|------|----------|
| 1 | `pnpm dev` → open `/` | Public home loads |
| 2 | `HealthBadge` or tRPC health query | `{ ok: true, db: true }` when DB configured |
| 3 | Visit `/app` logged out (auth profile) | Redirect to `/sign-in` |
| 4 | Sign in → `/app` | Protected page loads; tRPC demo works |
| 5 | Clerk webhook test event (optional) | User row upserted |

---

## Manual smoke tests — integrations (per intake add-on)

| Add-on | Test | Expected |
|--------|------|----------|
| `ai-sdk` | `/app/chat` signed in, no AI keys | UI loads; send → 503 or friendly error |
| `ai-sdk` | `/app/chat` with keys | Streamed assistant reply |
| `ai-sdk` | POST `/api/chat` logged out (Clerk) | 401 |
| `resend` | tRPC `email.ping` | `{ configured: true/false }` |
| `stripe` | tRPC `billing.status` | `{ configured: true/false }` |
| `stripe` | POST webhook without signature | 400 |
| `sentry` | Build with `SENTRY_DSN` unset | `pnpm build` passes |
| `posthog` | App loads without PostHog keys | No client throw |

Details: [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md#verification-phase-10).

---

## Deliverables

- [ ] **README** — setup, env table, scripts, **scaffold profile ID**, **installed add-ons**, package manager
- [ ] **Production habits** section — link checklist from [production-habits.md](production-habits.md)
- [ ] `.env.example` — matches `lib/env.ts` (including Phase 9 keys)
- [ ] No secrets in git diff
- [ ] No stray `console.log` / scaffold TODOs
- [ ] DB workflow (`push` vs `migrate`) documented

---

## Intentionally empty (list in README)

Depends on profile — only items **not** selected in intake add-ons:

| Item | Empty when |
|------|------------|
| Stripe routes | `stripe` not in add-ons |
| AI chat | `ai-sdk` not in add-ons |
| GitHub Actions | Unless user asked |
| Playwright | Unless user asked |
| Upstash rate limits | Document in production-habits; wire before launch |

Do not list “UI library” if shadcn profile was applied.

---

## Optional: autoreview

If scaffold was done in one agent session, invoke **`/review`** using the **autoreview** skill (`/review`) before the first feature commit.

---

## Scaffold complete

Report to the user:

- Project path and **scaffold profile**
- **Installed add-ons** and which env keys activate each
- Commands to run locally
- Vercel / Neon / Clerk / provider dashboard steps still manual
- Remaining items from [production-habits.md](production-habits.md) (CI, Playwright, Upstash, etc.)
