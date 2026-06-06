# Lens: State & Lifecycle

**Hunts for:** objects/resources used in an invalid state, leaked, double-released, or torn
down in the wrong order.

## Mental model

Every stateful thing has a **lifecycle**: created → initialized → used (through legal
transitions) → torn down. Bugs live in the transitions: a state reached that the code didn't
expect, a resource never released, or teardown racing use. Draw the implied state machine and
ask "what transition is missing or out of order?"

## Smells

**Resource leaks**
- Acquire without a guaranteed release on every path (incl. error/early-return/exception).
- Missing `finally`/`defer`/`with`/RAII/`using`; release only on the happy path.
- Listeners/observers/subscriptions/timers added but never removed.
- File handles, sockets, DB connections, locks held past their scope.

**Lifecycle / ordering**
- Use-before-init: a field read before its setup runs (lazy init, DI order, async init).
- Use-after-free / use-after-close / use-after-dispose.
- Double-free / double-close / double-release / double-dispose.
- Teardown that assumes init completed (init failed halfway → teardown crashes).
- Init order dependencies between modules/singletons (static init order).

**State-machine correctness**
- Operations valid only in certain states with no guard (e.g. `send()` before `connect()`).
- Missing transitions (no path out of an error state; stuck "loading").
- Idempotency: retried/duplicated operations that aren't safe to repeat (double-charge,
  double-insert, double-increment).
- Cache invalidation: stale entries after the source changes; cache and source diverge.
- Reset/cleanup that doesn't fully restore initial state (leftover flags).

## How to trace

1. Identify the resource or stateful object and its create/use/release sites.
2. Enumerate **all** exit paths from acquisition to release — especially error and early
   returns, exceptions, cancellations.
3. Check each path releases exactly once, and that no use occurs after release or before init.
4. For state machines, list legal states and the guards on each operation; find an operation
   reachable in an illegal state.

## Evidence to capture

The acquire site, the path that skips release (or the use in a bad state), the trigger that
takes that path, and the consequence (leak under load, crash, corruption, double-effect).

## Common false positives to reject

- A `defer`/`finally`/RAII guard does release on the path you suspected.
- The framework owns the lifecycle and guarantees teardown (e.g. request scope, DI container).
- The operation is genuinely idempotent (upsert, set-not-increment).
- A guard/state check upstream prevents the illegal transition.
