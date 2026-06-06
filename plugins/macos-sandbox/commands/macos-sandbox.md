---
description: Smoke-test a macOS .app/.pkg in a disposable Tart VM — launch, logs, screenshots, crashes
---

Smoke-test in a sandbox VM: **$ARGUMENTS**

Load and follow the **macos-sandbox** skill at `${CLAUDE_PLUGIN_ROOT}/skills/macos-sandbox/SKILL.md`:
use the macbox CLI or MCP to upload the build to a disposable Tart VM, launch it, and collect
logs, screenshots, and crash reports; drive guest automation as needed; report what happened.

If $ARGUMENTS is empty, ask for the path to the `.app`/`.pkg` to test.
