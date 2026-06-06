# Autoreview

Hard acceptance gate for session changes. Before marking work complete, review every file and
decision from the session and bring the implementation up to production quality.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install autoreview@roberts-skills
```

Then use `/review`.

### Cursor / Codex

Copy the skill folder into a skills location (both tools read `SKILL.md`):

```bash
cp -R plugins/autoreview/skills/autoreview ~/.agents/skills/   # Cursor + Codex (global)
cp -R plugins/autoreview/skills/autoreview ~/.cursor/skills/   # Cursor (global)
```

## Use it

```text
/review before we call this done — run the full acceptance checklist
```

See [`skills/autoreview/`](skills/autoreview/) for the full workflow and checklist.
