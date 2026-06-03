# Design skills

Agent skills for design work: reviewing interfaces, writing specs, and scaffolding UI that fits its platform.

## Skills in this category

| Skill | Version | What it covers |
| --- | --- | --- |
| [macOS Design](macos-design/) | 2026-05-28 | Native macOS app design and critique. HIG, Liquid Glass, menus, toolbars, sidebars, inspectors, safe areas, accessibility, SwiftUI and AppKit patterns. |
| [Web Marketing Landing](web-marketing-landing/) | 2026-06-02 | Premium SaaS marketing home page — aurora hero, glass nav, connector hub, bento grid, comparison/FAQ bands, CSS-driven motion (Next.js + Tailwind v4). |

## Replication guides

Portable, project-agnostic write-ups (from `/documenter`). Search the full catalog in [INDEX.md](../INDEX.md).

| Platform | Guide | Summary |
| --- | --- | --- |
| iOS | [liquidglass-animation.md](iOS/liquidglass-animation.md) | Expanding Liquid Glass composer shell with + menu and slash-command panels |
| iOS | [ios-sidebar-slide.md](iOS/ios-sidebar-slide.md) | Sidebar underlay with foreground card slide, gesture-driven open/close |
| macOS | [macos_immersive_onboarding_guide.md](macos-design/macos_immersive_onboarding_guide.md) | Immersive first-launch onboarding wizard with blur, motion, and permission steps |

The [macOS Design](macos-design/) skill also ships [notch-effect.md](macos-design/notch-effect.md) as a reference module.

## Install

Each skill has its own README with setup steps. The pattern is the same:

1. Copy the skill folder (e.g. `macos-design/`) into your assistant's skills location.
2. Keep all files together — hub skills link to reference modules by relative path.
3. Invoke the skill explicitly in a prompt.

See the [root README](../README.md) for general compatibility notes.
