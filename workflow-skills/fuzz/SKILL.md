---
name: fuzz
description: >
  Flush out hidden bugs dynamically by generating property-based tests, fuzz targets, or
  differential oracles, then shrinking failures into committed regression tests. Use when
  the user invokes /fuzz, wants to harden a function, or when bughunt needs to confirm a
  Probable finding at runtime.
disable-model-invocation: true
version: 2026-06-06.1
platforms: [language-agnostic]
primary_use_cases:
  - Harden a parser, encoder, state machine, or pure function against unexpected inputs
  - Turn a Probable static finding into a Confirmed one with an executable repro
  - Generate property-based tests around an invariant
  - Build a differential oracle between two implementations or old/new versions
---

# Fuzz & Property Harness

Static hunting finds *suspicious* code. This skill **proves** it — or finds what static
review missed — by **executing the code against generated inputs** and checking that
invariants hold. It's the dynamic counterpart to the [bughunt](../bughunt/SKILL.md) lenses.

Use it standalone to harden a function, or as the **confirm** step of a hunt: convert a
`Probable` finding into `Confirmed` with a failing test.

## Pick the technique

| Technique | Use when | What you need |
|-----------|----------|---------------|
| **Property-based testing** | A function has a stated property/invariant (round-trip, idempotence, ordering, bounds) | An oracle: a property that must always hold |
| **Fuzzing** | A surface parses/decodes untrusted or complex input and must never crash/hang | A target function + a "does not crash/leak/hang" oracle |
| **Differential testing** | Two implementations should agree (old vs new, fast vs reference, two libs) | Both impls + an equality oracle |
| **Metamorphic testing** | No oracle exists, but transformed inputs have predictable relations | A relation (e.g. `sort(reverse(x)) == sort(x)`) |

## Choosing the oracle (the hard part)

The bug-finding power is in the property, not the input generator. Good oracles:

- **Round-trip:** `decode(encode(x)) == x`; `parse(render(x)) == x`.
- **Invariants:** output always sorted; balance never negative; size within bounds.
- **Idempotence / commutativity:** `f(f(x)) == f(x)`; order independence.
- **Never-crash / never-hang:** no panics, no unhandled exceptions, terminates under a timeout.
- **Agreement:** matches a slow reference impl or the previous version (differential).
- **Conservation:** counts/sums preserved across a transform.

Seed the generator with the **boundary values** the numeric/boundaries lens cares about:
empty, single, max, negative, zero, NaN, huge, unicode, nested, duplicate.

## Per-ecosystem harness sketches

These are starting points — match the project's existing test runner and conventions.

- **Python** — `hypothesis` (`@given(strategies...)`); `atheris` for coverage-guided fuzzing.
- **JS/TS** — `fast-check` (`fc.assert(fc.property(...))`); `jazzer.js`/`jsfuzz` for fuzzing.
- **Go** — native `testing/quick` and `func FuzzXxx(f *testing.F)` with `go test -fuzz`.
- **Rust** — `proptest`/`quickcheck`; `cargo-fuzz` (libFuzzer) for `fuzz_target!`.
- **C/C++** — libFuzzer (`LLVMFuzzerTestOneInput`) or AFL++; run under ASan/UBSan.
- **Swift** — `SwiftCheck` for properties; libFuzzer via `-sanitize=fuzzer` for C-interop surfaces.
- **JVM** — `jqwik` for properties; `Jazzer` for coverage-guided fuzzing.

Run fuzzers under sanitizers (ASan/UBSan/TSan) where available — they turn silent
corruption into loud, locatable failures.

## From crash to regression test

1. **Reproduce** — capture the exact failing input.
2. **Shrink** — let the framework minimize it (or minimize by hand) to the smallest input
   that still fails. Most property frameworks shrink automatically.
3. **Pin it** — commit the minimized case as a normal, named regression test so it can
   never come back silently. Note the invariant it violated.
4. **Report** — hand the proven case back to [triage](../triage/SKILL.md) to record as
   `Confirmed`, with the failing test as the repro.

## Report-only by default

This skill writes **test/harness code**, not product fixes. It surfaces and proves defects;
fixing the underlying code is handed to the human or [autoreview](../autoreview/SKILL.md).
Don't leave throwaway fuzz scaffolding behind — keep the shrunk regression test, remove the
rest unless the user wants a permanent fuzz target.

## Related skills

- [bughunt](../bughunt/SKILL.md) — orchestrator; calls fuzz to confirm Probable findings
- [triage](../triage/SKILL.md) — records the proven crash as a Confirmed finding
- [autoreview](../autoreview/SKILL.md) — the fix/quality gate once the bug is proven
