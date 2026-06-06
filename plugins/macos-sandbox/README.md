# macOS Sandbox

Smoke-test macOS `.app`/`.pkg` builds in disposable Tart VMs via the
[macbox](https://github.com/robzilla1738/macbox) CLI or MCP — upload, launch, logs,
screenshots, crashes, and guest automation.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install macos-sandbox@roberts-skills
```

Then use `/macos-sandbox`.

### Cursor / Codex

```bash
cp -R plugins/macos-sandbox/skills/macos-sandbox ~/.agents/skills/   # Cursor + Codex
cp -R plugins/macos-sandbox/skills/macos-sandbox ~/.cursor/skills/   # Cursor
```

See [`skills/macos-sandbox/`](skills/macos-sandbox/) for the full workflow. Requires the macbox
CLI or MCP server on a macOS host.
