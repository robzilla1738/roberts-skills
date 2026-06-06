---
name: macos-notch
description: >
  Design and implement macOS Dynamic Island / notch-style apps: NSPanel,
  hardware-aligned geometry, state machine, module widgets (agent monitor,
  media, HUD, shelf, camera). Use for /macos-notch or notch-style macOS UI.
disable-model-invocation: true
version: 2026-06-03.2
platforms: [macOS, SwiftUI, AppKit]
primary_use_cases:
  - Scaffold a notch-style macOS utility with NSPanel and SwiftUI
  - Add or review a specific notch module (media, HUD, shelf, agents)
  - Compare OSS notch apps and choose an architecture
  - Critique notch alignment, motion, and menu-bar fallback
---

# macOS Notch

Hub skill for designing and implementing **notch-style macOS apps**: a top-center, hardware-aligned black shell that expands into useful modules — Dynamic Island behavior on MacBook displays.

Read this file first, then open only the spoke files relevant to the task.

## Mission

Create a notch utility that feels like **display hardware with context**, not a floating widget. The closed state should merge with the camera housing (or a centered pill on non-notch displays). The open state grows **downward** from a pinned top edge with calm spring motion.

## Non-negotiables

1. **Use a transparent nonactivating `NSPanel`** for the shell — not a titled document window. See [foundations.md](foundations.md).
2. **Separate AppKit positioning from SwiftUI content** — geometry and screen changes stay out of views.
3. **State machine over boolean soup** — closed, peek, open, expanded, dragging. See [foundations.md](foundations.md) and [module-peek-transient.md](module-peek-transient.md).
4. **Black closed shell** — no translucent glass on the hardware edge. See [visual-system.md](visual-system.md).
5. **Menu bar fallback** — notch may be unavailable on external displays. See [integration-shipping.md](integration-shipping.md).
6. **GPL caution** — [TheBoredTeam/boring.notch](https://github.com/TheBoredTeam/boring.notch) is GPL-3.0. Study patterns via [ecosystem-landscape.md](ecosystem-landscape.md); do not copy source into proprietary apps without compliance.
7. **Not physical-notch masking** — hiding the hardware notch (znotch-style) is a different product category. See [ecosystem-landscape.md](ecosystem-landscape.md).

## When to use this skill

- Building or reviewing a Dynamic Island / notch utility for macOS
- Adding a module (media, HUD, shelf, agents, camera) to an existing notch app
- Auditing alignment, hover timing, or focus-stealing behavior

## When not to use

- Standard document-based macOS apps — see the **macos-design** skill (its `layout-and-windowing.md` spoke)
- Hiding the physical notch without a panel app — see [ecosystem-landscape.md](ecosystem-landscape.md)
- Linux/GNOME notch clones — out of scope

## Topic router

| If the task involves… | Read |
|-----------------------|------|
| OSS landscape, licenses, picking an archetype | [ecosystem-landscape.md](ecosystem-landscape.md) |
| NSPanel, geometry, shape, state machine | [foundations.md](foundations.md) |
| Hover, drag, drop, springs, root view | [interactions-and-motion.md](interactions-and-motion.md) |
| Closed/open visual language, materials | [visual-system.md](visual-system.md) |
| Now playing / music | [module-media-now-playing.md](module-media-now-playing.md) |
| Volume, brightness, system HUD | [module-system-hud.md](module-system-hud.md) |
| Short-lived peeks and live activity | [module-peek-transient.md](module-peek-transient.md) |
| File drag shelf | [module-file-shelf.md](module-file-shelf.md) |
| Calendar glance | [module-calendar-glance.md](module-calendar-glance.md) |
| Camera mirror preview | [module-camera-mirror.md](module-camera-mirror.md) |
| Coding-agent session monitor | [module-agent-monitor.md](module-agent-monitor.md) |
| Menu bar, prefs, a11y, QA, launch | [integration-shipping.md](integration-shipping.md) |

## Common task bundles

| Task | Spokes to read |
|------|----------------|
| New notch app (MVP) | foundations → interactions-and-motion → visual-system → integration-shipping |
| One module only | foundations (skim) → relevant `module-*.md` |
| Agent status notch | ecosystem-landscape → foundations → module-agent-monitor → integration-shipping |
| Media + HUD utility | foundations → module-media-now-playing → module-system-hud → module-peek-transient |
| Design critique | visual-system → interactions-and-motion → integration-shipping (checklist) |
| OSS / license question | ecosystem-landscape |

## Spoke index

| File | Contents |
|------|----------|
| [ecosystem-landscape.md](ecosystem-landscape.md) | Public repos, taxonomy, GPL note, module map |
| [foundations.md](foundations.md) | Mental model, file tree, NSPanel, geometry, shape, state |
| [interactions-and-motion.md](interactions-and-motion.md) | Root view, hover/tap/drag, animation rules |
| [visual-system.md](visual-system.md) | Closed/open layout, color, materials |
| [module-media-now-playing.md](module-media-now-playing.md) | Music module |
| [module-system-hud.md](module-system-hud.md) | System HUD replacement |
| [module-peek-transient.md](module-peek-transient.md) | Peek kinds, timing, compact chips |
| [module-file-shelf.md](module-file-shelf.md) | File shelf / drop |
| [module-calendar-glance.md](module-calendar-glance.md) | Calendar glance |
| [module-camera-mirror.md](module-camera-mirror.md) | Camera mirror |
| [module-agent-monitor.md](module-agent-monitor.md) | Agent/coding-tool monitor |
| [integration-shipping.md](integration-shipping.md) | Menu bar, prefs, edge cases, checklist, build order |

## Related skills

- the **macos-design** skill (separate plugin) — general native macOS design (windows, HIG, Liquid Glass)
- **macos-design** spoke `appkit-patterns.md` — AppKit panels and safe areas
- **macos-design** spoke `accessibility.md` — Reduce Motion, permissions
