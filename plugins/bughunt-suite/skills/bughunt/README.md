# Bughunt

An offensive, hotspot-driven workflow for **bugs, pain points, and inefficiencies** across
project types — iOS, macOS, web, services, terminal tools. Where the **autoreview** skill
(`/review`) is a defensive gate on your own diff, bughunt assumes the code is guilty: a
zero-dependency toolkit ranks risk hotspots, agents inspect them through **13 analysis
lenses**, a mandatory skeptic pass refutes false positives, strict CI merge gates can enforce
verification and coverage, and findings are fingerprinted, deduped, baseline-diffed, and
rendered to markdown/HTML/SARIF with CI exit codes. **Report-only by default.**

Hub-and-spoke layout. The toolkit is a single stdlib-only `python3` file; everything degrades
to a pure-markdown pipeline when `python3` is absent — so it works with any AI coding
assistant that loads skills from markdown files.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## The suite

Bughunt is the orchestrator of a three-skill bug-hunting suite:

| Skill | Role |
| --- | --- |
| **bughunt** (this) | Orchestrator: recon → fan-out → hunt → **verify** → merge → report |
| [triage](../triage/) | Severity × confidence (+ impact rubric), minimal repro, the finding/report schema |
| [fuzz](../fuzz/) | Property/fuzz/differential harnesses that **run** to confirm findings dynamically |

It also plugs into the existing the **autoreview** skill (`/review`) (the fix gate) and `verify`
(runtime repro) skills.

## What you get

| File | Role |
| --- | --- |
| `SKILL.md` | Hub: mission, modes, the hunt loop, toolkit + capability ladder, lens/platform routing |
| `recon-and-scoping.md` | Deterministic pre-pass, platform detection, trust boundaries, hotspot ranking, hunt plan |
| `orchestration.md` | (Lens × hotspot) grid, hunter prompt, capability ladder (Workflow/Tasks/sequential) |
| `verification.md` | The mandatory adversarial skeptic pass — four refutation questions, verdict contract |
| `tooling.md` | `bughunt.py` reference — census/hotspots/signals/deps/merge/render/diff, state dir, CI |
| `scripts/` | `bughunt.py` (zero-dep toolkit), `hunt-workflow.js` (Workflow script), `schema/`, `selftest.py` |
| `lens-*.md` (13) | Analysis disciplines: taint, state/lifecycle, concurrency, boundaries/numeric, error/failure, contract/spec, auth/access, logic-correctness, resource/performance, dx-pain, product-ux, dependency-supply, data-migration |
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
  orchestration.md
  verification.md
  tooling.md
  lens-dataflow-taint.md
  lens-state-lifecycle.md
  lens-concurrency.md
  lens-boundaries-numeric.md
  lens-error-failure.md
  lens-contract-spec.md
  lens-auth-access.md
  lens-logic-correctness.md
  lens-resource-performance.md
  lens-dx-pain.md
  lens-product-ux.md
  lens-dependency-supply.md
  lens-data-migration.md
  platform-apple.md
  platform-web.md
  platform-systems.md
  platform-backend-cli.md
  platform-other.md
  scripts/
    bughunt.py
    hunt-workflow.js
    selftest.py
    schema/finding.schema.json
```

The `scripts/` directory is optional — copy it to get the deterministic toolkit (ranked
hotspots, structured findings, baseline diffing, SARIF). Without it, the skill runs the
pure-markdown fallback.

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

- You want a structured hunt across the riskiest parts of a codebase, not just the current diff.
- Deep adversarial review of a risky module, feature, or change.
- Before a release, audit, or handoff.

For reviewing your own session diff for quality, use the **autoreview** skill (`/review`) instead.

## Updating

Replace your local copy of the whole `bughunt` folder when a new version is published.
Compare the `version` field in `SKILL.md` front matter.

Current version: `2026-06-06.5`

## Notes

- **Report-only by default** — hunts and documents; hand fixing to a human or autoreview.
- **Deterministic where it counts** — `bughunt.py` (stdlib-only `python3`) ranks hotspots and
  owns structured findings; everything degrades to markdown when `python3` is absent.
- **Mandatory verify** — a skeptic pass refutes false positives before anything is reported;
  CI can require both verifier verdicts and coverage metadata.
- **Portable** — the capability ladder runs the same five phases via the Workflow tool,
  parallel Tasks, or a sequential single-agent walk.
- `disable-model-invocation: true` means the skill loads on explicit request.
