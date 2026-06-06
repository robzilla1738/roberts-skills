# Lens: Business-Logic Correctness

**Hunts for:** code that is **internally wrong** — it computes or decides the wrong thing even
with perfectly valid input and no failure. These bugs pass type checks, pass tests that
encode the same misunderstanding, and survive review because the code *looks* reasonable.

## Mental model

Ignore inputs, specs, and edge cases for a moment and ask the blunt question: **does this
code do the right thing?** Read the logic for what it *actually* says, pick a few concrete
values, run them through in your head, and compare the result to the obviously-intended
outcome. The gap is the bug.

## Smells

**Boolean & conditional logic**
- Inverted condition (a stray or missing `!`); negating a compound condition wrong (De Morgan:
  `!(a && b)` ≠ `!a && !b`).
- `&&` vs `||` swapped; mixing them without parens so precedence bites.
- Wrong comparison operator: `>` vs `>=`, `<` vs `>`, `==` vs `!=`.
- Assignment instead of comparison (`if (x = 5)`); truthiness used where an explicit check
  was meant.

**Branches & cases**
- Wrong or missing `default`/`else`; missing case in a switch; unintended fall-through.
- Ordered `if / else if` where an earlier branch swallows a case the later one meant to handle.
- A branch that can never be reached (dead logic), or two conditions that contradict.

**Calculations**
- Wrong formula; operator precedence error; sign error (`+`/`-` swapped).
- Unit mismatch in the math (mixing seconds and ms, cents and dollars).
- Percentage/discount/tax computed against the wrong base; rounding the wrong direction.
- Aggregation wrong: sum where average was meant, count including/excluding the wrong rows.

**The wrong thing referenced**
- **Copy-paste divergence:** a block cloned and edited inconsistently — uses `x` where `y`
  was meant, checks `start` twice instead of `start` and `end`, fixed in one copy not the other.
- Wrong field/property/index compared or returned; wrong enum/constant used (`Status.ACTIVE`
  vs `Status.ARCHIVED`).
- Off-by-one in a *business* threshold (free shipping at `>= 50` vs `> 50`).

**Flow**
- Early return / `continue` / `break` skipping work that must run.
- Wrong order of operations (validate after mutate; apply discount after tax when it should be
  before); an effect applied twice or not at all.
- A filter missing a negation (keeps what it should drop).

## How to trace

1. Read the block and state, in one sentence, what it's *supposed* to decide or compute.
2. Pick representative values plus the obvious boundaries; execute mentally; compare to intent.
3. For each conditional, ask: when is this true, and is that the set of cases I want?
4. For cloned/similar blocks, diff them line by line — divergences are prime suspects.

## Evidence to capture

The input(s), the wrong output vs the expected output, and the exact faulty expression
(`file:line`). Where possible, phrase it as a one-line failing assertion (`expected 50, got
55 when subtotal=50`) — that's the seed of a repro for [triage](../triage/SKILL.md).

## Common false positives to reject

- The behavior is intentional and correct, and you misread the intent — confirm against names,
  callers, and tests before reporting.
- A later step compensates (e.g. the value is re-normalized downstream).
- The "unreachable" branch is reachable via a path you missed.

## Cross-references

- [lens-contract-spec.md](lens-contract-spec.md) — checks code against its **stated** intent
  (docs/types/tests/names); this lens checks the logic **on its own terms** and against
  obvious intent, even when nothing is documented.
- [lens-boundaries-numeric.md](lens-boundaries-numeric.md) — numeric *edges*; this lens is the
  *rule itself* being wrong, not the boundary.
- Score and report via [triage](../triage/SKILL.md).
