# Lens: Contract vs Implementation

**Hunts for:** places where the code does something other than what it **promises** —
in its docs, comments, types, tests, names, or callers' assumptions. These are bugs hiding in
plain sight because the surrounding signals say the code is correct.

## Mental model

Every function has a contract, even if unwritten: preconditions, postconditions, invariants.
Collect the *stated* contract from all available sources, then check the implementation
honors it. A mismatch is a bug in the code **or** the contract — both are findings.

## Sources of the contract

- **Docstrings / comments** — "returns null if not found", "caller must hold the lock",
  "assumes sorted input", "never negative".
- **Types & signatures** — non-null/optional, ranges, enums, units in names (`timeoutMs`).
- **Tests** — what the tests assert is the contract; what they *don't* cover is a gap.
- **Names** — `isEmpty`, `validate`, `getOrCreate`, `ensureX` imply behavior.
- **Callers** — how call sites use the return value reveals their assumptions.
- **Specs / schemas / API docs** — OpenAPI, protobuf, JSON schema, RFCs.

## Smells

- Comment says one thing, code does another ("// inclusive" but code is exclusive).
- Doc says "returns null on miss" but code throws (or vice versa) — callers handle the wrong one.
- A documented invariant ("list stays sorted", "balance >= 0") not maintained on some path.
- Stale comment describing old behavior after a refactor.
- Name lies: `validateX` that doesn't reject, `getOrCreate` that sometimes returns null,
  `isEnabled()` with a side effect.
- Units/semantics mismatch: seconds vs ms, 0- vs 1-indexed, bytes vs chars across a boundary.
- Two callers assuming contradictory behavior of the same function.
- **Copy-paste divergence:** code cloned then edited inconsistently — one copy fixed, the
  other not; wrong variable used after paste (`x` where `y` was meant).
- Dead or contradictory logic: a branch that can never be reached, or two checks that
  contradict (`if x > 10 ... else if x > 5` ordering swallowing a case).
- Tests that assert the buggy behavior (the test encodes the bug as "correct").
- Boolean/flag whose true/false meaning is inverted somewhere along the chain.

## How to trace

1. For the function/module under review, gather its contract from every source above.
2. Read the implementation and check each promised pre/postcondition and invariant holds on
   **all** paths.
3. Where sources disagree (comment vs code vs test vs caller), that disagreement is the
   finding — determine which is right by impact.
4. For cloned code, diff the copies line by line; divergences are prime suspects.

## Evidence to capture

The stated contract (quote the comment/type/test/caller), the implementation behavior that
violates it (file:line), the input that exposes the gap, and which side is wrong.

## Common false positives to reject

- The comment/doc is stale but the code is actually correct (still worth flagging as a doc
  fix, but Low severity).
- The "unreachable" branch is reachable via a path you missed.
- The contract is intentionally looser than the name suggests and callers handle it correctly.
- A test asserts behavior that is correct and you misread the intent.
