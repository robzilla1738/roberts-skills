---
name: bughunt
description: >
  Adversarial whole-codebase hunter for bugs, pain points, and inefficiencies on any project
  type (iOS, macOS, web, services, terminal tools). A zero-dependency toolkit ranks hotspots,
  then parallel hunters sweep a grid of 13 analysis lenses x risk hotspots; a mandatory skeptic
  pass refutes false positives; findings are fingerprinted, deduped, baseline-diffed, and
  rendered to markdown/HTML/SARIF with CI exit codes. Report-only by default. Use when the user
  invokes /bughunt, asks to find hidden bugs, audit code for defects, hunt pain points or
  inefficiencies, do a deep code review, gate CI on findings, or hunt for what tests miss.
disable-model-invocation: true
version: 2026-06-06.4
platforms: [language-agnostic, Apple, Web, Systems, Backend, CLI, Android, .NET, PHP, SQL, IaC]
primary_use_cases:
  - Hunt an entire codebase for hidden defects, not just the current diff
  - Surface pain points and inefficiencies — perf, DX friction, UX gaps, supply-chain, data risk
  - Deep adversarial code review of a module, feature, or risky change
  - Produce a ranked, evidence-backed, reproducible report; baseline-diff and gate CI on it
---

# Bughunt

An **offensive, whole-codebase bug hunter**. Where the **autoreview** skill (`/review`) is a
defensive gate on *your own diff*, bughunt assumes the code is **guilty** and goes looking
for hidden defects across the whole target — on any platform.

Read this hub first, run **recon**, then open only the spokes your hunt plan selects.

## Mission

Find the bugs that tests, linters, and a tired reviewer miss — and **prove** them. The
output is a ranked, evidence-backed report, not a vibe. Default behavior is **report-only**:
hunt, document, hand fixing to a human or the **autoreview** skill (`/review`). Never edit
product code unless the user asks.

## What makes this powerful (not just a checklist)

1. **A deterministic spine** — a bundled zero-dependency toolkit (`bughunt.py`) ranks hotspots
   by churn × complexity × boundary × test-gap, surfaces pain signals (aged TODOs, config
   drift, risky deps), and owns structured findings: fingerprint, dedupe, suppress,
   baseline-diff, and render to markdown/HTML/SARIF with CI exit codes. See
   [tooling.md](tooling.md). Degrades to a pure-markdown pipeline when `python3` is absent.
2. **Breadth via fan-out** — split the target into a grid of **(lens × hotspot)** cells and
   run them as independent parallel hunters, so every risky area is examined through every
   relevant lens. A capability ladder runs the same phases whether or not the Workflow tool
   is available. See [orchestration.md](orchestration.md).
3. **Depth via specialized lenses + platform catalogs** — 13 lenses, each a distinct
   adversarial discipline (bugs, perf, DX, UX, supply-chain, data safety); each platform
   catalog encodes that ecosystem's specific footguns.
4. **Signal via mandatory verify + triage** — a skeptic pass tries to **refute every finding
   before it's reported** ([verification.md](verification.md)); survivors are confidence-rated,
   cross-validated, and reproduced by [triage](../triage/SKILL.md).

## First principle: signal over noise

A short list of **real, reproducible** bugs beats a long list of maybes. Every reported
finding names its **evidence** (`file:line` + trace + trigger + impact) and its
**confidence**. Speculative items are quarantined in their own section — never mixed in.
Before reporting anything, try to kill it (see the false-positive filter in
[triage](../triage/SKILL.md)). If it survives, report it.

## Operating principles

- **Assume guilt.** The code is wrong until you've checked. Read it for what it *does*, not
  what it's supposed to do.
- **Evidence-first.** No `file:line` + trace + trigger + impact → it's a question, not a finding.
- **Report, don't edit.** This skill is read-only by default. Surface and prove bugs; hand
  fixing to a human or the **autoreview** skill (`/review`). Only edit code if the user asks.
- **Scope before you scale.** On a large/unfamiliar repo, do recon and confirm scope/budget
  with the user before launching a deep hunt (see [recon-and-scoping.md](recon-and-scoping.md)).
- **Be honest about coverage.** Always state what you examined and what you did not.
- **Don't invent bugs.** A clean result is a valid, valuable outcome — see *When the hunt
  finds nothing* below. Never pad the report to look productive.

## Modes

| Mode | When | How |
|------|------|-----|
| **Quick scan** | Small target, a single file/module, or a diff; minutes | Single-agent sweep; pick 2–3 lenses + the platform catalog |
| **Deep hunt** | Whole codebase; the flagship mode | Full recon → fan-out across the (lens × hotspot) grid |
| **Targeted hunt** | User names a module/feature/file | Recon scoped to it → fan-out within scope |

Default to the mode the request implies; ask only if genuinely ambiguous.

## The hunt loop

Execute in order. Spokes carry the detail.

| Step | Do | Spoke |
|------|-----|-------|
| 1 | **Recon & pre-pass** — detect platform, run the deterministic pre-pass (census/hotspots/signals/deps), map trust boundaries, build the hunt plan | [recon-and-scoping.md](recon-and-scoping.md), [tooling.md](tooling.md) |
| 2 | **Fan-out** — build the (lens × hotspot) grid, dispatch hunters via the capability ladder (Workflow / parallel Tasks / sequential) | [orchestration.md](orchestration.md) |
| 3 | **Hunt** — each hunter runs one lens over one area using the relevant platform catalog; returns evidence as JSON | lens + platform spokes below |
| 4 | **Verify (mandatory)** — a skeptic pass tries to refute every candidate before it counts as a finding | [verification.md](verification.md) |
| 5 | **Merge & cross-validate** — `bughunt.py merge`: fingerprint, dedupe, cross-validate, suppress, baseline-diff | [orchestration.md](orchestration.md), [tooling.md](tooling.md) |
| 6 | **Triage** — severity × confidence (+ impact rubric), filter false positives, build minimal repros | [triage](../triage/SKILL.md) |
| 7 | **Confirm (optional)** — prove high-value findings dynamically or at runtime | [fuzz](../fuzz/SKILL.md), `verify` |
| 8 | **Report** — `bughunt.py render` the ranked markdown/HTML/SARIF; hand fixing off | [tooling.md](tooling.md), [triage](../triage/SKILL.md) report layout |

## Toolkit & capability ladder

The hunt has a **deterministic spine** and a **portable execution model**, so it works the same
on Claude Code, Cursor, or Codex.

- **Toolkit** — `bughunt.py` (zero-dependency, stdlib `python3`) under [`scripts/`](tooling.md)
  does the non-judgment work: rank hotspots, mine pain signals, audit deps, and
  fingerprint/dedupe/suppress/baseline-diff/render the findings. **Always probe `python3 --version`
  first.** If it's missing, run the **markdown fallback** — rank by the recon heuristics, keep
  findings in markdown, skip SARIF; nothing in the toolkit is required for the hunt to work.
- **Capability ladder** ([orchestration.md](orchestration.md)) — same five phases
  (Recon → Hunt → **Verify** → Merge → Report) on every rung: **(A)** invoke the shipped
  `hunt-workflow.js` when the Workflow tool is available; **(B)** parallel Tasks on standard
  Claude Code; **(C)** a sequential walk on single-agent tools. Verify is mandatory on all three.

## Example: one trip through the loop (condensed)

A small Node API repo, deep hunt:

1. **Recon** — detects Express + Postgres. Trust boundaries: HTTP routes, SQL. Hotspots by
   churn + boundary: `routes/invoices.js` (recently changed, near auth + SQL, no tests),
   `lib/pricing.js` (money math), `db/query.js`.
2. **Fan-out grid** — dispatch hunters: `auth-access × routes/invoices.js`,
   `taint × routes/invoices.js`, `logic-correctness × lib/pricing.js`,
   `resource-performance × db/query.js`. Platform catalog: web.
3. **Hunters report** (evidence-backed candidates):
   - `auth-access`: `GET /invoices/:id` loads by id with no ownership check → **IDOR**.
   - `logic-correctness`: discount applied after tax in `applyDiscount()` → wrong total.
   - `resource-performance`: invoice list issues one query per line item → **N+1**.
4. **Merge & cross-validate** — three distinct findings, no dupes; taint hunter found nothing
   new (SQL is parameterized — correctly *not* reported).
5. **Triage** — IDOR = `High-Confirmed` (wrote a failing test: user A reads user B's invoice);
   discount = `High-Probable` (traced values: $100 + 10% tax then −10% = $99, expected $90);
   N+1 = `Medium-Probable`.
6. **Report** — three findings, ranked, each with repro/trace; recommend fixing then `/review`.
   No edits made.

## When the hunt finds nothing

A clean result is a real outcome — report it honestly, never invent findings. Emit a short
report stating: what was examined (which lenses × hotspots), what was deliberately out of
scope, your confidence level, and any *Speculative* items worth a human glance. "I hunted X
with lenses Y and found no confirmed defects; here's the coverage" is a valid deliverable.

## Lens index (analysis disciplines)

Read on demand — only the lenses the hunt plan selects.

| Lens | Hunts for |
|------|-----------|
| [lens-dataflow-taint.md](lens-dataflow-taint.md) | Untrusted input reaching dangerous sinks: injection, deserialization, path traversal, SSRF, secret leakage |
| [lens-state-lifecycle.md](lens-state-lifecycle.md) | Illegal state transitions, resource/handle leaks, init/teardown order, idempotency, cache invalidation |
| [lens-concurrency.md](lens-concurrency.md) | Data races, TOCTOU, deadlock, reentrancy, async ordering & cancellation, shared mutable state |
| [lens-boundaries-numeric.md](lens-boundaries-numeric.md) | Off-by-one, overflow/truncation, precision, null/optional, empty/limit cases, encoding, time/DST |
| [lens-error-failure.md](lens-error-failure.md) | Swallowed errors, fail-open, partial writes, missing rollback, retry/timeout/cancel correctness |
| [lens-contract-spec.md](lens-contract-spec.md) | Code vs docs/tests/types/comments, violated invariants, dead/contradictory logic, copy-paste divergence |
| [lens-auth-access.md](lens-auth-access.md) | Broken authn/authz, IDOR, privilege escalation, tenant isolation, session/token/crypto/secret misuse |
| [lens-logic-correctness.md](lens-logic-correctness.md) | Internally wrong logic: inverted conditions, wrong operators/formulas, branch/case errors, wrong variable used |
| [lens-resource-performance.md](lens-resource-performance.md) | O(n²)+ complexity, N+1 queries, unbounded growth, memory blowups, DoS amplification at scale |
| [lens-dx-pain.md](lens-dx-pain.md) | Developer-experience friction: aged TODO/FIXME debt, flaky-test patterns, slow/serial scripts, config drift, unhelpful errors |
| [lens-product-ux.md](lens-product-ux.md) | User-facing pain: missing loading/empty/error states, swallowed feedback, dead feature flags, friction & dead ends |
| [lens-dependency-supply.md](lens-dependency-supply.md) | Supply-chain risk: vulnerable/unpinned/abandoned deps, lockfile drift, typosquats, unsafe install/CI |
| [lens-data-migration.md](lens-data-migration.md) | Data safety: destructive/irreversible migrations, unsafe backfills, schema/code skew, serialization drift |

## Platform index (ecosystem footguns)

Pick the one(s) recon identifies.

| Platform | Catalog |
|----------|---------|
| Apple — Swift/ObjC (iOS, macOS) | [platform-apple.md](platform-apple.md) |
| Web — JS/TS, browser, Node | [platform-web.md](platform-web.md) |
| Systems — C/C++/Rust/Go | [platform-systems.md](platform-systems.md) |
| Backend + CLI — Python/Ruby/Java + terminal tools | [platform-backend-cli.md](platform-backend-cli.md) |
| Other (Android/Kotlin, .NET/C#, PHP, Flutter/RN, SQL, IaC) **+ generic fallback for any unlisted language** | [platform-other.md](platform-other.md) |

## Spoke index

| File | Contents |
|------|----------|
| [recon-and-scoping.md](recon-and-scoping.md) | Deterministic pre-pass, platform detection, trust boundaries, hotspot ranking, hunt plan |
| [orchestration.md](orchestration.md) | (Lens × hotspot) grid, hunter prompt, capability ladder (Workflow/Tasks/sequential), merge/cross-validate |
| [verification.md](verification.md) | The mandatory adversarial skeptic pass — four refutation questions, verdict contract |
| [tooling.md](tooling.md) | `bughunt.py` reference — census/hotspots/signals/deps/merge/render/diff, state dir, CI mode |
| [lens-dataflow-taint.md](lens-dataflow-taint.md) | Source→sink tracing |
| [lens-state-lifecycle.md](lens-state-lifecycle.md) | State machines & resource lifecycle |
| [lens-concurrency.md](lens-concurrency.md) | Races, ordering, deadlock |
| [lens-boundaries-numeric.md](lens-boundaries-numeric.md) | Numeric & boundary conditions |
| [lens-error-failure.md](lens-error-failure.md) | Error & failure paths |
| [lens-contract-spec.md](lens-contract-spec.md) | Contract vs implementation |
| [lens-auth-access.md](lens-auth-access.md) | Authorization & access control |
| [lens-logic-correctness.md](lens-logic-correctness.md) | Business-logic correctness |
| [lens-resource-performance.md](lens-resource-performance.md) | Resource & performance at scale |
| [lens-dx-pain.md](lens-dx-pain.md) | Developer-experience pain |
| [lens-product-ux.md](lens-product-ux.md) | Product & UX pain |
| [lens-dependency-supply.md](lens-dependency-supply.md) | Dependency & supply chain |
| [lens-data-migration.md](lens-data-migration.md) | Data & migration safety |
| [platform-apple.md](platform-apple.md) | Swift/ObjC catalog |
| [platform-web.md](platform-web.md) | JS/TS/Node catalog |
| [platform-systems.md](platform-systems.md) | C/C++/Rust/Go catalog |
| [platform-backend-cli.md](platform-backend-cli.md) | Backend + CLI catalog |
| [platform-other.md](platform-other.md) | Android, .NET, PHP, Flutter/RN, SQL, IaC + generic fallback |

## When not to use

- **Just reviewing your own session diff for quality** → the **autoreview** skill (`/review`).
- **You already have one suspected bug to assess** → [triage](../triage/SKILL.md) directly.
- **You want to harden one function dynamically** → [fuzz](../fuzz/SKILL.md) directly.

## Related skills

- [triage](../triage/SKILL.md) — scoring, repro, and the report format bughunt emits
- [fuzz](../fuzz/SKILL.md) — confirm Probable findings dynamically
- the **autoreview** skill (`/review`) — the recommended fix/quality gate after reporting
- **verify** / `/verify` — drive the real app to reproduce a runtime-only bug
