# Bughunt Suite — Complete Guide

A deep, practical guide to **how bughunt-suite works** and **how to use it** — from a one-line
hunt to wiring it into CI. For install-only instructions see the [README](README.md); this
document is the manual.

> **What it is in one sentence:** an offensive, whole-codebase hunter for **bugs, pain points,
> and inefficiencies** that ranks risk deterministically, sweeps your code through 13 analysis
> lenses in parallel, makes a skeptic try to *disprove* every finding, and emits a ranked,
> fingerprinted, baseline-diffed report (markdown / HTML / SARIF) — **report-only by default.**

---

## Table of contents

1. [Philosophy](#1-philosophy)
2. [Quick start](#2-quick-start)
3. [Architecture at a glance](#3-architecture-at-a-glance)
4. [The hunt loop](#4-the-hunt-loop)
5. [The 13 lenses & 5 platform catalogs](#5-the-13-lenses--5-platform-catalogs)
6. [The toolkit: `bughunt.py`](#6-the-toolkit-bughuntpy)
7. [The findings schema](#7-the-findings-schema)
8. [Mandatory verification (the skeptic pass)](#8-mandatory-verification-the-skeptic-pass)
9. [Cross-lens clustering](#9-cross-lens-clustering)
10. [Severity, confidence & the impact rubric](#10-severity-confidence--the-impact-rubric)
11. [Scoping a hunt](#11-scoping-a-hunt)
12. [Baselines & suppressions](#12-baselines--suppressions)
13. [CI integration](#13-ci-integration)
14. [The capability ladder (how it runs anywhere)](#14-the-capability-ladder-how-it-runs-anywhere)
15. [`/triage` and `/fuzz`](#15-triage-and-fuzz)
16. [Portability & the markdown fallback](#16-portability--the-markdown-fallback)
17. [The eval fixture (how recall was measured)](#17-the-eval-fixture-how-recall-was-measured)
18. [Troubleshooting & FAQ](#18-troubleshooting--faq)
19. [A full worked example](#19-a-full-worked-example)

---

## 1. Philosophy

Four principles drive everything:

- **Assume guilt.** The code is wrong until you've checked. Read it for what it *does*, not
  what it's supposed to do.
- **Evidence or it didn't happen.** Every finding carries `file:line` + trigger + trace +
  impact. No evidence → it's a question, not a finding.
- **Signal over noise.** A short list of real, reproducible bugs beats a long list of maybes.
  A skeptic tries to kill every finding before it's reported; survivors are clustered, ranked,
  and proved.
- **Report, don't edit.** The hunt surfaces and proves defects; fixing is handed to a human or
  to a review/fix tool. It never edits product code unless you ask.

Bughunt is the **offensive** counterpart to a defensive review gate: where a review checks
*your own diff*, bughunt assumes the whole codebase is hiding defects and goes looking — across
correctness, security, performance, reliability, **and** developer/user pain.

---

## 2. Quick start

**Install (Claude Code):**

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install bughunt-suite@roberts-skills
```

**Run your first hunt:**

```text
/bughunt the whole repo — deep hunt, find the hidden bugs
```

That's it. The agent recons the target, runs the hunt (in parallel where supported), makes a
skeptic refute each candidate, and writes a ranked report into `.bughunt/` in your repo. It
does **not** change any code.

**Other common invocations:**

```text
/bughunt the sync engine, focus on concurrency and failure paths
/bughunt diff                  # only what changed on this branch
/bughunt staged quick          # fast scan of git-staged changes
/bughunt src/api               # scope to one directory
/bughunt ci                    # non-interactive; exit code gates a pipeline
```

`python3` is recommended (it powers the deterministic toolkit) but **not required** — without
it the hunt runs a pure-markdown pipeline (see [§16](#16-portability--the-markdown-fallback)).

---

## 3. Architecture at a glance

Bughunt-suite is **three skills**, **one toolkit**, and a **capability ladder**.

```
bughunt-suite/
├── commands/                    slash-command routers (/bughunt, /triage, /fuzz)
└── skills/
    ├── bughunt/                 the orchestrator (hub-and-spoke)
    │   ├── SKILL.md             hub: mission, hunt loop, lens/platform indexes
    │   ├── recon-and-scoping.md deterministic pre-pass + trust boundaries + hunt plan
    │   ├── orchestration.md     (lens × hotspot) grid + the capability ladder
    │   ├── verification.md      the mandatory skeptic pass
    │   ├── tooling.md           full bughunt.py reference
    │   ├── lens-*.md  (13)      one adversarial discipline each
    │   ├── platform-*.md (5)    ecosystem footguns (Apple/Web/Systems/Backend+CLI/Other)
    │   └── scripts/
    │       ├── bughunt.py       the zero-dependency toolkit (python3 stdlib only)
    │       ├── hunt-workflow.js  the Workflow-tool fan-out script (Rung A)
    │       ├── schema/finding.schema.json   the findings contract
    │       └── selftest.py      23 stdlib unit tests
    ├── triage/                  severity × confidence, repro, report format
    └── fuzz/                    property/fuzz/differential harnesses that RUN
```

- **`bughunt` (`/bughunt`)** — the orchestrator. Recons, fans out hunters, runs the skeptic
  pass, merges, and reports.
- **`triage` (`/triage`)** — owns the finding schema, the severity/confidence/impact rubrics,
  and minimal-repro discipline. Used standalone on a single bug, or as bughunt's scoring stage.
- **`fuzz` (`/fuzz`)** — generates and **runs** property-based / fuzz / differential harnesses
  to confirm a suspicion dynamically.

The **toolkit** (`bughunt.py`) is the deterministic spine: it ranks hotspots, mines pain
signals, audits dependencies, and owns the entire findings pipeline (validate → fingerprint →
dedupe → cluster → suppress → baseline-diff → render). The **lenses** are the judgment; the
toolkit is the bookkeeping.

---

## 4. The hunt loop

Every hunt runs the same eight steps, in order:

| # | Step | What happens |
|---|------|--------------|
| 1 | **Recon & pre-pass** | Detect platform, map trust boundaries, run the deterministic pre-pass (`census`/`hotspots`/`signals`/`deps`) to get a ranked target list and pain signals, build a hunt plan. |
| 2 | **Fan-out** | Build a grid of **(lens × hotspot)** cells and dispatch hunters — in parallel where supported. |
| 3 | **Hunt** | Each hunter examines *one area* through *one lens*, using the relevant platform catalog, and returns evidence-backed findings as JSON. |
| 4 | **Verify (mandatory)** | A skeptic tries to *refute* every candidate (four refutation questions). Refuted ones are quarantined. |
| 5 | **Merge** | `bughunt.py merge` fingerprints, dedupes, **clusters cross-lens duplicates**, suppresses, and baseline-diffs. |
| 6 | **Triage** | Severity × confidence (+ impact rubric); minimal repros for the top findings. |
| 7 | **Confirm (optional)** | Prove high-value findings dynamically with `/fuzz` or by driving the app. |
| 8 | **Report** | `bughunt.py render` emits the ranked markdown / HTML / SARIF into `.bughunt/`. |

The power comes from **breadth via fan-out** (many narrow, thorough passes beat one broad
pass) and **signal via the skeptic pass** (nothing reaches the report until someone has tried
to kill it).

---

## 5. The 13 lenses & 5 platform catalogs

A **lens** is a distinct adversarial discipline — a checklist of concrete, grep-able code
smells, how to trace them, what evidence to capture, and which false positives to reject. The
hunt plan picks only the lenses that fit the target.

| Lens | Hunts for |
|------|-----------|
| `dataflow-taint` | Untrusted input reaching dangerous sinks: injection, deserialization, path traversal, SSRF, secret leakage |
| `state-lifecycle` | Illegal state transitions, resource/handle leaks, init/teardown order, idempotency, cache invalidation |
| `concurrency` | Data races, TOCTOU, deadlock, reentrancy, async ordering & cancellation, shared mutable state |
| `boundaries-numeric` | Off-by-one, overflow/truncation, precision, null/optional, empty/limit cases, encoding, time/DST |
| `error-failure` | Swallowed errors, fail-open, partial writes, missing rollback, retry/timeout/cancel correctness |
| `contract-spec` | Code vs docs/tests/types/comments, violated invariants, dead/contradictory logic, copy-paste divergence |
| `auth-access` | Broken authn/authz, IDOR, privilege escalation, tenant isolation, session/token/crypto/secret misuse |
| `logic-correctness` | Inverted conditions, wrong operators/formulas, branch/case errors, wrong variable used |
| `resource-performance` | O(n²)+ complexity, N+1 queries, unbounded growth, memory blowups, DoS amplification at scale |
| `dx-pain` | Aged TODO/FIXME debt, flaky-test patterns, slow/serial scripts, config drift, unhelpful errors |
| `product-ux` | Missing loading/empty/error states, swallowed user feedback, dead feature flags, friction & dead ends |
| `dependency-supply` | Vulnerable/unpinned/abandoned deps, lockfile drift, typosquats, unsafe install/CI |
| `data-migration` | Destructive/irreversible migrations, unsafe backfills, schema/code skew, serialization drift |

The first nine catch **defects**; the last four catch **pain points and inefficiencies** —
the difference between a linter and a tool that tells you where your project actually hurts.

**Platform catalogs** layer ecosystem-specific footguns on top of the language-agnostic
lenses: `platform-apple` (Swift/ObjC), `platform-web` (JS/TS/Node), `platform-systems`
(C/C++/Rust/Go), `platform-backend-cli` (Python/Ruby/Java + CLIs), and `platform-other`
(Android/.NET/PHP/Flutter/SQL/IaC) — which also carries a **generic fallback** so the hunt
works on *any* unlisted language.

---

## 6. The toolkit: `bughunt.py`

A single zero-dependency file (`python3` standard library only — no `pip install`, ever). It
gives the hunt a deterministic spine. Invoke it as:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py [--root PATH] [--quiet] <subcommand> ...
```

> **Global flags go *before* the subcommand:** `--root PATH` (default: cwd) and `--quiet`.

It has 7 subcommands across two phases — **recon** (census/hotspots/signals/deps) and
**pipeline** (merge/render/diff).

### `census` — map the target

```bash
bughunt.py census [--functions] [--exclude GLOB...]
```

Languages, file sizes, and generated/vendored/test detection. `--functions` adds a shortlist
of pure-ish function candidates for `/fuzz`.

```jsonc
// census output (abridged, real)
{
  "totals": { "files": 131, "loc": 16579, "codeFiles": 12, "testFiles": 0 },
  "languages": { "javascript": { "files": 8, "loc": 590 }, ... }
}
```

### `hotspots` — rank files by likelihood-of-defect

```bash
bughunt.py hotspots [--top N] [--since DATE]
```

Ranks files so the hunt starts where risk and change collide, instead of wandering. The score
is a weighted blend: **churn 0.30 · complexity 0.25 · boundary 0.20 · recency 0.15 ·
test-gap 0.10**. Complexity is a stdlib proxy (branch-keyword density + nesting depth + LOC),
not true cyclomatic complexity. Off-git, it falls back to file mtime.

```jsonc
// hotspots output (real)
{
  "gitAvailable": true,
  "hotspots": [
    { "path": "scripts/bughunt.py", "score": 1.0, "churn": 1, "complexity": 401,
      "boundary": 1, "test_gap": 1,
      "reasons": ["complex (proxy 401)", "recently touched", "at a trust boundary", "no matching test file"] }
  ]
}
```

### `signals` — the pain-point pre-pass

```bash
bughunt.py signals [--max-age-days N]   # default 180
```

Deterministically mines what the `dx-pain` and `product-ux` lenses care about:
- **`todos`** — TODO/FIXME/HACK/XXX with age (via `git blame`) and author; `aged: true` past the threshold.
- **`flags`** — feature-flag references.
- **`configDrift`** — keys present in `.env.example` but missing from `.env` (and vice-versa), lockfile-vs-manifest drift.
- **`longScripts`** — npm scripts chaining many serial commands, oversized shell scripts.

### `deps` — dependency / supply-chain audit

```bash
bughunt.py deps [--osv]
```

Parses manifests and lockfiles and flags issues with codes: `UNPINNED`, `NO_LOCKFILE`,
`LOCK_DRIFT`, `TYPOSQUAT_SHAPE` (edit-distance to a popular package), `DEPRECATED_MARKER`.
**Offline by default.** `--osv` opts into a network query to OSV.dev for known advisories.

### `merge` — the pipeline core and CI gate

```bash
bughunt.py merge <files...|-> [--baseline P] [--suppress P] \
    [--write-baseline] [--out P] [--fail-on critical-high|any|none] [--no-cluster]
```

Takes one or more hunter findings-JSON files (or `-` for stdin) and **owns**:

1. **Validation** — the executable form of `schema/finding.schema.json`. Invalid findings are dropped with a stderr warning; merge **never aborts** on one bad finding.
2. **Fingerprinting** — a stable id per finding (see [§7](#7-the-findings-schema)).
3. **Dedupe** — collapses identical fingerprints, keeping the clearer write-up.
4. **Cross-lens clustering** — see [§9](#9-cross-lens-clustering); `--no-cluster` disables it.
5. **Suppression** — mutes fingerprints listed in `suppressions.json`.
6. **Baseline diff** — marks each finding `new` / `existing` / `fixed`.
7. **Id renumbering** — stable, severity-sorted `BH-001…` ids.

It writes the merged document to `--out` (default `.bughunt/findings.json`) and **exits** with
a CI-gate code (see [§13](#13-ci-integration)).

### `render` — reports in three formats

```bash
bughunt.py render <findings.json|-> [--formats md,html,sarif] [--md P] [--html P] [--sarif P]
```

- **`md`** — the canonical report layout (Summary / Baseline diff / Confirmed & Probable / Speculative / Refuted appendix / Coverage / Next step). Byte-compatible with the markdown finding block.
- **`html`** — a standalone, severity-colored page (no external assets).
- **`sarif`** — SARIF 2.1.0 for GitHub code scanning (one rule per lens, fingerprints as `partialFingerprints`).

### `diff` — compare two runs

```bash
bughunt.py diff <A.json> <B.json>
```

Fingerprint comparison → `{ new, fixed, unchanged, counts }`.

### The `.bughunt/` state directory

Each run reads/writes `.bughunt/` in the target repo:

| File | Git | Purpose |
|------|-----|---------|
| `baseline.json` | **commit** | the agreed set of known findings; `merge` diffs against it so the gate fires only on *new* defects |
| `suppressions.json` | **commit** | `{"suppressions": [{"fingerprint": "…", "reason": "…"}]}` — mute by-design findings |
| `findings.json` | gitignore | the latest merged document (regenerated each run) |
| `report.md` / `.html` / `.sarif` | gitignore | rendered reports |

Suggested `.gitignore`:

```gitignore
.bughunt/findings.json
.bughunt/report.*
```

### Self-test

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/selftest.py
```

23 stdlib unit tests cover the whole pipeline (schema round-trip, fingerprint stability,
dedupe, clustering, suppression, baseline diff, exit codes, SARIF/HTML). Run it after editing
`bughunt.py`.

---

## 7. The findings schema

Every finding has two equivalent shapes: the **markdown block** humans read, and a **JSON
object** the toolkit processes. `render` produces the markdown from the JSON, so you can author
either. The full contract is `scripts/schema/finding.schema.json`.

```jsonc
{
  "id": "BH-001",
  "title": "IDOR: any user can read any invoice",
  "lens": "auth-access",
  "severity": "High",                       // Critical | High | Medium | Low
  "confidence": 0.95,                        // float 0.0–1.0
  "confidenceLabel": "Confirmed",            // derived: ≥0.85 Confirmed, ≥0.5 Probable, else Speculative
  "location": { "file": "routes/invoices.js", "startLine": 42, "endLine": 42 },
  "fingerprint": "f3a9c1e0b7d24a55",         // filled by merge
  "trigger": "authenticated user requests GET /invoices/:id with another user's id",
  "trace": "req.params.id (routes/invoices.js:42) -> findById(id) -> no WHERE user_id filter",
  "impact": "horizontal privilege escalation — read any customer's invoice",
  "impactClass": "security",                 // see the impact rubric, §10
  "repro": "login as A, GET /invoices/{B}, expect 403, got 200",
  "fixSketch": "scope the query to the caller (WHERE id = ? AND user_id = ?)",
  "tags": ["idor", "broken-access-control"],
  "verified": { "by": "skeptic-pass", "method": "static-refutation", "verdict": "upheld", "note": "no upstream ownership guard" },
  "alsoFlaggedBy": [ { "lens": "dataflow-taint", "title": "…", "line": 42 } ],  // cross-lens convergence
  "baselineStatus": "new"                    // new | existing | fixed
}
```

**Required fields:** `title`, `lens`, `severity`, `confidence`, `location.file`,
`location.startLine`, `trigger`, `trace`, `impact`. Everything else is filled in by `merge` or
optional.

**The fingerprint** is `sha256(lens + NUL + relpath + NUL + normalized_snippet)[:16]`, where
the snippet is the anchor line(s) with whitespace collapsed and string/number literals
replaced by `§`. Because it **excludes line numbers**, a finding keeps the same fingerprint
when you refactor, reflow, or move the function — which is exactly what makes baseline diffing
and suppression hold up across edits. (If the snippet can't be read, the title is used.)

---

## 8. Mandatory verification (the skeptic pass)

This is what keeps the report trustworthy. After hunters produce candidates, a **skeptic**
agent tries to *refute* each one — its job is to kill the finding, not confirm it. It works
through four refutation questions:

1. **Upstream guard** — is there a validation, early return, type constraint, or invariant *before* this code that prevents the trigger?
2. **Trusted input** — is the "untrusted" value actually validated/trusted at the boundary it crosses?
3. **Covering test** — does an existing test already exercise this path passing?
4. **Documented intent** — is this behavior intentional and documented (comment, ADR, type)?

It returns a verdict — `upheld`, `refuted`, or `uncertain` — biased toward **refuted** on
genuine doubt. `merge` moves `refuted` findings into a transparency appendix and excludes them
from the report body and the CI gate; `uncertain` survives but is capped at Speculative.

This pass is **mandatory on every rung** of the capability ladder — it is never skipped, even
in the single-agent fallback.

---

## 9. Cross-lens clustering

The same bug often trips multiple lenses — an off-by-one loop looks wrong to
`boundaries-numeric`, `logic-correctness`, *and* `contract-spec`. Reporting it three times is
noise. So `merge` **clusters** findings that different lenses raised at overlapping lines into
**one primary finding** (the highest-severity / highest-confidence write-up), attaching the
others as an `alsoFlaggedBy` list and bumping confidence for the convergence (agreement across
independent lenses is strong signal).

Same-lens findings are never merged this way (fingerprint dedupe already handles exact
repeats; two distinct bugs the same lens found stay separate). Pass `--no-cluster` to keep
everything separate (legacy behavior: boost confidence, don't merge).

In the eval, clustering collapsed **49 raw findings → 26 clean ones** with no loss of recall —
one entry per bug, with the convergence still visible.

---

## 10. Severity, confidence & the impact rubric

Three orthogonal axes:

- **Severity** — impact *if triggered*, independent of likelihood: Critical / High / Medium / Low.
- **Confidence** — how sure it's real, independent of severity: a float `0–1`, labeled Confirmed (≥0.85) / Probable (≥0.5) / Speculative.
- **Impact class** — *which yardstick* the severity is measured against, so a non-security finding isn't force-fit into a security frame.

The **impact rubric** calibrates severity per `impactClass`:

| impactClass | What Critical/High looks like | What Low looks like |
|-------------|-------------------------------|---------------------|
| `security` | auth bypass, RCE, secret/PII disclosure, reachable injection | theoretical, behind strong guards |
| `correctness` | wrong result users act on; silent data divergence | wrong only on a contrived edge |
| `reliability` | crash/hang/outage under normal load; fail-open | degrades only under rare conditions |
| `performance` | O(n²)/N+1/unbounded growth that breaks at real scale | constant-factor waste on a cold path |
| `data-integrity` | destructive/irreversible migration, corruption, lost writes | recoverable, narrow-window skew |
| `dx` | broken build/test, footgun that routinely costs dev hours | stale TODO, cosmetic friction |
| `ux` | user can't recover (white screen, silent failure, double-charge) | minor polish / missing affordance |
| `supply-chain` | known-vulnerable/typosquat dep on a reachable path | unpinned but low-risk dev dep |

A High-severity DX or UX finding is legitimate and ranks above a Low-severity security nit —
score by **impact on the user/operator/developer**, not by how clever the bug is.

---

## 11. Scoping a hunt

Pass scope and depth in plain language to `/bughunt`; the command parses them:

| You type | Scope |
|----------|-------|
| `/bughunt` (or "the whole repo") | the entire repository |
| `/bughunt diff` | changes vs the merge base |
| `/bughunt staged` | git-staged changes only |
| `/bughunt src/api` | one directory |
| `/bughunt the sync engine` | a named module/feature |

| Depth | Behavior |
|-------|----------|
| `quick` | a handful of cells — fast, the top hotspots × highest-yield lenses |
| `deep` | full fan-out across the grid (the default for a whole-repo hunt) |

On a large or unfamiliar repo, the hunt does recon first and **confirms scope with you**
before fanning out — except under `ci`, which never prompts.

---

## 12. Baselines & suppressions

These let you adopt bughunt on a codebase that already has known issues, without drowning in
them.

**Baseline** — record the current findings as "known," so future runs only flag what's *new*:

```bash
# establish/refresh the baseline
bughunt.py merge .bughunt/raw-findings.json --write-baseline
```

`baseline.json` is committed. Later runs report `new` / `existing` / `fixed` against it, and
the CI gate fires only on newly-introduced Critical/High findings — so a legacy backlog never
blocks a PR, but regressions do.

**Suppression** — permanently mute a specific by-design finding. Add its fingerprint to
`.bughunt/suppressions.json`:

```json
{ "suppressions": [
  { "fingerprint": "f3a9c1e0b7d24a55", "reason": "intentional admin-only debug route, gated by infra" }
] }
```

Suppressed findings are excluded from the report body and the gate (they still appear in a
"Suppressed" section for transparency). Because fingerprints are line-number-independent, a
suppression survives refactors.

> Rule of thumb: **baseline** for "we'll get to these," **suppress** for "this is intentional."

---

## 13. CI integration

`/bughunt ci` runs non-interactively and surfaces `merge`'s exit code:

| Exit code | Meaning |
|-----------|---------|
| `0` | no new findings (clean) |
| `1` | new **Critical/High** finding(s) — fail the build |
| `2` | new **Medium/Low** finding(s) — warn |
| `3` | usage / IO error |

`--fail-on` tunes the gate: `critical-high` (default), `any`, or `none` (always 0 — report
without gating).

A minimal pipeline step:

```bash
ROOT="path/to/skills/bughunt/scripts/bughunt.py"

# 1. recon (optional, for logs/artifacts)
python3 "$ROOT" hotspots --top 20 > hotspots.json
python3 "$ROOT" signals > signals.json

# 2. ...drive the hunt, collecting hunter findings into hunters/*.json...

# 3. gate against the committed baseline; fail on new Critical/High
python3 "$ROOT" merge hunters/*.json --fail-on critical-high
GATE=$?

# 4. render SARIF for GitHub code scanning
python3 "$ROOT" render .bughunt/findings.json --formats sarif
# upload .bughunt/report.sarif via github/codeql-action/upload-sarif

exit $GATE
```

Because findings carry stable fingerprints, GitHub dedupes them across runs and tracks
fixed-vs-new automatically.

---

## 14. The capability ladder (how it runs anywhere)

The same five phases — **Recon → Hunt → Verify → Merge → Report** — run on any tool, via
whichever rung is available:

- **Rung A — Workflow tool present (Claude Code).** The agent runs the pre-pass via Bash,
  builds the grid, and invokes the shipped `scripts/hunt-workflow.js` through the Workflow
  tool. That script fans out one hunter per cell and one skeptic per candidate (pipelined), and
  returns the upheld findings as JSON; the agent pipes them through `merge` + `render`.
- **Rung B — standard Claude Code.** Identical phases by hand: parallel Task/Agent calls for
  the hunters, then a skeptic Task per surviving candidate, then `merge` + `render` via Bash.
- **Rung C — single-agent tools (Cursor / Codex).** A sequential walk of the grid: for each
  cell, hunt then immediately skeptic-verify before moving on; accumulate JSON; `merge` +
  `render` if `python3` is present, else hand-assemble the markdown report.

**Verify is mandatory on every rung.** The grid, the evidence contract, and the merge
discipline are identical; only the execution (parallel vs serial) changes.

---

## 15. `/triage` and `/fuzz`

**`/triage`** — turn a vague suspicion or a pile of findings into a precise, ranked,
evidence-backed report. It owns the finding schema, the severity/confidence/impact rubrics, and
the minimal-repro discipline (failing test → runtime repro → traced values, cheapest first).
Use it standalone on a single bug, or let bughunt call it as its scoring stage.

```text
/triage this crash report and give me a minimal repro
```

**`/fuzz`** — prove a finding (or harden a function) by **running** code, not just reading it.
The loop: **discover** a fuzzable target (a named function, or `census --functions`) → **pick
technique** (property / fuzz / differential / metamorphic) and design the oracle → **generate**
a harness in the project's own test runner → **run** it → **shrink** the failing input →
**emit** a committed regression test + a `verified: upheld` finding. It **asks before
installing** any test dependency, and with no test infra it generates the harness and marks it
*not executed* rather than faking a result.

```text
/fuzz this parser — decode(encode(x)) must round-trip and it must never crash
```

Both are report/test-only: they surface and prove, they don't fix product code.

---

## 16. Portability & the markdown fallback

Nothing hard-depends on the toolkit. The skill always probes `python3 --version` first; if it's
absent, the hunt runs a **pure-markdown pipeline**: hotspots ranked by the recon heuristics,
findings kept in the markdown finding-block format, no SARIF. The lenses, the evidence
contract, the mandatory skeptic pass, and the report layout are identical — you just lose the
deterministic ranking, fingerprinted baselining, and machine formats.

The same `SKILL.md` files are the native format for **Claude Code, Cursor, and Codex**, so the
suite is portable across all three (see the [README](README.md) for per-tool install).

---

## 17. The eval fixture (how recall was measured)

`eval/bughunt-fixture/` (in the marketplace repo, *outside* the plugin so installs stay lean)
is a deliberately buggy mini billing service — **29 planted bugs across all 13 lenses**, each
marked with a hidden `SEED:BUG-NNN <lens>` comment and recorded in `answer-key.json`.

> ⚠️ **Never `npm install` the fixture** — it lists an intentional typosquat dependency as a
> supply-chain seed, and a `preinstall` guard blocks installs. The eval is fully **static**.

To run it honestly you must **strip the SEED markers first** (they name the bug *and* its
lens — a giant hint). The RUNBOOK describes the procedure: copy the fixture to a temp dir,
blank the marker lines (preserving line numbers so the answer key stays valid), run the hunt
against the copy, then score reported findings against `answer-key.json` by lens + file +
line (±a few).

**Measured result:** with markers stripped, **90% recall (26/29)** and a **~0% true
false-positive rate** — every reported finding was a real defect, and clustering reduced 49 raw
findings to 26 clean ones. See `eval/bughunt-fixture/RUNBOOK.md` for the exact scoring recipe
and targets (recall ≥ 80%, FP < 20%).

This fixture is also a regression guard: re-run it after changing a lens or the toolkit to
confirm recall hasn't dropped.

---

## 18. Troubleshooting & FAQ

**`bughunt.py: error: unrecognized arguments: --quiet`**
Global flags (`--root`, `--quiet`) go **before** the subcommand:
`bughunt.py --root . --quiet merge …`, not `merge … --quiet`.

**The hunt reports the same bug several times.**
You likely ran `merge` with `--no-cluster`, or didn't run `merge` at all. The default merge
clusters cross-lens duplicates into one finding with `alsoFlaggedBy`.

**It found nothing.**
A clean result is a valid outcome — bughunt never pads. Check the report's *Coverage & gaps*
section for what was examined, and consider widening scope or adding lenses.

**Findings keep coming back after I "fixed" them.**
If they're intentional, **suppress** them (add the fingerprint to `suppressions.json`). If
they're a known backlog you'll address later, write a **baseline** so they're marked `existing`
and don't gate CI.

**No `python3` on the runner.**
The hunt still works in pure-markdown mode — you just don't get hotspot ranking, baselining, or
SARIF. Install `python3` (stdlib only; no packages needed) to enable the toolkit.

**`deps` didn't flag a known-vulnerable package.**
Offline `deps` flags *structural* issues (unpinned, no lockfile, drift, typosquat shape). For
known CVEs, run `deps --osv` (network, opt-in).

**Is it safe to run on a private/proprietary codebase?**
Yes — it's read-only by default and makes no network calls unless you pass `deps --osv`.

---

## 19. A full worked example

A small Node + Postgres API, deep hunt:

**1. Recon & pre-pass.** Detects Express + Postgres. Trust boundaries: HTTP routes, SQL.
`hotspots` ranks `routes/invoices.js` (recently changed, near auth + SQL, no tests),
`lib/pricing.js` (money math), `db/query.js`. `signals` surfaces a 9-month-old `FIXME` in the
auth middleware; `deps` flags an unpinned `express` and a missing lockfile.

**2. Fan-out grid.** Hunters dispatched: `auth-access × routes/invoices.js`,
`dataflow-taint × routes/invoices.js`, `logic-correctness × lib/pricing.js`,
`resource-performance × db/query.js`, `dependency-supply × package.json`. Platform: web.

**3. Hunt.** Candidates come back evidence-backed:
- `auth-access`: `GET /invoices/:id` loads by id with no ownership check → **IDOR**.
- `logic-correctness`: discount applied *after* tax in `applyDiscount()` → wrong total.
- `resource-performance`: invoice list issues one query per line item → **N+1**.
- `dependency-supply`: `express` unpinned, no lockfile committed.

**4. Verify.** A skeptic tries to kill each. The IDOR survives all four questions (no upstream
guard, id is attacker-controlled, no covering test, comment says "scope to user" — unmet) →
`upheld`. A speculative taint finding is `refuted` (the query is parameterized) → quarantined.

**5. Merge.** Fingerprints, dedupes, clusters; the IDOR was also raised by `dataflow-taint`, so
they cluster into one finding with `alsoFlaggedBy`. Baseline diff: all `new` (first run).

**6–8. Triage & report.** IDOR = `High` / Confirmed (wrote a failing test: user A reads B's
invoice); discount = `High` / Probable (traced $100 +10% tax −10% = $99, expected $90); N+1 =
`Medium` / Probable; unpinned dep = `Low` / supply-chain. `render` writes
`.bughunt/report.md`, `.html`, and `.sarif`. No code edited.

The deliverable: four ranked, reproducible findings — and a recommendation to fix the IDOR and
discount bugs first, then re-run with a written baseline so the next hunt only shows what's new.

---

*Part of [Bughunt Suite](README.md) · [Robert's Skills](https://github.com/robzilla1738/roberts-skills). Report-only by default; `disable-model-invocation: true` means each skill loads on explicit request.*
