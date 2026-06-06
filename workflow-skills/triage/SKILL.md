---
name: triage
description: >
  Triage a suspected bug or a set of findings into a ranked, evidence-backed report:
  assign severity and confidence, build a minimal reproduction or failing test, and
  emit a standard finding schema. Use when the user invokes /triage, hands you a crash
  or suspicious behavior to assess, or when bughunt needs to score and prove findings.
disable-model-invocation: true
version: 2026-06-06.1
platforms: [language-agnostic]
primary_use_cases:
  - Turn a vague "something is wrong here" into a precise, reproducible finding
  - Assign severity x confidence to one or many candidate bugs
  - Produce the canonical finding + report format that bughunt emits
  - Build a minimal repro or failing test that proves a defect
---

# Triage & Repro

Companion skill that converts raw suspicion into a **precise, ranked, evidence-backed
report**. It owns the **finding schema**, the **severity × confidence** model, and the
discipline of building a **minimal reproduction** before anything is called a bug.

Use it standalone on a single suspected bug, or as the scoring/reporting stage of
[bughunt](../bughunt/SKILL.md).

## First principle: evidence or it didn't happen

A finding is a claim that specific code does the wrong thing under a specific condition.
Every finding must carry:

- **Location** — `file:line` (the exact site, not "somewhere in this module").
- **Trace** — the data/control path from cause to effect.
- **Trigger** — the concrete condition or input that makes it fire.
- **Impact** — what actually goes wrong (crash, corruption, wrong result, leak, exposure).

If you cannot state all four, the item is a **question**, not a finding. Demote it or
investigate further. A short list of real bugs beats a long list of maybes — noise
destroys trust in the report.

## Severity rubric

Rate **impact if triggered**, independent of how likely it is.

| Severity | Meaning |
|----------|---------|
| **Critical** | Data loss/corruption, RCE, auth bypass, secret disclosure, crash on common path |
| **High** | Wrong result users rely on, privilege issue, leak/exhaustion under normal load, crash on a real edge |
| **Medium** | Incorrect behavior on an uncommon-but-reachable path; degraded reliability; recoverable |
| **Low** | Minor correctness/robustness issue, narrow edge, cosmetic-but-wrong |

## Confidence rubric

Rate **how sure you are it's real**, independent of severity.

| Confidence | Bar to clear |
|------------|--------------|
| **Confirmed** | Reproduced — a failing test, a runtime repro, or an unambiguous trace with no plausible guard |
| **Probable** | Strong static evidence; you traced it end to end but did not execute it |
| **Speculative** | Pattern looks wrong but a guard, invariant, or caller you can't see might save it |

**Speculative findings are quarantined** in their own section, never mixed with the rest.
When a defect is independently flagged by two different lenses, raise its confidence one
step (cross-validation).

## Building a minimal reproduction

For every Critical/High finding, try to produce proof, cheapest first:

1. **Failing unit/property test** — preferred; it's a regression guard the team can keep.
   Use the project's existing test runner and conventions.
2. **Runtime repro** — drive the real app/CLI to the failure. Hand off to the
   `verify` skill (`/verify`) when the bug only shows at runtime.
3. **Traced argument** — when neither is feasible (e.g. requires prod data), write the
   exact step-by-step trace with concrete values so a human can reproduce in minutes.

Minimize: strip the repro to the smallest input and fewest steps that still fail. Note
what you could *not* reproduce and why — never imply proof you don't have.

## Filtering false positives

Before reporting, attack your own finding:

- Is there a guard, early return, type constraint, or invariant upstream that prevents it?
- Is the "untrusted" input actually trusted/validated at the boundary?
- Does a test already cover this path passing?
- Is this intended behavior documented somewhere?

If the finding survives, report it. If it dies, drop it (or demote to Speculative with the
caveat stated).

## Finding schema

Emit each finding in this exact shape so reports are scannable and mergeable:

```markdown
### [SEV-CONF] <short title>
- **ID:** BH-001
- **Location:** path/to/file.ext:142
- **Lens:** concurrency            <!-- which discipline surfaced it -->
- **Severity:** High
- **Confidence:** Probable
- **Trigger:** <the condition/input that fires it>
- **Trace:** <cause -> ... -> effect, with file:line hops>
- **Impact:** <what goes wrong>
- **Repro:** <failing test / runtime steps / traced values, or "not reproduced: why">
- **Fix sketch:** <one or two lines; the direction, not a full patch>
```

`SEV-CONF` tag examples: `[Critical-Confirmed]`, `[High-Probable]`, `[Low-Speculative]`.

## Report layout

This is the canonical report `bughunt` produces and what `/triage` emits for a set:

```markdown
# Bug report — <target> — <date>

## Summary
<N findings: X critical, Y high, Z medium, W low. K confirmed, ... One-line headline.>

## Confirmed & Probable findings
<findings, sorted by severity then confidence, using the schema above>

## Speculative (needs a human eye)
<lower-confidence items, clearly separated>

## Coverage & gaps
<what was hunted (lenses x areas), what was NOT examined and why>

## Recommended next step
<e.g. "fix BH-001/BH-003 then run /review (autoreview)">
```

Single-bug `/triage` runs skip the multi-finding sections and emit one finding plus its repro.

## Report-only by default

Triage **assesses and proves**; it does not edit product code (beyond writing a repro/test
when asked). To fix, hand off to the human or to [autoreview](../autoreview/SKILL.md).

## Related skills

- [bughunt](../bughunt/SKILL.md) — the orchestrator that feeds findings here
- [fuzz](../fuzz/SKILL.md) — generate a harness to turn a Probable finding into Confirmed
- [autoreview](../autoreview/SKILL.md) — the fix/quality gate after findings are accepted
- **verify** / `/verify` — drive the real app to reproduce a runtime-only bug
