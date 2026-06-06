# Recon & Scoping

The hunt is only as good as its map. Before hunting, build a **target map**, identify
**where bugs are most likely to hide**, and produce a **hunt plan** that selects lenses and
platform catalogs. Don't spray attention evenly — concentrate it where risk and change
collide.

## 1. Detect platform & stack

Identify language(s), frameworks, and the trust model from the project's own signals:

- **Manifests:** `package.json`, `Package.swift`/`*.xcodeproj`, `Cargo.toml`, `go.mod`,
  `pyproject.toml`/`requirements.txt`, `pom.xml`/`build.gradle`, `Gemfile`, `CMakeLists.txt`.
- **Entry points:** `main`, server bootstrap, app delegate / `@main`, CLI argv parsing.
- **Test setup:** runner and conventions (you'll reuse these for repros).

Map each detected language to a platform catalog: Apple → [platform-apple.md](platform-apple.md),
JS/TS/Node → [platform-web.md](platform-web.md), C/C++/Rust/Go →
[platform-systems.md](platform-systems.md), Python/Ruby/Java + CLI tools →
[platform-backend-cli.md](platform-backend-cli.md). Anything else (Android/Kotlin, .NET/C#,
PHP, Flutter/RN, SQL, IaC) or an unlisted language → [platform-other.md](platform-other.md),
which also carries the **generic fallback** so the hunt works on any stack. Polyglot repos
select more than one.

## 2. Map trust boundaries (attack surface)

Bugs cluster where data crosses a boundary or where control is handed to/from the outside.
Enumerate every boundary the code has:

- **Network** — HTTP handlers, RPC, websockets, outbound calls.
- **Persistence** — DB queries, file I/O, caches, blob storage.
- **Process/IPC** — subprocesses, XPC/IPC, shared memory, env vars.
- **User input** — forms, CLI argv/stdin, URL schemes, deep links, file imports.
- **Deserialization** — JSON/XML/YAML/protobuf, `Codable`, pickle, plist.
- **Concurrency boundaries** — threads, queues, actors, async tasks, locks.
- **Third-party** — SDKs, FFI/native bridges, plugins.

For each boundary note: who controls the data, what validation exists, and what the sink does.
This directly seeds the [taint](lens-dataflow-taint.md) and [error/failure](lens-error-failure.md)
lenses.

## 3. Rank hotspots

Score files/modules by likelihood-of-defect, highest first:

- **Churn** — frequently changed code carries bugs. `git log --oneline -- <path> | wc -l`,
  or `git log --since=...` for recent activity.
- **Recency** — recently touched code hasn't been battle-tested. `git log -1 --format=%cr`.
- **Complexity/size** — long functions, deep nesting, many branches, big files.
- **Git-optional fallback** — if the target isn't a git repo (zip, export, shallow clone),
  skip the git heuristics and rank by file modification time, size/complexity, boundary
  proximity, and the bug-prone shapes/smell markers below instead.
- **Boundary proximity** — code at or near a trust boundary (from step 2).
- **Low test coverage** — paths with no tests (check the test dir for gaps).
- **Bug-prone shapes** — manual memory/locking, parsers, state machines, retries, money/time math.
- **Smell markers** — `TODO`, `FIXME`, `HACK`, `XXX`, "temporary", "for now", commented-out code.

A hotspot is hottest when several of these stack (e.g. a recently-churned, complex parser at
a network boundary with no tests).

## 4. Build the hunt plan

Produce a compact plan before fanning out:

```markdown
## Hunt plan — <target>
- **Platform(s):** <e.g. Swift (iOS) + Node service>
- **Mode:** quick scan | deep hunt | targeted
- **Trust boundaries:** <list, highest-risk first>
- **Hotspots (ranked):**
  1. path/to/x — why (churn + boundary + no tests)
  2. ...
- **Lenses selected:** <e.g. taint, concurrency, error-failure>  (+ rationale)
- **Platform catalogs:** <e.g. platform-apple, platform-web>
- **Out of scope / not examined:** <generated code, vendored deps, ...>
```

Selecting lenses: always consider **taint** at input boundaries, **concurrency** wherever
there's shared state/async, **error-failure** around I/O and external calls, **boundaries-
numeric** in parsing/math, **state-lifecycle** for anything with setup/teardown or a state
machine, and **contract-spec** everywhere there are docs/types/tests to check against. Also:
**auth-access** whenever there are users, permissions, sessions, or multi-tenancy;
**logic-correctness** broadly — especially on calculations, conditionals, and business rules;
**resource-performance** on loops over data, queries, caches, and user-controlled sizes.

## Scale & monorepos

A whole-repo deep hunt on a large or unfamiliar codebase can be unbounded. Before committing
to it:

- **Estimate size** (file count, languages, LOC) during detection.
- If it's large (e.g. a monorepo, or thousands of files), **present the ranked hotspots and a
  proposed scope/budget to the user and confirm** before fanning out — e.g. "I'll deep-hunt
  these 8 hotspots with these lenses; want me to widen, narrow, or focus on a package?"
- Prefer **targeted hunts per package/service** over one boil-the-ocean pass; hunt the
  highest-risk areas first and expand only if they're productive.
- Exclude generated code, vendored dependencies, and build output unless specifically asked.

## 5. Hand off

Pass the hunt plan to [fanout-orchestration.md](fanout-orchestration.md), which turns the
ranked hotspots × selected lenses into the actual hunter assignments.
