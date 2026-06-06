# Verify — the mandatory skeptic pass

Every candidate finding is **GUILTY of being a false positive** until a skeptic genuinely
tries — and fails — to kill it. Verify is not an optional polish step; it is the phase that
turns a *candidate* into a *finding*. It runs on **every rung** of the capability ladder
(see [orchestration.md](orchestration.md)) and is **never skipped** — not in quick mode, not
in deep mode, not when the hunter sounds confident.

Hunting optimizes for recall (find everything that *might* be wrong). Verify restores
precision (keep only what survives a hostile read). The two phases pull in opposite
directions on purpose; that tension is where the signal comes from.

## The four refutation questions

The skeptic must **genuinely attempt each one** by reading the cited code, not pattern-match
the title. A finding is killed the moment any single question lands. Read the surrounding
code, the callers, the types, and the tests before answering.

1. **Upstream guard** — Is there a validation, early return, type constraint, assertion, or
   invariant *before* this code that prevents the trigger from ever reaching it? Trace
   backward from the cited line to every caller. If the dangerous value can't arrive in the
   claimed shape, the finding is dead.

2. **Trusted input** — Is the "untrusted" value actually validated, sanitized, or otherwise
   trusted at the boundary it crosses? A value tainted three frames up may be parsed,
   range-checked, or escaped before it reaches the sink. Confirm the taint actually survives
   the whole path, not just that it *starts* untrusted.

3. **Covering test** — Does an existing test already exercise this exact path and pass?
   **Find it and read it.** If a test drives the same input down the same branch and asserts
   the correct outcome, either the bug isn't real or the test is asserting the bug as
   intended behavior — both are reasons to refute or downgrade. Don't take "there's probably
   a test" on faith; locate it.

4. **Documented intent** — Is this behavior intentional and documented somewhere — a comment
   on the line, an ADR, a type that encodes the constraint, a docstring, a `// SAFETY:` note,
   a test named for the edge case? Surprising-but-intended is not a bug.

If all four questions fail to kill it, the finding is **upheld**. If any one lands cleanly,
it is **refuted**. If the skeptic can neither confirm the bug nor land a refutation (e.g. the
trigger path is plausible but unproven, or the relevant guard is in code the skeptic can't
read), the verdict is **uncertain**.

## Verdict contract

The skeptic returns exactly this JSON object (it becomes the finding's `verified` field, per
[finding.schema.json](scripts/schema/finding.schema.json)):

```json
{
  "by": "skeptic-pass",
  "method": "static-refutation",
  "verdict": "upheld",
  "note": "one line: which question(s) you tried and what you found"
}
```

- `by` — always `"skeptic-pass"` for this phase (other verifiers — `fuzz`, `runtime-repro` —
  may write the field too).
- `method` — `"static-refutation"` (read the code), `"failing-test"` (you wrote/ran a test
  that fails on the bug), or `"runtime-repro"` (you reproduced it live). Most skeptic passes
  are `"static-refutation"`.
- `verdict` — one of `upheld` | `refuted` | `uncertain`.
- `note` — a single line naming which refutation question(s) you tried and what you saw. This
  is the audit trail; write it so a human can re-check your reasoning fast.

**Default to `refuted` when a refutation succeeds.** Use `uncertain` when you can neither
confirm the bug nor land a kill. Reserve `upheld` for findings where **all four questions
failed to kill it**. Bias toward refuted on genuine doubt — a missed real bug costs a human
one re-read; a false positive that ships erodes trust in the whole report.

## Where refuted and uncertain findings go

`bughunt.py merge` reads the `verified` verdict and routes each finding:

- **`refuted`** → moved to a **refuted appendix** in the report (kept for transparency, so a
  human can see what was considered and dismissed) and **excluded from the report body and
  the CI gate**. Merge already quarantines these — the agent's only job is to attach an
  honest verdict.
- **`uncertain`** → **stays in the report body**, but its confidence is **capped at
  Speculative** (it lands in the "needs a human eye" section, never in the ranked
  Confirmed/Probable list). A finding that survived hunting but couldn't be confirmed is a
  lead, not a result.
- **`upheld`** → flows through normally; its confidence is whatever the hunter assigned
  (and may be boosted by cross-validation — see below).

The agent does not hand-sort these; it attaches the verdict JSON to each finding and pipes
the lot to `merge`, which owns the routing.

## The SKEPTIC prompt template

Other rungs paste this block to dispatch a verifier (Rung B: one skeptic Task per surviving
finding; Rung C: inline after each cell; Rung A: the Workflow `Verify` phase). Substitute the
finding JSON for `{{FINDING}}` and the absolute lens spoke path for `{{LENS_PATH}}`.

```text
You are a SKEPTIC. Your job is to REFUTE this finding, not to confirm it. Assume it is a
false positive and try to prove it wrong.

FINDING:
{{FINDING}}

Read the cited code (location.file + the lines around location.startLine..endLine, plus its
callers and the relevant tests) and read the lens discipline at:
{{LENS_PATH}}

Genuinely attempt all four refutation questions — read code, do not guess:
  1. Upstream guard  — is there a validation / early return / type constraint / invariant
     BEFORE this code that prevents the trigger from ever arriving?
  2. Trusted input   — is the "untrusted" value actually validated or trusted at the
     boundary it crosses, before it reaches the sink?
  3. Covering test   — does an existing test exercise this exact path and pass? FIND it and
     READ it before answering.
  4. Documented intent — is this behavior intentional and documented (comment, ADR, type,
     test name)?

A finding raised independently by two DIFFERENT lenses (it will be tagged "cross-validated"
by merge) is stronger signal — weigh that against an easy refutation.

Return ONLY this JSON object, nothing else:
{"by":"skeptic-pass","method":"static-refutation","verdict":"upheld|refuted|uncertain",
 "note":"which question(s) you tried and what you found"}

Rules:
- Default to "refuted" when a refutation lands. Use "uncertain" when you can neither confirm
  the bug nor kill it. Reserve "upheld" for when ALL FOUR questions fail to kill it.
- Bias toward "refuted" on genuine doubt. A short list of real bugs beats a long list of
  maybes.
```

## Cross-validation is evidence

A finding independently raised by **two different lenses** over overlapping code is a strong
signal that it is real — convergence from disciplines that don't share assumptions is hard to
fake. `merge` detects this overlap, tags both findings `cross-validated`, and boosts their
confidence. A skeptic verifying a cross-validated finding should weigh that convergence
against an easy refutation: it raises the bar for landing a clean kill, though it does not
make the finding immune — a real upstream guard still refutes it.
