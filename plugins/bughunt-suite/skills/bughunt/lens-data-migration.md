# Lens: Data & Migration Safety

**Hunts for:** changes that can corrupt, lose, or desynchronize persistent data —
destructive or irreversible schema changes, unsafe backfills, schema/code skew
during a rollout, serialization drift across versions, and racing migrations.
These bugs don't manifest on the diff; they manifest on production data, often
irreversibly, during the deploy window.

## Mental model

For every migration and every change to how data is read or written, ask: **what
happens to the EXISTING rows, and to in-flight old-and-new code, during the
rollout window?** A migration is not a function of the schema alone — it runs
against live data while two versions of the app may be talking to the same store.
A bug exists whenever a change assumes an empty table, a single code version, a
short lock, or a re-run that never happens.

The defining property of this lens is *persistence across versions*: the damage
outlives the request, survives the rollback, and can't always be undone.

## Smells

**Destructive & irreversible**
- `DROP`/`DELETE`/`TRUNCATE`/rename with no backup and no reversible `down`
  migration — there's no path back if it's wrong.
- `ALTER` that rewrites or full-table-locks a large table on the hot path (adding
  an indexed column, changing a type) — blocks writes for the duration.
- Dropping/renaming a column while old code still reads it — the old version
  errors the moment the migration lands.

**Unsafe backfills**
- A backfill in one transaction over a whole table — long lock, statement timeout,
  replication lag; fails halfway with no progress saved.
- A backfill with no batching or resumability — can't be paused, retried, or
  continued from where it stopped.
- A default added to a huge table non-concurrently (a rewriting `ADD COLUMN ...
  DEFAULT` on engines that rewrite) — table-rewrite under lock.
- No idempotency — a re-run double-applies (double-increments, duplicate rows,
  re-sends) because there's no "already done" guard.

**Schema/code skew**
- Migration and the code depending on it shipped out of order — new code reads a
  column the migration hasn't added yet, or old code writes a column the migration
  already removed.
- `NOT NULL` (or a unique constraint) added without first handling existing
  `NULL`/duplicate rows — the migration fails or rejects valid old data.
- A change requiring an expand→migrate→contract sequence collapsed into one step.

**Serialization drift**
- An enum/JSON/protobuf/Avro shape changed without versioning so old persisted
  rows fail to deserialize (removed field, renamed key, tightened type).
- A date/number/encoding format change across versions (epoch vs ISO, string vs
  int id, charset) with no migration of stored values.
- A cache holding a stale serialized shape — old entries deserialize into the new
  code and crash or mis-map (ties [lens-state-lifecycle.md](lens-state-lifecycle.md)).

**Concurrency & ordering**
- Two migrations that can race (parallel deploy, multiple workers running
  migrations) with no advisory lock — see [lens-concurrency.md](lens-concurrency.md).
- A read-modify-write of shared rows during backfill with no row lock or
  optimistic-version check — lost updates.
- Eventual consistency assumed where a read-after-write is actually required (the
  new row isn't visible yet to the path that needs it).

## How to trace

1. Locate the migration files / ORM schema changes in the diff (e.g.
   `migrations/`, `schema.rb`, `alembic/`, `prisma/migrations/`).
2. Pair each migration with the application code that reads and writes the
   affected table/column/serialized shape — old version and new version both.
3. For each, walk the rollout window: before migrate, mid-migrate (mixed code),
   after migrate, and rollback — what does each see in existing rows?
4. Ask the three killers explicitly: is it reversible, is the backfill bounded and
   idempotent, and is the schema/code order safe under a partial deploy?

## Evidence to capture

The migration/change and the concrete data hazard: e.g. "`0042_drop_legacy.sql`
drops `users.legacy_id` but `UserSerializer` (deployed in the previous release)
still reads it → every read 500s during the window", or "backfill in
`backfill_totals.rb` runs one `UPDATE` over all rows in a transaction → lock +
statement timeout at ~2M rows, no resume". Name what happens to *existing* rows
and to *mixed-version* traffic, and whether it's reversible.

## Common false positives to reject

- A destructive change guarded by a tested, reversible `down` migration *and* a
  backup/snapshot step — state the guard.
- A migration on a table that is provably small and not on a hot path (state the
  size assumption).
- An expand/contract already split correctly across releases (the column is added
  in one deploy, read in the next) — verify the ordering.
- A backfill that *is* batched/resumable/idempotent via an existing helper.
- A serialization change behind an explicit version field with a tested fallback
  for old shapes.
- A migration framework that already takes an advisory lock and runs migrations
  single-flight.

## Cross-references

- [lens-state-lifecycle.md](lens-state-lifecycle.md) — boundary: **data-migration**
  is about *persistent* data across versions/rollouts; **state-lifecycle** about
  *in-process* resource/state and stale caches. A stale serialized cache entry
  touches both.
- [lens-boundaries-numeric.md](lens-boundaries-numeric.md) — null/empty/limit
  handling on *existing* rows a migration must survive.
- [lens-concurrency.md](lens-concurrency.md) — racing migrations and lost updates
  during backfill.
- [lens-error-failure.md](lens-error-failure.md) — partial writes and missing
  rollback when a migration fails mid-way.
- Confirm hazards on a copy of real data; score via [triage](../triage/SKILL.md) —
  data-integrity findings are frequently High/Critical.
