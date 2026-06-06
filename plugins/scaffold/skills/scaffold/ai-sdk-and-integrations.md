# AI SDK and product integrations

> Phase 9 implementation detail. Orchestration: [phase-integrations.md](phase-integrations.md). Back to [SKILL.md](SKILL.md).

Install and wire every add-on the user selects in intake — dependencies, env, routes, and demos. Phase 10 verification must pass before the skill is done.

---

## When to add what

| Need | Stack | Phase 9 section |
|------|--------|-----------------|
| Chat UI, streaming replies, tools | [Vercel AI SDK](https://ai-sdk.dev) (`ai`, `@ai-sdk/react`) | [AI SDK pattern](#ai-sdk-nextjs-pattern) |
| Unified models / fewer provider keys | [Vercel AI Gateway](https://vercel.com/docs/ai-gateway) | [Provider choice](#provider-choice) |
| Chat history in Postgres | Drizzle tables + `onFinish` | [Message persistence](#message-persistence) |
| Transactional email | Resend | [phase-integrations.md](phase-integrations.md#step-4--resend) |
| Subscriptions / usage billing | Stripe | [phase-integrations.md](phase-integrations.md#step-5--stripe) |
| Error monitoring | Sentry | [phase-integrations.md](phase-integrations.md#step-6--sentry) |
| Product analytics | PostHog | [phase-integrations.md](phase-integrations.md#step-7--posthog) |

---

## Architecture rules (non-negotiable for AI features)

1. **Streaming lives in Route Handlers** — `app/api/chat/route.ts` with `streamText` + `createUIMessageStreamResponse`. Do not stream LLM tokens through tRPC on day one.
2. **tRPC stays for CRUD** — threads list, settings, billing status, admin mutations.
3. **Secrets server-only** — model keys in `serverEnv()` only.
4. **Auth before generate** — Clerk `auth()` when profile uses auth; skip only when intake `auth: none`.
5. **Rate limit AI routes** — document Upstash in README; stub acceptable in scaffold.
6. **`maxDuration`** — `export const maxDuration = 30` on chat route.
7. **Build without keys** — `isAiConfigured()` → `503` with safe JSON; never throw at import time.

---

## Provider choice

| Approach | When | Env |
|----------|------|-----|
| **AI Gateway** (default on Vercel) | One key, many models | `AI_GATEWAY_API_KEY` |
| **Direct provider** | Local dev, single vendor | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` |

Set intake **AI provider** to pick default model strings in `lib/ai/models.ts`. Verify model IDs in [AI SDK docs](https://ai-sdk.dev) at scaffold time.

```bash
pnpm add ai @ai-sdk/react
```

---

## Env extensions (`lib/env.ts`)

Included in Phase 9 Step 1 — see [phase-integrations.md](phase-integrations.md#step-1--extend-libenvts-all-selected-add-ons-at-once).

---

## AI SDK — Next.js pattern

### File tree (additions)

```text
app/
  api/chat/route.ts
  app/chat/page.tsx
components/chat/Chat.tsx
lib/ai/models.ts
```

### Server — `app/api/chat/route.ts`

```typescript
import { auth } from "@clerk/nextjs/server";
import {
  convertToModelMessages,
  createUIMessageStreamResponse,
  streamText,
  toUIMessageStream,
  type UIMessage,
} from "ai";
import { isAiConfigured } from "@/lib/env";
import { resolveChatModel } from "@/lib/ai/models";

export const maxDuration = 30;

export async function POST(req: Request) {
  if (!isAiConfigured()) {
    return Response.json({ error: "AI not configured" }, { status: 503 });
  }

  const { userId } = await auth();
  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }

  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: resolveChatModel(),
    system: "You are a helpful assistant.",
    messages: await convertToModelMessages(messages),
  });

  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream }),
  });
}
```

For **`auth: none`** profiles, omit Clerk and document that the route must be protected before production (API key middleware or Vercel deployment protection).

**Tools / agents:** `tools` + `stopWhen: isStepCount(n)` on `streamText` when intake mentions agents.

### Client — `components/chat/Chat.tsx`

```tsx
"use client";

import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";

export function Chat() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: "/api/chat" }),
  });

  return (
    <div className="flex flex-col gap-4 max-w-lg">
      <ul className="space-y-2 min-h-[200px]">
        {messages.map((m) => (
          <li key={m.id}>
            <strong>{m.role}: </strong>
            {m.parts?.map((p, i) =>
              p.type === "text" ? <span key={i}>{p.text}</span> : null,
            )}
          </li>
        ))}
      </ul>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const input = e.currentTarget.elements.namedItem(
            "message",
          ) as HTMLInputElement;
          if (!input.value.trim()) return;
          sendMessage({ text: input.value });
          input.value = "";
        }}
      >
        <input name="message" className="border rounded px-2 py-1 w-full" />
        <button
          type="submit"
          disabled={status === "streaming"}
          className="mt-2 rounded bg-foreground text-background px-3 py-1 text-sm"
        >
          Send
        </button>
      </form>
    </div>
  );
}
```

---

## Message persistence

When intake **AI persistence** is `yes`:

- Add `chat_threads` / `chat_messages` in `db/schema.ts` ([phase-integrations.md](phase-integrations.md#persistence-ai--intake-persistence-yes))
- `pnpm db:generate` + migrate/push
- Save assistant + user messages in `streamText` `onFinish` when `userId` and DB are available

Reference: [AI SDK persistence example](https://github.com/vercel-labs/ai-sdk-persistence-db).

---

## Resend / Stripe / Sentry / PostHog

Implementation steps live in [phase-integrations.md](phase-integrations.md) Steps 4–7.

---

## Verification (Phase 10)

| # | Test | Expected |
|---|------|----------|
| A1 | POST `/api/chat` without session (Clerk app) | 401 |
| A2 | POST `/api/chat` without AI keys | 503 |
| A3 | Signed-in + keys → `/app/chat` | Streamed reply |
| R1 | `email.ping` tRPC | `{ configured: boolean }` |
| B1 | `billing.status` tRPC | `{ configured: boolean }` |

Re-run full [verification-checklist.md](verification-checklist.md) after Phase 9.

---

## Anti-patterns

| Avoid | Prefer |
|-------|--------|
| README-only add-ons when intake selected them | Phase 9 install + wire |
| `NEXT_PUBLIC_OPENAI_API_KEY` | `serverEnv()` |
| Streaming LLM via tRPC first | `app/api/chat/route.ts` |
| Throwing at import without API keys | `isAiConfigured()` guards |

---

## Related

- [phase-integrations.md](phase-integrations.md) — Phase 9 checklist
- [production-habits.md](production-habits.md) — CI, Playwright, Upstash (still post-launch)
- [foundation-env-and-errors.md](foundation-env-and-errors.md)
- [auth-clerk-optional.md](auth-clerk-optional.md)
