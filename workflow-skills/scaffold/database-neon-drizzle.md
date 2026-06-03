# Database — Neon + Drizzle

> Read when: Phase 4. Back to [SKILL.md](SKILL.md).

---

## Neon setup

1. Create project at [neon.tech](https://neon.tech).
2. Copy **pooled** connection string (recommended for serverless).
3. Set in `.env.local`:

```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

4. Add the same key to `.env.example` (empty value + comment).

---

## `drizzle.config.ts`

```typescript
import { config } from "dotenv";
config({ path: ".env.local" });
config({ path: ".env" });

import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql",
  schema: "./db/schema.ts",
  out: "./db/migrations",
  dbCredentials: {
    url: process.env.DATABASE_URL ?? "",
  },
  strict: true,
  verbose: true,
});
```

---

## `db/schema.ts` (minimal)

```typescript
import { pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").defaultRandom().primaryKey(),
  clerkId: text("clerk_id").unique(),
  email: text("email").notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
});
```

For `app-no-auth`, `clerkId` stays nullable until Clerk is added.

---

## `db/index.ts` — lazy singleton

Prevents `next build` from crashing when `DATABASE_URL` is unset at import time.

```typescript
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import * as schema from "./schema";

function getConnectionString(): string {
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error(
      "DATABASE_URL not set. Add your Neon connection string to .env.local.",
    );
  }
  return url;
}

let _db: ReturnType<typeof drizzle> | null = null;

export function getDb() {
  if (!_db) {
    const sql = neon(getConnectionString());
    _db = drizzle(sql, { schema });
  }
  return _db;
}

export const db = new Proxy({} as ReturnType<typeof drizzle>, {
  get(_target, prop) {
    return Reflect.get(getDb(), prop);
  },
});

export * from "./schema";
```

Use `getDb()` inside route handlers and tRPC context — not at module top level in shared imports.

---

## Migrations workflow

**Prototype / solo:**

```bash
pnpm db:push
```

**Team / production:**

```bash
pnpm db:generate   # creates SQL in db/migrations
# review SQL, commit
pnpm db:migrate    # add script: drizzle-kit migrate
```

Never edit applied migration files.

**Intake `push` vs `migrate`:**

| Workflow | Command | When |
|----------|---------|------|
| `push` | `pnpm db:push` | Solo prototype, fast iteration |
| `migrate` | `pnpm db:generate` then `pnpm db:migrate` | Team repos, production |

---

## Optional `db/relations.ts`

When tables reference each other, split relations from `schema.ts`:

```typescript
import { relations } from "drizzle-orm";
import { users } from "./schema";

export const usersRelations = relations(users, () => ({}));
```

Pass merged schema to `drizzle()` in `db/index.ts`: `{ ...schema, ...relations }`.

---

## Optional seed (dev)

`db/seed.ts` with `tsx`:

```typescript
import { getDb } from "./index";
import { users } from "./schema";

async function main() {
  const db = getDb();
  await db.insert(users).values({
    email: "dev@localhost",
    clerkId: null,
  }).onConflictDoNothing();
}

main().catch(console.error);
```

Add `"db:seed": "tsx db/seed.ts"` when using dev bypass auth.

---

## Health check query

Used by tRPC `health.check`:

```typescript
import { sql } from "drizzle-orm";

await getDb().execute(sql`SELECT 1`);
```

---

## Pitfalls

- Using unpooled URL on Vercel serverless — prefer Neon pooler.
- Importing `db` in client components — forbidden.
- Running `db:push` against production without review — use migrations for prod.

Next: [trpc-and-query.md](trpc-and-query.md).
