---
description: Hunt for hidden bugs, pain points, and inefficiencies across a codebase and report ranked, reproducible, baseline-diffed findings (report-only)
argument-hint: "[scope] [quick|deep] [ci] — e.g. \"the sync engine deep\", \"diff\", \"staged quick\", \"src/api\", \"ci\""
---

Run a bug hunt against: **$ARGUMENTS**

Load and follow the **bughunt** skill at `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/SKILL.md` exactly. Parse `$ARGUMENTS` for:

- **Scope** — `diff` (vs the merge base) · `staged` (git-staged changes) · a path like `src/api` · a named module · empty = whole repo.
- **Depth** — `quick` (a handful of cells, fast) · `deep` (full fan-out; the default for a whole-repo hunt).
- **`ci`** — non-interactive mode: don't ask the user anything, and surface the `bughunt.py merge` exit code (0 clean / 1 new Critical-High / 2 new Medium-Low) so a pipeline can gate on it.

Then run the loop:

1. **Recon & pre-pass** — detect platform and map trust boundaries. When `python3` is available, run the deterministic pre-pass for ranked targets: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py census`, `hotspots`, `signals`, `deps` (see [tooling.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/tooling.md)). On a large/unfamiliar repo, confirm scope first (skip the prompt under `ci`).
2. **Fan out** — build the (lens × hotspot) grid and dispatch hunters via the capability ladder in [orchestration.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/orchestration.md): the shipped Workflow script if available, else parallel Tasks, else a sequential walk. Hunters return findings as JSON.
3. **Verify (mandatory)** — a skeptic pass tries to refute every candidate before it reaches the report ([verification.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/verification.md)).
4. **Merge & triage** — pipe findings through `bughunt.py merge` (fingerprint, dedupe, cross-validate, suppress, baseline-diff) and score with the [triage](${CLAUDE_PLUGIN_ROOT}/skills/triage/SKILL.md) rubrics.
5. **Report** — `bughunt.py render` emits the ranked markdown (+ HTML + SARIF) into `.bughunt/`.

This is **report-only**: surface and prove bugs, do not edit code unless I ask. If `python3` is unavailable, follow the markdown fallback (no scripts; findings stay in markdown). If $ARGUMENTS is empty, ask what to hunt (whole repo, a module, or a diff) and which depth.
