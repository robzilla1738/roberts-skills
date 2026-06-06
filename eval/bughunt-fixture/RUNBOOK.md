# Bughunt eval fixture — RUNBOOK

> ⚠️ **Do NOT `npm install` this fixture.** It intentionally lists a typosquat
> dependency (`axxios`) as a supply-chain bug seed. The eval is **fully static** —
> bughunt reads `package.json`, it never installs anything. A `preinstall` guard
> blocks `npm install` so the typosquat name can't be resolved by accident.

## Purpose

This is a deliberately buggy mini billing/invoices service used to measure the
bughunt suite's **recall** (does it find the planted defects?) and
**false-positive rate** (how much does it over-report?). It is NOT meant to run
in production — some bugs would crash it on purpose, and it contains intentional
security holes (SQL injection, IDOR, fail-open auth, path traversal). Every
planted bug is marked in source with a hidden `SEED:BUG-0NN <lens-slug>` comment
and recorded in `answer-key.json`.

There are **29 planted bugs across all 13 lenses** (see the per-lens table at the
bottom of this file). Two of them (the dependency-supply pair) live in
`package.json` and are surfaced by the `deps` pre-pass rather than an inline
comment, since JSON has no comments.

When running the hunt as an eval, **strip or ignore the `SEED:BUG` markers** —
they are the answer key, not a hint the hunter should read. (A quick way to hunt
"blind" is to copy the fixture to a temp dir and `sed`-delete lines containing
`SEED:BUG` first, then run the hunt on the copy and map line numbers back.)

## Layout

```
bughunt-fixture/
  package.json              express UNPINNED + axxios typosquat + NO lockfile  (dependency-supply)
  .env.example              full key set (source of truth)
  .env                      missing FEATURE_BULK_EXPORT, extra SENTRY_DSN        (config drift)
  app/
    server.js               express bootstrap
    lib/auth.js             fail-open auth on bad token                          (error-failure)
    lib/pricing.js          off-by-one, float trunc, inverted cond, discount-after-tax, doc skew
                            (boundaries-numeric, logic-correctness, contract-spec)
    routes/invoices.js      IDOR, missing role check, SQL concat, path traversal, swallowed-200
                            (auth-access, dataflow-taint, error-failure)
    db/invoices.js          unbounded select, N+1, handle leak                   (resource-performance, state-lifecycle)
    cache/worker.js         TOCTOU, shared-state race, unbounded cache           (concurrency, state-lifecycle)
    ui/InvoiceList.jsx      swallowed-error UI, no loading/empty state, dead flag, copy-paste path
                            (product-ux, contract-spec)
  scripts/
    migrate_invoices.py     destructive backfill, schema/code skew               (data-migration)
    parse_receipts.py       aged FIXME, format drift, unhelpful catch, flaky sleep (dx-pain)
  answer-key.json           ground truth: id, lens, file, line, severity, impactClass, blurb
  RUNBOOK.md                this file
```

## How to run a hunt

Let `BH` be the toolkit path:

```bash
BH=../../plugins/bughunt-suite/skills/bughunt/scripts/bughunt.py
```

(Adjust the relative path to wherever the bughunt-suite plugin is installed; from
the fixture root the layout above resolves to `../../plugins/...`.)

1. **Deterministic pre-pass** (these feed the hunters; they catch the
   dependency-supply and signal-class seeds on their own):

   ```bash
   python3 "$BH" --root . hotspots   # rank files by likelihood-of-defect
   python3 "$BH" --root . signals    # aged TODOs, dead flags, config drift  -> dx-pain / product-ux
   python3 "$BH" --root . deps       # unpinned / no-lockfile / typosquat     -> dependency-supply
   ```

   Note the subcommands take `--root .` (a flag), not a positional path.

2. **Run the agent hunt** over this directory:

   ```
   /bughunt .
   ```

   The hunters produce a raw findings document (schema `finding.schema.json`); save it as
   `.bughunt/raw-findings.json`. Every Critical/High must carry a `verified.verdict` from the
   adversarial verify phase.

3. **Merge + render** the findings. `merge` validates, fingerprints, dedupes, and writes the
   canonical `.bughunt/findings.json` (use `--fail-on none` so the eval never exits non-zero);
   `render` turns that into reports:

   ```bash
   python3 "$BH" --root . merge .bughunt/raw-findings.json --fail-on none
   python3 "$BH" --root . render .bughunt/findings.json --formats md,html,sarif
   ```

## Scoring

A reported finding **matches** an answer-key entry when ALL of:

- `lens` matches the key's `lens`, AND
- `file` matches the key's `file` (relative to the fixture root, forward slashes), AND
- the finding's `location.startLine` is within **±3** of the key's `line`.

Each key may be matched by **at most one** finding (first/best match wins; don't
let one report double-count two keys).

- **recall** = matched_keys / total_keys (29)
- **precision** = matched_findings / total_reported
- **FP rate** = (reported findings that match NO key AND are not a real extra bug
  you confirm) / total_reported

### Targets

- **recall ≥ 80%** (≥ 24 of 29 keys matched)
- **FP rate < 20%**
- Every reported **Critical / High** finding carries `verified.verdict: "upheld"`
  (refuted/uncertain Criticals/Highs count against the run).

Some over-reporting is fine: if the hunt flags something that is NOT in the
answer key but you confirm it is a *genuine* defect, it does **not** count as a
false positive — note it as a real extra and (optionally) add it to the answer
key. The fixture is intentionally small and readable, so this is easy to adjudicate
by eye.

### Tiny scoring recipe

Eyeball-friendly, but here is a few-line scorer that compares
`.bughunt/findings.json` to `answer-key.json` by lens + file + line proximity:

```python
#!/usr/bin/env python3
import json

key = json.load(open("answer-key.json"))
doc = json.load(open(".bughunt/findings.json"))
findings = doc["findings"] if isinstance(doc, dict) else doc

TOL = 3
matched_keys = set()
matched_findings = set()

for fi, f in enumerate(findings):
    loc = f.get("location", {})
    ff, fl, flens = loc.get("file"), loc.get("startLine"), f.get("lens")
    for k in key:
        if k["id"] in matched_keys:
            continue
        if k["lens"] == flens and k["file"] == ff and abs(k["line"] - (fl or -999)) <= TOL:
            matched_keys.add(k["id"])
            matched_findings.add(fi)
            break

total_keys = len(key)
total_reported = len(findings)
recall = len(matched_keys) / total_keys if total_keys else 0
precision = len(matched_findings) / total_reported if total_reported else 0
fp_rate = (total_reported - len(matched_findings)) / total_reported if total_reported else 0

print(f"matched {len(matched_keys)}/{total_keys} keys")
print(f"recall    = {recall:.0%}")
print(f"precision = {precision:.0%}")
print(f"FP rate   = {fp_rate:.0%}  (before crediting confirmed real extras)")
missed = [k["id"] + " " + k["lens"] for k in key if k["id"] not in matched_keys]
if missed:
    print("missed:", ", ".join(missed))
```

Run it from the fixture root after a hunt:

```bash
python3 score.py   # if you save the snippet above as score.py
```

Then hand-adjudicate the unmatched reported findings: each is either a real extra
bug (does not count against FP rate) or a true false positive.

## Per-lens coverage

| lens                 | planted | bug ids                         |
|----------------------|---------|---------------------------------|
| dataflow-taint       | 2       | BUG-003, BUG-004                |
| state-lifecycle      | 2       | BUG-014, BUG-017                |
| concurrency          | 2       | BUG-015, BUG-016                |
| boundaries-numeric   | 2       | BUG-007, BUG-009                |
| error-failure        | 2       | BUG-001, BUG-006                |
| contract-spec        | 2       | BUG-011, BUG-021                |
| auth-access          | 2       | BUG-002, BUG-005                |
| logic-correctness    | 2       | BUG-008, BUG-010                |
| resource-performance | 2       | BUG-012, BUG-013                |
| dx-pain              | 4       | BUG-024, BUG-025, BUG-026, BUG-027 |
| product-ux           | 3       | BUG-018, BUG-019, BUG-020       |
| dependency-supply    | 2       | BUG-028, BUG-029                |
| data-migration       | 2       | BUG-022, BUG-023                |
| **total**            | **29**  |                                 |
