---
description: Flush out hidden bugs dynamically with property-based / fuzz / differential harnesses
---

Fuzz / property-test: **$ARGUMENTS**

Load and follow the **fuzz** skill at `${CLAUDE_PLUGIN_ROOT}/skills/fuzz/SKILL.md`:

- **Discover** the target — a named function/surface, or run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py census --functions` to shortlist fuzzable pure functions.
- Pick the technique (property-based, fuzzing, differential, or metamorphic) and design the **oracle** (round-trip, invariant, never-crash, agreement) — this is where the power is.
- Generate a harness in the project's existing test runner/library; **ask before installing** any new test dependency. Run under sanitizers where available.
- **Execute it.** On a failure: reproduce, **shrink** to the smallest input, keep or present it as a named regression test, and emit a findings entry marked `verified.verdict: upheld`. With no test infra, generate + present the harness clearly marked **not executed**.

Writes test/harness code, not product fixes. If $ARGUMENTS is empty, ask which function/surface to harden and what invariant should hold.
