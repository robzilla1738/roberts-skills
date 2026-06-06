# Production habits (post-scaffold)

> Read after Phase 10; document in project README. Back to [SKILL.md](SKILL.md).

The scaffold finishes **build-green** with intake-selected integrations installed (Phase 9). These habits are what teams add **before or after launch** — document in README; implement when the product needs them.

---

## When to add what

| Habit | Why | When |
|-------|-----|------|
| **GitHub Actions** — `typecheck`, `lint`, `test:run`, `build` | CI gate on every PR | First PR |
| **Prettier** + **lint-staged** + husky | Consistent formatting | Team repos |
| **Playwright** e2e | Critical path smoke (sign-in, `/app`, `/app/chat`) | After core UI stable |
| **Vercel Analytics** / Speed Insights | Traffic and performance | Production deploy |
| **Upstash rate limit** | Replace in-memory tRPC + `/api/chat` stubs | Multi-instance / before public launch |
| **Resend domain verify** | Deliverability | Before production email (if `resend` installed) |
| **Stripe products/prices** | Real checkout | After `stripe` webhook stub |
| **`workspaceProcedure` + tenant column** | Multi-tenant SaaS | Second account type in product |
| **AI multi-thread UX** | Thread picker, titles | If persistence was `no` in intake |
| **Sentry source maps / alerts** | Actionable errors | After `sentry` installed — configure in Sentry UI |
| **PostHog dashboards** | Funnels, feature flags | After `posthog` installed |
| **`assertProductionReadyEnv()`** | Block deploy with missing prod env | Pre-launch checklist |
| **Committed SQL migrations** | Safer than `db:push` on shared DB | Team / production |

---

## tRPC stubs to harden later

Scaffold may include:

- In-memory **rate limit** on `publicProcedure` — swap for Redis/Upstash ([production-habits](#when-to-add-what))
- **CSRF / origin check** TODO on `/api/trpc` — implement before public launch if using cookies

---

## SaaS: workspace-ready note

For `saas-dashboard` profile, README should say:

> When adding organizations/workspaces, introduce `workspaceId` on domain tables and a `workspaceProcedure` middleware. Do not add until the product needs multi-tenancy.

---

## README section template

```markdown
## Production checklist (after scaffold)

Installed integrations: {{list from intake}}

- [ ] CI: GitHub Actions
- [ ] E2E: Playwright
- [ ] Rate limits: Upstash on tRPC + /api/chat
- [ ] Provider keys in Vercel for: {{AI, Resend, Stripe, Sentry, PostHog as applicable}}
- [ ] Domain-specific product work (routers, billing flows, email templates)
```

---

## Related

- [phase-integrations.md](phase-integrations.md) — installed add-ons
- [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md) — AI SDK depth
- the **autoreview** skill (`/review`) — `/review` before merge
- [vercel-and-env.md](vercel-and-env.md) — deploy env
