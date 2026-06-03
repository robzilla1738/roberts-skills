# Workflow skills

Agent skills for process and quality workflows: acceptance gates, session reviews, and end-of-task verification.

## Skills in this category

| Skill | Version | What it covers |
| --- | --- | --- |
| [Autoreview](autoreview/) | 2026-05-28.1 | Hard acceptance gate before marking work complete. Reviews all session changes for production quality across correctness, architecture, maintainability, security, testing, and cleanup. |
| [macOS Sandbox](macos-sandbox/) | 2026-06-03.1 | Smoke-test `.app`/`.pkg` in disposable Tart VMs via [macbox](https://github.com/robzilla1738/macbox) CLI or MCP — upload, launch, logs, screenshots, crashes, guest automation. |

## Install

Each skill has its own README with setup steps. The pattern is the same:

1. Copy the skill folder (e.g. `autoreview/`) into your assistant's skills location.
2. Keep all files together.
3. Invoke the skill explicitly in a prompt (e.g. `/review`).

Autoreview is also listed in [INDEX.md](../INDEX.md).

See the [root README](../README.md) for general compatibility notes.
