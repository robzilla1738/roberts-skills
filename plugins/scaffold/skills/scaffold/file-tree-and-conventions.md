# File tree and conventions

> Read when: Phase 3 and 7 layout. Back to [SKILL.md](SKILL.md).

Canonical **single-app** tree after full scaffold:

```text
app/
  layout.tsx                 # fonts, globals, ClerkProvider + TrpcProvider (if auth)
  page.tsx                   # public home
  globals.css
  (auth)/
    sign-in/[[...sign-in]]/page.tsx
    sign-up/[[...sign-up]]/page.tsx
  app/
    layout.tsx               # authed shell (sidebar later)
    page.tsx                 # protected home + tRPC demo
  api/
    trpc/[trpc]/route.ts
    webhooks/clerk/route.ts  # if auth
components/
  providers/
    TrpcProvider.tsx         # or lib/trpc/client.tsx exports TrpcProvider
    theme-provider.tsx       # if shadcn + next-themes
  ui/                        # shadcn components
db/
  schema.ts
  relations.ts               # optional when relations grow
  index.ts
  migrations/                # after db:generate
drizzle.config.ts
lib/
  env.ts
  errors.ts
  cn.ts
  auth/
    current.ts               # getCurrentUser (if auth)
    config.ts                # isClerkConfigured (optional)
  trpc/
    server.ts
    context.ts
    procedures.ts
    middleware/
      rate-limit.ts
    client.tsx               # TRPCProvider + useTRPC
    server-caller.ts         # optional RSC caller
    routers/
      _app.ts
      health.ts
tests/
  errors.test.ts
vitest.config.ts
proxy.ts                     # Clerk (Next 16) — if auth
.env.example
.env.local                   # gitignored
```

---

## Folder rules

| Path | Rule |
|------|------|
| `app/` | Routes only; thin pages delegate to components |
| `components/` | React UI; client components need `"use client"` |
| `lib/` | Shared logic; DB access and tRPC routers stay server-side |
| `db/` | Schema + migrations; no React imports |
| `lib/trpc/routers/` | One file per domain router; merge in `_app.ts` |

---

## Route groups

| Route | Access |
|-------|--------|
| `/` | Public |
| `/sign-in`, `/sign-up` | Public (Clerk) |
| `/app/*` | Protected (Clerk + `protectedProcedure` demos) |
| `/api/trpc/*` | Public handler; auth inside procedures |

---

## `app/layout.tsx` provider order

```tsx
// Outermost → innermost
<ClerkProvider>           {/* omit if app-no-auth */}
  <TrpcProvider>
    {children}
  </TrpcProvider>
</ClerkProvider>
```

`TrpcProvider` must be a client component.

---

## Minimal protected shell — `app/app/layout.tsx`

```tsx
export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="border-b px-4 py-3">
        <span className="font-medium">App</span>
      </header>
      <main className="p-4">{children}</main>
    </div>
  );
}
```

---

## Demo pages

**Public `app/page.tsx`:** link to `/app` and `/sign-in`.

**Protected `app/app/page.tsx`:** `HealthBadge` with `useTRPC()` + `useQuery(trpc.health.check.queryOptions())` — proves end-to-end stack.

---

## Naming

- Routers: `health.ts`, `user.ts` — lowercase file, camelCase export `healthRouter`
- DB tables: plural `users` in Drizzle `pgTable("users", ...)`
- Env: `NEXT_PUBLIC_*` only for browser-safe values

---

## Monorepo note

If using `apps/web`, all paths above are relative to `apps/web/`. Keep `drizzle.config.ts` next to that app’s `package.json`.
