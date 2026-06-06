# macOS Design

Hub-and-spoke skill for designing, critiquing, and scaffolding native macOS applications.

Covers Human Interface Guidelines, Liquid Glass, menus and toolbars, safe areas, accessibility, and SwiftUI/AppKit patterns. Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Hub. Read this first. Routes the agent to the right reference files. |
| `foundations.md` | App archetypes, principles, onboarding, privacy |
| `layout-and-windowing.md` | Windows, split views, sidebars, inspectors, safe areas |
| `navigation.md` | Sidebar, tab, and segmented navigation; search; input |
| `toolbars-and-menus.md` | Toolbars, menus, shortcuts, context menus, menu bar extras |
| `liquid-glass.md` | Liquid Glass placement and restraint |
| `icons-and-visual-language.md` | Typography, color, SF Symbols, icons, motion |
| `accessibility.md` | VoiceOver, keyboard, contrast, localization |
| `swiftui-patterns.md` | SwiftUI shells, NavigationSplitView, commands |
| `appkit-patterns.md` | AppKit split views, responder chain, Mac Catalyst |
| *(moved)* | Notch-style apps → [macos-notch](../macos-notch/SKILL.md) skill |
| `macos_immersive_onboarding_guide.md` | Immersive first-launch onboarding wizard (blur, motion, permissions) |
| `critique-checklists.md` | Audit checklists, anti-patterns, output templates |

Keep the whole folder intact. The hub links to spoke files by relative path.

## Install

### 1. Copy the folder

Copy this entire `macos-design` directory into your assistant's skills location.

**Personal scope** (available in every project):

```
~/.<your-assistant>/skills/macos-design/
```

**Project scope** (shared with anyone who clones the repo):

```
<project>/.<your-assistant>/skills/macos-design/
```

Some tools use `.agents/skills/` instead of a dot-prefixed folder. Check your assistant's docs for the exact path. The requirement is the same: a directory named `macos-design` containing `SKILL.md` and the reference files beside it.

### 2. Verify the layout

```
macos-design/
  SKILL.md
  foundations.md
  layout-and-windowing.md
  navigation.md
  toolbars-and-menus.md
  liquid-glass.md
  icons-and-visual-language.md
  accessibility.md
  swiftui-patterns.md
  appkit-patterns.md
  notch-effect.md          # redirect → ../macos-notch/
  critique-checklists.md
```

### 3. Confirm your assistant sees it

Restart the assistant or reload skills if your tool requires that. Open a new session and check that `macos-design` appears in your skills list, or attach the folder manually.

## Use it

```text
Use the macos-design skill to design a document-based note app with a sidebar and inspector.
```

```text
Review this SwiftUI layout against macos-design. Focus on toolbar grouping and Liquid Glass usage.
```

```text
/macos-design scaffold a settings window for a menu bar extra app
```

The agent should read `SKILL.md` first, then open only the spoke files relevant to your task (usually one to three, not all eleven).

## Typical workflows

**New app design spec** — product intent, window model, navigation, menus, layout, visual system, accessibility, implementation plan.

**UI critique** — review existing code or mockups against the skill's checklists.

**SwiftUI or AppKit scaffold** — layout scaffolding from `swiftui-patterns.md` or `appkit-patterns.md`.

## Updating

Replace your local copy of the whole `macos-design` folder when a new version is published. Compare the `version` field in `SKILL.md` front matter.

Current version: `2026-05-28.1`

## Notes

- Written for LLM agents. Not a replacement for Apple's Human Interface Guidelines or testing in the latest Xcode.
- Assumes current macOS design language (including Liquid Glass) with availability checks for newer APIs.
- `disable-model-invocation: true` in front matter means the skill loads on explicit request, not every message. Remove that line if you want ambient auto-loading and your tool supports it.
