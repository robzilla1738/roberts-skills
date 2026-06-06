# Lens: Authorization & Access Control

**Hunts for:** the wrong actor being allowed to do or see something — broken authentication,
missing or incorrect authorization, privilege escalation, tenant isolation failures, and the
session/token/crypto/secret handling that underpins them.

## Mental model

For every sensitive action and every protected resource, ask three questions: **Who is
allowed?** **Is that actually enforced here — server-side, on every path?** **Is the check
scoped to *this* caller's identity and tenant?** A bug exists when the answer to any is "no"
or "not really." Authentication proves *who you are*; authorization decides *what you may do*
— most damaging access bugs are in the second.

## Smells

**Authentication**
- A route/endpoint/handler with no auth check while its siblings have one (the forgotten one).
- Auth enforced in the UI/client only; the API trusts the client.
- JWT: `alg: none` accepted, signature not verified, expiry/`nbf` not checked, secret confusion
  (HS/RS), tokens never invalidated on logout/password-change.
- Session fixation (session id not rotated after login); predictable/guessable tokens.

**Authorization (the high-yield area)**
- **IDOR:** acting on a client-supplied id (`/orders/:id`, `userId` from body) without
  checking the caller **owns** it. Horizontal escalation = reading/altering peers' data.
- Missing role/permission check on some actions while present on others; admin action reachable
  by a normal user. Vertical escalation.
- Authorization decided from client-supplied role/flags (`isAdmin` in the request/JWT claim the
  client can set) instead of server state.
- Check-then-act on permissions (permission revoked between check and use).
- Authorization at the wrong layer (checked in a controller but the resource is also reachable
  via a job, GraphQL resolver, or internal API that skips it).

**Multi-tenancy / data isolation**
- Queries not scoped by `tenant_id`/`org_id` — a filter that defaults to "all" if a param is
  missing. Shared caches keyed without the tenant. Row-level filters omitted on one path.

**Crypto & secrets**
- Hardcoded secrets/keys/credentials in source or config; secrets committed to the repo.
- Weak/incorrect crypto: MD5/SHA1 (or plain hashes) for passwords instead of bcrypt/scrypt/
  argon2; ECB mode; static/reused IV or nonce; home-rolled crypto; non-constant-time comparison
  of secrets/tokens.
- **Insecure randomness** for security tokens/ids (`Math.random`, `rand()`, time-seeded) where
  a CSPRNG is required.
- Secrets in logs, URLs/query strings, error messages, or shipped to the client.
- TLS/cert verification disabled (`verify=False`, `rejectUnauthorized:false`,
  `InsecureSkipVerify`).

## How to trace

1. Enumerate sensitive operations and protected resources (from recon's trust-boundary map).
2. For each, locate the enforcement point. Confirm it runs **server-side**, on **every** path
   that reaches the operation (controller, job, resolver, internal call).
3. Confirm the check is scoped to the caller's identity/tenant — not just "is logged in," but
   "is allowed *this* object."
4. For tokens/crypto/secrets, check generation, storage, transmission, and comparison.

## Evidence to capture

The resource/action, the missing or weak check (`file:line`), and a concrete attacker
scenario: e.g. "user A calls `GET /api/invoices/{B's id}` and receives user B's invoice — no
ownership check at `controller.rb:42`."

## Common false positives to reject

- Enforcement happens at a gateway/middleware/policy layer you hadn't read — verify it covers
  this path.
- The framework enforces ownership/tenancy globally (e.g. a default scope) and it's active here.
- The resource is genuinely public by design.
- The "client-supplied role" is re-validated server-side before use.

## Cross-references

- [lens-dataflow-taint.md](lens-dataflow-taint.md) — untrusted *input* reaching sinks; this
  lens is about *who is allowed*, not what the data contains.
- [lens-error-failure.md](lens-error-failure.md) — a check that **fails open** on error.
- Platform specifics: [platform-web.md](platform-web.md) (IDOR, JWT, CORS/CSRF),
  [platform-backend-cli.md](platform-backend-cli.md) (mass assignment, ORM scoping),
  [platform-apple.md](platform-apple.md) (Keychain, data protection).
- Score and report via [triage](../triage/SKILL.md); access-control flaws are often Critical/High.
