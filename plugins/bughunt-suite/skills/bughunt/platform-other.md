# Platform Catalog: Other Ecosystems & Generic Fallback

The four core catalogs (Apple, Web, Systems, Backend+CLI) cover the most common targets. This
catalog extends coverage to other ecosystems and — crucially — gives a **generic strategy for
any language not listed**, so the hunt never stalls on an unfamiliar stack.

## Android / Kotlin / Java (mobile)  (→ state-lifecycle, concurrency, error-failure)

- **Lifecycle:** work tied to `Activity`/`Fragment` lifecycle leaking the context; doing I/O in
  `onCreate`; state lost on configuration change/rotation; `Context` leaks (static/inner class).
- **Concurrency:** UI updates off the main thread; coroutine scope not cancelled with lifecycle
  (`viewModelScope`/`lifecycleScope` misuse); blocking the main thread (ANR).
- **NPE & null:** platform types from Java returning null into non-null Kotlin (`!!` crashes);
  `lateinit` accessed before init.
- **Intents/IPC:** trusting `Intent` extras/deep links (→ taint); exported components without
  permission; implicit intents leaking data.
- **Storage/permissions:** secrets in `SharedPreferences`/logs; runtime permission not checked.

## .NET / C#  (→ concurrency, error-failure, boundaries-numeric)

- **async/await:** `async void` (unobservable exceptions); `.Result`/`.Wait()` deadlocks;
  missing `ConfigureAwait(false)` in libraries; fire-and-forget tasks swallowing errors.
- **Disposal:** `IDisposable` not disposed (no `using`); disposing shared/injected objects.
- **Null:** `NullReferenceException`; nullable-reference-types warnings ignored.
- **LINQ:** multiple enumeration of `IEnumerable` (re-runs queries / side effects); deferred
  execution surprises; N+1 with EF Core (→ resource-performance).
- **Equality/struct:** value vs reference equality; mutable structs; `==` vs `.Equals`.
- **Security:** SQL via string concat, deserialization (`BinaryFormatter`), weak crypto (→ auth-access).

## PHP  (→ taint, auth-access, boundaries-numeric)

- **Injection:** SQL via interpolation (use PDO prepared statements); command injection
  (`exec`/`system`/`shell_exec`); XSS via unescaped echo; LFI/RFI via `include`/`require` on input.
- **Type juggling:** `==` loose comparison (`"0e123" == "0e456"` true; `0 == "abc"` varies by
  version); use `===`. `in_array`/`switch` loose matching.
- **Auth:** `password_hash`/`password_verify` (not md5/sha1); session fixation; `$_REQUEST`
  trusting mixed sources.
- **Files/deserialization:** `unserialize` on untrusted input (object injection); upload handling.

## Dart / Flutter & React Native (cross-platform mobile)  (→ state-lifecycle, concurrency)

- **Flutter:** `setState` after dispose; controllers (`AnimationController`, `TextEditingController`)
  not disposed; `BuildContext` used across async gaps; unbounded `ListView` building.
- **React Native:** same JS/TS footguns as [platform-web.md](platform-web.md) plus bridge
  serialization, native-module thread assumptions, and `useEffect` cleanup on unmount.

## SQL & data layer  (→ resource-performance, error-failure, logic-correctness)

- **Correctness:** `NULL` comparison semantics (`= NULL` never true; `NOT IN` with NULLs);
  `JOIN` fan-out duplicating rows; missing `GROUP BY` columns; implicit type coercion.
- **Transactions:** missing/incorrect isolation level; lost updates; long transactions holding locks.
- **Performance:** missing indexes; full scans; N+1 from the app; `SELECT *`; non-sargable
  predicates; unbounded result sets.
- **Migrations:** non-reversible; locking large tables; data backfill in a blocking migration.

## Infrastructure-as-code / config (Terraform, k8s, Docker, YAML)  (→ auth-access, error-failure)

- **Security:** secrets in plaintext/committed; overly broad IAM (`*` actions/resources);
  public buckets/security groups (`0.0.0.0/0`); privileged containers; `:latest` tags.
- **Reliability:** no resource limits/requests; missing health checks; no rollback strategy;
  single replica for critical services.
- **Config drift:** environment-specific values hardcoded; YAML indentation/type pitfalls
  (`no`/`yes` parsed as booleans, unquoted versions becoming floats).

## Data science / notebooks (Python)  (→ logic-correctness, boundaries-numeric)

- Hidden state / out-of-order cell execution; mutated DataFrames in place; `SettingWithCopyWarning`.
- Data leakage between train/test; off-by-one in slicing; silent `NaN` propagation; float equality.
- See also [platform-backend-cli.md](platform-backend-cli.md) for core Python footguns.

## Generic fallback — any unlisted language/framework

When the target's ecosystem isn't catalogued here, you still hunt effectively:

1. **Apply the language-agnostic lenses** — taint, state/lifecycle, concurrency,
   boundaries/numeric, error/failure, contract/spec, auth/access, logic-correctness,
   resource/performance all apply regardless of language.
2. **Identify this language's equivalents** of the universal footgun categories: How is null/
   absence represented? How are errors signalled (exceptions/return codes/Result)? What's the
   concurrency model? How is untrusted input parsed? What's the memory/resource model?
3. **Read its idioms first** — skim a few files and any linter/style config to learn the
   project's conventions, then look for deviations from them (deviations are bug-prone).
4. **Look up the language's known sharp edges** — most languages have a well-known "gotchas"
   list (equality, coercion, default mutability, scoping, integer behavior). Apply it.
5. **Ask the user** about domain-specific invariants and any house rules when the stack is
   unusual — they know the footguns that aren't in any catalog.

The catalogs are accelerants, not prerequisites. The lenses are the engine.

## Cross-references

- Core catalogs: [platform-apple.md](platform-apple.md), [platform-web.md](platform-web.md),
  [platform-systems.md](platform-systems.md), [platform-backend-cli.md](platform-backend-cli.md).
- Score and report via [triage](../triage/SKILL.md).
