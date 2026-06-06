# macOS Notch Apps

Design and implement macOS Dynamic Island / notch-style apps — NSPanel, hardware-aligned
geometry, state machine, module widgets (media, HUD, file shelf, peek, calendar, camera,
agent monitor). Command: `/macos-notch`.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install macos-notch@roberts-skills
```

Then use `/macos-notch`.

### Cursor / Codex

```bash
cp -R plugins/macos-notch/skills/macos-notch ~/.agents/skills/   # Cursor + Codex
cp -R plugins/macos-notch/skills/macos-notch ~/.cursor/skills/   # Cursor
```

See [`skills/macos-notch/`](skills/macos-notch/) for the hub and reference spokes.

## Related

- [macos-design](../macos-design/) — general native macOS app design (`/macos-design`).
  Install it alongside this plugin for the full native-macOS pair.
