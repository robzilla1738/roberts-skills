---
description: Flush out hidden bugs dynamically with property-based / fuzz / differential harnesses
---

Fuzz / property-test: **$ARGUMENTS**

Load and follow the **fuzz** skill at `${CLAUDE_PLUGIN_ROOT}/skills/fuzz/SKILL.md`:

- Pick the technique (property-based, fuzzing, differential, or metamorphic) for the target.
- Design the **oracle** (round-trip, invariant, never-crash, agreement) — this is where the power is.
- Use the project's existing test runner and the right per-ecosystem harness; run under sanitizers where available.
- On a failure: reproduce, **shrink** to the smallest input, and commit it as a named regression test.

Writes test/harness code, not product fixes. If $ARGUMENTS is empty, ask which function/surface to harden and what invariant should hold.
