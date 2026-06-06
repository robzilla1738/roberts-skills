# Product intake and scaffold profiles

> Phase 0 — run before `create-next-app`. Back to [SKILL.md](SKILL.md).

## Opening question (required)

Ask the user:

> **What are you building?** One sentence is enough — e.g. “B2B SaaS dashboard with teams”, “internal ops tool”, “API-first admin with thin UI”, “marketing site only”.

Map the answer to a **scaffold profile** below. If unclear, default to **`saas-dashboard`**.

---

## Archetypes → scaffold profile

| Archetype | When | Profile ID | Auth | DB + tRPC | UI |
|-----------|------|------------|------|-----------|-----|
| SaaS dashboard | Multi-user product, settings, billing later | `saas-dashboard` | Clerk | Full | shadcn + `next-themes` |
| Internal tool | Team-only, fast iteration | `internal-tool` | Clerk or dev-bypass | Full | shadcn (minimal chrome) |
| Public API + thin UI | Backend-first, admin UI later | `api-first` | None unless asked | Full | minimal |
| Marketing site | No authenticated app in this repo | `marketing-only` | — | — | — |
| Extend existing | Next.js repo already started | `extend-existing` | Gap analysis | Partial | — |

### Profile notes

**`saas-dashboard`** (default)

- `/app` protected shell, Clerk webhook user sync
- README: “workspace-ready” — add `workspaceId` / `workspaceProcedure` when multi-tenant (see [production-habits.md](production-habits.md))
- Foundations: env, errors, vitest, shadcn
- If product mentions chat/copilot/billing/email, include matching add-ons in intake (#8) — they will be **installed in Phase 9**

**`internal-tool`**

- Same stack as SaaS; simpler nav (single sidebar placeholder)
- Dev auth bypass optional (Clerk keys blank + seed user)

**`api-first`**

- Skip [foundation-ui.md](foundation-ui.md) shadcn init
- Skip [auth-clerk-optional.md](auth-clerk-optional.md) unless user requests auth
- Still run env, errors, vitest, DB, tRPC

**`marketing-only`**

- Stop scaffold. Open the **web-marketing-landing** skill.

**`extend-existing`**

- Inventory repo; run only missing phases/spokes (see [intake-and-variants.md](intake-and-variants.md)). Include Phase 9 for any add-on not yet wired.

---

## Out of scope for this skill

| Request | Route to |
|---------|----------|
| Supabase instead of Neon/Drizzle | Different stack — do not force this skill |
| NextAuth instead of Clerk | Note in README; see [auth-clerk-optional.md](auth-clerk-optional.md) fork |
| Expo / React Native | Separate mobile scaffold (not here) |
| Turborepo from day one | [intake-and-variants.md](intake-and-variants.md) monorepo fork |

---

## Secondary intake (required picks)

| # | Question | Options | Default |
|---|----------|---------|---------|
| 1 | Project name + directory | — | Ask |
| 2 | Package manager | `pnpm` \| `npm` | `pnpm` |
| 3 | Auth provider | `clerk` \| `none` \| `later` | Profile default |
| 4 | UI kit | `shadcn` \| `minimal` | Profile default |
| 5 | DB workflow | `push` (solo) \| `migrate` (team) | `migrate` for saas-dashboard, `push` for prototypes |
| 6 | Repo shape | `single-app` \| `turborepo` | `single-app` |
| 7 | `NEXT_PUBLIC_APP_URL` | URL | `http://localhost:3000` |
| 8 | **Add-ons** (installed in Phase 9) | `none` or comma-separated: `ai-sdk`, `resend`, `stripe`, `sentry`, `posthog` | Infer from product sentence; else `none` |
| 9 | AI provider (if `ai-sdk`) | `gateway` \| `openai` \| `anthropic` | `gateway` |
| 10 | AI chat persistence (if `ai-sdk`) | `yes` \| `no` | `yes` for saas-dashboard, `no` for api-first |

**Add-ons rule:** every ID listed in #8 must be fully wired in [phase-integrations.md](phase-integrations.md) before Phase 10. Do not document-only.

| Add-on | Typical trigger |
|--------|-----------------|
| `ai-sdk` | Chat, copilot, RAG, agents, tool calling |
| `resend` | Transactional email |
| `stripe` | Subscriptions or payments |
| `sentry` | Error monitoring from day one |
| `posthog` | Product analytics |

---

## Legacy variant mapping

| Old variant | Maps to profile |
|-------------|-----------------|
| `full-app` | `saas-dashboard` |
| `app-no-auth` | `api-first` or `internal-tool` with auth `none` |
| `marketing-only` | `marketing-only` |
| `extend-existing` | `extend-existing` |

---

## Intake output template

Post this plan before coding; wait for user confirmation:

```text
Scaffold profile: saas-dashboard
Product: {{one-liner}}
Path: {{directory}}
Package manager: pnpm
Auth: clerk
UI: shadcn
DB workflow: migrate
Repo shape: single-app
NEXT_PUBLIC_APP_URL: http://localhost:3000
Add-ons (Phase 9 install): ai-sdk, resend
AI provider: gateway
AI persistence: yes

Phases: 0, 1, 2, 2b, 2c, 3, 4, 5, 6, 7, 8, 9, 10
Skipped: —
Spokes: intake-product-profiles, stack-and-tooling, foundation-env-and-errors,
  foundation-testing, foundation-ui, database-neon-drizzle, trpc-and-query,
  auth-clerk-optional, file-tree, vercel-and-env, phase-integrations,
  ai-sdk-and-integrations, verification-checklist, production-habits (read)
```

Proceed to [phases-greenfield.md](phases-greenfield.md).
