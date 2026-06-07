---
description: Fast bughunt variant — fan out Composer 2.5 / Grok hunters via the Cursor CLI (cursor-agent), with the skeptic pass kept on a strong reasoner. Report-only.
argument-hint: "[scope] [quick|deep] [hunt-model] — e.g. \"the sync engine deep\", \"src/api\", \"deep composer-2.5\""
---

Run a **fast** bug hunt against: **$ARGUMENTS**

Same hunt, faster substrate: the `(lens × hotspot)` grid is fanned out by the **Cursor CLI**
(`cursor-agent`) on a fast model (Composer 2.5 / Grok) instead of the Workflow tool, while the
mandatory skeptic pass stays on a **strong reasoner** (Opus 4.8). This is **Rung A-CLI** of the
capability ladder — usable inside Cursor, Claude Code, or any shell with `cursor-agent` on PATH.

Load and follow the **bughunt** skill at `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/SKILL.md` exactly,
selecting the **Rung A-CLI** path in [orchestration.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/orchestration.md).

Parse `$ARGUMENTS` for **scope** (`diff` · `staged` · a path · a module · empty = whole repo),
**depth** (`quick` · `deep`, default `deep`), and an optional **hunt-model** id (default
`composer-2.5`; discover ids with `cursor-agent --list-models`).

Then run the loop:

1. **Preflight** — confirm `cursor-agent` is on PATH (`cursor-agent --version`) and auth is set
   (`CURSOR_API_KEY` or a prior `cursor-agent login`). If it is **not** available, fall back to
   the standard `/bughunt` rungs (Workflow / Tasks / sequential) and say so.
2. **Recon & pre-pass** — detect platform, map trust boundaries, and run the deterministic
   pre-pass: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py census`,
   `hotspots`, `signals`, `deps` (see [tooling.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/tooling.md)).
   On a large/unfamiliar repo, confirm scope first.
3. **Build the grid** — form `cells: [{ lens, platform, area, files, lensPath, platformPath }]`
   (absolute spoke paths under `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/`) and write `cells.json`.
4. **Hunt + Verify (one command)** —
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/hunt-cursor.mjs \
       --cells cells.json --workspace "$PWD" \
       --hunt-model composer-2.5 --verify-model claude-opus-4-8-thinking-high \
     | python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py merge - \
         --require-verified --require-coverage --strict --write-baseline
   ```
   Hunters are **read-only** (`--mode ask`, never `--force`). Keep the verify model strong — do
   not move the skeptic pass to the fast model.
5. **Report** — `python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py render .bughunt/findings.json`
   emits ranked markdown (+ HTML + SARIF) into `.bughunt/`.

This is **report-only**: surface and prove bugs, do not edit code unless I ask. To then prove
high-value Probable findings at runtime in parallel sandboxes, see the optional Confirm rung in
[confirm.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/confirm.md). If $ARGUMENTS is empty, ask what
to hunt and which depth.
