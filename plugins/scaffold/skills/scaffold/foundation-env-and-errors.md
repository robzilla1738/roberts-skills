# Foundation — env and errors

> Phase 2b. Back to [SKILL.md](SKILL.md).

Typed configuration and domain errors are industry baseline for production Next.js apps. Keep this **minimal** — grow `lib/env.ts` as features ship.

**Rule:** Do not read `process.env` in `lib/` except inside `lib/env.ts`.

---

## `lib/env.ts`

```typescript
import { z } from "zod";

const optionalUrl = z.preprocess(
  (v) => (typeof v === "string" && v.trim() === "" ? undefined : v),
  z.string().url().optional(),
);

const serverSchema = z.object({
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
  DATABASE_URL: z.string().min(1).optional(),
  CLERK_SECRET_KEY: z.string().optional(),
});

const clientSchema = z.object({
  NEXT_PUBLIC_APP_URL: optionalUrl,
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z.string().optional(),
  NEXT_PUBLIC_CLERK_SIGN_IN_URL: z.string().default("/sign-in"),
  NEXT_PUBLIC_CLERK_SIGN_UP_URL: z.string().default("/sign-up"),
});

export type ServerEnv = z.infer<typeof serverSchema>;
export type ClientEnv = z.infer<typeof clientSchema>;

let cachedServer: ServerEnv | null = null;
let cachedClient: ClientEnv | null = null;

function parse<T>(schema: z.ZodType<T>, data: unknown, label: string): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    const msg = result.error.issues.map((i) => i.path.join(".") + ": " + i.message).join("; ");
    throw new Error(`Invalid ${label} environment: ${msg}`);
  }
  return result.data;
}

export function serverEnv(): ServerEnv {
  if (!cachedServer) {
    cachedServer = parse(serverSchema, process.env, "server");
  }
  return cachedServer;
}

export function clientEnv(): ClientEnv {
  if (!cachedClient) {
    cachedClient = parse(
      clientSchema,
      {
        NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
        NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY:
          process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
        NEXT_PUBLIC_CLERK_SIGN_IN_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL,
        NEXT_PUBLIC_CLERK_SIGN_UP_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL,
      },
      "client",
    );
  }
  return cachedClient;
}

/** Test helper */
export function resetEnvCacheForTesting() {
  cachedServer = null;
  cachedClient = null;
}
```

Use `serverEnv().DATABASE_URL` inside `getDb()` when you want validation at first DB access (optional in early scaffold).

---

## `lib/errors.ts`

```typescript
export type AppErrorCode =
  | "NOT_FOUND"
  | "FORBIDDEN"
  | "UNAUTHORIZED"
  | "VALIDATION"
  | "CONFLICT"
  | "RATE_LIMIT"
  | "EXTERNAL_SERVICE"
  | "INTERNAL";

const STATUS_FOR_CODE: Record<AppErrorCode, number> = {
  NOT_FOUND: 404,
  FORBIDDEN: 403,
  UNAUTHORIZED: 401,
  VALIDATION: 400,
  CONFLICT: 409,
  RATE_LIMIT: 429,
  EXTERNAL_SERVICE: 502,
  INTERNAL: 500,
};

export class AppError extends Error {
  readonly code: AppErrorCode;
  readonly httpStatus: number;
  readonly details?: Record<string, unknown>;

  constructor(
    code: AppErrorCode,
    message: string,
    options?: { details?: Record<string, unknown> },
  ) {
    super(message);
    this.name = "AppError";
    this.code = code;
    this.httpStatus = STATUS_FOR_CODE[code];
    this.details = options?.details;
  }
}

export class NotFoundError extends AppError {
  constructor(message = "Not found", details?: Record<string, unknown>) {
    super("NOT_FOUND", message, { details });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = "Unauthorized", details?: Record<string, unknown>) {
    super("UNAUTHORIZED", message, { details });
  }
}

export class ValidationError extends AppError {
  constructor(message = "Validation failed", details?: Record<string, unknown>) {
    super("VALIDATION", message, { details });
  }
}

export class RateLimitError extends AppError {
  constructor(message = "Too many requests") {
    super("RATE_LIMIT", message);
  }
}

export function isAppError(err: unknown): err is AppError {
  return err instanceof AppError;
}
```

Wire into tRPC in [trpc-and-query.md](trpc-and-query.md) `errorFormatter`.

---

## Exit criterion

- `lib/env.ts` and `lib/errors.ts` exist
- No other `lib/*` file reads `process.env` directly
- tRPC formatter maps `AppError` and `ZodError`

Next: [foundation-testing.md](foundation-testing.md).
