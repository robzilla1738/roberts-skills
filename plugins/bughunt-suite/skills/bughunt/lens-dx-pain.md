# Lens: Developer-Experience Pain

**Hunts for:** friction that slows, misleads, or silently misinforms the
developers who maintain this code — aged debt, flaky tests, slow scripts, config
drift, and error surfaces that hide the cause. These don't crash production; they
tax every future change and erode trust in the codebase.

## Mental model

Ask of every piece of tooling, test, and diagnostic: **when this goes wrong, can
the next developer figure out why — fast — and is the path of least resistance
the correct one?** A bug in this lens is anything that makes a maintainer slower,
wronger, or more frustrated than the code's actual difficulty warrants: a comment
that lies, a test that fails for reasons unrelated to the change, an error that
names nothing, a setup step that no-ops.

This lens is about the *human* feedback loop, not runtime behavior. The defect is
real even when the program is correct — the cost is paid in developer-hours and
mistaken fixes.

## Smells

**Aged & abandoned debt**
- `TODO`/`FIXME`/`HACK`/`XXX`/`WTF` markers that are old per `git blame` —
  `bughunt.py signals` surfaces these with `ageDays` and `author`; anything months
  old that still gates real behavior is a finding, not a note.
- Commented-out code blocks left in place (dead alternatives, "old version
  below") — they rot, confuse diffs, and hide intent.
- "temporary", "for now", "quick fix", "will remove" that shipped and stayed;
  workarounds for a bug/version that no longer exists.
- A `FIXME` describing a known-broken edge case that no test or issue tracks.

**Flaky-test patterns**
- `sleep`/`setTimeout`/`Thread.sleep` fixed-duration waits instead of polling a
  condition with a timeout — passes on a fast machine, flakes on CI.
- Order-dependent tests sharing mutable state (module globals, a shared DB row, a
  singleton not reset between cases) — green only in a particular run order.
- Real network/clock/filesystem in a "unit" test: live HTTP calls, `Date.now()`/
  `time.time()` without a fake, real `fs` writes — slow and non-deterministic.
- Non-deterministic seeds (`Math.random`, unseeded `rand`, `uuid` in an assertion)
  flowing into an assertion; reliance on map/dict iteration order.

**Slow & serial scripts**
- npm/Make/CI scripts chaining many `&&` steps serially that are independent and
  could run in parallel (lint + typecheck + test fan-out).
- Build/test steps with no caching — full reinstall/rebuild every run, no
  cache key on lockfile, recompiling unchanged modules.
- O(n) shell loops that shell out per item (`for f in ...; do <spawn> $f; done`)
  instead of one batched invocation — process-spawn cost dominates.

**Config drift & onboarding traps**
- `.env.example` keys missing from the real config, or real config reading vars
  absent from `.env.example` — `bughunt.py signals` reports these under
  `configDrift`; a new clone won't run.
- Required env vars read with no default *and* no clear error
  (`process.env.X.foo`, `os.environ["X"]` deep in a path) — a missing var
  surfaces as a cryptic `undefined`/`KeyError` far from the cause.
- Setup steps that silently no-op when a precondition is unmet (a script that
  `exit 0`s on a missing tool, a guard that skips without warning).

**Unhelpful error surfaces**
- `catch`/`except` that logs `"Error"`, `"failed"`, or `e.message` alone — no
  operation name, no input id, no `cause`/stack — the dev gets no thread to pull.
- Errors swallowed entirely (`catch {}`, `except: pass`, `.catch(() => {})`) so a
  failing dev sees *nothing*; see [lens-error-failure.md](lens-error-failure.md).
- Generic messages that don't name the offending input/file/field ("invalid
  input", "something went wrong") when the value causing it is in hand.

## How to trace

1. Run `bughunt.py signals` and read `todos`, `flags`, `configDrift`, and
   `longScripts` — this is the pre-pass that points at the highest-density debt.
2. Open each cited `file:line` and read the surrounding code; confirm the marker
   still gates live behavior or the drift still breaks a fresh clone.
3. For tests, trace whether failure is deterministic: look for time/network/order
   coupling and whether a wait polls a condition or just sleeps.
4. For error surfaces, ask what a developer hitting this in CI/logs would actually
   see, and whether it names enough to locate the cause.

## Evidence to capture

The artifact and *who pays*: the `file:line`, the marker/`ageDays`/`author` (for
debt), or the specific drift (key present in X, missing in Y). For flaky tests,
the source of non-determinism (e.g. "1500ms `setTimeout`; CI runner is slower").
For error surfaces, the *missing* context (e.g. "logs `e.message` only — no
record id, no operation"). Impact is in developer-hours: "every onboarding hits
this", "this test flakes ~1/20 and blocks merges", "a missing `DATABASE_URL`
surfaces 4 frames deep as `undefined`".

## Common false positives to reject

- A `TODO` that is genuinely informational and gates nothing — a pointer, not a
  defect; state that it's inert.
- A "flaky-looking" wait that polls a real condition with a bounded timeout
  (that's correct, not a sleep-flake).
- Network/clock use in a test directory explicitly marked integration/e2e, where
  realism is the point.
- `.env.example` keys intentionally omitted because they're optional with a sane
  default (verify the default exists).
- An error message that *is* generic but is rethrown with full context one frame
  up where it's actually handled.
- A serial script whose steps have a real ordering dependency.

## Cross-references

- [lens-contract-spec.md](lens-contract-spec.md) — stale docs/comments that
  misdescribe behavior; here the lie is in *dev-facing debt markers and config*,
  there in the *contract* between caller and callee.
- [lens-error-failure.md](lens-error-failure.md) — swallowed/under-context errors.
  Boundary: **dx-pain** is about the *developer's* ability to diagnose;
  **error-failure** about whether the *system stays correct* at runtime. The same
  empty `catch {}` is a finding in both lenses for different reasons.
- [lens-product-ux.md](lens-product-ux.md) — the same swallow that hides an error
  from a developer often hides it from the end user too.
- Score and prioritize via [triage](../triage/SKILL.md); dx findings are usually
  Low/Medium severity but high frequency.
