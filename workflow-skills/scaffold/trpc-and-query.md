# tRPC and TanStack Query

> Read when: Phase 5 and 7. Back to [SKILL.md](SKILL.md).

---

## Architecture

```text
Browser → TrpcProvider (React Query) → POST /api/trpc → appRouter → procedures → getDb()
Server Components → createCaller(appRouter) → same routers (no HTTP)
```

- Routers and context: **server only**
- `TrpcProvider`: **client only** (`"use client"`)

---

## `lib/trpc/server.ts`

```typescript
import { initTRPC, TRPCError } from "@trpc/server";
import superjson from "superjson";
import { ZodError } from "zod";
import type { TrpcContext } from "./context";

const t = initTRPC.context<TrpcContext>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    if (error.cause instanceof ZodError) {
      return {
        ...shape,
        message: "Invalid input",
        data: {
          ...shape.data,
          code: "BAD_REQUEST",
          zodIssues: error.cause.issues,
        },
      };
    }
    return {
      ...shape,
      message:
        error.code === "INTERNAL_SERVER_ERROR"
          ? "Internal server error"
          : shape.message,
      data: {
        ...shape.data,
        stack: undefined,
      },
    };
  },
});

export const router = t.router;
export const middleware = t.middleware;
export const procedure = t.procedure;
export const createCallerFactory = t.createCallerFactory;
```

Extend with typed `AppError` when the app grows.

---

## `lib/trpc/context.ts`

```typescript
import { randomUUID } from "node:crypto";
import type { getCurrentUser } from "@/lib/auth/current";

type DbUser = Awaited<ReturnType<typeof getCurrentUser>>;

export interface TrpcContext {
  requestId: string;
  headers: Headers;
  getUser: () => Promise<DbUser>;
}

export type AuthedTrpcContext = TrpcContext & { user: DbUser };

export async function createTrpcContext(opts: { req: Request }): Promise<TrpcContext> {
  const requestId =
    opts.req.headers.get("x-request-id") ??
    opts.req.headers.get("x-vercel-id") ??
    randomUUID();

  let cachedUser: DbUser | null = null;

  return {
    requestId,
    headers: opts.req.headers,
    async getUser() {
      if (cachedUser) return cachedUser;
      const { getCurrentUser } = await import("@/lib/auth/current");
      cachedUser = await getCurrentUser();
      return cachedUser;
    },
  };
}
```

For `app-no-auth`, replace `getCurrentUser` with a stub or remove `protectedProcedure`.

---

## `lib/trpc/procedures.ts`

```typescript
import { TRPCError } from "@trpc/server";
import { procedure } from "./server";
import { middleware } from "./server";

export const publicProcedure = procedure;

const authMiddleware = middleware(async ({ ctx, next }) => {
  let user;
  try {
    user = await ctx.getUser();
  } catch {
    throw new TRPCError({ code: "UNAUTHORIZED", message: "Authentication required" });
  }
  return next({ ctx: { ...ctx, user } });
});

export const protectedProcedure = procedure.use(authMiddleware);
```

---

## `lib/trpc/routers/health.ts`

```typescript
import { sql } from "drizzle-orm";
import { getDb } from "@/db";
import { publicProcedure, router } from "../server";

export const healthRouter = router({
  check: publicProcedure.query(async () => {
    let dbOk = false;
    try {
      await getDb().execute(sql`SELECT 1`);
      dbOk = true;
    } catch {
      dbOk = false;
    }
    return { ok: true as const, db: dbOk };
  }),
});
```

---

## `lib/trpc/routers/_app.ts`

```typescript
import { router } from "../server";
import { healthRouter } from "./health";

export const appRouter = router({
  health: healthRouter,
});

export type AppRouter = typeof appRouter;
```

---

## `lib/trpc/client.ts`

```typescript
import { createTRPCReact } from "@trpc/react-query";
import type { AppRouter } from "./routers/_app";

export const api = createTRPCReact<AppRouter>();
```

---

## `app/api/trpc/[trpc]/route.ts`

```typescript
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/lib/trpc/routers/_app";
import { createTrpcContext } from "@/lib/trpc/context";

const MAX_BODY_BYTES = 1024 * 1024;

async function handler(req: Request) {
  // Recommended: CSRF / origin check for mutations in production.
  // See joyflow rejectCrossSiteRequest pattern — implement when adding cookies.

  let request = req;
  if (req.method === "POST") {
    const contentLength = Number(req.headers.get("content-length") ?? 0);
    if (contentLength > MAX_BODY_BYTES) {
      return Response.json({ error: "Request body too large" }, { status: 413 });
    }
  }

  const response = await fetchRequestHandler({
    endpoint: "/api/trpc",
    req: request,
    router: appRouter,
    createContext: () => createTrpcContext({ req: request }),
  });

  const headers = new Headers(response.headers);
  headers.set("Cache-Control", "no-store");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export { handler as GET, handler as POST };
```

---

## `components/providers/TrpcProvider.tsx`

```tsx
"use client";

import { useState, type ReactNode } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { httpBatchLink } from "@trpc/client";
import superjson from "superjson";
import { api } from "@/lib/trpc/client";

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        refetchOnWindowFocus: false,
      },
    },
  });
}

function getBaseUrl() {
  if (typeof window !== "undefined") return "";
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export function TrpcProvider({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => makeQueryClient());
  const [trpcClient] = useState(() =>
    api.createClient({
      links: [
        httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
          transformer: superjson,
        }),
      ],
    }),
  );

  return (
    <api.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </api.Provider>
  );
}
```

---

## RSC server caller (optional)

`lib/trpc/server-caller.ts`:

```typescript
import { createCallerFactory } from "./server";
import { appRouter } from "./routers/_app";

const createCaller = createCallerFactory(appRouter);

export async function getTrpcCaller() {
  const { getCurrentUser } = await import("@/lib/auth/current");
  return createCaller({
    requestId: "rsc",
    headers: new Headers(),
    getUser: getCurrentUser,
  });
}
```

Use in Server Components: `const caller = await getTrpcCaller(); await caller.health.check();`

---

## Client demo

```tsx
"use client";
import { api } from "@/lib/trpc/client";

export function HealthBadge() {
  const { data, isLoading } = api.health.check.useQuery();
  if (isLoading) return <span>Checking…</span>;
  return <span>API {data?.ok ? "ok" : "fail"} · DB {data?.db ? "ok" : "down"}</span>;
}
```

---

## Anti-patterns

- Calling `getDb()` from client components
- Duplicating auth checks in every procedure instead of `protectedProcedure`
- Returning raw `Error.stack` from procedures

Next: [auth-clerk-optional.md](auth-clerk-optional.md) or [verification-checklist.md](verification-checklist.md).
