# Platform Catalog: Apple (Swift / Objective-C)

Ecosystem-specific footguns for iOS and macOS. Pair with the analysis lenses — this catalog
tells you *what shapes are dangerous here and where they hide*.

## Optionals & unwrapping  (→ boundaries-numeric)

- **Force-unwrap `!`** on optionals that can be nil at runtime — `value!`, `as!` casts,
  `try!`. Each is a potential crash. Hunt every `!` not provably safe.
- Implicitly unwrapped optionals (`var x: T!`) read before assignment (esp. IBOutlets,
  DI-injected, lifecycle-dependent properties).
- `as!` downcasts on data of uncertain type (decoded JSON, `Any` from ObjC, notification
  userInfo).
- Empty-collection `.first!`/`.last!`, `array[index]` out of range, `String.Index` misuse.

## Memory management  (→ state-lifecycle)

- **Retain cycles:** closures capturing `self` strongly where the closure outlives or is
  owned by self (stored closures, Combine sinks, `Task {}`, delegates). Look for missing
  `[weak self]`/`[unowned self]`.
- Strong delegate references (delegates should usually be `weak`).
- `unowned` references outliving their target → crash on access.
- Timers (`Timer.scheduledTimer` with target) and `NotificationCenter`/KVO observers retaining
  and never invalidated/removed → leaks.
- ObjC: over/under-retain in manual bridging, `__bridge` cast mistakes.

## Concurrency  (→ concurrency)

- **Main-thread violations:** UIKit/AppKit calls off the main thread; UI updates from a
  background queue (data race + crash). And the inverse: heavy work on the main thread.
- `@MainActor` correctness: actor isolation assumed but crossed; `nonisolated` misuse.
- **Sendable** violations: non-Sendable types crossing actor/task boundaries (data races).
- `DispatchQueue.sync` causing deadlock (esp. `sync` to main from main, or reentrant `sync`
  on a serial queue).
- Captured mutable state in concurrent `DispatchQueue.async`/`Task` without isolation.
- `async let` / `TaskGroup` cancellation not propagated; unstructured `Task {}` leaking.
- `await` suspension points invalidating invariants held across them.

## Codable & serialization  (→ boundaries-numeric, error-failure)

- Decoding assuming keys present/optional incorrectly; force-unwrap after decode.
- `try?` on decode swallowing real format errors (silent nil).
- Date/number decoding strategy mismatches; floating point for currency.
- Migrating persisted models (UserDefaults, Core Data, SwiftData) without versioning.

## Lifecycle  (→ state-lifecycle)

- View controller / SwiftUI view lifecycle assumptions: using a value before `viewDidLoad`/
  `onAppear`; work in `init` that belongs in a lifecycle callback.
- `deinit` doing work that requires a still-valid graph (already torn down).
- App backgrounding/foregrounding state not handled; tasks not suspended/resumed.
- SwiftUI: `@State`/`@StateObject` vs `@ObservedObject` ownership mistakes causing reset or
  stale state; `onAppear` firing more/less than expected.

## Other Apple-specific

- URL scheme / universal link handlers trusting input (→ taint).
- Keychain/UserDefaults storing secrets in the wrong place; data protection class wrong.
- `NSError`/`Result` ignored; completion handlers not called on all paths (→ error-failure).
- Combine: missing `store(in:)` cancels the subscription immediately; or never cancelling.

## High-yield hunt spots

App delegates and scene lifecycle, networking/decoding layers, closure-heavy view models,
anything touching `DispatchQueue`/`Task`/actors, IBOutlet-heavy controllers, persistence/
migration code, and every `!`/`try!`/`as!` in the changed files.
