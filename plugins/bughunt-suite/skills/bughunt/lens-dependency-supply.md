# Lens: Dependency & Supply Chain

**Hunts for:** risk entering through third-party packages and the build pipeline —
unpinned versions, vulnerable or abandoned deps, typosquat/confusion shapes,
untrusted install/CI code, and over-broad attack surface. The code you wrote may
be perfect; the code you *pulled in* runs with the same privileges.

## Mental model

Treat every dependency and every build step as **untrusted code you chose to
run**. Ask: **what exactly executes when I install/build, where does it come from,
and can it change under me without my noticing?** A bug here is anything that lets
the dependency graph or pipeline shift to something you didn't review — an
unpinned range, a missing lockfile, a `@main` action, a `curl | bash`, a name one
typo away from a popular package.

The blast radius is the whole process: a compromised transitive dep at install
time can exfiltrate secrets or backdoor the artifact regardless of how clean your
own code is.

## Smells

**Unpinned & unlocked**
- Version ranges (`^`, `~`, `*`, `>=`, `latest`) on *direct* deps — the resolved
  version drifts on the next install. `bughunt.py deps` flags these as `UNPINNED`.
- Missing lockfile (no `package-lock.json`/`yarn.lock`/`pnpm-lock.yaml`/
  `poetry.lock`/`requirements.txt` pins) — `deps` flags `NO_LOCKFILE`; builds are
  not reproducible.
- Lockfile out of sync with the manifest — `deps` reports `LOCK_DRIFT` (also in
  the top-level `lockDrift` array); the lock no longer reflects declared deps.

**Vulnerable & abandoned**
- Known-deprecated/unmaintained packages — `deps` flags `DEPRECATED_MARKER` for
  well-known offenders (`request`, `node-sass`, `tslint`, `moment`, …).
- Deps with no release in years, archived upstream, or with an open
  unmaintained/looking-for-maintainer notice.
- Packages superseded by a stdlib/native API (a polyfill for a feature now
  built in; `left-pad`-class one-liners).
- Run `deps --osv` to query OSV.dev for advisories when network is allowed
  (opt-in; results land in the `advisories` array).

**Typosquat & confusion**
- A package name one edit-distance from a popular one — `deps` flags
  `TYPOSQUAT_SHAPE` (`lodahs`, `momnet`, `expres`); a slip in the manifest pulls
  attacker code.
- An internal/private package name that could be shadowed by a public one of the
  same name on the default registry (dependency confusion) — pin the scope and
  registry.
- `install`/`postinstall`/`preinstall` hooks that fetch or execute remote code at
  install time — arbitrary code on every `npm install`.

**Trust & integrity**
- `curl ... | bash`, `wget -O- | sh`, or piped installers in CI/setup scripts —
  unreviewed, unversioned remote code.
- Unpinned GitHub Actions (`uses: org/action@main` / `@v3` floating tag) instead
  of a pinned commit SHA — the action can change under you.
- Deps or scripts fetched over plain `http://`; no integrity/SRI hash on CDN
  `<script>`/`<link>` tags.

**Over-broad surface**
- A heavy dependency pulled in for one trivial function (whole date/util library
  for one helper) — large surface for tiny value.
- A transitive dep doing privileged work (network, fs, child_process) that the
  app never reviews but ships with.
- A dev/test-only dependency bundled into the production artifact.

## How to trace

1. Start from `bughunt.py deps` JSON: read `ecosystems`, each `deps[].issues`
   (`UNPINNED`/`NO_LOCKFILE`/`LOCK_DRIFT`/`DEPRECATED_MARKER`/`TYPOSQUAT_SHAPE`),
   `lockDrift`, and `advisories` (if `--osv` was run).
2. Open the cited manifests and lockfiles; confirm the range/drift/squat shape and
   whether the dep is direct or transitive.
3. Scan CI configs and install scripts for `curl|bash`, floating action tags,
   `http://` fetches, and `*install` lifecycle hooks.
4. For each flagged dep, ask: how much code does it bring, what privileges does it
   exercise, and is it reachable in production.

## Evidence to capture

The package/manifest and the precise issue: name, declared range/version, the
`deps` issue code, and *what can change* (e.g. "`lodash: ^4.17.0` in
`package.json`, no lockfile → next install can pull any 4.x", or "`uses:
actions/checkout@main` in `ci.yml` → action code is not pinned"). For advisories,
the CVE/OSV id and affected range. State the blast radius (install-time code exec,
non-reproducible build, supply-chain swap).

## Common false positives to reject

- A range that *is* fully constrained by a committed, in-sync lockfile (the lock
  is the real pin) — confirm `LOCK_DRIFT` is absent.
- A "deprecated" marker on a package the repo has already pinned to a known-good
  version and intentionally vendored/frozen.
- A `TYPOSQUAT_SHAPE` that is actually the correct, intended package (the heuristic
  is name-shape only) — verify against the real registry name.
- An internal action/dep pinned by SHA elsewhere in the same workflow.
- A "heavy" dep that's genuinely load-bearing across many call sites, not one
  helper.
- A dev dependency that is correctly excluded from the production build (verify
  the bundler/`devDependencies` boundary).

## Cross-references

- [lens-dataflow-taint.md](lens-dataflow-taint.md) — a dependency *is* an
  untrusted-code boundary; taint reasoning extends to data crossing into and out
  of third-party code, not just user input.
- [lens-data-migration.md](lens-data-migration.md) — a dep upgrade that changes a
  serialization shape can desync persisted data.
- [lens-contract-spec.md](lens-contract-spec.md) — a dep's API contract changing
  across a version bump (semver lies, breaking minor releases).
- Score via [triage](../triage/SKILL.md); supply-chain findings range from Low
  (cosmetic drift) to Critical (install-time RCE).
