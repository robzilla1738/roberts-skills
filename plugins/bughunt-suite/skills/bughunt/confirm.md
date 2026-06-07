# Confirm — the optional E2B-backed runtime proof rung

Hunt and the static skeptic pass earn a finding at most **Probable**: traced end-to-end but
not executed. **Confirmed** is reserved for runtime/property-test proof (see
[verification.md](verification.md) and the [triage](../triage/SKILL.md) rubric). This spoke is
the **optional** Confirm step (hunt-loop step 7) done in **parallel isolated E2B sandboxes** —
the one place in the hunt where a sandbox actually belongs.

## Why E2B only here

Hunt and static-Verify are **read-only static analysis** — they read code and reason; they run
nothing, so an isolated sandbox buys them nothing (and a sandbox per hunter would pay for
unused isolation plus a repo sync per cell). **Confirm runs untrusted repro/fuzz code** to make
a bug fire — exactly what a throwaway microVM is for. Running it across findings in parallel
both speeds the tail up and lets you confirm more findings at once.

This rung is **strictly opt-in**. Without it, the hunt is complete and honest — Probable
findings simply stay Probable, and you can confirm by hand with [fuzz](../fuzz/SKILL.md) /
`verify`. Use it when you have several high-value Probable findings worth proving fast.

## Division of labour

- **The agent (or [fuzz](../fuzz/SKILL.md)) writes the repro.** Turning a finding into runnable
  code — the setup commands and the one command whose exit code decides the verdict — is a
  judgment task. The agent supplies these via a **repro-map** JSON keyed by finding `id` or
  `fingerprint`.
- **`scripts/confirm-e2b.py` is the execution substrate.** It spins one ephemeral sandbox per
  finding, syncs the repo, runs setup + the repro, maps the exit code to a verdict, and stamps
  the finding's `verified` with a **dynamic** method. It owns isolation, parallelism, timeouts,
  and teardown — not judgment.

## The repro-map

```json
{
  "BH-001": {
    "setup": ["npm ci"],
    "cmd": "npx jest tests/idor.repro.test.js",
    "expect": "nonzero-means-bug",
    "method": "failing-test"
  }
}
```

- `setup` — commands to prepare the repo (install, build). Each must exit 0 or the finding is
  left `uncertain` with the failure noted.
- `cmd` — the single command whose exit code is the verdict.
- `expect` — `nonzero-means-bug` (a failing test proves the defect) or `zero-means-bug`.
- `method` — the dynamic verdict method to stamp: `failing-test` | `runtime-repro` |
  `property-test` (these are what earn **Confirmed**).

A finding with no repro-map entry is **left Probable** (recorded, not blocked).

## Running it

```bash
# repo synced via git clone inside each sandbox
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/confirm-e2b.py .bughunt/findings.json \
    --repro-map repros.json --repo-url https://github.com/you/repo --repo-ref main \
  | python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py merge - \
      --require-verified --require-coverage --strict --write-baseline

# re-render with the upgraded verdicts
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py render .bughunt/findings.json
```

The script reads a **merged** findings document, runs the selected repros, sets
`verified = {by:"e2b-confirm", method:"<dynamic>", verdict:"upheld|refuted|uncertain", note}`,
and prints a findings document you pipe **back into `merge`**. Merge re-routes the verdicts:
upheld-with-runtime-proof re-labels to **Confirmed**, repros that don't fire flip to
**refuted** (→ transparency appendix), and ambiguous ones stay **uncertain** (Speculative).
No merge/schema changes are needed — the `verified.method` enum already includes the dynamic
values.

### Selection

By default it targets **Critical/High** findings that are not already runtime-confirmed (tune
with `--severity`, or `--all`). Only those with a repro-map entry actually execute.

### Repo sync, fastest first

- `--template <id>` — an E2B template/snapshot with the repo + toolchain **pre-baked**. Fork
  per finding; skips per-sandbox clones. **Recommended** for repeated runs.
- `--repo-url [--repo-ref]` — `git clone --depth 1` inside each sandbox.

## Guardrails (E2B bills per second)

A stalled repro is a real cost, so the script enforces:

- **`--timeout`** (default 300s) — a hard per-sandbox ceiling; the sandbox is created with it
  and every command inherits it.
- **`--concurrency`** (default 4) — cap on parallel sandboxes. E2B Hobby allows 20 concurrent;
  stay well under your plan's limit.
- **Always-teardown** — each sandbox is `kill()`-ed in a `finally`, even on error/timeout.
- **No secret upload** — only the repo you point it at enters the sandbox.

## Degrade

Requires `pip install e2b` and an `E2B_API_KEY`. With **neither**, or in `--dry-run`,
`confirm-e2b.py` prints a clear notice and passes the findings through **unchanged with exit 0**
— the pipeline is never blocked and the Confirm step falls back to manual
[fuzz](../fuzz/SKILL.md) + `verify`. `--dry-run` also previews *which* findings would be
confirmed (stamping them `uncertain` with the intended dynamic method) without creating any
sandbox — used by `selftest.py` to keep CI offline.

## Related

- [fuzz](../fuzz/SKILL.md) — builds the property-test repro this rung executes; can also run
  locally without E2B.
- [verification.md](verification.md) — the static skeptic pass that precedes Confirm; its
  `verified` contract is what this rung upgrades.
- [triage](../triage/SKILL.md) — the Confirmed/Probable/Speculative rubric this rung moves
  findings through.
