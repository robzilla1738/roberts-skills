# macOS Notch

Design and implement macOS Dynamic Island / notch-style apps: transparent top-center panel, hardware-aligned geometry, state machine, and module widgets (media, HUD, shelf, agents, camera).

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

**Upstream patterns:** Public OSS on [macbook-notch](https://github.com/topics/macbook-notch); primary reference [boring.notch](https://github.com/TheBoredTeam/boring.notch) (GPL-3.0 — patterns only).

---

## What you get

Hub-and-spoke layout:

| File | Role |
| --- | --- |
| `SKILL.md` | Hub — read first; routes to spokes |
| `ecosystem-landscape.md` | OSS audit, taxonomy, licenses |
| `foundations.md` | NSPanel, geometry, shape, state machine |
| `interactions-and-motion.md` | Hover, drag, animation |
| `visual-system.md` | Closed/open visual language |
| `module-*.md` | Per-widget deep dives |
| `integration-shipping.md` | Menu bar, prefs, QA, build order |

## Install

Copy the entire `macos-notch` directory into your assistant's skills location.

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/macos-notch/` |
| Codex | `~/.agents/skills/macos-notch/` |
| Cursor | `~/.cursor/skills/macos-notch/` |

Invoke explicitly (e.g. attach the skill or mention `/macos-notch`).

## Use it

```text
/macos-notch — design a notch-style app with media controls and a file shelf
```

```text
Review my notch panel: hover timing, focus stealing, and external display behavior
```

## Updating

Replace this folder when a new version is published. Compare `version` in `SKILL.md` front matter.

Current version: `2026-06-03.1`

## Notes

- Formerly a single spoke inside **macos-design** (`notch-effect.md`); now a dedicated skill.
- `disable-model-invocation: true` — loads on explicit request.
