# Workflow skills

Agent skills for process and quality workflows: acceptance gates, session reviews, and end-of-task verification.

## Skills in this category

| Skill | Version | What it covers |
| --- | --- | --- |
| [Autoreview](autoreview/) | 2026-05-28.1 | Hard acceptance gate before marking work complete. Reviews all session changes for production quality across correctness, architecture, maintainability, security, testing, and cleanup. |
| [Bughunt](bughunt/) | 2026-06-06.1 | Offensive whole-codebase bug hunter for any project type. Recon → parallel fan-out across analysis lenses × risk hotspots → merge, cross-validate, report ranked reproducible findings. Report-only. Invoke with `/bughunt`. |
| [Triage](triage/) | 2026-06-06.1 | Turn a suspected bug or a batch of findings into a ranked, evidence-backed report — severity × confidence, minimal repro, standard finding schema. Companion to bughunt. Invoke with `/triage`. |
| [Fuzz](fuzz/) | 2026-06-06.1 | Flush out hidden bugs dynamically — property-based tests, fuzz targets, differential oracles — and shrink failures into regression tests. Companion to bughunt. Invoke with `/fuzz`. |
| [macOS Sandbox](macos-sandbox/) | 2026-06-03.1 | Smoke-test `.app`/`.pkg` in disposable Tart VMs via [macbox](https://github.com/robzilla1738/macbox) CLI or MCP — upload, launch, logs, screenshots, crashes, guest automation. |
| [Scaffold](scaffold/) | 2026-06-03.2 | Product-driven greenfield Next.js — intake profiles, env/errors, Vitest, tRPC, optional Clerk, Neon/Drizzle, Vercel. Invoke with `/scaffold`. |

## Install

Each skill has its own README with setup steps. The pattern is the same:

1. Copy the skill folder (e.g. `autoreview/`) into your assistant's skills location.
2. Keep all files together.
3. Invoke the skill explicitly in a prompt (e.g. `/review`).

Autoreview is also listed in [INDEX.md](../INDEX.md).

See the [root README](../README.md) for general compatibility notes.
