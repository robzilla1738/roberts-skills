# Phase 9 — Integrations (intake add-ons)

> Run after Phase 8, **before** Phase 10 verify. Back to [SKILL.md](SKILL.md).

**Skip this phase** only when intake add-ons are exactly `none`.

When the user selects add-ons in intake, **install dependencies, extend env, add typed stubs/routes, and wire demos** in this phase. Do not defer to README-only. The scaffold is not complete until Phase 10 passes with every selected add-on represented in code.

---

## Add-on matrix

| Add-on ID | Packages (verify on npm) | Files to add / update |
|-----------|--------------------------|------------------------|
| `ai-sdk` | `ai`, `@ai-sdk/react` | `lib/ai/*`, `app/api/chat/route.ts`, `components/chat/*`, `app/app/chat/page.tsx`, optional `db` chat tables |
| `resend` | `resend` | `lib/resend.ts`, `lib/trpc/routers/email.ts` (health/send stub) |
| `stripe` | `stripe` | `lib/stripe.ts`, `app/api/webhooks/stripe/route.ts` |
| `sentry` | `@sentry/nextjs` | `instrumentation.ts`, `sentry.*.config.ts`, `next.config` wrap |
| `posthog` | `posthog-js` | `lib/posthog.ts`, `components/providers/PostHogProvider.tsx`, root layout |

Deep AI patterns: [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md).

---

## Intake fields used here

| Field | Values | Effect |
|-------|--------|--------|
| Add-ons (#8) | comma-separated IDs | Which rows in the matrix run |
| AI provider (#9) | `gateway` \| `openai` \| `anthropic` | `lib/ai/models.ts` default model string |
| AI persistence (#10) | `yes` \| `no` | Drizzle `chat_threads` / `chat_messages` when `yes` |
| Auth (#3) | `clerk` \| `none` | Chat route auth vs open (api-first only) |

Defaults when user does not specify: `gateway`, persistence `no` for `api-first`, `yes` for `saas-dashboard` + `ai-sdk`.

---

## Step 1 — Extend `lib/env.ts` (all selected add-ons at once)

Merge into **server** schema (all optional — build must pass without secrets):

```typescript
// AI
OPENAI_API_KEY: z.string().min(1).optional(),
ANTHROPIC_API_KEY: z.string().min(1).optional(),
AI_GATEWAY_API_KEY: z.string().min(1).optional(),
// Email
RESEND_API_KEY: z.string().min(1).optional(),
RESEND_FROM_EMAIL: z.string().email().optional(),
// Stripe
STRIPE_SECRET_KEY: z.string().min(1).optional(),
STRIPE_WEBHOOK_SECRET: z.string().min(1).optional(),
// Sentry
SENTRY_DSN: z.string().url().optional(),
// PostHog — server
POSTHOG_API_KEY: z.string().min(1).optional(),
```

Merge into **client** schema when needed:

```typescript
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().optional(),
NEXT_PUBLIC_POSTHOG_KEY: z.string().optional(),
NEXT_PUBLIC_POSTHOG_HOST: z.string().url().optional(),
```

Add helpers:

```typescript
export function isAiConfigured(env: ServerEnv = serverEnv()) {
  return !!(env.AI_GATEWAY_API_KEY || env.OPENAI_API_KEY || env.ANTHROPIC_API_KEY);
}
export function isResendConfigured(env: ServerEnv = serverEnv()) {
  return !!env.RESEND_API_KEY;
}
export function isStripeConfigured(env: ServerEnv = serverEnv()) {
  return !!env.STRIPE_SECRET_KEY;
}
```

Sync **`.env.example`** in the same commit — see [vercel-and-env.md](vercel-and-env.md).

---

## Step 2 — Install dependencies

One install pass (adjust list to selected add-ons):

```bash
pnpm add ai @ai-sdk/react
pnpm add resend
pnpm add stripe
pnpm add @sentry/nextjs
pnpm add posthog-js
```

Run from project root after Phase 8. Re-run `pnpm install` before Phase 10.

---

## Step 3 — `ai-sdk`

### `lib/ai/models.ts`

```typescript
import { serverEnv } from "@/lib/env";

export type AiProviderPreference = "gateway" | "openai" | "anthropic";

export function defaultChatModel(preference: AiProviderPreference = "gateway") {
  switch (preference) {
    case "openai":
      return "openai/gpt-4o";
    case "anthropic":
      return "anthropic/claude-sonnet-4-20250514";
    default:
      return "openai/gpt-4o"; // AI Gateway model id — verify in AI SDK docs
  }
}

export function resolveChatModel(preference: AiProviderPreference) {
  const env = serverEnv();
  if (env.AI_GATEWAY_API_KEY) return defaultChatModel("gateway");
  if (env.OPENAI_API_KEY) return defaultChatModel("openai");
  if (env.ANTHROPIC_API_KEY) return defaultChatModel("anthropic");
  return defaultChatModel(preference);
}
```

Pass `preference` from intake into this module (constant in file or env `AI_PROVIDER=gateway`).

### `app/api/chat/route.ts`

- `export const maxDuration = 30`
- If `!isAiConfigured()` → `503` JSON `{ error: "AI not configured" }` (build still passes)
- If auth profile uses Clerk → `auth()`; require `userId` unless intake `auth: none`
- `streamText` + `createUIMessageStreamResponse` + `toUIMessageStream`

See [ai-sdk-and-integrations.md](ai-sdk-and-integrations.md#server-appapichatroutets) for full handler template.

### `components/chat/Chat.tsx`

Working minimal UI: message list, input, submit via `useChat` + `DefaultChatTransport({ api: "/api/chat" })`. Show inline notice when AI env keys are missing (client can infer from failed 503 or pass `aiConfigured` from server component).

### `app/app/chat/page.tsx`

Render `<Chat />` inside protected shell. Link from `app/app/page.tsx`.

### Persistence (`ai` + intake persistence `yes`)

Add to `db/schema.ts`:

```typescript
export const chatThreads = pgTable("chat_threads", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: text("user_id").notNull(),
  title: text("title"),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

export const chatMessages = pgTable("chat_messages", {
  id: uuid("id").defaultRandom().primaryKey(),
  threadId: uuid("thread_id")
    .notNull()
    .references(() => chatThreads.id, { onDelete: "cascade" }),
  role: text("role").notNull(), // user | assistant | system
  content: text("content").notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});
```

Run `pnpm db:generate` + migrate/push per intake. Persist in `streamText` `onFinish` when DB + keys are available.

---

## Step 4 — `resend`

### `lib/resend.ts`

```typescript
import { Resend } from "resend";
import { isResendConfigured, serverEnv } from "@/lib/env";

export function getResend() {
  const key = serverEnv().RESEND_API_KEY;
  if (!key) throw new Error("RESEND_API_KEY not configured");
  return new Resend(key);
}

export async function sendEmailSafe(params: {
  to: string;
  subject: string;
  html: string;
}) {
  if (!isResendConfigured()) {
    return { ok: false as const, reason: "not_configured" };
  }
  const from = serverEnv().RESEND_FROM_EMAIL ?? "onboarding@resend.dev";
  await getResend().emails.send({ from, ...params });
  return { ok: true as const };
}
```

### tRPC `email.ping` (public or protected)

Returns `{ configured: boolean }` — proves wiring without sending mail in CI.

---

## Step 5 — `stripe`

### `lib/stripe.ts`

```typescript
import Stripe from "stripe";
import { isStripeConfigured, serverEnv } from "@/lib/env";

let client: Stripe | null = null;

export function getStripe() {
  if (!client) {
    const key = serverEnv().STRIPE_SECRET_KEY;
    if (!key) throw new Error("STRIPE_SECRET_KEY not configured");
    client = new Stripe(key, { apiVersion: "2025-02-24.acacia" });
  }
  return client;
}

export function isStripeReady() {
  return isStripeConfigured();
}
```

Verify `apiVersion` against [Stripe API changelog](https://stripe.com/docs/api/versioning) at scaffold time.

### `app/api/webhooks/stripe/route.ts`

- Read raw body
- `stripe.webhooks.constructEvent` with `STRIPE_WEBHOOK_SECRET`
- Return `400` on bad signature; `200` on success
- Stub comment for `checkout.session.completed` handler

### tRPC `billing.status`

Returns `{ configured: boolean }`.

---

## Step 6 — `sentry`

Follow current [@sentry/nextjs](https://docs.sentry.io/platforms/javascript/guides/nextjs/) App Router setup:

1. `sentry.client.config.ts` / `sentry.server.config.ts` — init only when `SENTRY_DSN` is set
2. `instrumentation.ts` — `register()` + `onRequestError` export
3. Wrap `next.config` with `withSentryConfig` when DSN present (or always wrap with empty DSN guard)

Build **must** pass with `SENTRY_DSN` unset.

---

## Step 7 — `posthog`

### `lib/posthog.ts`

Server singleton using `posthog-js` for browser; for server capture use `PostHog` from `posthog-node` if you add it, or client-only for scaffold.

### `components/providers/PostHogProvider.tsx`

Init `posthog` only when `NEXT_PUBLIC_POSTHOG_KEY` is set. Wrap in `app/layout.tsx` inside `TrpcProvider`.

---

## Step 8 — Merge routers and layout

- `_app.ts` — merge `emailRouter`, `billingRouter` if created
- `app/layout.tsx` — `PostHogProvider` when `posthog` selected
- README **Integrations** section — list installed add-ons + env keys required for each to activate

---

## Phase exit criterion

- [ ] Every intake add-on has installed package(s) in `package.json`
- [ ] `lib/env.ts` + `.env.example` include all keys for selected add-ons
- [ ] `pnpm typecheck`, `pnpm lint`, `pnpm test:run`, `pnpm build` pass (Phase 10 re-runs)
- [ ] Demos: `/app/chat` (ai-sdk), tRPC pings (resend/stripe), providers (posthog/sentry) wired
- [ ] No product business logic beyond integration **stubs/demos**

Next: [verification-checklist.md](verification-checklist.md) (Phase 10).
