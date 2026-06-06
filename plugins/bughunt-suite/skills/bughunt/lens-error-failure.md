# Lens: Error & Failure Paths

**Hunts for:** what happens when things go wrong. The happy path gets tested; the failure
paths are where the real bugs and the real damage live.

## Mental model

Assume every fallible operation **will** fail at the worst moment — mid-write, after a
partial side effect, on retry, during cancellation. Ask: is the failure detected, handled
correctly, and does the system end in a consistent state?

## Smells

**Swallowed / mishandled errors**
- Empty `catch {}` / `except: pass` / `_ = try?` / ignored error return (`_, _ = f()`, Go
  `_ = err`); the error is dropped and execution continues as if it succeeded.
- Catch-log-continue when the operation's result was required.
- Catching too broad (swallowing programmer errors / cancellations).
- Returning a default/zero/empty on error that the caller can't distinguish from success.

**Fail-open vs fail-closed**
- Security/authorization check that, on error, defaults to *allow* instead of *deny*.
- Feature flag / config load failure that enables instead of disables.
- Validation that's skipped (not failed) when the validator errors.

**Partial failure / atomicity**
- Multi-step side effects with no rollback: step 1 commits, step 2 fails, state inconsistent.
- Write to two stores (DB + cache, DB + queue) without reconciliation on partial failure.
- Non-atomic file writes (truncate then write; crash leaves empty/corrupt file).

**Retry / timeout / cancellation**
- Retrying non-idempotent operations (duplicate side effects).
- No backoff/jitter → retry storms / thundering herd.
- Missing or unbounded timeouts (hang forever on a slow dependency).
- Retrying on non-retryable errors (4xx, validation); not retrying on transient ones.
- Cancellation that leaves resources held or state half-updated.

**Error-path resource leaks**
- The acquire/release lens's nemesis: cleanup that only runs on success (see
  [lens-state-lifecycle.md](lens-state-lifecycle.md)).

**Error information**
- Leaking stack traces / internal details to users (cross-ref [taint](lens-dataflow-taint.md)).
- Errors that lose the cause (no wrapping/context) making them undiagnosable.

## How to trace

1. List every fallible call in the area (I/O, network, parse, allocation, external).
2. For each, ask: is the error checked? On error, what state are we in, and is it consistent?
3. For security/critical checks, force the error branch and see if it fails open.
4. For multi-step mutations, ask what's left behind if step k fails.
5. For retries, check idempotency and termination (backoff, cap, timeout).

## Evidence to capture

The failing operation, how the failure is (mis)handled, the resulting inconsistent state or
wrong outcome, and the trigger (which dependency fails / which step crashes).

## Common false positives to reject

- The "ignored" error genuinely cannot occur or is truly irrelevant (state why).
- A transaction / `defer` rollback / idempotency key makes the partial failure safe.
- The default-on-error is intentional and safe (documented fail-open by design).
- An outer handler (middleware, supervisor) correctly handles what looks unhandled locally.
