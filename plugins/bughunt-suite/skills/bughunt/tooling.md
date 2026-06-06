# Toolkit — bughunt.py

## What it is

`scripts/bughunt.py` is a zero-dependency python3 CLI (stdlib only — no pip install,
no virtualenv). It gives the hunt a **deterministic spine**: ranked targets instead of
wandering, structured findings instead of prose, fingerprinted dedupe, baseline diffing,
suppression, and md/HTML/SARIF reports + CI exit codes. The hunt stops being a vibe and
starts being reproducible.

Invoke it as:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py <subcommand>
```

**ALWAYS probe `python3 --version` first.** If python3 is absent, the skill degrades to the
**pure-markdown pipeline**: rank hotspots by the recon heuristics by hand, keep findings in
markdown, no SARIF, no baseline gate. Nothing in this file is required for that path — it is
strictly an accelerator. When python3 is present, prefer it; it replaces guesswork with data.

Global flags: `--root <dir>` (repo root, default cwd) and `--quiet` (suppress stderr
progress). Every subcommand emits JSON to stdout; `render` also writes report files.

## Subcommands

### census

```bash
python3 .../bughunt.py census [--functions] [--exclude <glob>...]
```

The pre-pass **map** of the target. Walks the tree (skipping `.git`, `node_modules`,
`vendor`, build output, etc.), classifies each file by language, and flags generated /
vendored / test files. Returns:

```
{ root, commit, files[{path, lang, bytes, loc, generated, vendored, tests}],
  languages{<lang>: {files, loc}}, totals{files, loc, bytes, codeFiles, testFiles} }
```

With `--functions` it adds `functions[]` — a heuristic shortlist of **pure-function
candidates** (`{file, name, startLine, endLine, params[], pure_guess}`) for handing to
`/fuzz`. Pure candidates are returned first; if none look pure, the first 50 are returned.

### hotspots

```bash
python3 .../bughunt.py hotspots [--top N] [--since "6 months ago"] [--exclude ...]
```

Ranks files by **likelihood-of-defect**, highest first. This is the deterministic version of
the recon "rank hotspots" step — it feeds the (lens × hotspot) grid directly. Returns:

```
{ gitAvailable, weights,
  hotspots[{path, score, churn, complexity, recency_days, boundary, test_gap, reasons[]}] }
```

Ranking is a weighted blend of **churn × complexity × recency × boundary × test-gap**:

| Signal | Weight | Meaning |
|--------|--------|---------|
| churn | **0.30** | commit count touching the file (git log) |
| complexity | **0.25** | stdlib proxy, see below |
| boundary | **0.20** | 1 if the path or first 4 KB hits a trust-boundary keyword (route/handler/auth/sql/parse/exec/…) |
| recency | **0.15** | newer last-touch ⇒ higher boost (linear decay over 365 days) |
| test_gap | **0.10** | 1 if no matching test file was found for the file's stem |

`complexity` is a **stdlib proxy**, not real cyclomatic complexity: branch-keyword density
(`if/for/while/case/catch/&&/||/?…`) + nesting depth (max indent) + LOC/40. It is a cheap
ranking signal, not a metric to report.

Off-git (zip, export, shallow clone) `gitAvailable` is `false`: churn drops to 0 and recency
falls back to file **mtime**. Use the manual recon heuristics to sanity-check the ordering.

### signals

```bash
python3 .../bughunt.py signals [--max-age-days N] [--exclude ...]
```

The **pain-point** pre-pass. Feeds `lens-dx-pain` and `lens-product-ux`. Returns:

```
{ gitAvailable, maxAgeDays,
  todos[{file, line, kind, text, ageDays, author, aged}],
  flags[{file, line, ref}],
  configDrift[{file, key, note}],
  longScripts[{path, kind, note}] }
```

- `todos` — `TODO/FIXME/HACK/XXX` markers. Age comes from `git blame` (capped at 400 blames
  so huge repos stay fast); `aged` is `true` when `ageDays >= --max-age-days` (default 180).
- `flags` — feature-flag / toggle references (capped at 300).
- `configDrift` — keys declared in `.env.example` but missing from `.env`/`.env.local`, and
  vice-versa (undocumented keys).
- `longScripts` — shell scripts over 300 lines and `package.json` scripts chaining ≥3 serial
  `&&` commands.

### deps

```bash
python3 .../bughunt.py deps [--osv]
```

Manifest / lockfile audit. **Offline by default.** Feeds `lens-dependency-supply`. Returns:

```
{ ecosystems[{manager, manifest, lockfile, locked}],
  deps[{name, version, manager, pinned, direct, issues[], typosquatOf?}],
  lockDrift[{name, note}], advisories[], osvQueried }
```

Offline issue codes: `UNPINNED`, `NO_LOCKFILE`, `LOCK_DRIFT`, `TYPOSQUAT_SHAPE` (edit-distance-1
from a popular package name), `DEPRECATED_MARKER`. Add `--osv` to **opt in** to a network
query against OSV.dev — it populates `advisories[{name, id, severity, source}]` and fails
soft (stays offline) if the request errors.

### merge

```bash
python3 .../bughunt.py merge <files...|-> [--baseline P] [--suppress P] \
    [--write-baseline] [--out P] [--fail-on critical-high|any|none] [--no-cluster]
```

The **CI gate** and the heart of the pipeline. Takes one or more hunter findings JSON files
(or `-` for stdin), and **owns**:

- **Validation** — the executable form of `schema/finding.schema.json`. Invalid findings are
  dropped with a stderr warning; merge **never aborts** on a bad finding.
- **Fingerprinting** — assigns a stable fingerprint to each finding (see below).
- **Dedupe** — collapses identical fingerprints, keeping the clearer write-up.
- **Cross-lens clustering** — when several *different* lenses flag the same bug at overlapping
  lines, collapses them into one primary finding carrying an `alsoFlaggedBy` list, with a
  convergence confidence bump and a `cross-validated` tag. This is what stops one bug being
  reported three times. `--no-cluster` keeps them separate (legacy: boost only, no merge).
- **Suppression** — mutes findings whose fingerprint is in `suppressions.json`.
- **Baseline diff** — marks each finding `new` vs `existing` against `baseline.json`, and
  lists `fixed` ones that disappeared.
- **Id renumbering** — stable severity-sorted `BH-001…` ids.

Output is the merged findings document (also written to `--out`, default
`.bughunt/findings.json`). `--write-baseline` snapshots the current set as the new baseline.

### render

```bash
python3 .../bughunt.py render <findings.json|-> [--formats md,html,sarif] \
    [--md P] [--html P] [--sarif P]
```

Turns a merged findings document into reports. Defaults to all three formats into `.bughunt/`.

- **md** — byte-compatible with the triage report layout (same finding blocks). This *is* the
  triage report; don't hand-write it when the toolkit is present.
- **html** — a single standalone file, no external assets, styled finding cards.
- **sarif** — SARIF **2.1.0** for GitHub code scanning (one rule per lens, fingerprints as
  `partialFingerprints`).

### diff

```bash
python3 .../bughunt.py diff <A> <B>
```

Fingerprint comparison of two findings runs. Returns:

```
{ new[], fixed[], unchanged[], counts{new, fixed, unchanged} }
```

Use it to answer "what changed since the last hunt?" without re-running the whole pipeline.

## State directory — `.bughunt/`

The hunted repo gets a `.bughunt/` directory. Two files are **agreed state — commit them**;
the rest are regenerated every run — **gitignore them**.

| File | Commit? | What it is |
|------|---------|-----------|
| `baseline.json` | **commit** | the agreed set of known findings; `merge` diffs against it so the gate only fires on *new* defects |
| `suppressions.json` | **commit** | `{"suppressions": [{"fingerprint": "…", "reason": "…"}]}` — add a fingerprint here to mute a by-design finding from both the gate and the report body |
| `findings.json` | gitignore | the merged run output |
| `report.md` / `report.html` / `report.sarif` | gitignore | rendered reports |

Add to `.gitignore`:

```gitignore
.bughunt/findings.json
.bughunt/report.*
```

## CI mode

`/bughunt ci` runs the pipeline **non-interactively** and surfaces `merge`'s exit code:
**0** clean, **1** new Critical/High, **2** new Medium/Low. A minimal CI shape:

```bash
ROOT=${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py

# 1. deterministic pre-pass
python3 "$ROOT" hotspots --top 20 > hotspots.json
python3 "$ROOT" signals  > signals.json

# 2. drive the hunt -> one or more hunter findings JSON files (hunters/*.json)

# 3. gate: merge against the committed baseline, fail on new Critical/High
python3 "$ROOT" merge hunters/*.json --fail-on critical-high
GATE=$?   # 0 clean / 1 new crit-high / 2 new med-low

# 4. render SARIF and upload it to GitHub code scanning
python3 "$ROOT" render .bughunt/findings.json --formats sarif
# - uses: github/codeql-action/upload-sarif@v3
#   with: { sarif_file: .bughunt/report.sarif }

exit $GATE
```

## Fingerprints & baselines

A finding's fingerprint is `sha256(lens + NUL + relpath + NUL + normalized-snippet)[:16]`
(`NUL` = the `\x00` byte, a separator so the parts can't bleed into each other). The snippet is
**normalized** before hashing — whitespace collapsed and string/number literals replaced — so
the fingerprint **survives line shifts and reformatting**. That stability is exactly what
makes baseline diffing and suppression hold up across edits: refactor the file, move the
function down 40 lines, reflow it, and the same bug keeps the same fingerprint. (If the
snippet can't be read, the title is used as the basis instead.)

## Self-test

`scripts/selftest.py` exercises the whole pipeline (census → hotspots → signals → deps →
merge → render → diff). Run it after editing `bughunt.py`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/selftest.py
```
