# Vercel and environment

> Read when: Phase 8. Back to [SKILL.md](SKILL.md).

---

## Environment source of truth

All variables are declared in **`lib/env.ts`** ([foundation-env-and-errors.md](foundation-env-and-errors.md)). `.env.example` must stay in sync with that schema.

---

## `.env.example` template

Commit this file; copy to `.env.local` for local dev.

```env
# --- Core ------------------------------------------------------------------
NODE_ENV=development

# Public origin (metadata, redirects). Required in production.
NEXT_PUBLIC_APP_URL=http://localhost:3000

# --- Database --------------------------------------------------------------
# Neon Postgres pooled connection string
DATABASE_URL=

# --- Auth (Clerk) — optional for app-no-auth ---------------------------
# Leave blank for dev bypass only if documented in README
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
CLERK_WEBHOOK_SECRET=

# --- AI (Phase 9 if ai-sdk) ----------------------------------------------
AI_GATEWAY_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# --- Email (Phase 9 if resend) -------------------------------------------
RESEND_API_KEY=
RESEND_FROM_EMAIL=

# --- Stripe (Phase 9 if stripe) ------------------------------------------
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# --- Observability (Phase 9) ---------------------------------------------
SENTRY_DSN=
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
POSTHOG_API_KEY=

# --- Vercel (set in dashboard, not locally) ------------------------------
# VERCEL_URL is auto-injected on preview/production
```

Include only sections for add-ons selected in intake. Phase 9 extends `lib/env.ts` to match — see [phase-integrations.md](phase-integrations.md).

---

## Local setup

```bash
cp .env.example .env.local
# Fill DATABASE_URL from Neon
# Fill Clerk keys if using auth
pnpm install
pnpm db:push
pnpm dev
```

---

## Vercel project

1. Import Git repository.
2. Framework preset: **Next.js**.
3. Build command: `pnpm build` (default).
4. Install command: `pnpm install`.
5. Node.js version: **22.x** (match `engines`).

---

## Environment variables (Vercel dashboard)

| Variable | Environments |
|----------|----------------|
| `DATABASE_URL` | Production, Preview |
| `NEXT_PUBLIC_APP_URL` | Production (prod URL), Preview (optional) |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | All (if auth) |
| `CLERK_SECRET_KEY` | Production, Preview |
| `CLERK_WEBHOOK_SECRET` | Production |

Use Vercel **Neon integration** to inject `DATABASE_URL` on preview branches when possible.

---

## Clerk production checklist

- [ ] Production instance keys in Vercel Production only
- [ ] Webhook URL: `https://{{domain}}/api/webhooks/clerk`
- [ ] Sign-in/up URLs match `NEXT_PUBLIC_CLERK_*_URL`
- [ ] Allowed redirect URLs include preview domains if needed

---

## Preview deploy checklist

- [ ] `pnpm build` passes locally
- [ ] Preview has `DATABASE_URL` (Neon branch or shared dev DB — team policy)
- [ ] Clerk development instance allows preview origin
- [ ] Smoke: home loads, `health.check` works, `/app` auth flow

---

## `vercel.json`

Usually **not required** for standard Next.js 16. Add only for:

- Custom headers
- Rewrites to external API
- Cron jobs

---

## Project README section (scaffold deliverable)

Include:

1. Prerequisites (Node 22, pnpm 10, Neon, Clerk)
2. Env table (from `.env.example`)
3. Scripts (`dev`, `build`, `db:*`)
4. Deploy link placeholder
5. “What’s next” — first domain router, design system, CI

---

## Pitfalls

- Committing `.env.local`
- Using production Neon branch for every preview without isolation
- Forgetting `NEXT_PUBLIC_APP_URL` in production (broken metadata/redirects)

Next: Phase 9 [phase-integrations.md](phase-integrations.md) if add-ons selected, then [verification-checklist.md](verification-checklist.md) (Phase 10).
