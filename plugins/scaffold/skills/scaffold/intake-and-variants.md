# Intake router

> Read first on every `/scaffold` run. Back to [SKILL.md](SKILL.md).

**Do not create files until platform + product intake is complete.**

1. **[platform-router.md](platform-router.md)** — platform family + integration recommendations
2. **Profile file** — [intake-product-profiles.md](intake-product-profiles.md) (web) or [intake-native-profiles.md](intake-native-profiles.md) (iOS/macOS)
3. Post intake output template; user confirms
4. Execute phase bundle — [phases-greenfield.md](phases-greenfield.md) or [phases-native-greenfield.md](phases-native-greenfield.md)

This file covers **legacy aliases**, **extend-existing**, and **monorepo** only.

---

## Quick path

1. Ask: **What platform?** → [platform-router.md](platform-router.md)
2. Ask: **What are you building?** → family profile file
3. **Recommend** add-ons; user confirms
4. Post intake output template
5. Execute the matching phase bundle

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
