# tRPC and TanStack Query

> Read when: Phase 5 and 7. Requires [foundation-env-and-errors.md](foundation-env-and-errors.md). Back to [SKILL.md](SKILL.md).

---

## Packages

```bash
pnpm add @trpc/server @trpc/client @trpc/tanstack-react-query @tanstack/react-query superjson zod
```

**Preferred client:** `@trpc/tanstack-react-query` (current tRPC + TanStack Query integration).

**Legacy:** `@trpc/react-query` + `createTRPCReact` still works (joyflow-style); do not mix both in one app.

---

## Architecture

```text
Browser → TRPCProvider → POST /api/trpc → appRouter → procedures → getDb()
Server Components → createCaller(appRouter) → same routers (no HTTP)
```

---

## `lib/trpc/server.ts`

```typescript
import { initTRPC, TRPCError } from "@trpc/server";
import superjson from "superjson";
import { ZodError } from "zod";
import { AppError, isAppError } from "@/lib/errors";
import type { TrpcContext } from "./context";

function appErrorToTrpcCode(err: AppError): TRPCError["code"] {
  switch (err.code) {
    case "NOT_FOUND":
      return "NOT_FOUND";
    case "FORBIDDEN":
      return "FORBIDDEN";
    case "UNAUTHORIZED":
      return "UNAUTHORIZED";
    case "VALIDATION":
      return "BAD_REQUEST";
    case "CONFLICT":
      return "CONFLICT";
    case "RATE_LIMIT":
      return "TOO_MANY_REQUESTS";
    default:
      return "INTERNAL_SERVER_ERROR";
  }
}

const t = initTRPC.context<TrpcContext>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    const cause = error.cause;
    if (isAppError(cause)) {
      return {
        ...shape,
        message: cause.code === "INTERNAL" ? "Internal server error" : cause.message,
        data: {
          ...shape.data,
          code: appErrorToTrpcCode(cause),
          appError: { code: cause.code, details: cause.details },
        },
      };
    }
    if (cause instanceof ZodError) {
      return {
        ...shape,
        message: "Invalid input",
        data: { ...shape.data, code: "BAD_REQUEST", zodIssues: cause.issues },
      };
    }
    return {
      ...shape,
      message:
        error.code === "INTERNAL_SERVER_ERROR" ? "Internal server error" : shape.message,
      data: { ...shape.data, stack: undefined },
    };
  },
});

export const router = t.router;
export const middleware = t.middleware;
export const procedure = t.procedure;
export const createCallerFactory = t.createCallerFactory;
```

---

## `lib/trpc/middleware/rate-limit.ts` (stub)

In-memory bucket — replace with Upstash before multi-region prod ([production-habits.md](production-habits.md)).

```typescript
import { RateLimitError } from "@/lib/errors";
import { middleware } from "../server";

const buckets = new Map<string, { count: number; resetAt: number }>();

export function rateLimit(options?: { capacity?: number; windowMs?: number }) {
  const capacity = options?.capacity ?? 120;
  const windowMs = options?.windowMs ?? 60_000;

  return middleware(async ({ ctx, next }) => {
    const key = ctx.requestId;
    const now = Date.now();
    let bucket = buckets.get(key);
    if (!bucket || now >= bucket.resetAt) {
      bucket = { count: 0, resetAt: now + windowMs };
      buckets.set(key, bucket);
    }
    bucket.count += 1;
    if (bucket.count > capacity) {
      throw new RateLimitError();
    }
    return next();
  });
}
```

---

## `lib/trpc/procedures.ts`

```typescript
import { TRPCError } from "@trpc/server";
import { procedure, middleware } from "./server";
import { rateLimit } from "./middleware/rate-limit";

const authMiddleware = middleware(async ({ ctx, next }) => {
  try {
    const user = await ctx.getUser();
    return next({ ctx: { ...ctx, user } });
  } catch {
    throw new TRPCError({ code: "UNAUTHORIZED", message: "Authentication required" });
  }
});

export const publicProcedure = procedure.use(rateLimit());
export const protectedProcedure = publicProcedure.use(authMiddleware);
```

For `api-first` without auth, omit `protectedProcedure` usage until Clerk is added.

---

## `lib/trpc/context.ts`

```typescript
import { randomUUID } from "node:crypto";

export interface TrpcContext {
  requestId: string;
  headers: Headers;
  getUser: () => Promise<{ id: string; email: string }>;
}

export type AuthedTrpcContext = TrpcContext & {
  user: Awaited<ReturnType<TrpcContext["getUser"]>>;
};

export async function createTrpcContext(opts: { req: Request }): Promise<TrpcContext> {
  const requestId =
    opts.req.headers.get("x-request-id") ??
    opts.req.headers.get("x-vercel-id") ??
    randomUUID();

  let cachedUser: Awaited<ReturnType<TrpcContext["getUser"]>> | null = null;

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

For no-auth scaffold, stub `getCurrentUser` to throw or return a dev user.

---

## Routers

`lib/trpc/routers/health.ts` — unchanged pattern from prior spoke.

`lib/trpc/routers/_app.ts` — merge `healthRouter`.

---

## `lib/trpc/client.tsx`

```tsx
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createTRPCClient, httpBatchLink } from "@trpc/client";
import { createTRPCContext } from "@trpc/tanstack-react-query";
import { useState, type ReactNode } from "react";
import superjson from "superjson";
import type { AppRouter } from "@/lib/trpc/routers/_app";

export const { TRPCProvider, useTRPC } = createTRPCContext<AppRouter>();

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { staleTime: 30_000, refetchOnWindowFocus: false },
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
    createTRPCClient<AppRouter>({
      links: [
        httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
          transformer: superjson,
        }),
      ],
    }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      <TRPCProvider trpcClient={trpcClient} queryClient={queryClient}>
        {children}
      </TRPCProvider>
    </QueryClientProvider>
  );
}
```

---

## `app/api/trpc/[trpc]/route.ts`

```typescript
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/lib/trpc/routers/_app";
import { createTrpcContext } from "@/lib/trpc/context";

const MAX_BODY_BYTES = 1024 * 1024;

async function handler(req: Request) {
  // TODO(production): reject cross-site mutations — validate Origin/Referer
  // when using cookie-based sessions. See production-habits.md.

  if (req.method === "POST") {
    const contentLength = Number(req.headers.get("content-length") ?? 0);
    if (contentLength > MAX_BODY_BYTES) {
      return Response.json({ error: "Request body too large" }, { status: 413 });
    }
  }

  const response = await fetchRequestHandler({
    endpoint: "/api/trpc",
    req,
    router: appRouter,
    createContext: () => createTrpcContext({ req }),
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

## Client demo (`useTRPC`)

```tsx
"use client";

import { useQuery } from "@tanstack/react-query";
import { useTRPC } from "@/lib/trpc/client";

export function HealthBadge() {
  const trpc = useTRPC();
  const { data, isLoading } = useQuery(trpc.health.check.queryOptions());
  if (isLoading) return <span>Checking…</span>;
  return (
    <span>
      API {data?.ok ? "ok" : "fail"} · DB {data?.db ? "ok" : "down"}
    </span>
  );
}
```

---

## RSC server caller (optional)

`lib/trpc/server-caller.ts` — `createCallerFactory(appRouter)` with manual context.

---

## Anti-patterns

- Raw `process.env` outside `lib/env.ts`
- `getDb()` in client components
- Copy-pasting auth in every procedure instead of `protectedProcedure`

Next: [auth-clerk-optional.md](auth-clerk-optional.md) or [verification-checklist.md](verification-checklist.md).
