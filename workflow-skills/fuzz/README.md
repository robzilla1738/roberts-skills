# Fuzz

Flush out hidden bugs dynamically: generate property-based tests, fuzz targets, or
differential oracles, run them, and shrink any failure into a committed regression test.

The dynamic counterpart to [bughunt](../bughunt/)'s static lenses — and standalone-useful
any time you want to harden a parser, encoder, state machine, or pure function.

Works with any AI coding assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Technique selection, oracle design, per-ecosystem harness sketches, crash→regression-test flow |

## Install

### 1. Copy the folder

Copy this entire `fuzz` directory into your assistant's skills location.

**Personal scope** (available in every project):

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/fuzz/` |
| Codex | `~/.agents/skills/fuzz/` |
| Cursor | `~/.cursor/skills/fuzz/` |

**Project scope** (shared with anyone who clones the repo):

```
<project>/.<your-assistant>/skills/fuzz/
```

The requirement is the same: a directory named `fuzz` containing `SKILL.md`.

### 2. Verify the layout

```
fuzz/
  SKILL.md
  README.md
```

## Use it

```text
/fuzz this parser — it should never crash and decode(encode(x)) must round-trip
```

```text
/fuzz to confirm BH-003 from the hunt and turn it into a failing test
```

## When to use it

- Hardening a function with a clear invariant (round-trip, idempotence, bounds, ordering).
- Confirming a Probable static finding at runtime.
- Building a differential oracle between two implementations or versions.

## Updating

Replace your local copy of the whole `fuzz` folder when a new version is published. Compare
the `version` field in `SKILL.md` front matter.

Current version: `2026-06-06.1`

## Notes

- Writes test/harness code, not product fixes. Keep the shrunk regression test; hand fixing
  to [autoreview](../autoreview/) or a human.
- Match the project's existing test runner and conventions; run under sanitizers where available.
- `disable-model-invocation: true` means the skill loads on explicit request.
