# Foundation — testing

> Phase 2c. Back to [SKILL.md](SKILL.md).

Vitest is the default unit/integration test runner for Vite-compatible Next apps. **Playwright** is deferred to [production-habits.md](production-habits.md).

---

## Install

```bash
pnpm add -D vitest @vitejs/plugin-react
```

For API-only tests, `@vitejs/plugin-react` is optional but harmless.

---

## `vitest.config.ts`

```typescript
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    exclude: ["tests/e2e/**", "node_modules/**", ".next/**"],
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL(".", import.meta.url)),
    },
  },
});
```

---

## Scripts (`package.json`)

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run"
  }
}
```

---

## Sample test — `tests/errors.test.ts`

```typescript
import { describe, expect, it } from "vitest";
import { AppError, isAppError, UnauthorizedError } from "@/lib/errors";

describe("AppError", () => {
  it("maps unauthorized to 401", () => {
    const err = new UnauthorizedError();
    expect(err.httpStatus).toBe(401);
    expect(isAppError(err)).toBe(true);
  });

  it("does not treat generic Error as AppError", () => {
    expect(isAppError(new Error("nope"))).toBe(false);
  });
});
```

Add router or rate-limit tests when those modules exist.

---

## Exit criterion

- `pnpm test:run` passes with at least one test

Next: [foundation-ui.md](foundation-ui.md) (if profile includes UI kit) or Phase 4 database.
