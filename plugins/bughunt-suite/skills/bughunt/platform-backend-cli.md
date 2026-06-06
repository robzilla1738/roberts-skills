# Platform Catalog: Backend + CLI (Python / Ruby / Java + Terminal Tools)

Footguns for backend services in dynamic/JVM languages and for command-line tools. Pair with
the analysis lenses.

## Python  (→ boundaries-numeric, error-failure, concurrency)

- **Mutable default args:** `def f(x, acc=[])` — the default is shared across calls (classic
  silent state bug). Same for `={}`.
- **Bare/broad except:** `except:` / `except Exception: pass` swallowing everything incl.
  `KeyboardInterrupt`/bugs.
- Late binding closures in loops (`lambda: i` capturing the final `i`).
- `is` vs `==` for value comparison (works for small ints by luck, breaks otherwise).
- Truthiness swallowing valid values (`if not x` true for `0`, `''`, `[]`, `None` alike).
- **Concurrency:** GIL means threads don't parallelize CPU but **do** interleave — shared
  state still races; `asyncio` blocking calls stalling the loop; `multiprocessing` pickling.
- `datetime` naive vs aware; `dict` ordering assumptions on old versions.
- Dynamic `eval`/`exec`/`pickle.loads`/`yaml.load` on untrusted data (→ taint).

## Ruby  (→ error-failure, contract-spec)

- `rescue => e` swallowing; rescuing `Exception` (too broad).
- `nil` propagation (`NoMethodError` on nil); `&.` missing where chains can be nil.
- Monkey-patching changing behavior far from the call site; method redefinition.
- Mutable constants/strings shared; `||=` memoization caching `nil`/`false` wrongly.
- Mass assignment / unsafe `send`/`eval` on user input (→ taint).

## Java / JVM  (→ boundaries-numeric, concurrency, error-failure)

- **NullPointerException:** unchecked nulls; `Optional` misuse; autoboxing NPE (`Integer`→`int`).
- `equals`/`hashCode` contract violations (broken `HashMap`/`HashSet` behavior); using `==` on
  objects/boxed numbers.
- **Concurrency:** non-thread-safe collections (`HashMap`) shared; missing `volatile`/`synchronized`;
  check-then-act on shared state; `SimpleDateFormat`/`Calendar` not thread-safe.
- Resource leaks: streams/connections not in try-with-resources.
- Integer overflow; `int`/`long` division; `BigDecimal` for money (not `double`).
- Deserialization of untrusted data (Java serialization RCE); SQL via string concat.
- Exceptions swallowed in `catch` blocks; `finally` masking exceptions / swallowing returns.

## ORM / data layer  (any backend, → error-failure, contract-spec, taint)

- **N+1 queries:** loop issuing a query per row (perf bug that bites at scale).
- Missing transaction boundaries; partial commits on failure (→ error-failure).
- Lazy-loading outside session/context → errors or extra queries.
- Raw SQL fragments with interpolation (→ taint); mass-assignment of protected fields.
- Migrations that aren't reversible or lock large tables.

## CLI / terminal tools  (→ taint, error-failure, boundaries-numeric)

- **Argv/quoting:** building shell commands from args without quoting; word-splitting; globbing
  of untrusted strings. Prefer arg arrays over shell strings.
- **Exit codes:** returning 0 on failure (breaks `&&`/CI); not distinguishing error classes.
- **Broken pipe / SIGPIPE:** crashing when output is piped to `head`/`grep -q` and closed early.
- **Buffering:** stdout block-buffered when piped → lost/delayed output; mixing buffered stdout
  with unbuffered stderr ordering.
- **Signals:** no `SIGINT`/`SIGTERM` handling → no cleanup of temp files / partial output on Ctrl-C.
- **Temp files:** predictable names / race (`/tmp/app.$$`) → symlink attacks; use `mkstemp`.
- **stdin:** assuming a TTY; hanging waiting for input when none piped; not handling EOF.
- **Paths/encoding:** spaces/unicode/newlines in filenames; relative-path assumptions; `~`/env
  expansion bugs.
- **Bash specifically:** missing `set -euo pipefail`; unquoted `$var` and `$@`; `[ ]` vs `[[ ]]`;
  `cd` without `||exit`; `rm -rf "$DIR/"` when `$DIR` may be empty (→ catastrophic deletion);
  pipeline exit status hiding failures (without `pipefail`).

## High-yield hunt spots

Request handlers and service boundaries, the ORM/data layer (N+1, transactions, injection),
auth/permission code, anything calling out to the shell or deserializing input, argument
parsing and exit-code paths in CLIs, and shell scripts lacking strict mode.
