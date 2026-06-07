# Bughunt Suite Release Notes

## bughunt-suite 2.2.0 - 2026-06-07

This release adds two new rungs to the capability ladder — a faster Hunt substrate and a more
powerful Confirm tail — without changing the deterministic spine, the finding schema, or any
existing behavior. Both degrade cleanly when their tooling is absent, and the core hunt stays
zero-dependency.

- **Fast variant — Rung A-CLI (`scripts/hunt-cursor.mjs`).** A zero-dependency Node
  orchestrator that fans out the `(lens × hotspot)` grid as parallel `cursor-agent`
  subprocesses, so the hunt can run on a fast model (Composer 2.5 / Grok) from any shell with
  the Cursor CLI — including inside Cursor, which it upgrades from a sequential Rung-C tool to a
  true parallel fan-out. Hunters are **read-only by construction** (`--mode ask`, never
  `--force`). It emits the same `{schemaVersion, coverage, findings}` document as the Workflow
  rung, so `merge`/`render` are unchanged. New `/bughunt-cursor` command.
- **Signal preserved.** Hunters may use a fast model for breadth, but the mandatory skeptic pass
  stays on a strong reasoner (Opus 4.8). Speed where breadth matters; intelligence at the
  signal gate.
- **Confirm rung — E2B (`scripts/confirm-e2b.py`, opt-in).** Runs Probable findings' repros in
  parallel ephemeral E2B sandboxes to earn **Confirmed** verdicts, with per-sandbox timeouts, a
  concurrency cap, and always-on teardown. The agent supplies executable repros via a
  repro-map; the script owns isolation/parallelism. Degrades to the manual `/fuzz` + `verify`
  path when no `E2B_API_KEY`/SDK is present. New `confirm.md` spoke.
- **Tests.** `selftest.py` gains five offline tests covering both rungs via `--dry-run` (no
  `cursor-agent`, no E2B, no network); the suite stays 100% offline and green.

## bughunt-suite 2.1.0 - 2026-06-06

This hardening release makes the suite more enforceable and more honest for real-world use.

- Added stricter CI merge gates: `--require-verified`, `--require-coverage`, and `--strict`.
- Demoted `uncertain` verifier verdicts to Speculative and preserved refuted findings for the transparency appendix.
- Fixed cross-lens clustering so upheld findings win over uncertain duplicates when choosing the primary finding.
- Cleaned up candidate finding schema behavior so hunters do not need to provide `id`.
- Included selected project dot-directories such as `.github`, `.circleci`, `.devcontainer`, `.husky`, `.claude`, `.cursor`, and `.agents` in recon.
- Preserved and rendered coverage metadata, and made it enforceable in CI.
- Tightened fuzz candidate heuristics so obvious request/response handlers are not promoted as pure targets.
- Updated docs and public positioning to describe a structured, evidence-first hunt workflow rather than overpromising a universal scanner.
