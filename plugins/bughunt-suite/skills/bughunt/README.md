# Bughunt

An offensive, whole-codebase bug hunter for any project type — iOS, macOS, web, services,
terminal tools. Where the **autoreview** skill (`/review`) is a defensive gate on your own diff,
bughunt assumes the code is guilty: it recons the target, fans out parallel hunters across a
grid of analysis **lenses × risk hotspots**, then merges, cross-validates, and reports
ranked, reproducible findings. **Report-only by default.**

Hub-and-spoke layout, pure markdown. Works with any AI coding assistant that loads skills
from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## The suite

Bughunt is the orchestrator of a three-skill bug-hunting suite:

| Skill | Role |
| --- | --- |
| **bughunt** (this) | Orchestrator: recon → fan-out → hunt → merge → report |
| [triage](../triage/) | Severity × confidence, minimal repro, the finding/report schema |
| [fuzz](../fuzz/) | Property/fuzz/differential harnesses to confirm findings dynamically |

It also plugs into the existing the **autoreview** skill (`/review`) (the fix gate) and `verify`
(runtime repro) skills.

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Hub: mission, modes, the hunt loop, lens/platform routing tables |
| `recon-and-scoping.md` | Platform detection, trust boundaries, hotspot ranking, hunt plan |
| `fanout-orchestration.md` | (Lens × hotspot) grid, hunter prompt, merge/cross-validate, sequential fallback |
| `lens-*.md` (9) | Analysis disciplines: taint, state/lifecycle, concurrency, boundaries/numeric, error/failure, contract/spec, auth/access, logic-correctness, resource/performance |
| `platform-*.md` (5) | Ecosystem footguns: Apple, Web, Systems, Backend+CLI, Other (Android/.NET/PHP/Flutter/SQL/IaC + generic fallback) |

## Install

### 1. Copy the folder

Copy this entire `bughunt` directory into your assistant's skills location. For the full
suite, also copy [triage](../triage/) and [fuzz](../fuzz/).

**Personal scope** (available in every project):

| Assistant | Path |
| --- | --- |
| Claude Code | `~/.claude/skills/bughunt/` |
| Codex | `~/.agents/skills/bughunt/` |
| Cursor | `~/.cursor/skills/bughunt/` |

**Project scope** (shared with anyone who clones the repo):

```
<project>/.<your-assistant>/skills/bughunt/
```

The requirement is the same: a directory named `bughunt` containing `SKILL.md` and its spokes.

### 2. Verify the layout

```
bughunt/
  SKILL.md
  README.md
  recon-and-scoping.md
  fanout-orchestration.md
  lens-dataflow-taint.md
  lens-state-lifecycle.md
  lens-concurrency.md
  lens-boundaries-numeric.md
  lens-error-failure.md
  lens-contract-spec.md
  lens-auth-access.md
  lens-logic-correctness.md
  lens-resource-performance.md
  platform-apple.md
  platform-web.md
  platform-systems.md
  platform-backend-cli.md
  platform-other.md
```

## Use it

```text
/bughunt the whole repo — deep hunt, I want the hidden bugs
```

```text
/bughunt the sync engine, focus on concurrency and failure paths
```

```text
/bughunt quick scan of this diff before I push
```

The agent recons the target, runs the hunt (parallel where supported), and ends with a
ranked, evidence-backed report. It does not edit code unless you ask.

## When to use it

- You want bugs across an entire codebase, not just the current diff.
- Deep adversarial review of a risky module, feature, or change.
- Before a release, audit, or handoff.

For reviewing your own session diff for quality, use the **autoreview** skill (`/review`) instead.

## Updating

Replace your local copy of the whole `bughunt` folder when a new version is published.
Compare the `version` field in `SKILL.md` front matter.

Current version: `2026-06-06.3`

## Notes

- **Report-only by default** — hunts and documents; hand fixing to a human or autoreview.
- **Portable** — parallel fan-out is the flagship, but a sequential single-agent fallback is
  built in for assistants without sub-agents.
- `disable-model-invocation: true` means the skill loads on explicit request.
