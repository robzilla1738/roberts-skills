# Auth — Clerk (optional)

> Read when: Phase 6 (`full-app` with auth). Skip for `app-no-auth`. Back to [SKILL.md](SKILL.md).

Deep Clerk patterns live in the global **clerk-auth** skill — this spoke covers scaffold wiring only.

---

## Environment

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
```

Add to `.env.example` with comments. Never commit real keys.

---

## Sign-in / sign-up pages

`app/(auth)/sign-in/[[...sign-in]]/page.tsx`:

```tsx
import { SignIn } from "@clerk/nextjs";

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn />
    </div>
  );
}
```

`app/(auth)/sign-up/[[...sign-up]]/page.tsx` — same with `<SignUp />`.

---

## `app/layout.tsx`

```tsx
import { ClerkProvider } from "@clerk/nextjs";
import { TrpcProvider } from "@/components/providers/TrpcProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ClerkProvider>
          <TrpcProvider>{children}</TrpcProvider>
        </ClerkProvider>
      </body>
    </html>
  );
}
```

---

## `proxy.ts` (Next.js 16)

Clerk uses `proxy.ts` at the project root (not legacy `middleware.ts` only).

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher([
  "/app(.*)",
  "/api/trpc(.*)",
]);

export default clerkMiddleware(async (auth, request) => {
  if (isProtectedRoute(request)) {
    await auth.protect({
      unauthenticatedUrl: new URL("/sign-in", request.url).toString(),
    });
  }
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

Adjust protected routes if tRPC should allow anonymous `health.check` only — split matchers or use public procedures without `auth.protect` on the whole `/api/trpc` path (advanced: protect in procedure only).

**Scaffold default:** protect `/app` and `/api/trpc`; `health.check` is `publicProcedure` but still behind Clerk session on the route — for local dev without Clerk use `app-no-auth` or optional bypass below.

---

## `lib/auth/config.ts`

```typescript
export function isClerkConfigured(): boolean {
  return Boolean(
    process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY &&
      process.env.CLERK_SECRET_KEY,
  );
}

export function shouldUseSeededAuth(): boolean {
  return process.env.NODE_ENV === "development" && !isClerkConfigured();
}
```

---

## `lib/auth/current.ts` (minimal)

```typescript
import "server-only";
import { eq } from "drizzle-orm";
import { getDb, users } from "@/db";
import { isClerkConfigured, shouldUseSeededAuth } from "./config";

export async function getCurrentUser() {
  if (shouldUseSeededAuth()) {
    const rows = await getDb()
      .select()
      .from(users)
      .limit(1);
    const user = rows[0];
    if (!user) throw new Error("No dev user. Run db:seed or create a user row.");
    return user;
  }

  if (!isClerkConfigured()) {
    throw new Error("Clerk is not configured.");
  }

  const { auth, currentUser } = await import("@clerk/nextjs/server");
  const session = await auth();
  if (!session.userId) {
    throw new Error("Not signed in");
  }

  const clerkUser = await currentUser();
  const email =
    clerkUser?.primaryEmailAddress?.emailAddress ?? `${session.userId}@clerk.local`;

  const db = getDb();
  const existing = await db
    .select()
    .from(users)
    .where(eq(users.clerkId, session.userId))
    .limit(1);

  if (existing[0]) return existing[0];

  const inserted = await db
    .insert(users)
    .values({
      clerkId: session.userId,
      email,
    })
    .returning();

  return inserted[0]!;
}
```

Prefer webhook sync for production; inline upsert is acceptable for scaffold.

---

## Webhook — `app/api/webhooks/clerk/route.ts`

```typescript
import { headers } from "next/headers";
import { Webhook } from "svix";
import type { WebhookEvent } from "@clerk/nextjs/server";
import { eq } from "drizzle-orm";
import { getDb, users } from "@/db";

export async function POST(req: Request) {
  const secret = process.env.CLERK_WEBHOOK_SECRET;
  if (!secret) {
    return new Response("Webhook secret not configured", { status: 500 });
  }

  const payload = await req.text();
  const headerPayload = await headers();
  const wh = new Webhook(secret);

  let event: WebhookEvent;
  try {
    event = wh.verify(payload, {
      "svix-id": headerPayload.get("svix-id")!,
      "svix-timestamp": headerPayload.get("svix-timestamp")!,
      "svix-signature": headerPayload.get("svix-signature")!,
    }) as WebhookEvent;
  } catch {
    return new Response("Invalid signature", { status: 400 });
  }

  const db = getDb();

  if (event.type === "user.created" || event.type === "user.updated") {
    const { id, email_addresses } = event.data;
    const email = email_addresses[0]?.email_address;
    if (!email) return new Response("No email", { status: 400 });

    await db
      .insert(users)
      .values({ clerkId: id, email })
      .onConflictDoUpdate({
        target: users.clerkId,
        set: { email, updatedAt: new Date() },
      });
  }

  return new Response("OK", { status: 200 });
}
```

Install: `pnpm add svix`. Set `CLERK_WEBHOOK_SECRET` in Vercel. Register endpoint in Clerk Dashboard.

---

## Dev bypass (optional)

When `shouldUseSeededAuth()` is true:

1. Leave Clerk env vars empty.
2. Seed one `users` row.
3. `getCurrentUser()` returns that row without Clerk.

Do not enable in production.

---

## Pitfalls

- Using `middleware.ts` only on Next 16 without `proxy.ts` — follow Clerk’s latest App Router guide.
- Protecting `/api/trpc` while testing anonymous health — use `app-no-auth` or narrow matcher.
- Missing webhook idempotency — use `onConflictDoUpdate`.

See **clerk-auth** skill for organizations, MFA, and advanced middleware.
