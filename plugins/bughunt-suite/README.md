# Bughunt Suite

An offensive, whole-codebase **hunting plugin** for **bugs, pain points, and inefficiencies**
on any project type — iOS, macOS, web, services, terminal tools, and more. A zero-dependency
toolkit ranks risk hotspots, parallel hunters sweep a grid of **13 analysis lenses × risk
hotspots**, a mandatory skeptic pass refutes false positives, and findings are fingerprinted,
deduped, baseline-diffed, and rendered to **markdown / HTML / SARIF** with **CI exit codes**.
**Report-only** by default.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What's inside

Three skills + three slash commands:

| Skill | Command | Role |
| --- | --- | --- |
| `bughunt` | `/bughunt` | Orchestrator: recon → fan-out → hunt → **verify** → merge → report |
| `triage` | `/triage` | Severity × confidence (+ impact rubric), minimal repro, the finding/report schema |
| `fuzz` | `/fuzz` | Property/fuzz/differential harnesses that **run** to confirm findings dynamically |

**13 lenses:** taint · state/lifecycle · concurrency · boundaries/numeric · error/failure ·
contract/spec · auth/access · logic-correctness · resource/performance · **dx-pain** ·
**product-ux** · **dependency-supply** · **data-migration**.
**5 platform catalogs:** Apple · Web · Systems · Backend+CLI · Other (Android/.NET/PHP/
Flutter/SQL/IaC) **+ a generic fallback for any unlisted language**.

**Toolkit (`skills/bughunt/scripts/bughunt.py`, zero-dependency `python3`):** deterministic
hotspot ranking, pain-signal mining, dependency audit, structured findings with fingerprint
dedupe, suppression, baseline diffing (“3 new, 2 fixed”), and markdown/HTML/SARIF rendering
with CI exit codes. Degrades to a pure-markdown pipeline when `python3` is unavailable.

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install bughunt-suite@roberts-skills
```

Then use `/bughunt`, `/triage`, `/fuzz`. Update later with `/plugin marketplace update roberts-skills`.

### Cursor

Cursor loads skills from `SKILL.md`. Clone this repo, then from the repo root copy the three
skill folders into a Cursor skills location:

```bash
git clone https://github.com/robzilla1738/roberts-skills.git && cd roberts-skills
cp -R plugins/bughunt-suite/skills/{bughunt,triage,fuzz} ~/.cursor/skills/        # global
# or, project scope:
cp -R plugins/bughunt-suite/skills/{bughunt,triage,fuzz} .cursor/skills/
```

Invoke with `/bughunt` (or `@bughunt` to attach as context).

### Codex

Codex loads skills from `.agents/skills/`. Copy the skill folders there:

```bash
cp -R plugins/bughunt-suite/skills/{bughunt,triage,fuzz} ~/.agents/skills/         # global
# or, project scope (anywhere from CWD up to repo root):
cp -R plugins/bughunt-suite/skills/{bughunt,triage,fuzz} .agents/skills/
```

Invoke with `/skills` or `$bughunt`.

> Tip: `.agents/skills/` is read by **both** Cursor and Codex, so a single copy there covers both.

## Use it

```text
/bughunt the whole repo — deep hunt, find the hidden bugs
/bughunt the sync engine, focus on concurrency and failure paths
/bughunt diff — only what changed on this branch
/bughunt ci — non-interactive; exit 1 on new Critical/High (gate a pipeline)
/triage this crash report and give me a minimal repro
/fuzz this parser — decode(encode(x)) must round-trip and it must never crash
```

Each run writes a ranked report and reusable state into `.bughunt/` in the target repo
(`report.md` / `.html` / `.sarif`, plus a committable `baseline.json` and `suppressions.json`).

## Layout

```
bughunt-suite/
  .claude-plugin/plugin.json
  commands/         bughunt.md · triage.md · fuzz.md
  skills/
    bughunt/        SKILL.md + recon, orchestration, verification, tooling,
                    13 lenses, 5 platform catalogs, scripts/ (bughunt.py + hunt-workflow.js)
    triage/         SKILL.md
    fuzz/           SKILL.md
```

## Notes

- **Report-only** — hunts and documents; hand fixing to a human or the **autoreview** plugin (`/review`).
- **Deterministic spine** — `bughunt.py` (stdlib-only `python3`) ranks hotspots and owns
  structured findings, baseline diffing, and SARIF; the hunt still works in pure markdown
  when `python3` is absent.
- **Mandatory verify** — a skeptic pass refutes false positives before anything is reported.
- **Portable** — a capability ladder runs the same five phases via the Workflow tool, parallel
  Tasks, or a sequential single-agent walk. The same `SKILL.md` files are native to Claude
  Code, Cursor, and Codex.

Current versions: `bughunt` 2026-06-06.4 · `triage` 2026-06-06.3 · `fuzz` 2026-06-06.2 · plugin 2.0.0
