---
description: Hunt for hidden bugs across a codebase or target and report ranked, reproducible findings (report-only)
---

Run a bug hunt against: **$ARGUMENTS**

Load and follow the **bughunt** skill at `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/SKILL.md` exactly:

1. **Recon & scope** — detect platform, map trust boundaries, rank hotspots, build a hunt plan. On a large/unfamiliar repo, confirm scope with the user first.
2. **Fan out** — build the (lens × hotspot) grid and dispatch parallel hunters (or run the sequential fallback). Give each hunter its lens's smell list + the evidence contract.
3. **Merge & cross-validate** — dedupe, cluster, and boost confidence when two lenses agree.
4. **Triage** — assign severity × confidence, filter false positives, build minimal repros (use the triage skill at `${CLAUDE_PLUGIN_ROOT}/skills/triage/SKILL.md`).
5. **Report** — emit the ranked, evidence-backed report.

This is **report-only**: surface and prove bugs, do not edit code unless I ask. If $ARGUMENTS is empty, ask what to hunt (whole repo, a module, or a diff) and which depth (quick scan vs deep hunt).
