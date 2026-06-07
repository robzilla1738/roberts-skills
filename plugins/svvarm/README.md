# svvarm

Opinionated design director for frontend interfaces — reviews, fixes, and builds UI with a
38-pattern anti-slop standard covering color, typography, layout, copy, interaction, and
production. One command, zero AI slop.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install svvarm@roberts-skills
```

Then use `/svvarm`.

### Cursor / Codex

```bash
cp -R plugins/svvarm/skills/svvarm ~/.agents/skills/   # Cursor + Codex
cp -R plugins/svvarm/skills/svvarm ~/.cursor/skills/   # Cursor
```

## Usage

```
/svvarm init                       # New project — 6 questions, creates .svvarm/context.md design brief
/svvarm setup                      # Existing project — scans code first, baseline slop score
/svvarm audit                      # Full quality review: slop + production + polish
/svvarm build me a landing page    # Full build — creative brief → design spec → self-audit
/svvarm the fonts feel off         # Any natural-language design request routes itself
```

## How it's fast

Two-tier reference library: full builds read one compiled ~5K-token digest
(`references/core.md`) instead of every reference file; focused tasks read only the one
deep file for their domain (color, typography, layout, content, slop, polish, interaction,
motion, icons, inspiration, font pairings).

Project memory lives in `.svvarm/` (markdown design brief + decision log) inside the
project you use it on. The SessionStart hook shows a rainbow banner in projects with
`.svvarm/` initialized — optional, requires `python3`, never blocks.

See [`skills/svvarm/`](skills/svvarm/) for the hub and references.
