# Intake and variants

> Read first on every `/scaffold` run. Back to [SKILL.md](SKILL.md).

Do not create files until intake answers are recorded (in chat or a short plan comment).

---

## Required questions

| # | Question | Default if unspecified |
|---|----------|------------------------|
| 1 | **Project name** and target directory | Ask user |
| 2 | **Variant** | `full-app` |
| 3 | **Auth** (Clerk) | Yes for `full-app`; No for `app-no-auth` |
| 4 | **Public app URL** (`NEXT_PUBLIC_APP_URL`) | `http://localhost:3000` |
| 5 | **Repo shape** | Single Next.js app (not Turborepo) |

Optional:

- Design system / UI kit preference (shadcn, none)
- Dev auth bypass (Clerk keys blank → seeded user) — off by default

---

## Variants

### `full-app` (default)

Full stack: Tailwind v4, Drizzle + Neon, tRPC, Clerk, `/app` protected shell, Vercel-ready env.

**Spokes:** all except marketing redirect.

### `app-no-auth`

Same as full-app but **no Clerk**. Use `publicProcedure` only; leave `clerkId` nullable on `users` for future auth.

**Skip:** [auth-clerk-optional.md](auth-clerk-optional.md).

**Still protect sensitive routes later** when auth is added — document in project README.

### `marketing-only`

No database, no tRPC, no Clerk in this repo.

**Action:** Stop scaffold workflow. Open [web-marketing-landing](../../design-skills/web-marketing-landing/SKILL.md) and follow [stack-and-scaffold.md](../../design-skills/web-marketing-landing/stack-and-scaffold.md).

### `extend-existing`

User already has a Next.js repo.

**Action:**

1. List what exists (package.json, `app/`, `lib/`, `db/`, `api/trpc`, Clerk, Drizzle).
2. Map gaps to phases in [phases-greenfield.md](phases-greenfield.md).
3. Run only missing phases; do not re-bootstrap with `create-next-app`.

---

## Monorepo fork (out of v1 default)

For Turborepo (`apps/web` + `packages/*`):

1. Create monorepo with `pnpm create turbo@latest` or manual workspace `pnpm-workspace.yaml`.
2. Apply single-app phases inside `apps/web` using paths relative to that app.
3. Share types package only when needed — avoid premature abstraction.

Document chosen layout in the project README. Do not duplicate monorepo setup in this skill beyond this note.

---

## Intake output template

```text
Scaffold plan
- Project: {{name}}
- Path: {{directory}}
- Variant: full-app | app-no-auth | marketing-only | extend-existing
- Auth: yes | no
- NEXT_PUBLIC_APP_URL: {{url}}
- Phases: 0,1,2,3,4,5,6,7,8,9 (list skipped)
```

Proceed to [phases-greenfield.md](phases-greenfield.md) Phase 0 sign-off, then Phase 1.
