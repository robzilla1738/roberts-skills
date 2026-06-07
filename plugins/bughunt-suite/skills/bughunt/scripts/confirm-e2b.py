#!/usr/bin/env python3
"""confirm-e2b.py — the optional E2B-backed Confirm rung for bughunt (hunt-loop step 7).

This is where E2B sandboxes actually belong. The Hunt and static-Verify phases are read-only
static analysis and gain nothing from a sandbox. The *Confirm* tail does: it RUNS a repro or a
fuzz/property harness against a Probable finding to earn a **Confirmed** verdict — and that is
exactly the kind of untrusted-code execution a throwaway isolated sandbox is for. Doing it
across findings in parallel both speeds the tail up and lets you confirm more findings.

Division of labour (matches the rest of bughunt):
  - The AGENT (or the /fuzz skill) constructs the executable repro for a finding — the setup
    commands and the one command whose exit code decides the verdict. It hands them in via a
    --repro-map JSON keyed by finding id or fingerprint.
  - THIS SCRIPT is the deterministic execution substrate: it spins one ephemeral E2B sandbox
    per finding, syncs the repo, runs setup + the repro, maps the exit code to a verdict, and
    stamps the finding's `verified` field with a DYNAMIC method (failing-test / runtime-repro /
    property-test). It owns isolation, parallelism, timeouts, and teardown — not judgment.

Output is a findings document you pipe straight back into merge, which re-routes verdicts and
re-labels confirmed findings:

    python3 confirm-e2b.py .bughunt/findings.json --repro-map repros.json \\
      | python3 bughunt.py merge - --require-verified --require-coverage --strict --write-baseline

STRICTLY OPTIONAL / OPT-IN. Requires `pip install e2b` and an E2B_API_KEY. With neither (or in
--dry-run), it degrades cleanly: the Confirm step stays the manual /fuzz + verify path and the
pipeline is never blocked — Probable findings simply remain Probable.

Guardrails (E2B bills per second — a stalled repro is a real cost): every sandbox has a hard
--timeout, concurrency is capped with --concurrency, sandboxes are always killed in a finally,
and nothing from your environment is uploaded beyond the repo you point it at.

Zero-dependency for --dry-run/--help (stdlib only). The `e2b` import happens lazily, only on a
live run, so this file loads and self-tests without the SDK installed.
"""

import argparse
import concurrent.futures
import json
import os
import sys

DYNAMIC_METHODS = ("failing-test", "runtime-repro", "property-test")
DEFAULT_SEVERITIES = ("Critical", "High")


def eprint(*a):
    print(*a, file=sys.stderr)


def load_doc(path):
    raw = sys.stdin.read() if path == "-" else open(path, "r", encoding="utf-8").read()
    doc = json.loads(raw)
    if not isinstance(doc, dict) or not isinstance(doc.get("findings"), list):
        raise ValueError("input must be a merged findings document with a 'findings' array")
    return doc


def finding_key(f):
    return f.get("id") or f.get("fingerprint") or f.get("title")


def already_confirmed(f):
    v = f.get("verified") or {}
    return v.get("verdict") == "upheld" and v.get("method") in DYNAMIC_METHODS


def select(findings, severities, want_all, repro_map):
    """Pick findings worth a runtime confirm: high-value, not already runtime-confirmed, and
    either carrying a repro spec (live) or any repro/fixSketch hint (dry-run preview)."""
    out = []
    for f in findings:
        if already_confirmed(f):
            continue
        if not want_all and f.get("severity") not in severities:
            continue
        has_spec = finding_key(f) in repro_map
        has_hint = bool(f.get("repro") or f.get("fixSketch"))
        if has_spec or has_hint or want_all:
            out.append(f)
    return out


# --------------------------------------------------------------------------------------------
# Live path — one ephemeral E2B sandbox per finding. Imported lazily.
# --------------------------------------------------------------------------------------------
def _cmd(sandbox, cmd, cwd, timeout):
    """Run a shell command, returning (exit_code, stdout, stderr) whether or not it raised."""
    try:
        from e2b import CommandExitException  # type: ignore
    except Exception:  # pragma: no cover - SDK shape guard
        CommandExitException = None
    try:
        r = sandbox.commands.run(cmd, cwd=cwd, timeout=timeout)
        return r.exit_code, getattr(r, "stdout", ""), getattr(r, "stderr", "")
    except Exception as e:  # CommandExitException carries the failed result's fields
        if CommandExitException and isinstance(e, CommandExitException):
            return (getattr(e, "exit_code", 1), getattr(e, "stdout", ""), getattr(e, "stderr", ""))
        return 1, "", f"{type(e).__name__}: {e}"


def confirm_one(finding, spec, args):
    """Reproduce one finding inside a fresh sandbox; return its `verified` verdict object."""
    from e2b import Sandbox  # lazy: only needed on a live run

    key = finding_key(finding)
    method = spec.get("method", "failing-test")
    if method not in DYNAMIC_METHODS:
        method = "failing-test"
    expect = spec.get("expect", "nonzero-means-bug")
    workdir = args.workdir
    sandbox = None
    try:
        sandbox = Sandbox(template=args.template, timeout=args.timeout,
                          api_key=os.environ.get("E2B_API_KEY"))
        # 1) sync the repo
        if args.repo_url:
            ref = f" --branch {args.repo_ref}" if args.repo_ref else ""
            code, _o, err = _cmd(sandbox, f"git clone --depth 1{ref} {args.repo_url} {workdir}",
                                 cwd="/", timeout=args.timeout)
            if code != 0:
                return _verdict("uncertain", method, f"repo clone failed: {err[-300:]}")
        # 2) setup commands from the repro spec (deps, build)
        for s in spec.get("setup", []):
            code, _o, err = _cmd(sandbox, s, cwd=workdir, timeout=args.timeout)
            if code != 0:
                return _verdict("uncertain", method, f"setup failed `{s[:60]}`: {err[-300:]}")
        # 3) the repro command — its exit code decides the verdict
        cmd = spec.get("cmd")
        if not cmd:
            return _verdict("uncertain", method, "repro spec had no 'cmd'")
        code, out, err = _cmd(sandbox, cmd, cwd=workdir, timeout=args.timeout)
        reproduced = (code != 0) if expect == "nonzero-means-bug" else (code == 0)
        tail = (out or err or "")[-300:].replace("\n", " ")
        verdict = "upheld" if reproduced else "refuted"
        note = (f"e2b repro `{cmd[:50]}` exit={code} ({expect}); "
                f"{'reproduced' if reproduced else 'did not reproduce'}. {tail}")
        return _verdict(verdict, method, note)
    except Exception as e:  # sandbox create / network / SDK error -> honest uncertain
        return _verdict("uncertain", method, f"e2b error for {key}: {type(e).__name__}: {e}")
    finally:
        if sandbox is not None:
            try:
                sandbox.kill()
            except Exception:
                pass


def _verdict(verdict, method, note):
    return {"by": "e2b-confirm", "method": method, "verdict": verdict, "note": note[:800]}


def run_live(candidates, repro_map, args):
    runnable = [(f, repro_map[finding_key(f)]) for f in candidates if finding_key(f) in repro_map]
    skipped = [f for f in candidates if finding_key(f) not in repro_map]
    for f in skipped:
        eprint(f"[confirm] no repro-map entry for {finding_key(f)} — left Probable")
    if not runnable:
        eprint("[confirm] nothing to run (provide --repro-map with executable repros; see confirm.md)")
        return {}
    eprint(f"[confirm] running {len(runnable)} repro(s) in E2B "
           f"(template={args.template}, concurrency={args.concurrency}, timeout={args.timeout}s)")
    verdicts = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {ex.submit(confirm_one, f, spec, args): f for f, spec in runnable}
        for fut in concurrent.futures.as_completed(futs):
            f = futs[fut]
            v = fut.result()
            verdicts[finding_key(f)] = v
            eprint(f"[confirm] {finding_key(f)}: {v['verdict']} ({v['method']})")
    return verdicts


# --------------------------------------------------------------------------------------------
def main(argv):
    ap = argparse.ArgumentParser(description="E2B-backed Confirm rung for bughunt (opt-in).")
    ap.add_argument("findings", help="merged findings JSON file, or - for stdin")
    ap.add_argument("--repro-map", help="JSON: {id|fingerprint: {setup:[...], cmd, expect, method}}")
    ap.add_argument("--repo-url", help="git URL to clone into each sandbox")
    ap.add_argument("--repo-ref", help="branch/tag/ref to clone (default: repo default)")
    ap.add_argument("--template", default="base", help="E2B template/snapshot id (bake repo+toolchain here to skip clones)")
    ap.add_argument("--workdir", default="/home/user/repo", help="path inside the sandbox to run in")
    ap.add_argument("--severity", default=",".join(DEFAULT_SEVERITIES), help="comma list of severities to target")
    ap.add_argument("--all", action="store_true", help="ignore severity filter; consider every finding")
    ap.add_argument("--concurrency", type=int, default=4, help="max parallel sandboxes (E2B Hobby cap is 20)")
    ap.add_argument("--timeout", type=int, default=300, help="per-sandbox timeout in seconds")
    ap.add_argument("--dry-run", action="store_true", help="select + stamp without creating sandboxes (offline)")
    ap.add_argument("--out", help="write the updated findings doc here (default: stdout)")
    args = ap.parse_args(argv)

    doc = load_doc(args.findings)
    findings = doc["findings"]
    severities = tuple(s.strip() for s in args.severity.split(",") if s.strip())
    repro_map = {}
    if args.repro_map:
        repro_map = json.load(open(args.repro_map, "r", encoding="utf-8"))

    candidates = select(findings, severities, args.all, repro_map)
    eprint(f"[confirm] {len(candidates)}/{len(findings)} finding(s) selected for confirm "
           f"(severities={severities}{' +all' if args.all else ''})")

    if args.dry_run:
        # Offline preview: stamp each candidate with a dynamic method + uncertain verdict so the
        # downstream merge accepts it and a human can see what WOULD be confirmed.
        for f in candidates:
            spec = repro_map.get(finding_key(f), {})
            method = spec.get("method", "runtime-repro")
            if method not in DYNAMIC_METHODS:
                method = "runtime-repro"
            f["verified"] = _verdict("uncertain", method, "dry-run: no sandbox executed")
        emit(doc, args.out)
        eprint(f"[confirm] dry-run stamped {len(candidates)} finding(s) (no E2B calls)")
        return 0

    # Live path needs the SDK + a key; degrade to a clean no-op passthrough otherwise.
    if not os.environ.get("E2B_API_KEY"):
        eprint("[confirm] E2B_API_KEY not set — Confirm rung unavailable; leaving findings as-is "
               "(fall back to manual /fuzz + verify). Pipeline not blocked.")
        emit(doc, args.out)
        return 0
    try:
        import e2b  # noqa: F401
    except Exception:
        eprint("[confirm] `e2b` SDK not installed (pip install e2b) — Confirm rung unavailable; "
               "leaving findings as-is. Pipeline not blocked.")
        emit(doc, args.out)
        return 0

    verdicts = run_live(candidates, repro_map, args)
    for f in findings:
        v = verdicts.get(finding_key(f))
        if v:
            f["verified"] = v
    emit(doc, args.out)
    return 0


def emit(doc, out_path):
    out = {"schemaVersion": doc.get("schemaVersion", "1.0"),
           "coverage": doc.get("coverage", {}),
           "findings": doc["findings"]}
    text = json.dumps(out, indent=2)
    if out_path:
        open(out_path, "w", encoding="utf-8").write(text + "\n")
        eprint(f"[confirm] wrote {out_path}")
    else:
        sys.stdout.write(text + "\n")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (ValueError, json.JSONDecodeError, OSError) as e:
        eprint(f"confirm-e2b.py: {e}")
        sys.exit(3)
