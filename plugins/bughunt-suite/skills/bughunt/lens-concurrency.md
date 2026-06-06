# Lens: Concurrency

**Hunts for:** bugs that appear only under specific interleavings of threads, tasks, or
async operations. The highest-yield, lowest-test-coverage lens — these rarely show in tests
and rarely reproduce on demand.

## Mental model

Assume the scheduler is adversarial: anything that *can* interleave *will*, at the worst
moment. Any state shared across concurrent actors without correct synchronization is a
suspect. Any "check then act" that isn't atomic is a suspect.

## Smells

**Data races**
- Shared mutable state (globals, singletons, fields, captured vars) read/written from
  multiple threads/tasks without a lock, atomic, or actor.
- Non-atomic compound updates (`count += 1`, `if not in map: map[k]=v`) under concurrency.
- A lock protecting writes but not reads (or vice versa); inconsistent lock discipline.
- Collections mutated while iterated from another thread.

**TOCTOU (time-of-check to time-of-use)**
- Check a condition, then act on it, with a gap where it can change: `exists()` then `open()`;
  `if balance >= amount` then `balance -= amount`; permission check then use.

**Ordering / atomicity**
- Assuming completion order of async tasks/callbacks/promises.
- Partial visibility: one field updated, dependent field not yet, observed in between.
- `await`/yield in the middle of an invariant-violating window.

**Deadlock / liveness**
- Locks acquired in inconsistent orders across call sites (lock-ordering deadlock).
- Holding a lock across an `await`, blocking call, or callback that may re-enter.
- Reentrancy: a callback/notification re-enters code that assumed it wasn't reentrant.

**Cancellation / shutdown**
- Cancelled tasks that leave state half-updated or resources held.
- Work continuing after shutdown; callbacks firing after the target is gone.

## How to trace

1. Identify every piece of state shared across concurrent actors in this area.
2. For each, list all access sites and the synchronization on each. Find an unsynchronized
   (or inconsistently synchronized) access.
3. For each check-then-act, ask what happens if the state changes in the gap.
4. For each lock, map acquisition order across sites; look for a cycle or an `await`/blocking
   call held under it.

## Evidence to capture

The shared state, the two (or more) concurrent paths that conflict, the interleaving that
breaks it (state X at line A, preempted, line B observes/overwrites), and the consequence.

## Common false positives to reject

- The state is confined to one thread/actor/queue (e.g. always on the main thread/`@MainActor`,
  serial queue) — no real concurrency.
- It's protected by an atomic, lock, or actor you initially missed.
- The value is immutable after publication (safe to share).
- The "race" window is closed by a happens-before guarantee (await on creation, memory fence).
