# Bughunt Suite

An offensive, whole-codebase **bug-hunting plugin** for any project type — iOS, macOS, web,
services, terminal tools, and more. It recons the target, fans out parallel hunters across a
grid of **9 analysis lenses × risk hotspots**, then merges, cross-validates, and reports
ranked, reproducible findings. **Report-only** by default.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## What's inside

Three skills + three slash commands:

| Skill | Command | Role |
| --- | --- | --- |
| `bughunt` | `/bughunt` | Orchestrator: recon → fan-out → hunt → merge → report |
| `triage` | `/triage` | Severity × confidence, minimal repro, the finding/report schema |
| `fuzz` | `/fuzz` | Property/fuzz/differential harnesses to confirm findings dynamically |

**9 lenses:** taint · state/lifecycle · concurrency · boundaries/numeric · error/failure ·
contract/spec · auth/access · logic-correctness · resource/performance.
**5 platform catalogs:** Apple · Web · Systems · Backend+CLI · Other (Android/.NET/PHP/
Flutter/SQL/IaC) **+ a generic fallback for any unlisted language**.

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install bughunt-suite@roberts-skills
```

Then use `/bughunt`, `/triage`, `/fuzz`. Update later with `/plugin marketplace update roberts-skills`.

### Cursor

Cursor loads skills from `SKILL.md`. Copy the three skill folders into a Cursor skills location:

```bash
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
/triage this crash report and give me a minimal repro
/fuzz this parser — decode(encode(x)) must round-trip and it must never crash
```

## Layout

```
bughunt-suite/
  .claude-plugin/plugin.json
  commands/         bughunt.md · triage.md · fuzz.md
  skills/
    bughunt/        SKILL.md + recon, fan-out, 9 lenses, 5 platform catalogs
    triage/         SKILL.md
    fuzz/           SKILL.md
```

## Notes

- **Report-only** — hunts and documents; hand fixing to a human or the **autoreview** plugin (`/review`).
- **Portable** — parallel fan-out is the flagship, with a sequential single-agent fallback for
  assistants without sub-agents.
- The same `SKILL.md` files are the native format for Claude Code, Cursor, and Codex.

Current versions: `bughunt` 2026-06-06.3 · `triage` 2026-06-06.2 · `fuzz` 2026-06-06.1
