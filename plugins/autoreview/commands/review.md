---
description: Hard acceptance gate — review all session changes for production quality before marking work done
---

Run the production-quality acceptance review.

Load and follow the **autoreview** skill at `${CLAUDE_PLUGIN_ROOT}/skills/autoreview/SKILL.md`:
review every change made this session for correctness, code quality, architecture,
maintainability, security/reliability, and testing; fix any shortcuts or tech debt found;
run available lint/typecheck/test/build commands; and end with a concise review summary
including any remaining risks.

$ARGUMENTS
