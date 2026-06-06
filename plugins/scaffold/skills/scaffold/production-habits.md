# Production habits (post-scaffold)

> Read after Phase 9; document in project README. Not auto-installed unless user asks. Back to [SKILL.md](SKILL.md).

The base scaffold stops at a **build-green foundation**. These habits match mature production Next.js repos and current industry practice.

---

## When to add what

| Habit | Why | When |
|-------|-----|------|
| **GitHub Actions** — `typecheck`, `lint`, `test:run`, `build` | CI gate on every PR | First PR |
| **Prettier** + **lint-staged** + husky | Consistent formatting | Team repos |
| **Playwright** e2e | Critical path smoke (sign-in, `/app`) | After core UI stable |
| **Sentry** or similar | Error monitoring | Before public launch |
| **Vercel Analytics** / Speed Insights | Traffic and performance | Production deploy |
| **Upstash rate limit** | Replace in-memory tRPC rate limit | Multi-instance / production |
| **`workspaceProcedure` + tenant column** | Multi-tenant SaaS | Second account type in product |
| **Stripe / Resend / AI SDK** | Product features | Per intake add-ons |
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
## Production checklist (not done in scaffold)

- [ ] CI: GitHub Actions
- [ ] E2E: Playwright
- [ ] Monitoring: Sentry
- [ ] Rate limits: Upstash (if multi-region)
- [ ] Billing: Stripe (if applicable)
```

---

## Related

- the **autoreview** skill (`/review`) — `/review` before merge
- [vercel-and-env.md](vercel-and-env.md) — deploy env
