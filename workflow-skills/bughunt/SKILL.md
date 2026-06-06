---
name: bughunt
description: >
  Adversarial whole-codebase bug hunter for any project type (iOS, macOS, web, services,
  terminal tools). Recon the target, fan out parallel hunters across a grid of analysis
  lenses x risk hotspots, then merge, cross-validate, and report ranked, reproducible
  findings. Report-only by default. Use when the user invokes /bughunt, asks to find
  hidden bugs, audit code for defects, do a deep code review, or hunt for what tests miss.
disable-model-invocation: true
version: 2026-06-06.1
platforms: [language-agnostic, Apple, Web, Systems, Backend, CLI]
primary_use_cases:
  - Hunt an entire codebase for hidden defects, not just the current diff
  - Deep adversarial code review of a module, feature, or risky change
  - Find concurrency, lifecycle, taint, numeric, failure-path, and contract bugs
  - Produce a ranked, evidence-backed, reproducible bug report
---

# Bughunt

An **offensive, whole-codebase bug hunter**. Where [autoreview](../autoreview/SKILL.md) is a
defensive gate on *your own diff*, bughunt assumes the code is **guilty** and goes looking
for hidden defects across the whole target — on any platform.

Read this hub first, run **recon**, then open only the spokes your hunt plan selects.

## Mission

Find the bugs that tests, linters, and a tired reviewer miss — and **prove** them. The
output is a ranked, evidence-backed report, not a vibe. Default behavior is **report-only**:
hunt, document, hand fixing to a human or [autoreview](../autoreview/SKILL.md). Never edit
product code unless the user asks.

## What makes this powerful (not just a checklist)

1. **Breadth via fan-out** — split the target into a grid of **(lens × hotspot)** cells and
   run them as independent parallel hunters, so every risky area is examined through every
   relevant lens. See [fanout-orchestration.md](fanout-orchestration.md).
2. **Depth via specialized lenses + platform catalogs** — each lens is a distinct adversarial
   discipline; each platform catalog encodes that ecosystem's specific footguns.
3. **Signal via triage + proof** — confidence-rate every finding, cross-validate across
   lenses, and reproduce the top ones. Handled by [triage](../triage/SKILL.md).

## First principle: signal over noise

A short list of **real, reproducible** bugs beats a long list of maybes. Every reported
finding names its **evidence** (`file:line` + trace + trigger + impact) and its
**confidence**. Speculative items are quarantined in their own section — never mixed in.
Before reporting anything, try to kill it (see the false-positive filter in
[triage](../triage/SKILL.md)). If it survives, report it.

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
| 1 | **Recon & scope** — detect platform, map trust boundaries, rank hotspots, build the hunt plan | [recon-and-scoping.md](recon-and-scoping.md) |
| 2 | **Fan-out** — build the (lens × hotspot) grid, dispatch parallel hunters (or sequential fallback) | [fanout-orchestration.md](fanout-orchestration.md) |
| 3 | **Hunt** — each hunter runs one lens over one area using the relevant platform catalog; collects evidence | lens + platform spokes below |
| 4 | **Merge & cross-validate** — dedupe, cluster, boost confidence when two lenses agree | [fanout-orchestration.md](fanout-orchestration.md) |
| 5 | **Triage** — severity × confidence, filter false positives, build minimal repros | [triage](../triage/SKILL.md) |
| 6 | **Confirm (optional)** — prove high-value findings dynamically or at runtime | [fuzz](../fuzz/SKILL.md), `verify` |
| 7 | **Report** — emit the ranked report; hand fixing off | [triage](../triage/SKILL.md) report layout |

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

## Platform index (ecosystem footguns)

Pick the one(s) recon identifies.

| Platform | Catalog |
|----------|---------|
| Apple — Swift/ObjC (iOS, macOS) | [platform-apple.md](platform-apple.md) |
| Web — JS/TS, browser, Node | [platform-web.md](platform-web.md) |
| Systems — C/C++/Rust/Go | [platform-systems.md](platform-systems.md) |
| Backend + CLI — Python/Ruby/Java + terminal tools | [platform-backend-cli.md](platform-backend-cli.md) |

## Spoke index

| File | Contents |
|------|----------|
| [recon-and-scoping.md](recon-and-scoping.md) | Platform detection, trust boundaries, hotspot ranking, hunt plan |
| [fanout-orchestration.md](fanout-orchestration.md) | (Lens × hotspot) grid, hunter prompt template, merge/dedup/cross-validate, sequential fallback |
| [lens-dataflow-taint.md](lens-dataflow-taint.md) | Source→sink tracing |
| [lens-state-lifecycle.md](lens-state-lifecycle.md) | State machines & resource lifecycle |
| [lens-concurrency.md](lens-concurrency.md) | Races, ordering, deadlock |
| [lens-boundaries-numeric.md](lens-boundaries-numeric.md) | Numeric & boundary conditions |
| [lens-error-failure.md](lens-error-failure.md) | Error & failure paths |
| [lens-contract-spec.md](lens-contract-spec.md) | Contract vs implementation |
| [platform-apple.md](platform-apple.md) | Swift/ObjC catalog |
| [platform-web.md](platform-web.md) | JS/TS/Node catalog |
| [platform-systems.md](platform-systems.md) | C/C++/Rust/Go catalog |
| [platform-backend-cli.md](platform-backend-cli.md) | Backend + CLI catalog |

## When not to use

- **Just reviewing your own session diff for quality** → [autoreview](../autoreview/SKILL.md).
- **You already have one suspected bug to assess** → [triage](../triage/SKILL.md) directly.
- **You want to harden one function dynamically** → [fuzz](../fuzz/SKILL.md) directly.

## Related skills

- [triage](../triage/SKILL.md) — scoring, repro, and the report format bughunt emits
- [fuzz](../fuzz/SKILL.md) — confirm Probable findings dynamically
- [autoreview](../autoreview/SKILL.md) — the recommended fix/quality gate after reporting
- **verify** / `/verify` — drive the real app to reproduce a runtime-only bug
