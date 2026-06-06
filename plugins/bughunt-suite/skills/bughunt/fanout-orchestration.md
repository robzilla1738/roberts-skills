# Fan-out Orchestration

The power multiplier. Instead of one linear pass, run **many independent adversarial passes
in parallel**, each narrow enough to be thorough, then merge the results. Narrow scope +
many passes beats broad scope + one pass.

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
a hot hotspot meets a high-yield lens.

## Dispatch parallel hunters

Spawn one sub-agent per cell (or per small batch of related cells). Run independent cells
**concurrently** — issue the agent calls together rather than one at a time. Each hunter gets
a tight, self-contained prompt.

### Hunter prompt template

```
You are a bug hunter. Examine ONLY <files/area> through the <LENS> lens.

Read these references first:
- bughunt/lens-<lens>.md  (the discipline)
- bughunt/platform-<platform>.md  (ecosystem footguns)

For every defect you find, return a finding with:
- Location (file:line)
- Trigger (the exact condition/input that fires it)
- Trace (cause -> ... -> effect, with file:line hops)
- Impact (what goes wrong)
- Confidence (Confirmed / Probable / Speculative) with one line of justification

Rules:
- Evidence or it doesn't count. No location+trace+trigger+impact -> don't report it.
- Try to kill each finding before reporting (is there a guard, validation, invariant?).
- Report NOTHING if you find nothing real. Do not pad. Do not edit any code.
- Stay in your lane: only <LENS> on <area>.
```

Keep each hunter read-only and scoped. The narrowness is what makes it thorough and what
keeps false positives down.

### Giving hunters the lens guidance (portability)

Sub-agents don't always share your filesystem or know where this skill is installed, so
"Read `bughunt/lens-<lens>.md`" may not resolve for them. Make the guidance reach the hunter
by whichever of these works in your tool, in order of preference:

1. **Pass the absolute path** to the lens/platform spoke if sub-agents can read files (in a
   Claude Code plugin the install root is `${CLAUDE_PLUGIN_ROOT}`; the spokes are under
   `${CLAUDE_PLUGIN_ROOT}/skills/bughunt/`).
2. **Inline the checklist** — paste the lens's *Smells* list and the relevant platform
   footguns directly into the hunter prompt. This is the most portable option and works even
   when the hunter has no file access at all.
3. **Run that cell yourself** sequentially (the fallback below) if neither is possible.

Either way, the hunter must receive the lens's smell list + evidence contract — never assume
it already knows the discipline.

## Budget & stop policy

- **Quick scan:** a handful of cells, often sequential, no sub-agents needed.
- **Deep hunt:** batch cells; start with the top hotspots × highest-yield lenses; expand to
  more cells only if early passes are productive or coverage gaps remain.
- **Stop** when the top hotspots are covered by their relevant lenses and additional cells
  stop producing new, real findings (diminishing returns). Note any cells you deliberately
  skipped in the report's coverage section.

## Merge & cross-validate

Collect all hunter outputs and consolidate:

1. **Dedupe** — same `file:line` + same root cause = one finding. Keep the clearest write-up.
2. **Cluster** — group findings that share a root cause (one bug, many symptoms) so the
   report addresses the cause, not each symptom separately.
3. **Cross-validate (confidence boost)** — when two *different lenses* independently flag the
   same code, raise its confidence one step. Convergence is strong signal.
4. **Resolve conflicts** — if one hunter flags code another implicitly cleared, re-examine;
   the guard one saw may kill the other's finding.

Hand the consolidated set to [triage](../triage/SKILL.md) for severity × confidence scoring,
false-positive filtering, repro building, and the final report.

## Sequential fallback (portability)

Not every assistant can spawn sub-agents. The skill must still work single-agent:

- Walk the grid **cell by cell** in priority order, one lens × hotspot at a time.
- Between cells, **reset focus** — explicitly switch to the new lens's mindset so you don't
  carry the previous lens's assumptions. Re-read the lens spoke if needed.
- Keep a running findings list and apply the same merge/cross-validate rules at the end.

The grid, the evidence contract, and the merge discipline are identical; only the execution
(parallel vs serial) changes.
