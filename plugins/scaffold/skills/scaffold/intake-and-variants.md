# Intake router

> Read first on every `/scaffold` run. Back to [SKILL.md](SKILL.md).

**Do not create files until product intake is complete.**

Full intake lives in **[intake-product-profiles.md](intake-product-profiles.md)** — archetype, profile ID, secondary picks, and output template.

This file covers **legacy aliases** and **extend-existing** / **monorepo** only.

---

## Quick path

1. Ask: **What are you building?**
2. Pick profile in [intake-product-profiles.md](intake-product-profiles.md)
3. Post intake output template
4. Execute [phases-greenfield.md](phases-greenfield.md)

---

## Extend-existing

1. List what exists: `package.json`, `app/`, `lib/env.ts`, `lib/trpc/`, `db/`, `proxy.ts`, `vitest.config.ts`, UI kit.
2. Map gaps to phases (skip phases already satisfied).
3. Do **not** re-run `create-next-app`.

---

## Monorepo fork

For Turborepo (`apps/web` + packages):

1. `pnpm create turbo@latest` or manual `pnpm-workspace.yaml`
2. Run single-app phases inside **`apps/web`**
3. Pin engines at repo root; `packageManager` in root `package.json`

Document layout in project README. No full monorepo generator in this skill.

---

## Supabase / Prisma

Not supported as defaults. If user insists on Supabase or Prisma, stop and agree on a custom plan — do not half-apply Neon/Drizzle spokes.
