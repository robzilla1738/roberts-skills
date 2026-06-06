# macOS Sandbox (macbox)

Smoke-test macOS `.app` and `.pkg` builds in disposable Tart VMs using the [macbox](https://github.com/robzilla1738/macbox) CLI or MCP server — upload artifacts, launch, capture screenshots/logs/crashes, run guest automation, then reset or destroy the sandbox.

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

**Upstream:** [macbox `skills/macos-sandbox/`](https://github.com/robzilla1738/macbox/tree/main/skills/macos-sandbox) on `main`

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Full macbox workflow: prerequisites, CLI/MCP steps, guest tools, safety rules |

## Prerequisites (host)

1. [Tart](https://tart.run/) and a prepared base image (e.g. `macos-sequoia-clean`)
2. SSH key `~/.ssh/macbox_id` authorized for guest `admin`
3. macbox installed — see the [macbox README](https://github.com/robzilla1738/macbox) for CLI setup and MCP config

## Install

### 1. Copy the folder

Copy this entire `macos-sandbox` directory into your assistant's skills location.

**Personal scope** (available in every project):

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/macos-sandbox/` |
| Codex | `~/.agents/skills/macos-sandbox/` |
| Cursor | `~/.cursor/skills/macos-sandbox/` |

**Project scope** (shared with anyone who clones the repo):

```
<project>/.<your-assistant>/skills/macos-sandbox/
```

### 2. Verify the layout

```
macos-sandbox/
  SKILL.md
  README.md
```

### 3. Confirm your assistant sees it

Restart the assistant or reload skills if your tool requires that. Attach the folder or mention macbox / macOS sandbox testing in your prompt.

## Use it

```text
Smoke-test MyApp.app in a macbox sandbox and report launch status, logs, and any crashes.
```

```text
Use the macos-sandbox skill: upload the pkg, run smoke test, screenshot, then destroy the VM.
```

The agent should follow the skill workflow (doctor → sandbox → upload → test → collect evidence → destroy) and summarize artifacts under `~/.macbox/runs/<run_id>/`.

## When to use it

- After building a macOS app or installer locally
- When you need an isolated guest to reproduce launch failures
- Before shipping a build that must not touch your host environment

## Updating

Replace this folder when [macbox `skills/macos-sandbox/SKILL.md`](https://github.com/robzilla1738/macbox/blob/main/skills/macos-sandbox/SKILL.md) changes on `main`. Compare the `version` field in `SKILL.md` front matter.

Current version: `2026-06-03.1` (synced from macbox `main`, commit `fa06486`).

## Notes

- Skill id is `macos-sandbox`; the tool is **macbox**.
- `disable-model-invocation: true` — loads on explicit request, not every message.
- Do not upload secrets, SSH keys, or `.env` files into guests.
