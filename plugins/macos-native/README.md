# macOS Native Design

Two skills for building native macOS experiences:

| Skill | Command | Covers |
| --- | --- | --- |
| `macos-design` | `/macos-design` | Native macOS app design — HIG, Liquid Glass, menus, toolbars, sidebars, safe areas, accessibility, SwiftUI/AppKit |
| `macos-notch` | `/macos-notch` | Dynamic Island / notch-style apps — NSPanel, geometry, state machine, module widgets |

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install macos-native@roberts-skills
```

Then use `/macos-design` or `/macos-notch`.

### Cursor / Codex

```bash
cp -R plugins/macos-native/skills/{macos-design,macos-notch} ~/.agents/skills/   # Cursor + Codex
cp -R plugins/macos-native/skills/{macos-design,macos-notch} ~/.cursor/skills/   # Cursor
```

See [`skills/macos-design/`](skills/macos-design/) and [`skills/macos-notch/`](skills/macos-notch/)
for the hubs and reference spokes.
