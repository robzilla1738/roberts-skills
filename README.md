# Robert's Skills

Provider-agnostic agent skills for AI coding assistants — packaged as a **plugin marketplace**
that works with **Claude Code, Cursor, and Codex**.

Each skill is a folder of markdown files (`SKILL.md` + references) that teaches an agent how to
do one kind of work well: hunt bugs, review code, design native macOS/iOS UI, scaffold a
full-stack app. Plain files, no lock-in. Install as a Claude Code plugin in one command, or
copy the skill folder into Cursor/Codex.

**Author:** [Robert Courson](https://robertcourson.com) · [robertcourson.com](https://robertcourson.com)

---

## Available plugins

| Plugin | Skills / commands | Description |
| --- | --- | --- |
| [bughunt-suite](plugins/bughunt-suite/) | `/bughunt` `/triage` `/fuzz` | **Flagship.** Offensive whole-codebase hunter for bugs, pain points, and inefficiencies — a zero-dependency toolkit ranks hotspots, parallel hunters sweep 13 lenses × risk hotspots, a mandatory skeptic pass refutes false positives, and findings are fingerprinted, baseline-diffed, and rendered to markdown/HTML/SARIF with CI exit codes. Plus triage (severity × confidence + repro) and fuzz (runs property/fuzz harnesses). Report-only. |
| [autoreview](plugins/autoreview/) | `/review` | Hard acceptance gate before marking work complete. Reviews all session changes for production quality — correctness, architecture, maintainability, security, testing, cleanup. |
| [scaffold](plugins/scaffold/) | `/scaffold` | Product-driven greenfield Next.js — intake profiles, typed env, Vitest, tRPC, Neon/Drizzle, optional Clerk, Vercel. |
| [macos-design](plugins/macos-design/) | `/macos-design` | Design, critique, and scaffold native macOS apps — HIG, Liquid Glass, menus, toolbars, safe areas, accessibility, SwiftUI/AppKit. |
| [macos-notch](plugins/macos-notch/) | `/macos-notch` | Design and implement macOS Dynamic Island / notch-style apps — NSPanel, geometry, state machine, module widgets. |
| [macos-sandbox](plugins/macos-sandbox/) | `/macos-sandbox` | Smoke-test macOS `.app`/`.pkg` in disposable Tart VMs via [macbox](https://github.com/robzilla1738/macbox) CLI or MCP. |
| [web-marketing-landing](plugins/web-marketing-landing/) | `/landing-page` | Design and scaffold a premium SaaS marketing home page (aurora hero, glass nav, bento grid) on Next.js + Tailwind v4. |

Portable replication guides (patterns captured from real projects) live in [guides/](guides/)
and are cataloged in **[INDEX.md](INDEX.md)**.

## Install

### Claude Code — plugin marketplace (one command)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install bughunt-suite@roberts-skills
```

Install any other plugin the same way (`/plugin install <name>@roberts-skills`). Update with
`/plugin marketplace update roberts-skills`. Browse with `/plugin`.

### Cursor

Cursor loads skills from `SKILL.md`. Copy the skill folder(s) into a Cursor skills location:

```bash
git clone https://github.com/robzilla1738/roberts-skills.git
cp -R roberts-skills/plugins/bughunt-suite/skills/* ~/.cursor/skills/     # global
# or project scope: .cursor/skills/
```

Invoke with `/<skill-name>` (e.g. `/bughunt`) or attach with `@<skill-name>`.

### Codex

Codex loads skills from `.agents/skills/`. Copy the skill folder(s) there:

```bash
cp -R roberts-skills/plugins/bughunt-suite/skills/* ~/.agents/skills/     # global
# or project scope: .agents/skills/ (read from CWD up to repo root)
```

Invoke with `/skills` or `$<skill-name>`.

> `.agents/skills/` is read by **both** Cursor and Codex, so one copy there covers both tools.

### Install a single skill (any tool)

Every skill works standalone — you don't need the whole repo or even the whole plugin.
Grab just the skill folder you want:

```bash
# Claude Code (personal skills — available in every project)
npx degit robzilla1738/roberts-skills/plugins/bughunt-suite/skills/triage ~/.claude/skills/triage

# Cursor
npx degit robzilla1738/roberts-skills/plugins/bughunt-suite/skills/triage ~/.cursor/skills/triage

# Codex (also read by Cursor)
npx degit robzilla1738/roberts-skills/plugins/bughunt-suite/skills/triage ~/.agents/skills/triage
```

Swap the path for any skill listed in [INDEX.md](INDEX.md) (`plugins/<plugin>/skills/<name>`).
Each skill folder is self-contained — `SKILL.md` plus its reference spokes.

Two caveats vs. a plugin install: you don't get the plugin's slash command registered
(invoke the skill by name instead), and updates are manual (re-run the command). Note
**bughunt** is the one skill best installed via its plugin — it reads its sibling skills
`triage` and `fuzz` as part of its pipeline.

## How it's structured

```
roberts-skills/
  .claude-plugin/marketplace.json     # lists every plugin
  plugins/
    bughunt-suite/
      .claude-plugin/plugin.json      # plugin manifest
      commands/                       # slash commands (/bughunt, /triage, /fuzz)
      skills/
        bughunt/  SKILL.md + spokes   # the actual skill content
        triage/   SKILL.md
        fuzz/     SKILL.md
    autoreview/ · scaffold/ · macos-design/ · macos-notch/ · macos-sandbox/ · web-marketing-landing/
  guides/                             # portable replication write-ups (not skills)
  INDEX.md
```

- **Skill** — a `skills/<name>/` folder with a `SKILL.md` (YAML front matter: `name`,
  `description`, `version`). Simple skills are one file; complex ones use **hub-and-spoke**
  (a small `SKILL.md` that routes to reference spokes read on demand).
- **Plugin** — a bundle of one or more related skills plus slash commands, installable in
  Claude Code via the marketplace.
- The same `SKILL.md` files are the native format for all three assistants.

## Compatibility

No vendor-specific APIs. No scripts required unless a skill explicitly ships them. Claude Code
gets one-command plugin install; Cursor and Codex read the same `SKILL.md` files directly.

## Updates

In Claude Code: `/plugin marketplace update roberts-skills`. For Cursor/Codex: pull this repo
and re-copy the skill folder. Compare the `version` field in a skill's `SKILL.md` front matter.

## Related projects

- [supergoal](https://github.com/robzilla1738/supergoal) — plan deeply, ship autonomously
- [htmlshop](https://github.com/robzilla1738/htmlshop) — local visual editor for HTML designs
- [macbox](https://github.com/robzilla1738/macbox) — disposable macOS VMs for smoke-testing
- [Memorwise](https://github.com/robzilla1738/Memorwise) — local-first NotebookLM alternative

Full list at [robertcourson.com](https://robertcourson.com).

## License

MIT. See [LICENSE](LICENSE).
