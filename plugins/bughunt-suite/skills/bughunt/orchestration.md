# Fan-out orchestration

The power multiplier. Instead of one linear pass, run **many independent adversarial passes
in parallel**, each narrow enough to be thorough, then verify, merge, and report. Narrow
scope + many passes beats broad scope + one pass.

Every hunt — whatever the tool — runs the **same five phases**:

> **Recon → Hunt → Verify → Merge → Report**

Recon ranks the target and picks lenses ([recon-and-scoping.md](recon-and-scoping.md)). Hunt
runs the grid below. **Verify is mandatory** ([verification.md](verification.md)) — it is a
first-class phase, not a footnote. Merge and Report are owned by
[`bughunt.py`](scripts/bughunt.py). What changes between tools is only the *execution* of
those phases (parallel sub-agents vs. one agent walking the grid) — see the capability ladder.

## The (lens × hotspot) grid

Take the ranked hotspots and selected lenses from the [hunt plan](recon-and-scoping.md) and
form a grid. Each **cell** = one lens applied to one hotspot. Cells are independent, so they
fan out cleanly.

```
                hotspot A (parser)   hotspot B (auth)   hotspot C (sync engine)
taint                 ✓                    ✓                   ·
auth-access           ·                    ✓                   ·
concurrency           ·                    ·                   ✓
boundaries-numeric    ✓                    ·                   ✓
error-failure         ✓                    ✓                   ✓
logic-correctness     ✓                    ✓                   ✓
```

Don't fill every cell — only the combinations that make sense (a sync engine gets
concurrency; a parser gets boundaries; a network handler gets taint). Prioritize cells where
a **hot hotspot** meets a **high-yield lens**.

**Seed the grid from the deterministic pre-pass**, don't guess it:

- **Hotspots** come from `python3 scripts/bughunt.py hotspots` (ranked files by
  churn × complexity × recency × boundary × test-gap). These are the grid's columns.
- **Lenses** come from recon (platform + trust boundaries). These are the rows.
- **Pain-point lenses** route off signals, not hotspots: send the `dx-pain` and `product-ux`
  lenses at the output of `python3 scripts/bughunt.py signals` (TODO age, feature flags,
  config drift), and send the `dependency-supply` lens at `python3 scripts/bughunt.py deps`
  (dependency audit). `data-migration` rides on hotspots that touch schema/migration files.

So a complete grid is `hotspots × code-lenses` plus a few targeted cells fed by
`signals`/`deps` for the pain-point and supply lenses.

## Hunter prompt template

Each hunter gets a tight, self-contained, **read-only** prompt. The narrowness is what makes
it thorough and what keeps false positives down.

```text
You are a bug hunter. Examine ONLY <files/area> through the <LENS> lens.

Read these references first:
- bughunt/lens-<lens>.md  (the discipline — absolute path provided below)
- bughunt/platform-<platform>.md  (ecosystem footguns)

For every defect you find, collect:
- Location (file:line, range)
- Trigger (the exact condition/input that fires it)
- Trace (cause -> ... -> effect, with file:line hops)
- Impact (what goes wrong)
- Confidence (a number 0-1) with one line of justification

Rules:
- Evidence or it doesn't count. No location+trace+trigger+impact -> don't report it.
- Try to kill each finding before reporting (is there a guard, validation, invariant?).
- Report NOTHING if you find nothing real. Do not pad. Do not edit any code.
- Stay in your lane: only <LENS> on <area>.

Return your findings as a JSON object:
  {schemaVersion: "1.0", findings: [...]}
where each finding matches scripts/schema/finding.schema.json — required fields:
  title, lens, severity (Critical|High|Medium|Low), confidence (0-1),
  location {file, startLine, endLine}, trigger, trace, impact.
Also set impactClass (security|correctness|reliability|performance|data-integrity|dx|ux|
supply-chain) and source.hunter (e.g. "<LENS> x <area>").
Report NOTHING (an empty findings array) if you find nothing real.
```

Keep each hunter read-only and scoped. Hunters return **strict JSON** — the harness collects
it and pipes it straight to `merge`; prose write-ups break the pipeline.

## The capability ladder

Different assistants have different fan-out machinery. Pick the **highest rung your tool
supports**; the five phases (Recon → Hunt → **Verify** → Merge → Report) are identical on
every rung. **Verify is mandatory on all three rungs** — see [verification.md](verification.md).

### Rung A — Workflow tool available (Claude Code with the Workflow tool)

The orchestrating agent drives the whole loop and offloads the parallel Hunt+Verify to the
shipped workflow script.

1. **Recon (inline, Bash):** run the deterministic pre-pass —
   `python3 scripts/bughunt.py census --functions`, `… hotspots`, `… signals`, `… deps` —
   and read the JSON.
2. **Build the grid** from `hotspots × lenses` (+ pain-point/supply cells from
   `signals`/`deps`), as `cells: [{ lens, platform, area, files:[...], lensPath, platformPath }]`.
   `lensPath`/`platformPath` are **absolute paths** to the spoke files (under the plugin root,
   `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/`).
3. **Hunt + Verify (Workflow):** invoke the shipped script —
   ```
   Workflow({
     scriptPath: '<abs>/scripts/hunt-workflow.js',
     args: { cells, evidenceContract, skepticPrompt, hunterPreamble }
   })
   ```
   The script fans out one hunter per cell, then runs the mandatory skeptic pass on every
   candidate finding (it drops `refuted` ones), and returns `{schemaVersion:"1.0", findings}`.
   `hunterPreamble` = the evidence contract + JSON-return instructions; `skepticPrompt` = the
   SKEPTIC template from [verification.md](verification.md) (with `{{FINDING}}` /
   `{{LENS_PATH}}` placeholders).
4. **Merge (Bash):** pipe the workflow's findings JSON to merge and write the baseline —
   ```
   echo "$WORKFLOW_JSON" | python3 scripts/bughunt.py merge - --write-baseline
   ```
5. **Report (Bash):** `python3 scripts/bughunt.py render .bughunt/findings.json` →
   md/html/sarif.

### Rung B — standard Claude Code (Task/Agent fan-out, no Workflow tool)

Identical phases, done by hand with the Task/Agent tool.

1. **Recon (Bash):** run the same pre-pass commands; read the JSON.
2. **Build the grid** the same way.
3. **Hunt (concurrent Tasks):** dispatch **one Task per cell, concurrently** — issue all the
   Task calls in a **single message** (multiple tool calls), not one at a time. Each Task gets
   the hunter prompt above and **returns strict JSON**. Collect every cell's findings.
4. **Verify (concurrent Tasks):** for **every surviving candidate finding**, dispatch one
   skeptic Task using the SKEPTIC template from [verification.md](verification.md). Again,
   fan these out concurrently. Each returns the verdict JSON; attach it as the finding's
   `verified` field.
5. **Merge + Report (Bash):** combine all findings into one
   `{schemaVersion:"1.0", findings:[...]}` document and pipe it in —
   ```
   echo "$ALL_FINDINGS" | python3 scripts/bughunt.py merge - --write-baseline
   python3 scripts/bughunt.py render .bughunt/findings.json
   ```

### Rung C — single-agent tools (Cursor / Codex, no sub-agents)

No fan-out machinery: walk the grid **sequentially**, but run all five phases.

1. **Recon:** run the pre-pass if `python3` is present (see Portability for the no-Python case).
2. **Build the grid** and order cells by priority (hot hotspot × high-yield lens first).
3. **Hunt + Verify, cell by cell:** for **each** cell in priority order, hunt it, then
   **immediately skeptic-verify every finding it produced** (the four refutation questions
   from [verification.md](verification.md)) **before moving to the next cell**. Reset focus
   between cells — explicitly switch to the new lens's mindset and re-read the lens spoke so
   you don't carry the previous lens's assumptions. Accumulate the verified findings as JSON.
4. **Merge + Report:** if `python3` is present, pipe the accumulated JSON to
   `bughunt.py merge` + `render`. If not, **hand-assemble** the markdown report using the
   triage layout (severity × confidence sections; refuted in an appendix; uncertain capped at
   Speculative). The hunt still works without the scripts — only the automation is lost.

**Explicitly: Verify is mandatory on all three rungs.** A hunt that skips it has not run the
skill.

## Budget & stop policy

- **Quick scan:** a handful of cells, often sequential, no sub-agents needed. Cap the grid at
  **~6 cells** — the top hotspots × the 2–3 highest-yield lenses.
- **Deep hunt:** batch cells; start with the top hotspots × highest-yield lenses. Cap the
  active grid at **~24 cells**; **batch the rest** and expand into them only if early passes
  are productive or coverage gaps remain.
- **Stop** when the top hotspots are covered by their relevant lenses and additional cells
  stop producing new, real findings (**diminishing returns**).
- **Record skipped cells** in the report's coverage section — be honest about what was
  examined and what was deliberately deferred or skipped.

## Merge & cross-validate

`bughunt.py merge` **owns** the consolidation logic — the agent's only job is to collect
**clean JSON** from the hunters + skeptics and pipe it in. Specifically, `merge`:

> validates each finding against the schema (dropping malformed ones); **fingerprints** each
> by `lens + relpath + normalized snippet` so the id is stable across line shifts;
> **dedupes** findings that share a fingerprint (keeping the clearer write-up);
> **clusters cross-lens duplicates** — when several *different* lenses flag the same bug at
> overlapping lines, it collapses them into one primary finding with an `alsoFlaggedBy` list
> and a convergence confidence boost (so the same bug isn't reported three times; pass
> `--no-cluster` to keep them separate); quarantines `verified.verdict == "refuted"` findings
> into a separate **refuted** appendix; applies **suppressions** from
> `.bughunt/suppressions.json`; and runs a **baseline diff** (`new` / `existing` / `fixed`)
> so CI can gate only on newly introduced Critical/High findings.

Do **not** re-implement dedupe, clustering, or the confidence boost by hand — that's what
caused drift before. Hand `merge` clean JSON; let it do the bookkeeping.

## Portability

Sub-agents don't always share your filesystem or know where the skill is installed, so
"Read `bughunt/lens-<lens>.md`" may not resolve. Make the lens guidance reach the hunter by
whichever works in your tool, in order of preference:

1. **Pass the absolute path** to the lens/platform spoke if sub-agents can read files. In a
   Claude Code plugin the install root is `${CLAUDE_PLUGIN_ROOT}`; the spokes live under
   `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/` (this is the `lensPath`/`platformPath` the grid
   cells carry).
2. **Inline the checklist** — paste the lens's *Smells* list (and the relevant platform
   footguns) directly into the hunter prompt. The most portable option; works even when the
   hunter has no file access at all.
3. **Run that cell yourself** sequentially (Rung C) if neither is possible.

Either way the hunter must receive the lens's smell list + the evidence contract — never
assume it already knows the discipline.

**No `python3`?** The scripts are an accelerant, not a dependency. Without Python, skip the
pre-pass and merge/render: rank hotspots by hand (churn from `git log`, boundaries by reading
imports), build the grid the same way, run the same five phases, and **hand-assemble the
markdown report** using the triage layout. The hunt still works — you only lose the
deterministic ranking, fingerprinting, and baseline gate.
