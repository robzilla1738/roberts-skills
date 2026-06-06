# Platform Catalog: Systems (C / C++ / Rust / Go)

Footguns for systems languages — memory, undefined behavior, and the unsafe boundaries.
Pair with the analysis lenses.

## C / C++

**Memory safety  (→ state-lifecycle, boundaries-numeric)**
- Buffer overflows: `strcpy`/`strcat`/`sprintf`/`gets`, off-by-one in bounds, missing NUL terminator.
- Use-after-free, double-free, dangling pointers (esp. returning address of local, freed-then-used).
- Uninitialized memory read; reading past allocation.
- Memory/resource leaks on error paths (early return before `free`/`close`).
- Iterator/pointer invalidation after container resize/erase (`vector` realloc, `erase` in loop).
- Mismatched `new`/`delete` vs `new[]`/`delete[]`; `malloc`/`free` vs `new`/`delete`.

**Undefined behavior  (→ boundaries-numeric)**
- Signed integer overflow (UB), shift by >= width, `INT_MIN`/-1.
- Null-pointer deref the optimizer assumes can't happen; strict-aliasing violations.
- Out-of-bounds access; data races (also UB in C++11+).
- Order-of-evaluation/sequence-point assumptions (`i = i++`).

**Other**
- Format string bugs (`printf(user)`); integer→size conversions; signed/unsigned comparison.
- Error returns ignored (`malloc` returning NULL, `read`/`write` short counts).
- C++: exception safety (leak/partial state if a ctor/op throws); rule-of-3/5/0 violations;
  dangling references to temporaries; `std::move`-then-use.

## Rust  (→ concurrency, error-failure, state-lifecycle)

- **`unsafe` blocks:** every one is a manual safety contract — verify invariants (valid
  pointers, no aliasing `&mut`, correct lifetimes, no UB). This is where Rust bugs live.
- **FFI boundaries:** raw pointers from C, null handling, ownership/free responsibility,
  `CString` lifetime, `repr(C)` layout assumptions.
- `unwrap`/`expect`/`panic!`/array indexing on values that can be None/Err/out-of-range (panic).
- Integer overflow (panics in debug, **wraps in release** — silent corruption).
- `mem::transmute`, `from_raw`/`into_raw` ownership mistakes.
- Blocking calls inside async (starving the executor); holding a `std::sync` lock across `.await`.
- `Rc`/`RefCell` borrow panics at runtime; reference cycles leaking with `Rc`.
- Ignored `Result` (`let _ =`, `#[must_use]` ignored).

## Go  (→ concurrency, error-failure, state-lifecycle)

- **Goroutine leaks:** goroutines blocked forever on a channel send/receive nobody serves;
  missing context cancellation.
- **Channel bugs:** send on closed channel (panic), close twice, deadlock on unbuffered
  channel, nil channel blocking forever.
- **Data races:** shared maps/slices/fields written from multiple goroutines without a mutex
  (run with `-race`). Maps are not concurrency-safe.
- **`nil` deref:** nil pointer, nil map write (panic), nil interface vs nil pointer (`err != nil`
  surprises when a typed nil is boxed).
- **Ignored errors:** `_ = f()`, error returned but not checked; `defer` errors dropped.
- **Loop variable capture** in goroutines/closures (pre-1.22 footgun; verify Go version).
- `defer` in a loop accumulating until function return (resource held too long).
- Slice aliasing: `append` mutating a shared backing array; subslice retaining a huge array.
- `recover` only in deferred funcs; panics across goroutines crash the process.

## High-yield hunt spots

Every `unsafe`/FFI boundary, manual allocation/free sites, parsers and byte handling,
goroutine/channel orchestration, shared-state concurrency, and all error-return sites. Run
the language's race/sanitizer tooling (`-race`, ASan/UBSan/TSan, Miri) where you can — pair
with [fuzz](../fuzz/SKILL.md).
