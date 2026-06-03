# Web Marketing Landing

Agnostic agent skill for building a premium SaaS marketing home page: aurora hero, scroll-driven glass nav, connector hub, bento grid, comparison bands, and CSS-only motion.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Hub — mission, section blueprint, routing, greenfield checklist |
| `foundations.md` | Tokens, typography, card/button utilities |
| `layout-sections.md` | Section order, grids, spacing |
| `hero-aurora.md` | Hero panel, backdrop, feature cards, orbit |
| `shell-and-nav.md` | Marketing shell, scroll nav, footer |
| `connector-hub.md` | 5×3 integration grid |
| `motion-and-effects.md` | CSS keyframes, glass, washes |
| `section-components.md` | Bento, comparison, FAQ, previews |
| `stack-and-scaffold.md` | Next.js + Tailwind v4 file tree |
| `seo-metadata.md` | Metadata and JSON-LD |

## Install

Copy the entire `web-marketing-landing` folder into your assistant's skills location.

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/web-marketing-landing/` |
| Codex | `~/.agents/skills/web-marketing-landing/` |
| Cursor | `~/.cursor/skills/web-marketing-landing/` |

Invoke explicitly (e.g. attach the skill or mention `/web-marketing-landing`).

## Usage

1. Read `SKILL.md` and the spokes listed in its routing table.
2. Scaffold with `stack-and-scaffold.md` or port from a reference repo.
3. Implement sections in blueprint order; swap `{{Brand}}` / `{{AppUrl}}` placeholders.
4. Run production build and check reduced-motion behavior.

## Version

`2026-06-02.1` — see `SKILL.md` front matter.
