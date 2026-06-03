# Foundation — UI kit

> Phase 3 (profiles with `shadcn`). Skip for `api-first` / `minimal`. Back to [SKILL.md](SKILL.md).

---

## Profile: `shadcn` (default for saas-dashboard, internal-tool)

After Tailwind v4 base from [stack-and-tooling.md](stack-and-tooling.md):

```bash
pnpm dlx shadcn@latest init
```

Use defaults compatible with **Tailwind v4** and App Router when the CLI prompts. Prefer **New York** or project aesthetic; stick to one style.

Add essentials:

```bash
pnpm dlx shadcn@latest add button sonner
pnpm add next-themes
```

### Theme provider — `components/providers/theme-provider.tsx`

```tsx
"use client";

import { ThemeProvider as NextThemesProvider } from "next-themes";
import type { ReactNode } from "react";

export function ThemeProvider({ children }: { children: ReactNode }) {
  return (
    <NextThemesProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </NextThemesProvider>
  );
}
```

### Root layout order

```tsx
<ThemeProvider>
  <TrpcProvider>
    {children}
    <Toaster />
  </TrpcProvider>
</ThemeProvider>
```

Import `Toaster` from `@/components/ui/sonner` (path after shadcn add).

---

## Profile: `minimal`

- `lib/cn.ts` only
- No `components/ui/*`
- Plain Tailwind on `app/page.tsx`

---

## Alternative: Base UI

[joyflow-monorepo](https://github.com/) uses `@base-ui-components/react` instead of shadcn. Pick **one** component system per app — do not init both.

---

## Exit criterion

- Home page uses at least one styled control (shadcn `Button` or Tailwind utilities)
- Dark mode works if `next-themes` was added

Next: [database-neon-drizzle.md](database-neon-drizzle.md).
