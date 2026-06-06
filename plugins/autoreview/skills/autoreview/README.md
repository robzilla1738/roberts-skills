# Autoreview

Hard acceptance gate for session changes. Before marking work complete, review every file and decision from the session and bring the implementation up to production quality.

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Full review workflow, checklist, acceptance criteria, and required final response format |

## Install

### 1. Copy the folder

Copy this entire `autoreview` directory into your assistant's skills location.

**Personal scope** (available in every project):

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/autoreview/` |
| Codex | `~/.agents/skills/autoreview/` |
| Cursor | `~/.cursor/skills/autoreview/` |

**Project scope** (shared with anyone who clones the repo):

```
<project>/.<your-assistant>/skills/autoreview/
```

Some tools use `.agents/skills/` instead of a dot-prefixed folder. Check your assistant's docs for the exact path. The requirement is the same: a directory named `autoreview` containing `SKILL.md`.

### 2. Verify the layout

```
autoreview/
  SKILL.md
  README.md
```

### 3. Confirm your assistant sees it

Restart the assistant or reload skills if your tool requires that. Open a new session and check that `autoreview` appears in your skills list, or attach the folder manually.

## Use it

```text
/review
```

```text
/review before we call this done — run the full acceptance checklist
```

The agent should review all session changes, fix any issues found, run available validation, and end with a concise review summary.

## When to use it

Run `/review` at the end of a coding session before declaring the task complete. The skill enforces a production-quality gate: no tech debt, shortcuts, TODOs, dead code, or bandaids left behind.

## Updating

Replace your local copy of the whole `autoreview` folder when a new version is published. Compare the `version` field in `SKILL.md` front matter.

Current version: `2026-05-28.1`

## Notes

- Written for LLM agents as a hard acceptance gate, not a lightweight code skim.
- `disable-model-invocation: true` in front matter means the skill loads on explicit request, not every message. Remove that line if you want ambient auto-loading and your tool supports it.
