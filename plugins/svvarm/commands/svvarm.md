---
description: Opinionated design director — review, fix, or build frontend UI with zero AI slop
---

Design task: **$ARGUMENTS**

Load and follow the **svvarm** skill at `${CLAUDE_PLUGIN_ROOT}/skills/svvarm/SKILL.md`.
Route the request through its routing table: `init` and `setup` onboard a project,
`audit` runs the full quality review, anything else is a natural-language design
instruction (focused tasks read one deep reference; full builds read the core digest).

If $ARGUMENTS is empty, enter CDO mode: load `.svvarm/context.md` if it exists and ask
what we're working on; otherwise offer to run init or setup.
