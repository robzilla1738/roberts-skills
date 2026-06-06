# Lens: Resource & Performance

**Hunts for:** code that works fine in dev but degrades, exhausts resources, or falls over at
scale. These bugs are invisible on small data and a quiet machine — they surface as latency
spikes, out-of-memory crashes, and outages in production.

## Mental model

Ask the scaling question on every hot path: **what happens at 1000× the data, load, or
iterations?** and **what grows without bound?** Correctness isn't enough — code that is
correct but quadratic or unbounded is still a bug waiting for traffic.

## Smells

**Algorithmic complexity**
- Nested loops over the same/related inputs → O(n²) or worse.
- A linear scan inside a loop: membership test against a list/array in a loop (use a set/map);
  repeated `.find`/`.indexOf`/`includes` per item.
- String built by concatenation in a loop (quadratic copying) instead of a builder/buffer.
- Work that could be hoisted out of a loop recomputed each iteration; sorting inside a loop.

**Query efficiency (data layer)**
- **N+1 queries:** a query per row instead of a batch/join/`IN` (see also
  [platform-backend-cli.md](platform-backend-cli.md)).
- Fetch-everything-then-filter-in-memory instead of filtering in the query.
- Missing pagination/`LIMIT` → unbounded result sets; loading a full table.
- Query in a loop; lazy-load triggering hidden round trips.

**Unbounded growth**
- Caches/maps/lists/buffers that only ever grow — no eviction, TTL, or size cap.
- Accumulating state across requests (module/global scope) in a long-lived process.
- Recursion with no depth bound; queues/backlogs with no limit; log/metric cardinality blowups.

**Memory**
- Reading an entire file/HTTP response/upload into memory instead of streaming.
- Large allocations on a hot path; big temporary copies; boxing in tight loops.
- Holding references that prevent GC (listeners, closures, caches) — long-lived big objects.

**I/O & concurrency efficiency**
- Blocking I/O on an event-loop / UI / hot path.
- No connection pooling, or no cap on concurrency → resource exhaustion under load.
- Serial awaits that could be batched (`Promise.all`/`errgroup`); missing timeouts letting
  slow calls pile up (ties [lens-error-failure.md](lens-error-failure.md)).

**DoS amplification (attacker-driven load)**
- User-controlled sizes/counts driving allocation or work: huge `limit`/`pageSize`, deeply
  nested JSON, decompression bombs (zip/gzip), image/regex bombs.
- Catastrophic regex backtracking on untrusted input (ReDoS).
- Unbounded fan-out (one request spawning N downstream calls scaling with user input).

**Wasted work**
- Recomputation that should be memoized/cached; re-parsing/re-serializing repeatedly;
  re-establishing connections per call.

## How to trace

1. Identify the largest realistic input/data set and the highest realistic load.
2. Follow the hot path and characterize its cost: is it linear in input, or worse? What state
   does it accumulate across calls?
3. Find anything that grows without an explicit bound, or any per-item cost that multiplies.
4. For attacker-driven paths, check whether a small request can cause large work/allocation.

## Evidence to capture

The operation and its scaling behavior (e.g. "O(n²) over `items`", "grows unbounded with
request count", "one query per row"), the load/data that triggers degradation, and the
consequence (p99 latency, OOM, connection exhaustion, outage). A back-of-envelope ("at 10k
rows this is 100M comparisons") is strong evidence.

## Common false positives to reject

- The input is provably bounded small by an upstream limit/validation.
- The framework/driver handles pooling, batching, or paging and it's active here.
- The data set is tiny by design and will never grow (state the assumption).
- The "quadratic" loop runs over a constant-size collection.

## Cross-references

- [lens-state-lifecycle.md](lens-state-lifecycle.md) — resource **leaks** (acquire without
  release); this lens is about *scale/efficiency* of correct-but-costly code.
- [lens-error-failure.md](lens-error-failure.md) — retry storms and missing timeouts.
- [lens-dataflow-taint.md](lens-dataflow-taint.md) — attacker-controlled values; here they
  drive *cost* (ReDoS, decompression bombs) rather than injection.
- Confirm scaling experimentally with [fuzz](../fuzz/SKILL.md); score via [triage](../triage/SKILL.md).
