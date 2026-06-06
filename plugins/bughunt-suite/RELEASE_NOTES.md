# Bughunt Suite Release Notes

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
