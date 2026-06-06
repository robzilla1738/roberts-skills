# Lens: Dataflow & Taint

**Hunts for:** untrusted data reaching a dangerous operation without adequate validation,
sanitization, or escaping.

## Mental model

Every input from outside your trust boundary is **tainted** until proven clean. Follow each
tainted value forward: where does it flow, and does it reach a **sink** that interprets it as
code, a path, a query, or a request? A bug exists when taint reaches a sink and no
sanitizer sits on the path.

```
SOURCE (tainted)  ->  ...propagation...  ->  SINK (dangerous)
   request body         passed, concatenated      SQL string / exec / fs path / HTML
```

## Sources (where taint enters)

Request params/body/headers, URL/query, cookies, CLI argv/stdin, env vars, file contents,
deserialized payloads (JSON/XML/YAML/pickle/plist), DB rows written by users, third-party
API responses, deep links / URL schemes, IPC messages, filenames in uploads.

## Sinks (where taint hurts)

| Sink | Bug class |
|------|-----------|
| SQL/ORM raw query | SQL injection |
| `exec`/`system`/shell, subprocess with shell | Command injection |
| HTML/DOM/template render | XSS |
| File path open/read/write | Path traversal |
| Outbound HTTP with user-controlled URL | SSRF |
| Redirect target | Open redirect |
| Deserializer on untrusted bytes | Object injection / RCE |
| `eval`/dynamic code/format string | Code injection |
| Log statement | Secret/PII leakage |
| LDAP/NoSQL/XPath query | Respective injection |

## Smells

- String concatenation/interpolation building a query, command, path, or URL.
- "Validation" that's a denylist, or happens after use, or is bypassable.
- Sanitizer for the wrong context (HTML-escaping a value used in a SQL string).
- Trust placed in client-supplied IDs for authorization (see also IDOR in platform-web).
- Decoding/parsing untrusted bytes with a permissive/unsafe deserializer.
- Secrets, tokens, or full request objects passed to loggers.

## How to trace

1. List the sources reachable in this area (from recon's trust-boundary map).
2. For each, follow the value through assignments, function calls, and returns to a sink.
3. On the path, look for a sanitizer/validator/parameterization that neutralizes it **for the
   sink's context**. No correct sanitizer on the path → candidate finding.
4. Confirm the sink actually interprets the data dangerously (a parameterized query is safe;
   raw concatenation is not).

## Evidence to capture

Source location, the propagation path (file:line hops), the sink, and a concrete malicious
input that would exploit it (e.g. `'; DROP TABLE`, `../../etc/passwd`, `http://169.254.169.254/`).

## Common false positives to reject

- The value is parameterized/bound at the sink (e.g. prepared statement) → safe.
- A correct, context-appropriate sanitizer sits on every path to the sink.
- The "source" is actually internal/trusted and never user-controlled.
- A type constraint (enum, validated int) makes malicious values unrepresentable.
