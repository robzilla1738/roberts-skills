# Lens: Product & UX

**Hunts for:** code that produces a broken, confusing, or dead-end experience for
the end user — missing loading/empty/error states, silently-failing actions,
flags stuck off, double-submits, and presentation that can't be perceived or
acted on. The system may be internally correct while the user is left blank,
stuck, or misled.

## Mental model

For every user-facing render and handler, enumerate the outcomes the user can hit
— **loading, success, empty, error** — and ask: **can the user *see* what state
they're in, and *act* on it?** A bug exists whenever an outcome branch renders
nothing, renders `undefined`/`null`, spins forever, or fails without telling the
user. Correctness of the data is not enough; the user has to be informed and
recoverable.

This lens follows outcome *branches*, not data flow. The question is never "is the
value right" but "what does the human see when it isn't, and what can they do
next."

## Smells

**Missing async states**
- A data fetch with no loading state — the UI shows nothing, or stale data, while
  the request is in flight.
- No empty state for zero results — a list renders blank, or "undefined"/"0
  results" leaks a raw value instead of a designed empty view.
- No error state — a failed request shows a spinner forever, a white screen, or a
  partially-rendered shell with no message.

**Swallowed user feedback**
- A `catch` that neither shows the user an error nor retries — the action
  silently fails and the user assumes it worked (see
  [lens-error-failure.md](lens-error-failure.md), [lens-dx-pain.md](lens-dx-pain.md)).
- Form submit with no success/failure signal — no toast, no inline error, no
  state change; the user clicks again, unsure.
- Optimistic update with no rollback on failure — the UI shows the new state, the
  server rejected it, and the two silently diverge.

**Dead or stuck flags**
- Feature flags checked but never toggled on, defaulting a feature off forever —
  `bughunt.py signals` surfaces flag refs under `flags`; trace whether the gate
  is ever set true.
- Gated code paths that are statically unreachable (a flag const'd to `false`, a
  branch behind a condition that can't hold).
- A/B branches where one arm is dead code — the experiment shipped but only one
  variant can run.

**Friction & dead ends**
- No disabled/pending state on a submit button → double-submit, duplicate order,
  duplicate charge.
- Destructive action (delete, overwrite, cancel) with no confirm step or undo.
- Navigation that drops unsaved input — no dirty-state guard before route change
  or unload.
- Infinite load with no timeout or retry affordance — the user can only refresh
  the whole page.

**Accessibility & correctness of presentation**
- Interactive element with no accessible label/role (`<div onClick>`, icon button
  with no `aria-label`) — unusable by keyboard/screen reader.
- Status conveyed by color only (red/green with no text/icon) — invisible to
  colorblind users.
- Copy that interpolates a raw error object, `null`, `undefined`, `[object
  Object]`, or an internal id into user-visible text.

## How to trace

1. Find the user-facing boundaries: components, route handlers, and endpoints
   returning HTML/JSON that a UI consumes.
2. For each, enumerate the outcome branches — loading, success, empty, error —
   and check that each renders something the user can perceive.
3. For every action (submit, delete, navigate), check there's a pending state, a
   result signal, and a recovery path on failure.
4. Check perceivability: labels/roles on interactive elements, non-color status,
   and that no raw internal value reaches the screen.

## Evidence to capture

The specific outcome branch that fails the user and what they see: e.g. "fetch at
`UserList.tsx:30` has loading + success branches but no error branch — a 500
leaves an infinite spinner", or "submit handler `checkout.ts:88` has no pending
state on the button → second click fires a duplicate POST". Name the user-visible
symptom (blank screen, infinite spinner, silent no-op, double charge), not just
the missing code.

## Common false positives to reject

- A loading/empty/error state handled one layer up (a shared `<Suspense>`,
  error boundary, or wrapper) — verify it actually covers this branch.
- A flag that *is* toggled elsewhere (env, remote config, admin panel) — confirm
  it's truly stuck before flagging.
- An internal/admin/dev-only surface where polish is out of scope (state it).
- A "missing confirm" on an action that is trivially reversible (has an undo).
- A button without an explicit pending state that the framework already disables
  during the in-flight mutation.
- Raw-value-in-copy that is actually behind a `// dev only` / debug guard.

## Cross-references

- [lens-error-failure.md](lens-error-failure.md) — the runtime side of a swallowed
  failure. Boundary: **product-ux** cares whether the *user is informed and
  recoverable*; **error-failure** whether the *system stays correct*. A silent
  `catch` is a finding in both for different reasons.
- [lens-state-lifecycle.md](lens-state-lifecycle.md) — stale/diverged UI state and
  optimistic-update rollback as a state-machine problem.
- [lens-dx-pain.md](lens-dx-pain.md) — the same swallow that blanks the user often
  blinds the developer too.
- Platform specifics in [platform-web.md](platform-web.md) and
  [platform-apple.md](platform-apple.md); score via [triage](../triage/SKILL.md).
