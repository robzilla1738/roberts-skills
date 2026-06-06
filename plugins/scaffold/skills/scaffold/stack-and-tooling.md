# Stack and tooling

> Read when: Phase 1–2 bootstrap and dependency install. Back to [SKILL.md](SKILL.md).

---

## Pinned versions (verify on npm at scaffold time)

| Package | Target | Role |
|---------|--------|------|
| `next` | 16.x | App Router |
| `react` / `react-dom` | 19.x | UI |
| `typescript` | 5.9+ | Types |
| `tailwindcss` | 4.x | Styling |
| `@tailwindcss/postcss` | 4.x | PostCSS |
| `@trpc/server` / `client` / `tanstack-react-query` | 11.x | API |
| `vitest` | 3.x+ | Unit tests |
| `@tanstack/react-query` | 5.x | Client cache |
| `superjson` | 2.x | tRPC transformer |
| `zod` | 4.x | Input validation |
| `@clerk/nextjs` | 7.x | Auth (optional) |
| `drizzle-orm` | 0.45+ | ORM |
| `@neondatabase/serverless` | 1.x | Neon driver |
| `drizzle-kit` | 0.31+ | Migrations (dev) |
| `tsx` | 4.x | Scripts |
| `server-only` | latest | Server boundary marker |
| `clsx` + `tailwind-merge` | latest | `cn()` helper |

---

## `package.json` essentials

```json
{
  "private": true,
  "engines": {
    "node": "22.x",
    "pnpm": ">=10 <11"
  },
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "db:generate": "drizzle-kit generate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio",
    "test": "vitest",
    "test:run": "vitest run"
  }
}
```

**DB workflow** (from intake): `db:push` for solo prototypes; add `"db:migrate": "drizzle-kit migrate"` when profile says `migrate`.

---

## Install commands (after create-next-app)

```bash
pnpm add @trpc/server @trpc/client @trpc/tanstack-react-query @tanstack/react-query superjson zod server-only clsx tailwind-merge
pnpm add drizzle-orm @neondatabase/serverless
pnpm add -D drizzle-kit tsx dotenv vitest

# If auth variant:
pnpm add @clerk/nextjs
```

---

## `tsconfig.json` paths

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## `postcss.config.mjs` (Tailwind v4)

```javascript
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

---

## `lib/cn.ts`

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## `app/globals.css` load order

```css
@import "tailwindcss";

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  background: var(--background);
  color: var(--foreground);
}
```

Extend with design tokens when a design system is chosen.

---

## `next.config.ts` notes

- No special config required for tRPC fetch adapter.
- If using Clerk proxy, follow Clerk docs for Next 16 `proxy.ts` export name (project may export `proxy` from `proxy.ts`).

---

## `.gitignore` additions

Ensure present:

```gitignore
.env
.env.local
.env*.local
```

Commit `.env.example` only.

---

## Phase 9 packages (intake add-ons only)

Install in Phase 9 — not during Phase 2. See [phase-integrations.md](phase-integrations.md).

| Add-on | Packages |
|--------|----------|
| `ai-sdk` | `ai`, `@ai-sdk/react` |
| `resend` | `resend` |
| `stripe` | `stripe` |
| `sentry` | `@sentry/nextjs` |
| `posthog` | `posthog-js` |

---

## Pitfalls

- Using `src/` directory while docs assume `@/*` at repo root — pick one and align tree.
- Installing Phase 9 packages in Phase 2 before intake is confirmed — wait for add-on list.
- Installing Prisma alongside Drizzle — pick Drizzle for this stack.
- Missing `typecheck` script — CI will not catch TS errors before build.

**Prettier** — optional; see [production-habits.md](production-habits.md).

Next: [foundation-env-and-errors.md](foundation-env-and-errors.md) (Phase 2b).
