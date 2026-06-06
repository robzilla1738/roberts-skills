---
description: Triage a suspected bug or a set of findings — severity × confidence, minimal repro, standard report
---

Triage: **$ARGUMENTS**

Load and follow the **triage** skill at `${CLAUDE_PLUGIN_ROOT}/skills/triage/SKILL.md`:

- Demand evidence (location, trace, trigger, impact) — anything without it is a question, not a finding.
- Assign **severity** (Critical/High/Medium/Low) × **confidence** (Confirmed/Probable/Speculative).
- For Critical/High items, build a **minimal reproduction** or failing test (cheapest first).
- Aggressively filter false positives; quarantine speculative items.
- Emit the standard finding schema / report layout.

Report-only — assess and prove, don't fix. If $ARGUMENTS is empty, ask for the bug or findings to triage.
