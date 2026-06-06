# Platform Catalog: Web (JavaScript / TypeScript / Node)

Footguns for browser and Node code. Pair with the analysis lenses.

## Injection & output  (→ taint)

- **XSS:** `innerHTML`/`outerHTML`/`insertAdjacentHTML`, `dangerouslySetInnerHTML`,
  `document.write`, unescaped template interpolation, `v-html`. Trace user data to the DOM.
- **DOM/URL sinks:** `eval`, `Function()`, `setTimeout(string)`, `location`/`href` from input,
  `postMessage` without origin check.
- **Server injection:** raw SQL string building, `child_process.exec` with interpolation
  (use `execFile`/args), template engines with autoescape off, NoSQL query objects from body
  (`{$gt: ...}` injection).
- **Path traversal / SSRF:** `fs` paths and `fetch`/`axios` URLs built from user input.

## Authorization & sessions  (→ taint, contract-spec)

- **IDOR / missing authz:** endpoints that authenticate but don't check the user *owns* the
  resource (`/orders/:id` returning anyone's order). Trust in client-supplied IDs/roles.
- Authz check on the client only; server trusts it.
- CSRF on state-changing routes without token/SameSite.
- CORS misconfig: `Access-Control-Allow-Origin: *` with credentials; reflecting Origin.
- JWT: `alg: none`, unverified signature, secret confusion, no expiry check.
- Secrets in client bundles / `NEXT_PUBLIC_`/`VITE_` exposure / committed `.env`.

## Async pitfalls  (→ concurrency, error-failure)

- **Unhandled promise rejections:** missing `await`, floating promises, `.then` without
  `.catch`, `await` missing inside `try` so errors escape the handler.
- `forEach` with an async callback (doesn't await); use `for...of` + await or `Promise.all`.
- `Promise.all` where one rejection drops the rest (vs `allSettled`); unbounded concurrency.
- Race conditions on shared module-scope state in a server handling concurrent requests.
- `async` constructor / effect not awaited; state read before resolution.

## Type coercion & equality  (→ boundaries-numeric, contract-spec)

- `==` vs `===` coercion surprises (`0 == ''`, `null == undefined`, `[] == false`).
- `||` for defaults swallowing valid falsy values (`0`, `''`, `false`) — use `??`.
- `parseInt` without radix; `NaN` propagation; `JSON.parse` on untrusted/invalid input.
- Number precision: money in floats, `0.1 + 0.2`, integers past `MAX_SAFE_INTEGER`.
- **Prototype pollution:** merging/cloning untrusted objects touching `__proto__`/`constructor`.

## React / frontend  (→ state-lifecycle, concurrency)

- `useEffect` dependency arrays: missing deps (stale closure) or wrong deps (loops, refetch storms).
- Missing cleanup in effects (subscriptions, timers, listeners) → leaks and setState-after-unmount.
- Stale closures capturing old state/props; using state right after `setState` expecting sync update.
- Keys in lists unstable/index-based causing wrong reconciliation.
- Race between fast successive fetches: late response overwrites newer (no abort/ignore).

## Node / supply chain  (→ error-failure, taint)

- Unhandled `'error'` events on streams/emitters crashing the process.
- Unbounded buffering / backpressure ignored.
- `process.env` read without validation; missing env crashes late.
- Dependency risk: typosquats, `postinstall` scripts, lockfile not committed, unpinned ranges.
- `child_process`/deserialization of untrusted data; regex DoS (catastrophic backtracking).

## High-yield hunt spots

Request handlers and middleware (authz!), anything touching the DOM with user data, async
data-fetching layers, React effects, money/date math, object-merge utilities, and the
dependency manifest.
