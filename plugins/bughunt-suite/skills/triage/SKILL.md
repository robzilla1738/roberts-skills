---
name: triage
description: >
  Triage a suspected bug or a set of findings into a ranked, evidence-backed report:
  assign severity and confidence, build a minimal reproduction or failing test, and
  emit the standard finding schema (markdown + JSON). Use when the user invokes /triage,
  hands you a crash or suspicious behavior to assess, or when bughunt needs to score,
  prove, baseline-diff, and report findings.
disable-model-invocation: true
version: 2026-06-06.3
platforms: [language-agnostic]
primary_use_cases:
  - Turn a vague "something is wrong here" into a precise, reproducible finding
  - Assign severity x confidence to one or many candidate bugs (security and non-security)
  - Produce the canonical finding + report format that bughunt emits (markdown and JSON)
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

## Impact rubric (what "severity" *means* per finding class)

bughunt hunts more than security bugs. A finding's `impactClass` tells you which yardstick
to hold its severity against, so a pain-point or inefficiency isn't force-fit into a
security frame (and isn't dismissed because it isn't a CVE). Same four severity levels,
calibrated per class:

| impactClass | What Critical/High looks like here | What Low looks like |
|-------------|-----------------------------------|---------------------|
| **security** | auth bypass, RCE, secret/PII disclosure, injection on a reachable path | theoretical issue behind strong guards |
| **correctness** | wrong result users act on; silent data divergence | wrong only on a contrived edge |
| **reliability** | crash/hang/outage under normal load; fail-open | degrades only under rare conditions |
| **performance** | O(n²)/N+1/unbounded growth that breaks at real scale | constant-factor waste on a cold path |
| **data-integrity** | destructive/irreversible migration, corruption, lost writes | recoverable, narrow-window skew |
| **dx** | broken build/test, footgun that routinely costs dev hours | stale TODO, cosmetic friction |
| **ux** | user can't recover (white screen, silent failure, double-charge) | minor polish / missing affordance |
| **supply-chain** | known-vulnerable/typosquat dep on a reachable path | unpinned but low-risk dev dep |

Score by **user/operator/developer impact**, not by how clever the bug is. A High-severity
DX or UX finding is legitimate and belongs above a Low-severity security nit.

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

Each finding has two equivalent shapes: the **markdown block** below (what humans read) and
a **JSON object** (what the toolkit dedupes, fingerprints, baselines, and exports). They are
the same finding — `bughunt.py render` produces the markdown from the JSON, so you can author
either. The JSON contract lives at `bughunt/scripts/schema/finding.schema.json`; see
[the toolkit](../bughunt/tooling.md).

Emit each finding in this exact markdown shape so reports are scannable and mergeable:

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

**JSON ⇄ label mapping.** In JSON, `confidence` is a float `0.0–1.0`; the label you show is
derived (`≥0.85` → Confirmed, `≥0.5` → Probable, else Speculative). Set `impactClass` (see the
impact rubric) so non-security findings sort correctly. The mandatory verify pass records its
result in `verified.verdict` (`upheld`/`refuted`/`uncertain`); `bughunt.py merge` quarantines
`refuted` findings into a report appendix. You do not fingerprint, dedupe, or cluster by hand —
`merge` owns that, including collapsing the same bug seen by multiple lenses into one finding
with an `alsoFlaggedBy` list. See [verification.md](../bughunt/verification.md) and
[orchestration.md](../bughunt/orchestration.md).

## Report layout

This is the canonical report `bughunt` produces and what `/triage` emits for a set:

```markdown
# Bug report — <target> — <date>

## Summary
<N findings: X critical, Y high, Z medium, W low. K confirmed, ... One-line headline.>

## Baseline diff            <!-- only when a baseline exists; from `bughunt.py merge` -->
<N new, M fixed, K suppressed since the last baselined run. List the fixed ones.>

## Confirmed & Probable findings
<findings, sorted by severity then confidence, using the schema above>

## Speculative (needs a human eye)
<lower-confidence items, clearly separated>

## Refuted (appendix)       <!-- candidates the verify pass killed; transparency only -->
<title, location, and why it was refuted>

## Coverage & gaps
<what was hunted (lenses x areas), what was NOT examined and why>

## Recommended next step
<e.g. "fix BH-001/BH-003 then run /review (autoreview)">
```

`bughunt.py render` emits exactly this layout from the merged findings JSON (Baseline diff and
Refuted sections appear only when there's something to show). Single-bug `/triage` runs skip the
multi-finding sections and emit one finding plus its repro.

## Worked example

A filled-in finding (note the concrete evidence and the failing test as repro):

```markdown
### [High-Confirmed] IDOR: any user can read any invoice
- **ID:** BH-001
- **Location:** routes/invoices.js:42
- **Lens:** auth-access
- **Severity:** High
- **Confidence:** Confirmed
- **Trigger:** authenticated user requests GET /invoices/:id with another user's id
- **Trace:** route handler reads `req.params.id` (routes/invoices.js:42) → `Invoice.findById(id)`
  (db/invoices.js:18) → returns row with no `WHERE user_id = req.user.id` filter
- **Impact:** horizontal privilege escalation — full read of any customer's invoice data
- **Repro:** test "user A cannot read user B's invoice" — log in as A, GET /invoices/{B's id},
  expect 403/404, actual 200 with B's data (tests/invoices.idor.test.js)
- **Fix sketch:** scope the query to the caller (`WHERE id = ? AND user_id = ?`) or assert ownership
```

And a small report assembled from a hunt:

```markdown
# Bug report — billing-service — 2026-06-06

## Summary
3 findings: 0 critical, 2 high, 1 medium. 1 confirmed, 2 probable.
Headline: an IDOR exposes all invoices; discount math overcharges.

## Confirmed & Probable findings
### [High-Confirmed] IDOR: any user can read any invoice
... (as above) ...

### [High-Probable] Discount applied after tax → wrong total
- **ID:** BH-002 · **Location:** lib/pricing.js:67 · **Lens:** logic-correctness
- **Trigger:** any order with a discount code
- **Trace:** `applyTax()` runs before `applyDiscount()`; discount taken on the taxed amount
- **Impact:** customers overcharged; totals disagree with quoted price
- **Repro:** subtotal=100, tax=10%, discount=10% → expected 90.00, got 99.00
- **Fix sketch:** apply discount to subtotal before tax

### [Medium-Probable] N+1 query loading invoice line items
- **ID:** BH-003 · **Location:** db/invoices.js:55 · **Lens:** resource-performance
- **Trigger:** listing an invoice with many line items
- **Trace:** loops rows issuing one SELECT per line item instead of a join/batch
- **Impact:** latency grows linearly with line items; slow under load
- **Repro:** invoice with 200 items → 201 queries (query log)
- **Fix sketch:** single join or batched `IN (...)`

## Speculative (needs a human eye)
- None.

## Coverage & gaps
Hunted: auth-access, taint, logic-correctness, resource-performance over routes/invoices.js,
lib/pricing.js, db/invoices.js. Not examined: the admin console, background jobs.

## Recommended next step
Fix BH-001 and BH-002 first, then run `/review` (autoreview) before merging.
```

## Report-only by default

Triage **assesses and proves**; it does not edit product code (beyond writing a repro/test
when asked). To fix, hand off to the human or to the **autoreview** skill (`/review`).

## Related skills

- [bughunt](../bughunt/SKILL.md) — the orchestrator that feeds findings here
- [fuzz](../fuzz/SKILL.md) — generate a harness to turn a Probable finding into Confirmed
- the **autoreview** skill (`/review`) — the fix/quality gate after findings are accepted
- **verify** / `/verify` — drive the real app to reproduce a runtime-only bug
