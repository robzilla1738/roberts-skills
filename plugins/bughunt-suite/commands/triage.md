---
description: Triage a suspected bug or a set of findings — severity × confidence, minimal repro, standard report
---

Triage: **$ARGUMENTS**

Load and follow the **triage** skill at `${CLAUDE_PLUGIN_ROOT}/skills/triage/SKILL.md`:

- Demand evidence (location, trace, trigger, impact) — anything without it is a question, not a finding.
- Assign **severity** (Critical/High/Medium/Low) × **confidence** (Confirmed/Probable/Speculative), scoring non-security findings against the **impact rubric** (dx/ux/performance/data-integrity/supply-chain), not just a security frame.
- For Critical/High items, build a **minimal reproduction** or failing test (cheapest first).
- Aggressively filter false positives; quarantine speculative items.
- Emit the standard finding schema / report layout. If you have findings as JSON (or a `.bughunt/findings.json`), pipe them through `python3 ${CLAUDE_PLUGIN_ROOT}/skills/bughunt/scripts/bughunt.py merge` then `render` to get the deduped, baseline-diffed markdown/HTML/SARIF report — see [tooling.md](${CLAUDE_PLUGIN_ROOT}/skills/bughunt/tooling.md).

Report-only — assess and prove, don't fix. If $ARGUMENTS is empty, ask for the bug or findings to triage.
