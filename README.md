# Robert's Skills

Provider-agnostic agent skills for AI coding assistants.

Each skill is a folder of markdown files that teach an agent how to do one kind of work well: design review, native UI scaffolding, domain-specific workflows. Plain files, no lock-in. Copy a folder into wherever your assistant loads skills and use it.

**Author:** [Robert Courson](https://robertcourson.com) · [robertcourson.com](https://robertcourson.com)

---

## Why these exist

Most assistants can write code. Fewer of them know how to design a macOS app that actually feels native, or when to stop before every panel turns into Liquid Glass. Skills fix that gap by giving the agent a structured playbook instead of hoping general knowledge is enough.

I use these in my own projects and publish the ones that hold up outside a single codebase.

## Quick start

```bash
git clone https://github.com/robzilla1738/roberts-skills.git
```

Pick a skill from the table below, open its README, and copy the whole folder into your assistant's skills directory (personal or project scope). Mention the skill in a prompt or attach it if your tool supports that.

For portable replication guides (patterns captured from real projects), see **[INDEX.md](INDEX.md)** — the searchable catalog of everything in this repo.

Every skill README explains the exact folder layout and how to update when new versions land here.

## Available skills

### [Design skills](design-skills/)

| Skill | Description |
| --- | --- |
| [macOS Design](design-skills/macos-design/) | Design, critique, and scaffold native macOS apps. HIG, Liquid Glass, menus, toolbars, safe areas, accessibility, SwiftUI and AppKit. Hub-and-spoke layout with 10 reference modules. |
| [Web Marketing Landing](design-skills/web-marketing-landing/) | Design and scaffold a premium SaaS marketing home page (aurora hero, glass nav, connector hub, bento grid, CSS motion). Next.js + Tailwind v4. |

### [Workflow skills](workflow-skills/)

| Skill | Description |
| --- | --- |
| [Autoreview](workflow-skills/autoreview/) | Hard acceptance gate before marking work complete. Reviews all session changes for production quality — correctness, code quality, architecture, maintainability, security, testing, and cleanup. Invoke with `/review`. |

More categories and skills will show up here as they're published.

## How skills are structured

**Simple skill** — one `SKILL.md` file with everything inline.

**Hub-and-spoke skill** — `SKILL.md` routes the agent to reference files it reads only when the task needs them. The macOS Design skill works this way: the hub stays small, spokes cover layout, navigation, accessibility, SwiftUI patterns, and so on.

```
design-skills/
  macos-design/
    README.md          setup instructions
    SKILL.md           hub — read first
    foundations.md     reference modules
    layout-and-windowing.md
    ...
```

Skills use YAML front matter (`name`, `description`, `version`) so assistants can discover and route to them.

## Compatibility

These skills target any assistant that loads custom instructions from markdown on disk. Install paths differ by tool (`~/.<assistant>/skills/`, `.agents/skills/`, project-scoped rules folders), but the content is the same everywhere.

No vendor-specific APIs. No scripts required unless a skill explicitly ships them.

## Updates

Pull this repo or re-copy the skill folder when you want the latest version. Compare the `version` field in a skill's `SKILL.md` front matter to see what you're running.

## Related projects

Other open-source work from Robert:

- [supergoal](https://github.com/robzilla1738/supergoal) — plan deeply, ship autonomously
- [htmlshop](https://github.com/robzilla1738/htmlshop) — local visual editor for HTML designs
- [Memorwise](https://github.com/robzilla1738/Memorwise) — local-first NotebookLM alternative

Full list at [robertcourson.com](https://robertcourson.com).

## License

MIT. See [LICENSE](LICENSE).
