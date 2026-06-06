#!/usr/bin/env python3
"""Self-tests for bughunt.py (stdlib unittest, zero dependencies).

Run:  python3 selftest.py [-v]

Covers: subcommand JSON shapes (git + non-git fallback), schema round-trip
(merge -> render md -> parse back), fingerprint stability, dedupe + cross-lens
confidence bump, suppression, baseline diff, CI exit codes, SARIF structure,
standalone HTML, coverage enforcement, verifier-aware clustering, and the diff subcommand.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bughunt  # noqa: E402

PY = sys.executable or "python3"
SCRIPT = HERE / "bughunt.py"
GIT = shutil.which("git") is not None


def run_cli(args, cwd, stdin=None):
    return subprocess.run([PY, str(SCRIPT)] + args, cwd=cwd,
                          input=stdin, capture_output=True, text=True, timeout=120)


def make_finding(**over):
    f = {
        "id": "BH-001",
        "title": "IDOR: any user can read any invoice",
        "lens": "auth-access",
        "severity": "High",
        "confidence": 0.9,
        "location": {"file": "routes/invoices.js", "startLine": 3, "endLine": 4},
        "trigger": "GET /invoices/:id with another user's id",
        "trace": "req.params.id (routes/invoices.js:3) -> findById with no owner filter",
        "impact": "horizontal privilege escalation",
        "impactClass": "security",
        "repro": "login as A, GET /invoices/B, got 200",
        "fixSketch": "scope query to caller",
    }
    f.update(over)
    return f


def doc(findings):
    return json.dumps({"schemaVersion": "1.0", "findings": findings})


class TempRepo(unittest.TestCase):
    """Base: a small temp project with one bug-shaped file."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="bughunt-selftest-"))
        (self.dir / "routes").mkdir()
        (self.dir / "routes" / "invoices.js").write_text(
            "const db = require('../db');\n"
            "// TODO: add ownership check before ship\n"
            "exports.get = async (req, res) => {\n"
            "  const invoice = await db.findById(req.params.id);\n"
            "  res.json(invoice);\n"
            "};\n")
        (self.dir / "routes" / "handler.js").write_text(
            "const handler = (req, res, next) => {\n"
            "  res.json({ ok: true });\n"
            "};\n")
        (self.dir / "lib").mkdir()
        (self.dir / "lib" / "pricing.js").write_text(
            "function applyDiscount(total, pct) {\n"
            "  if (pct > 100) { return total; }\n"
            "  return total - (total * pct) / 100;\n"
            "}\n"
            "module.exports = { applyDiscount };\n")
        (self.dir / "package.json").write_text(json.dumps({
            "name": "fixture", "dependencies": {"express": "^4.18.0", "lodahs": "1.0.0"},
            "scripts": {"slow": "a && b && c && d && e"}}))
        (self.dir / ".env.example").write_text("API_KEY=\nDB_URL=\n")
        (self.dir / ".env").write_text("API_KEY=x\nEXTRA=1\n")
        (self.dir / ".github" / "workflows").mkdir(parents=True)
        (self.dir / ".github" / "workflows" / "ci.yml").write_text("name: ci\non: [push]\n")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)


class TestCensusHotspotsSignalsDeps(TempRepo):
    def test_census_shape(self):
        r = run_cli(["census", "--functions"], self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        for key in ("root", "files", "languages", "totals", "functions"):
            self.assertIn(key, out)
        self.assertGreaterEqual(out["totals"]["files"], 4)
        self.assertIn("javascript", out["languages"])
        names = {f["name"] for f in out["functions"]}
        self.assertIn("applyDiscount", names)
        self.assertNotIn("handler", names)
        handler_src = (self.dir / "routes" / "handler.js").read_text()
        handler = bughunt.find_functions("routes/handler.js", "javascript", handler_src)[0]
        self.assertFalse(handler["pure_guess"])
        paths = {f["path"] for f in out["files"]}
        self.assertIn(".github/workflows/ci.yml", paths)

    def test_hotspots_non_git_mtime_fallback(self):
        r = run_cli(["hotspots", "--top", "5"], self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertFalse(out["gitAvailable"])
        self.assertTrue(out["hotspots"])
        top = out["hotspots"][0]
        for key in ("path", "score", "churn", "complexity", "boundary", "test_gap", "reasons"):
            self.assertIn(key, top)
        paths = [h["path"] for h in out["hotspots"]]
        self.assertIn("routes/invoices.js", paths)  # boundary hit

    @unittest.skipUnless(GIT, "git not on PATH")
    def test_hotspots_git_churn(self):
        env = {**os.environ, "GIT_AUTHOR_DATE": "2024-01-01T00:00:00",
               "GIT_COMMITTER_DATE": "2024-01-01T00:00:00",
               "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        for cmd in (["git", "init", "-q"], ["git", "add", "."],
                    ["git", "commit", "-qm", "one"]):
            subprocess.run(cmd, cwd=self.dir, env=env, capture_output=True, check=True)
        (self.dir / "routes" / "invoices.js").write_text("// churned\n" * 3)
        subprocess.run(["git", "commit", "-aqm", "two"], cwd=self.dir, env=env,
                       capture_output=True, check=True)
        r = run_cli(["hotspots"], self.dir)
        out = json.loads(r.stdout)
        self.assertTrue(out["gitAvailable"])
        inv = next(h for h in out["hotspots"] if h["path"] == "routes/invoices.js")
        self.assertEqual(inv["churn"], 2)

    @unittest.skipUnless(GIT, "git not on PATH")
    def test_signals_todo_age(self):
        env = {**os.environ, "GIT_AUTHOR_DATE": "2024-01-01T00:00:00",
               "GIT_COMMITTER_DATE": "2024-01-01T00:00:00",
               "GIT_AUTHOR_NAME": "alice", "GIT_AUTHOR_EMAIL": "a@t",
               "GIT_COMMITTER_NAME": "alice", "GIT_COMMITTER_EMAIL": "a@t"}
        for cmd in (["git", "init", "-q"], ["git", "add", "."],
                    ["git", "commit", "-qm", "one"]):
            subprocess.run(cmd, cwd=self.dir, env=env, capture_output=True, check=True)
        r = run_cli(["signals", "--max-age-days", "180"], self.dir)
        out = json.loads(r.stdout)
        todo = next(t for t in out["todos"] if t["kind"] == "TODO")
        self.assertEqual(todo["file"], "routes/invoices.js")
        self.assertIsNotNone(todo["ageDays"])
        self.assertGreater(todo["ageDays"], 180)
        self.assertTrue(todo["aged"])
        self.assertEqual(todo["author"], "alice")

    def test_signals_config_drift_and_scripts(self):
        r = run_cli(["signals"], self.dir)
        out = json.loads(r.stdout)
        keys = {(d["file"], d["key"]) for d in out["configDrift"]}
        self.assertIn((".env", "DB_URL"), keys)          # documented but missing
        self.assertIn((".env.example", "EXTRA"), keys)   # present but undocumented
        self.assertTrue(any(s["kind"] == "npm-script" for s in out["longScripts"]))

    def test_deps_offline(self):
        r = run_cli(["deps"], self.dir)
        out = json.loads(r.stdout)
        self.assertFalse(out["osvQueried"])
        by_name = {d["name"]: d for d in out["deps"]}
        self.assertIn("UNPINNED", by_name["express"]["issues"])
        self.assertIn("NO_LOCKFILE", by_name["express"]["issues"])
        self.assertIn("TYPOSQUAT_SHAPE", by_name["lodahs"]["issues"])
        self.assertEqual(by_name["lodahs"]["typosquatOf"], "lodash")


class TestFingerprint(TempRepo):
    def test_stable_across_line_shift_and_whitespace(self):
        f1 = make_finding()
        fp1 = bughunt.fingerprint(self.dir, f1)
        # shift the anchor down two lines, reformat whitespace
        src = (self.dir / "routes" / "invoices.js").read_text()
        (self.dir / "routes" / "invoices.js").write_text("// pad\n// pad\n" + src.replace(
            "exports.get = async (req, res) => {", "exports.get   =  async (req, res) =>  {"))
        f2 = make_finding(location={"file": "routes/invoices.js", "startLine": 5, "endLine": 6})
        fp2 = bughunt.fingerprint(self.dir, f2)
        self.assertEqual(fp1, fp2)

    def test_differs_by_lens_and_snippet(self):
        f1 = make_finding()
        f2 = make_finding(lens="dataflow-taint")
        self.assertNotEqual(bughunt.fingerprint(self.dir, f1), bughunt.fingerprint(self.dir, f2))
        f3 = make_finding(location={"file": "lib/pricing.js", "startLine": 1, "endLine": 2})
        self.assertNotEqual(bughunt.fingerprint(self.dir, f1), bughunt.fingerprint(self.dir, f3))

    def test_missing_file_falls_back_to_title(self):
        f = make_finding(location={"file": "gone/away.js", "startLine": 1})
        fp = bughunt.fingerprint(self.dir, f)
        self.assertTrue(re.fullmatch(r"[0-9a-f]{16}", fp))


class TestMerge(TempRepo):
    def merge(self, findings, extra_args=(), stdin_doc=None):
        r = run_cli(["merge", "-", "--fail-on", "none", *extra_args], self.dir,
                    stdin=stdin_doc or doc(findings))
        self.assertIn(r.returncode, (0,), r.stderr)
        return json.loads(r.stdout), r

    def test_validation_drops_invalid_keeps_valid(self):
        bad = {"title": "no location", "lens": "auth-access", "severity": "High",
               "confidence": 0.9, "trigger": "x", "trace": "y", "impact": "z"}
        out, r = self.merge([make_finding(), bad])
        self.assertEqual(len(out["findings"]), 1)
        self.assertEqual(out["summary"]["invalidDropped"], 1)
        self.assertIn("invalid", r.stderr)

    def test_strict_fails_on_invalid(self):
        bad = {"title": "no location", "lens": "auth-access", "severity": "High",
               "confidence": 0.9, "trigger": "x", "trace": "y", "impact": "z"}
        r = run_cli(["merge", "-", "--strict", "--fail-on", "none"], self.dir,
                    stdin=doc([make_finding(), bad]))
        self.assertEqual(r.returncode, 3)
        self.assertIn("strict merge rejected", r.stderr)

    def test_require_verified_rejects_missing_verdict(self):
        r = run_cli(["merge", "-", "--require-verified", "--fail-on", "none"], self.dir,
                    stdin=doc([make_finding()]))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["summary"]["invalidDropped"], 1)
        self.assertEqual(out["findings"], [])

        verified = make_finding(verified={"by": "skeptic-pass", "method": "static-refutation",
                                          "verdict": "upheld", "note": "no guard"})
        r = run_cli(["merge", "-", "--require-verified", "--strict", "--fail-on", "none"],
                    self.dir, stdin=doc([verified]))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(len(out["findings"]), 1)

    def test_uncertain_capped_to_speculative(self):
        uncertain = make_finding(confidence=0.95,
                                 verified={"by": "skeptic-pass",
                                           "method": "static-refutation",
                                           "verdict": "uncertain",
                                           "note": "could not prove or refute"})
        out, _ = self.merge([uncertain])
        f = out["findings"][0]
        self.assertLess(f["confidence"], 0.5)
        self.assertEqual(f["confidenceLabel"], "Speculative")
        self.assertIn("uncertain", f["tags"])

    def test_dedupe_prefers_upheld_over_uncertain(self):
        uncertain = make_finding(title="uncertain duplicate",
                                 confidence=0.95,
                                 verified={"by": "skeptic-pass",
                                           "method": "static-refutation",
                                           "verdict": "uncertain",
                                           "note": "could not prove or refute"})
        upheld = make_finding(title="upheld duplicate",
                              confidence=0.48,
                              verified={"by": "skeptic-pass",
                                        "method": "static-refutation",
                                        "verdict": "upheld",
                                        "note": "no guard"})
        out, _ = self.merge([uncertain, upheld])
        self.assertEqual(len(out["findings"]), 1)
        f = out["findings"][0]
        self.assertEqual(f["title"], "upheld duplicate")
        self.assertEqual(f["verified"]["verdict"], "upheld")

    def test_upheld_duplicate_wins_over_uncertain_cluster(self):
        uncertain = make_finding(title="uncertain critical candidate",
                                 severity="Critical",
                                 confidence=0.95,
                                 verified={"by": "skeptic-pass",
                                           "method": "static-refutation",
                                           "verdict": "uncertain",
                                           "note": "could not prove or refute"})
        upheld = make_finding(title="upheld high duplicate",
                              lens="dataflow-taint",
                              severity="High",
                              confidence=0.9,
                              verified={"by": "skeptic-pass",
                                        "method": "static-refutation",
                                        "verdict": "upheld",
                                        "note": "no guard"})
        out, _ = self.merge([uncertain, upheld])
        self.assertEqual(len(out["findings"]), 1)
        f = out["findings"][0]
        self.assertEqual(f["title"], "upheld high duplicate")
        self.assertEqual(f["verified"]["verdict"], "upheld")
        self.assertEqual(f["confidenceLabel"], "Confirmed")
        self.assertEqual(f["alsoFlaggedBy"][0]["title"], "uncertain critical candidate")

    def test_all_uncertain_cluster_stays_speculative(self):
        a = make_finding(confidence=0.95,
                         verified={"by": "skeptic-pass",
                                   "method": "static-refutation",
                                   "verdict": "uncertain",
                                   "note": "could not prove or refute"})
        b = make_finding(lens="dataflow-taint",
                         title="taint maybe reaches query",
                         confidence=0.9,
                         verified={"by": "skeptic-pass",
                                   "method": "static-refutation",
                                   "verdict": "uncertain",
                                   "note": "caller unclear"})
        out, _ = self.merge([a, b])
        self.assertEqual(len(out["findings"]), 1)
        f = out["findings"][0]
        self.assertEqual(f["verified"]["verdict"], "uncertain")
        self.assertLess(f["confidence"], 0.5)
        self.assertEqual(f["confidenceLabel"], "Speculative")

    def test_coverage_preserved(self):
        raw = {
            "schemaVersion": "1.0",
            "coverage": {
                "plannedCells": 2,
                "executedCells": 1,
                "skippedCells": [{"lens": "concurrency", "area": "sync", "reason": "budget"}],
                "filesRead": ["routes/invoices.js"],
                "commandsRun": ["bughunt.py hotspots"],
                "notExamined": ["admin console"],
            },
            "findings": [make_finding()],
        }
        out, _ = self.merge([], stdin_doc=json.dumps(raw))
        self.assertEqual(out["coverage"]["plannedCells"], 2)
        self.assertEqual(out["coverage"]["notExamined"], ["admin console"])

    def test_require_coverage_fails_without_metadata(self):
        r = run_cli(["merge", "-", "--require-coverage", "--fail-on", "none"], self.dir,
                    stdin=doc([make_finding()]))
        self.assertEqual(r.returncode, 3)
        self.assertIn("coverage metadata required", r.stderr)

    def test_require_coverage_passes_with_metadata(self):
        raw = {
            "schemaVersion": "1.0",
            "coverage": {"plannedCells": 1, "executedCells": 1},
            "findings": [make_finding()],
        }
        r = run_cli(["merge", "-", "--require-coverage", "--fail-on", "none"], self.dir,
                    stdin=json.dumps(raw))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["coverage"]["executedCells"], 1)

    def test_fingerprint_and_label_filled(self):
        out, _ = self.merge([make_finding()])
        f = out["findings"][0]
        self.assertTrue(re.fullmatch(r"[0-9a-f]{16}", f["fingerprint"]))
        self.assertEqual(f["confidenceLabel"], "Confirmed")
        self.assertEqual(f["id"], "BH-001")

    def test_dedupe_same_fingerprint(self):
        a = make_finding(confidence=0.6, trace="short")
        b = make_finding(confidence=0.9, trace="much longer and clearer trace with hops")
        out, _ = self.merge([a, b])
        self.assertEqual(len(out["findings"]), 1)
        self.assertEqual(out["findings"][0]["confidence"], 0.9)

    def test_cross_lens_cluster(self):
        # Same bug at overlapping lines under two lenses -> one primary + alsoFlaggedBy.
        a = make_finding(confidence=0.6)
        b = make_finding(lens="dataflow-taint", confidence=0.6, title="taint reaches query")
        out, _ = self.merge([a, b])
        self.assertEqual(len(out["findings"]), 1)
        self.assertEqual(out["summary"]["clustered"], 1)
        primary = out["findings"][0]
        self.assertIn("cross-validated", primary["tags"])
        self.assertAlmostEqual(primary["confidence"], 0.7, places=2)
        self.assertEqual(len(primary["alsoFlaggedBy"]), 1)
        lenses = {primary["lens"], primary["alsoFlaggedBy"][0]["lens"]}
        self.assertEqual(lenses, {"auth-access", "dataflow-taint"})

    def test_no_cluster_legacy_boost(self):
        # --no-cluster keeps both, boosts confidence (legacy behavior).
        a = make_finding(confidence=0.6)
        b = make_finding(lens="dataflow-taint", confidence=0.6, title="taint reaches query")
        out, _ = self.merge([a, b], extra_args=["--no-cluster"])
        self.assertEqual(len(out["findings"]), 2)
        self.assertEqual(out["summary"]["clustered"], 0)
        for f in out["findings"]:
            self.assertAlmostEqual(f["confidence"], 0.75, places=2)
            self.assertIn("cross-validated", f["tags"])

    def test_same_lens_not_clustered(self):
        # Two DIFFERENT bugs found by the SAME lens at nearby lines stay separate.
        a = make_finding(title="bug one", location={"file": "routes/invoices.js", "startLine": 3, "endLine": 3})
        b = make_finding(title="bug two", location={"file": "routes/invoices.js", "startLine": 4, "endLine": 4})
        out, _ = self.merge([a, b])
        self.assertEqual(len(out["findings"]), 2)
        self.assertEqual(out["summary"]["clustered"], 0)

    def test_refuted_quarantined(self):
        a = make_finding()
        b = make_finding(lens="logic-correctness", title="not actually a bug",
                         location={"file": "lib/pricing.js", "startLine": 2},
                         verified={"by": "skeptic-pass", "method": "static-refutation",
                                   "verdict": "refuted", "note": "guard at line 2 prevents it"})
        out, _ = self.merge([a, b])
        self.assertEqual(len(out["findings"]), 1)
        self.assertEqual(len(out["refuted"]), 1)
        self.assertEqual(out["summary"]["refuted"], 1)

    def test_suppression(self):
        out1, _ = self.merge([make_finding()])
        fp = out1["findings"][0]["fingerprint"]
        sup = self.dir / ".bughunt" / "suppressions.json"
        sup.parent.mkdir(exist_ok=True)
        sup.write_text(json.dumps({"suppressions": [{"fingerprint": fp, "reason": "by design"}]}))
        out2, _ = self.merge([make_finding()])
        f = out2["findings"][0]
        self.assertTrue(f["suppressed"])
        self.assertEqual(f["suppressedReason"], "by design")
        self.assertEqual(out2["summary"]["suppressed"], 1)

    def test_baseline_one_new_one_fixed(self):
        a = make_finding()
        b = make_finding(lens="logic-correctness", title="discount after tax",
                         location={"file": "lib/pricing.js", "startLine": 3})
        self.merge([a, b], extra_args=["--write-baseline"])
        c = make_finding(lens="resource-performance", title="N+1 in listing",
                         location={"file": "lib/pricing.js", "startLine": 5},
                         severity="Medium")
        out, r = self.merge([a, c])
        statuses = {f["title"]: f["baselineStatus"] for f in out["findings"]}
        self.assertEqual(statuses["IDOR: any user can read any invoice"], "existing")
        self.assertEqual(statuses["N+1 in listing"], "new")
        self.assertEqual(out["summary"]["fixed"], 1)
        self.assertEqual(out["baselineDiff"]["fixed"][0]["title"], "discount after tax")
        self.assertIn("1 new, 1 fixed", r.stderr.replace("1 new", "1 new"))

    def test_exit_codes(self):
        # new High -> 1
        r = run_cli(["merge", "-"], self.dir, stdin=doc([make_finding()]))
        self.assertEqual(r.returncode, 1)
        # new Medium only -> 0 under default critical-high gate
        r = run_cli(["merge", "-"], self.dir, stdin=doc(
            [make_finding(severity="Medium", title="meh",
                          location={"file": "lib/pricing.js", "startLine": 2})]))
        self.assertEqual(r.returncode, 0)
        # new Medium only -> 2 under fail-on any
        r = run_cli(["merge", "-", "--fail-on", "any"], self.dir, stdin=doc(
            [make_finding(severity="Medium", title="meh",
                          location={"file": "lib/pricing.js", "startLine": 2})]))
        self.assertEqual(r.returncode, 2)
        # clean -> 0
        r = run_cli(["merge", "-"], self.dir, stdin=doc([]))
        self.assertEqual(r.returncode, 0)
        # fail-on none -> 0 despite High
        r = run_cli(["merge", "-", "--fail-on", "none"], self.dir, stdin=doc([make_finding()]))
        self.assertEqual(r.returncode, 0)
        # baselined finding is not "new" -> 0
        run_cli(["merge", "-", "--write-baseline", "--fail-on", "none"],
                self.dir, stdin=doc([make_finding()]))
        r = run_cli(["merge", "-"], self.dir, stdin=doc([make_finding()]))
        self.assertEqual(r.returncode, 0)


class TestRenderAndDiff(TempRepo):
    def merged(self, findings):
        r = run_cli(["merge", "-", "--fail-on", "none"], self.dir, stdin=doc(findings))
        return json.loads(r.stdout)

    def test_md_round_trip(self):
        merged = self.merged([make_finding(), make_finding(
            lens="resource-performance", title="N+1 in listing", severity="Medium",
            confidence=0.6, impactClass="performance",
            location={"file": "lib/pricing.js", "startLine": 5})])
        (self.dir / "merged.json").write_text(json.dumps(merged))
        r = run_cli(["render", "merged.json", "--formats", "md"], self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        md = (self.dir / ".bughunt" / "report.md").read_text()
        # canonical block shape survives
        self.assertIn("### [High-Confirmed] IDOR: any user can read any invoice", md)
        self.assertIn("- **Location:** routes/invoices.js:3", md)
        self.assertIn("- **Lens:** auth-access", md)
        self.assertIn("## Confirmed & Probable findings", md)
        self.assertIn("## Coverage & gaps", md)
        # lossless for required fields
        for f in merged["findings"]:
            self.assertIn(f["title"], md)
            self.assertIn(f"{f['location']['file']}:{f['location']['startLine']}", md)
            self.assertIn(f["trigger"], md)
            self.assertIn(f["impact"], md)
            self.assertIn(f["fingerprint"], md)

    def test_html_standalone(self):
        merged = self.merged([make_finding()])
        (self.dir / "merged.json").write_text(json.dumps(merged))
        run_cli(["render", "merged.json", "--formats", "html"], self.dir)
        html = (self.dir / ".bughunt" / "report.html").read_text()
        self.assertIn("<style>", html)
        self.assertIn("IDOR: any user can read any invoice", html)
        self.assertNotIn("src=\"http", html)  # no external assets

    def test_sarif_structure(self):
        merged = self.merged([make_finding(), make_finding(
            severity="Low", title="aged FIXME", lens="dx-pain", confidence=0.6,
            impactClass="dx", location={"file": "lib/pricing.js", "startLine": 2})])
        (self.dir / "merged.json").write_text(json.dumps(merged))
        run_cli(["render", "merged.json", "--formats", "sarif"], self.dir)
        sarif = json.loads((self.dir / ".bughunt" / "report.sarif").read_text())
        self.assertEqual(sarif["version"], "2.1.0")
        run = sarif["runs"][0]
        self.assertEqual(run["tool"]["driver"]["name"], "bughunt")
        self.assertTrue(run["tool"]["driver"]["rules"])
        res = run["results"][0]
        self.assertIn(res["level"], ("error", "warning", "note"))
        loc = res["locations"][0]["physicalLocation"]
        self.assertIn("uri", loc["artifactLocation"])
        self.assertIn("startLine", loc["region"])
        self.assertIn("bughuntFingerprint/v1", res["partialFingerprints"])
        levels = {r["ruleId"]: r["level"] for r in run["results"]}
        self.assertEqual(levels["bughunt/auth-access"], "error")
        self.assertEqual(levels["bughunt/dx-pain"], "note")

    def test_diff_subcommand(self):
        m1 = self.merged([make_finding()])
        m2 = self.merged([make_finding(), make_finding(
            lens="logic-correctness", title="discount after tax",
            location={"file": "lib/pricing.js", "startLine": 3})])
        (self.dir / "a.json").write_text(json.dumps(m1))
        (self.dir / "b.json").write_text(json.dumps(m2))
        r = run_cli(["diff", "a.json", "b.json"], self.dir)
        out = json.loads(r.stdout)
        self.assertEqual(out["counts"], {"new": 1, "fixed": 0, "unchanged": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
