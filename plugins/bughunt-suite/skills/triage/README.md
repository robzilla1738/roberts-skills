# Triage

Turn a suspected bug — or a pile of candidate findings — into a precise, ranked,
evidence-backed report. Assigns severity × confidence, builds a minimal reproduction or
failing test, and emits a standard finding schema.

Standalone-useful for any single bug, and the scoring/reporting stage of
[bughunt](../bughunt/).

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Finding schema, severity × confidence rubrics, minimal-repro discipline, report layout |

## Install

### 1. Copy the folder

Copy this entire `triage` directory into your assistant's skills location.

**Personal scope** (available in every project):

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/triage/` |
| Codex | `~/.agents/skills/triage/` |
| Cursor | `~/.cursor/skills/triage/` |

**Project scope** (shared with anyone who clones the repo):

```
<project>/.<your-assistant>/skills/triage/
```

The requirement is the same: a directory named `triage` containing `SKILL.md`.

### 2. Verify the layout

```
triage/
  SKILL.md
  README.md
```

## Use it

```text
/triage this crash report — assess severity and give me a minimal repro
```

```text
/triage these findings from the hunt and rank them
```

## When to use it

- You have one suspected bug and want it assessed and reproduced.
- You have a batch of candidate findings (e.g. from [bughunt](../bughunt/)) and need them
  scored, deduped, proven, and reported.

## Updating

Replace your local copy of the whole `triage` folder when a new version is published.
Compare the `version` field in `SKILL.md` front matter.

Current version: `2026-06-06.1`

## Notes

- Report-only: it assesses and proves, it does not edit product code. Hand fixing to
  the **autoreview** skill (`/review`) or a human.
- `disable-model-invocation: true` means the skill loads on explicit request. Remove that
  line for ambient auto-loading if your tool supports it.
