/*
 * hunt-workflow.js — Rung A of the bughunt capability ladder.
 *
 * Invoked by orchestration.md (Rung A) via the Claude Code Workflow tool:
 *
 *   Workflow({
 *     scriptPath: '<abs>/scripts/hunt-workflow.js',
 *     args: { cells, hunterPreamble, skepticPrompt }   // + optional evidenceContract
 *   })
 *
 * It fans out one HUNTER agent per (lens x hotspot) cell, then runs the mandatory
 * adversarial VERIFY pass — one SKEPTIC agent per candidate finding — and returns the
 * findings with verifier verdicts as a strict {schemaVersion:"1.0", coverage, findings:[...]}
 * document. The orchestrating agent pipes that to
 * `python3 bughunt.py merge - --require-verified --require-coverage --strict --write-baseline`,
 * which routes refuted findings into the transparency appendix and renders.
 *
 * EVERYTHING comes in via the global `args` (cells + the two prompt strings). The script
 * builds NO state of its own from the outside world.
 *
 * Workflow runtime constraints (do not violate — the runtime enforces these):
 *   - Plain JavaScript only. No TypeScript syntax.
 *   - The wall clock and the RNG are BANNED: any current-time or random primitive throws.
 *     Derive nothing from Date / performance.now / Math.random / crypto — there is none to use.
 *   - No filesystem and no environment access from inside the script. Cells carry absolute
 *     lensPath/platformPath strings; the AGENT reads those files, the script never does.
 *   - The body is async. Available hooks: agent(prompt, opts), parallel(thunks),
 *     pipeline(items, ...stages), log(msg), phase(title), and the globals args / budget.
 *   - agent(prompt, { schema }) returns a schema-validated object.
 *   - This file must begin with `export const meta = {...}` as a pure literal.
 */

export const meta = {
  name: 'bughunt-fanout',
  description: 'Parallel lens x hotspot hunters with a mandatory adversarial verify pass',
  phases: [{ title: 'Hunt' }, { title: 'Verify' }],
}

// args = {
//   cells: [{ lens, platform, area, files:[...], lensPath, platformPath }],
//   hunterPreamble: string,   // evidence contract + JSON-return instructions
//   skepticPrompt: string,    // template with {{FINDING}} / {{LENS_PATH}} placeholders
// }

// The 13 lens slugs that may appear in a finding's "lens" field.
const LENS_SLUGS = [
  'dataflow-taint', 'state-lifecycle', 'concurrency', 'boundaries-numeric',
  'error-failure', 'contract-spec', 'auth-access', 'logic-correctness',
  'resource-performance', 'dx-pain', 'product-ux', 'dependency-supply', 'data-migration',
]

const SEVERITIES = ['Critical', 'High', 'Medium', 'Low']

const IMPACT_CLASSES = [
  'security', 'correctness', 'reliability', 'performance',
  'data-integrity', 'dx', 'ux', 'supply-chain',
]

// JSON Schema for a hunter's return: { schemaVersion, findings:[finding] }.
// Mirrors the required fields of scripts/schema/finding.schema.json (id/fingerprint are
// filled later by `bughunt.py merge`, so they are not required here).
const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['findings'],
  properties: {
    schemaVersion: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'lens', 'severity', 'confidence', 'location', 'trigger', 'trace', 'impact'],
        properties: {
          title: { type: 'string', minLength: 4 },
          lens: { type: 'string', enum: LENS_SLUGS },
          severity: { type: 'string', enum: SEVERITIES },
          confidence: { type: 'number', minimum: 0, maximum: 1 },
          location: {
            type: 'object',
            required: ['file', 'startLine'],
            properties: {
              file: { type: 'string' },
              startLine: { type: 'integer', minimum: 1 },
              endLine: { type: 'integer', minimum: 1 },
              note: { type: 'string' },
            },
          },
          trigger: { type: 'string' },
          trace: { type: 'string' },
          impact: { type: 'string' },
          impactClass: { type: 'string', enum: IMPACT_CLASSES },
          repro: { type: 'string' },
          fixSketch: { type: 'string' },
          tags: { type: 'array', items: { type: 'string' } },
          source: {
            type: 'object',
            properties: {
              hunter: { type: 'string' },
              detectedBy: { type: 'string', enum: ['agent', 'script', 'fuzz'] },
            },
          },
        },
      },
    },
  },
}

// JSON Schema for a skeptic's verdict (becomes the finding's `verified` field).
const VERDICT_SCHEMA = {
  type: 'object',
  required: ['by', 'method', 'verdict', 'note'],
  properties: {
    by: { type: 'string' },
    method: {
      type: 'string',
      enum: ['static-refutation', 'failing-test', 'runtime-repro', 'property-test', 'manual-review'],
    },
    verdict: { type: 'string', enum: ['upheld', 'refuted', 'uncertain'] },
    note: { type: 'string' },
  },
}

// Defensive arg handling: some Workflow invocations deliver `args` as a JSON STRING
// (the documented stringification footgun) rather than a parsed object. Normalize it,
// and fail loudly with an actionable message if the cells grid never arrived.
let A = typeof args === 'string' ? safeParse(args) : (args || {})
function safeParse(s) { try { return JSON.parse(s) } catch (e) { return {} } }
if (!A || !Array.isArray(A.cells) || A.cells.length === 0) {
  throw new Error(
    'hunt-workflow.js: args.cells must be a non-empty array of (lens x hotspot) cells, each ' +
    '{ lens, files:[...], lensPath, platformPath, area }. Got args of type "' + typeof args +
    '". Pass args as a real JSON object (orchestration.md Rung A), not a stringified blob.')
}
const HUNTER_PREAMBLE = A.hunterPreamble || 'You are a bug hunter. Report only real, evidence-backed defects through the assigned lens.'
const SKEPTIC_PROMPT = A.skepticPrompt || 'Refute or uphold finding {{FINDING}} after reading {{LENS_PATH}}; return the verdict JSON.'

function hunterPrompt(cell) {
  return [
    HUNTER_PREAMBLE,
    'Examine ONLY these files through the ' + cell.lens + ' lens: ' + cell.files.join(', '),
    'Read the lens discipline first: ' + cell.lensPath,
    cell.platformPath ? 'Platform footguns: ' + cell.platformPath : '',
    'Set source.hunter to "' + cell.lens + ' x ' + cell.area + '".',
    'Return {schemaVersion:"1.0", findings:[...]}. Empty findings if nothing real.',
  ].filter(Boolean).join('\n\n')
}

function skepticPrompt(finding, cell) {
  return SKEPTIC_PROMPT
    .replace('{{FINDING}}', JSON.stringify(finding))
    .replace('{{LENS_PATH}}', cell.lensPath)
}

phase('Hunt')

// For each cell: hunt it, then fan out a skeptic over every candidate finding it produced.
// pipeline runs the cells; stage 1 is the hunter, stage 2 is the per-finding verify fan-out.
const perCell = await pipeline(
  A.cells,
  cell => agent(hunterPrompt(cell), { label: 'hunt:' + cell.lens + ' x ' + cell.area, phase: 'Hunt', schema: FINDINGS_SCHEMA }),
  (hunt, cell) => parallel((hunt && hunt.findings ? hunt.findings : []).map(f => () =>
    agent(skepticPrompt(f, cell), { label: 'verify:' + (f.title || '').slice(0, 40), phase: 'Verify', schema: VERDICT_SCHEMA })
      .then(v => ({ ...f, verified: v }))
      .catch(() => ({ ...f, verified: { by: 'skeptic-pass', method: 'static-refutation', verdict: 'uncertain', note: 'verifier errored' } }))
  ))
)

// Flatten the per-cell arrays and preserve every verifier verdict. merge owns the routing:
// upheld/uncertain stay in the body, refuted findings move to the transparency appendix.
const findings = perCell.flat().filter(Boolean)
const filesRead = Array.from(new Set(A.cells.flatMap(cell => cell.files || []))).sort()
const coverage = {
  plannedCells: A.cells.length,
  executedCells: A.cells.length,
  skippedCells: A.skippedCells || [],
  filesRead,
  commandsRun: A.commandsRun || [],
  notExamined: A.notExamined || [],
}
log(findings.length + ' findings returned after verify')
return { schemaVersion: '1.0', coverage, findings }
