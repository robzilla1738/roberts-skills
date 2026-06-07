#!/usr/bin/env node
/*
 * hunt-cursor.mjs — Rung A-CLI of the bughunt capability ladder.
 *
 * The same Hunt + mandatory Verify phases as hunt-workflow.js (Rung A), but driven by the
 * Cursor CLI (`cursor-agent`) instead of the Claude Code Workflow tool. It fans out one
 * HUNTER per (lens x hotspot) cell on a FAST model (Composer 2.5 / Grok), then runs the
 * mandatory adversarial SKEPTIC pass on a STRONG reasoner (Opus 4.8), and prints a strict
 * {schemaVersion:"1.0", coverage, findings:[...]} document to stdout — byte-compatible with
 * hunt-workflow.js so the SAME merge command consumes it:
 *
 *   node hunt-cursor.mjs --cells cells.json \
 *     | python3 bughunt.py merge - --require-verified --require-coverage --strict --write-baseline
 *
 * WHY THIS RUNG: it turns Cursor (a single-agent tool, Rung C = sequential) into a true
 * parallel fan-out, and is usable from any shell with `cursor-agent` on PATH (Cursor,
 * Claude Code, CI). Composer 2.5 has no external API — `cursor-agent` is the way to reach it.
 *
 * SIGNAL OVER NOISE: hunters use a fast model for breadth; the skeptic/verify pass stays on a
 * strong reasoner. That split is what keeps the hunt "just as powerful" while going faster.
 *
 * READ-ONLY BY CONSTRUCTION: every cursor-agent invocation uses `--mode ask` (Q&A, read-only)
 * and NEVER passes `--force`/`--yolo`, so a hunter physically cannot edit your code. `--trust`
 * only suppresses the interactive workspace-trust prompt; it does not grant write access.
 *
 * Zero runtime dependencies — Node stdlib only (node:child_process, node:fs, node:readline).
 *
 * Auth: `cursor-agent` uses its stored login, or the CURSOR_API_KEY env var.
 * Discover exact model ids with: `cursor-agent --list-models`.
 */

import { spawn } from 'node:child_process'
import { readFileSync } from 'node:fs'

// ----- the 13 lens slugs / enums (mirror hunt-workflow.js + finding.schema.json) -----------
const LENS_SLUGS = [
  'dataflow-taint', 'state-lifecycle', 'concurrency', 'boundaries-numeric',
  'error-failure', 'contract-spec', 'auth-access', 'logic-correctness',
  'resource-performance', 'dx-pain', 'product-ux', 'dependency-supply', 'data-migration',
]
const REQUIRED_FINDING_FIELDS = [
  'title', 'lens', 'severity', 'confidence', 'location', 'trigger', 'trace', 'impact',
]

// ----- defaults so the script is self-sufficient with just --cells ------------------------
const DEFAULT_HUNT_MODEL = 'composer-2.5'              // fast breadth; `composer-2.5-fast`, `grok-build-0.1`, `grok-4.3` also work
const DEFAULT_VERIFY_MODEL = 'claude-opus-4-8-thinking-high'  // strong reasoner — the signal gate
const DEFAULT_CONCURRENCY = 6
const DEFAULT_TIMEOUT_MS = 240000                     // 4 min/agent; guards the known headless-hang

const DEFAULT_HUNTER_PREAMBLE = [
  'You are a bug hunter. Examine the assigned files through ONE lens only and report only',
  'real, evidence-backed defects.',
  '',
  'For every defect collect: location (file:line range), trigger (exact condition/input),',
  'trace (cause -> ... -> effect with file:line hops), impact (what goes wrong), and a',
  'confidence number 0-1 with one line of justification.',
  '',
  'Rules:',
  '- Evidence or it does not count. No location+trace+trigger+impact -> do not report it.',
  '- Try to KILL each finding before reporting (is there a guard, validation, or invariant?).',
  '- Report NOTHING if you find nothing real. Do not pad. Do NOT edit any code.',
  '- Stay in your lane: only the assigned lens on the assigned files.',
].join('\n')

// The canonical SKEPTIC template from verification.md (with {{FINDING}} / {{LENS_PATH}}).
const DEFAULT_SKEPTIC_PROMPT = [
  'You are a SKEPTIC. Your job is to REFUTE this finding, not to confirm it. Assume it is a',
  'false positive and try to prove it wrong.',
  '',
  'FINDING:',
  '{{FINDING}}',
  '',
  'Read the cited code (location.file + the lines around location.startLine..endLine, plus its',
  'callers and the relevant tests) and read the lens discipline at:',
  '{{LENS_PATH}}',
  '',
  'Genuinely attempt all four refutation questions — read code, do not guess:',
  '  1. Upstream guard  — is there a validation / early return / type constraint / invariant',
  '     BEFORE this code that prevents the trigger from ever arriving?',
  '  2. Trusted input   — is the "untrusted" value actually validated or trusted at the',
  '     boundary it crosses, before it reaches the sink?',
  '  3. Covering test   — does an existing test exercise this exact path and pass? FIND it and',
  '     READ it before answering.',
  '  4. Documented intent — is this behavior intentional and documented (comment, ADR, type,',
  '     test name)?',
  '',
  'Return ONLY this JSON object, nothing else:',
  '{"by":"skeptic-pass","method":"static-refutation","verdict":"upheld|refuted|uncertain",',
  ' "note":"which question(s) you tried and what you found"}',
  '',
  'Rules:',
  '- Default to "refuted" when a refutation lands. Use "uncertain" when you can neither confirm',
  '  the bug nor kill it. Reserve "upheld" for when ALL FOUR questions fail to kill it.',
  '- Bias toward "refuted" on genuine doubt.',
].join('\n')

// ----- tiny arg parser ---------------------------------------------------------------------
function parseArgs(argv) {
  const o = {
    cells: null, huntModel: DEFAULT_HUNT_MODEL, verifyModel: DEFAULT_VERIFY_MODEL,
    concurrency: DEFAULT_CONCURRENCY, timeoutMs: DEFAULT_TIMEOUT_MS, workspace: process.cwd(),
    inlineLenses: false, dryRun: false, help: false,
  }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--cells') o.cells = argv[++i]
    else if (a === '--hunt-model') o.huntModel = argv[++i]
    else if (a === '--verify-model') o.verifyModel = argv[++i]
    else if (a === '--concurrency') o.concurrency = Math.max(1, parseInt(argv[++i], 10) || DEFAULT_CONCURRENCY)
    else if (a === '--timeout') o.timeoutMs = Math.max(1000, (parseInt(argv[++i], 10) || 0) * 1000)
    else if (a === '--workspace') o.workspace = argv[++i]
    else if (a === '--inline-lenses') o.inlineLenses = true
    else if (a === '--dry-run') o.dryRun = true
    else if (a === '-h' || a === '--help') o.help = true
    else eprint(`warning: ignoring unknown arg "${a}"`)
  }
  return o
}

const HELP = `hunt-cursor.mjs — Cursor-CLI fan-out rung for bughunt (Rung A-CLI)

Usage:
  node hunt-cursor.mjs --cells cells.json [options] | python3 bughunt.py merge - ...
  cat cells.json | node hunt-cursor.mjs [options] | python3 bughunt.py merge - ...

The cells JSON is the same shape hunt-workflow.js expects:
  { "cells": [ { "lens", "platform", "area", "files":[...], "lensPath", "platformPath" } ],
    "hunterPreamble"?: string, "skepticPrompt"?: string,
    "skippedCells"?: [...], "commandsRun"?: [...], "notExamined"?: [...] }

Options:
  --cells <file>      cells JSON file (default: read stdin)
  --hunt-model <id>   fast model for hunters    (default: ${DEFAULT_HUNT_MODEL})
  --verify-model <id> strong model for skeptics (default: ${DEFAULT_VERIFY_MODEL})
  --concurrency <n>   max parallel cursor-agent calls (default: ${DEFAULT_CONCURRENCY})
  --timeout <sec>     per-agent timeout in seconds (default: ${DEFAULT_TIMEOUT_MS / 1000})
  --workspace <path>  workspace dir for cursor-agent (default: cwd)
  --inline-lenses     paste lens/platform spoke text into prompts instead of passing paths
  --dry-run           emit deterministic stubs without calling cursor-agent (offline test)
  -h, --help          show this help

Discover model ids with: cursor-agent --list-models
Hunters are READ-ONLY: --mode ask, never --force. Keep the verify model strong (signal gate).`

function eprint(msg) { process.stderr.write(msg + '\n') }

// ----- robust JSON extraction --------------------------------------------------------------
// Pull the first balanced {...} object out of text (handles ``` fences, leading prose).
function extractFirstObject(text) {
  const start = text.indexOf('{')
  if (start < 0) return null
  let depth = 0, inStr = false, esc = false
  for (let i = start; i < text.length; i++) {
    const c = text[i]
    if (inStr) {
      if (esc) esc = false
      else if (c === '\\') esc = true
      else if (c === '"') inStr = false
    } else if (c === '"') inStr = true
    else if (c === '{') depth++
    else if (c === '}') { depth--; if (depth === 0) return text.slice(start, i + 1) }
  }
  return null
}
function parseLooseJSON(text) {
  if (text == null) return null
  try { return JSON.parse(text) } catch { /* fall through */ }
  const obj = extractFirstObject(String(text))
  if (obj) { try { return JSON.parse(obj) } catch { /* fall through */ } }
  return null
}

// ----- one cursor-agent call ---------------------------------------------------------------
// Returns the model's final answer TEXT (the envelope's `result` string), or throws.
function runCursor(prompt, model, opt) {
  return new Promise((resolve, reject) => {
    const args = [
      '--print', '--mode', 'ask', '--trust',
      '--output-format', 'json', '--model', model,
      '--workspace', opt.workspace,
      prompt, // positional; spawn (not a shell) so no escaping/injection concerns
    ]
    const child = spawn('cursor-agent', args, { stdio: ['ignore', 'pipe', 'pipe'] })
    let out = '', err = '', done = false
    const timer = setTimeout(() => {
      if (done) return
      done = true
      child.kill('SIGKILL')
      reject(new Error(`cursor-agent timed out after ${opt.timeoutMs}ms`))
    }, opt.timeoutMs)
    child.stdout.on('data', d => { out += d })
    child.stderr.on('data', d => { err += d })
    child.on('error', e => {
      if (done) return
      done = true; clearTimeout(timer)
      reject(new Error(`cursor-agent spawn failed: ${e.message} (is it on PATH? CURSOR_API_KEY set?)`))
    })
    child.on('close', code => {
      if (done) return
      done = true; clearTimeout(timer)
      const env = parseLooseJSON(out)
      if (!env) return reject(new Error(`cursor-agent gave no JSON (exit ${code}). stderr: ${err.slice(0, 400)}`))
      if (env.is_error) return reject(new Error(`cursor-agent error: ${String(env.result || '').slice(0, 400)}`))
      const result = typeof env.result === 'string' ? env.result : JSON.stringify(env.result)
      resolve(result)
    })
  })
}

// ----- prompt builders (mirror hunt-workflow.js) -------------------------------------------
function readSpoke(path) { try { return readFileSync(path, 'utf8') } catch { return null } }

function hunterPrompt(cell, opt, preamble) {
  const parts = [
    preamble,
    `Examine ONLY these files through the ${cell.lens} lens: ${(cell.files || []).join(', ')}`,
  ]
  if (opt.inlineLenses) {
    const lensText = cell.lensPath ? readSpoke(cell.lensPath) : null
    const platText = cell.platformPath ? readSpoke(cell.platformPath) : null
    if (lensText) parts.push(`--- LENS DISCIPLINE (${cell.lens}) ---\n${lensText}`)
    if (platText) parts.push(`--- PLATFORM FOOTGUNS (${cell.platform || ''}) ---\n${platText}`)
  } else {
    if (cell.lensPath) parts.push(`Read the lens discipline first: ${cell.lensPath}`)
    if (cell.platformPath) parts.push(`Platform footguns: ${cell.platformPath}`)
  }
  parts.push(`Set source.hunter to "${cell.lens} x ${cell.area}".`)
  parts.push(
    'Return ONLY a JSON object {"schemaVersion":"1.0","findings":[...]} and nothing else — no ' +
    'prose, no markdown fences. Each finding needs: title, lens, severity ' +
    '(Critical|High|Medium|Low), confidence (0-1), location {file,startLine[,endLine]}, ' +
    'trigger, trace, impact. Empty findings array if nothing real.')
  return parts.join('\n\n')
}

function skepticPrompt(finding, cell, template) {
  return template
    .replace('{{FINDING}}', JSON.stringify(finding))
    .replace('{{LENS_PATH}}', cell.lensPath || `the ${cell.lens} lens discipline`)
}

// ----- bounded-concurrency map -------------------------------------------------------------
async function mapLimit(items, limit, fn) {
  const results = new Array(items.length)
  let next = 0
  async function worker() {
    while (true) {
      const i = next++
      if (i >= items.length) return
      results[i] = await fn(items[i], i)
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length || 1) }, worker))
  return results
}

// ----- light normalization (merge owns strict validation) ----------------------------------
function sanitizeFinding(f, cell) {
  if (!f || typeof f !== 'object') return null
  for (const k of REQUIRED_FINDING_FIELDS) if (f[k] === undefined || f[k] === null) return null
  if (!LENS_SLUGS.includes(f.lens)) f.lens = cell.lens // trust the cell's lens slug
  f.source = f.source || {}
  if (!f.source.hunter) f.source.hunter = `${cell.lens} x ${cell.area}`
  if (!f.source.detectedBy) f.source.detectedBy = 'agent'
  return f
}

// ----- main --------------------------------------------------------------------------------
async function main() {
  const opt = parseArgs(process.argv.slice(2))
  if (opt.help) { process.stdout.write(HELP + '\n'); return 0 }

  const raw = opt.cells ? readFileSync(opt.cells, 'utf8') : readFileSync(0, 'utf8')
  const A = parseLooseJSON(raw) || {}
  if (!Array.isArray(A.cells) || A.cells.length === 0) {
    eprint('hunt-cursor.mjs: input must be a JSON object with a non-empty "cells" array ' +
      '(each { lens, files:[...], lensPath, platformPath, area }). See --help.')
    return 3
  }
  const preamble = A.hunterPreamble || DEFAULT_HUNTER_PREAMBLE
  const skTemplate = A.skepticPrompt || DEFAULT_SKEPTIC_PROMPT
  const cells = A.cells
  const notExamined = Array.isArray(A.notExamined) ? A.notExamined.slice() : []

  eprint(`[hunt-cursor] ${cells.length} cells | hunt=${opt.huntModel} verify=${opt.verifyModel} ` +
    `| concurrency=${opt.concurrency}${opt.dryRun ? ' | DRY-RUN' : ''}`)

  // -- Phase: Hunt (fast model, bounded concurrency) ----------------------------------------
  const huntResults = await mapLimit(cells, opt.concurrency, async (cell, i) => {
    if (opt.dryRun) {
      return {
        cell,
        findings: [sanitizeFinding({
          title: `dry-run stub finding for ${cell.lens}`,
          lens: cell.lens, severity: 'Low', confidence: 0.5,
          location: { file: (cell.files && cell.files[0]) || 'stub.txt', startLine: 1, endLine: 1 },
          trigger: 'dry-run', trace: 'dry-run -> stub', impact: 'none (offline stub)',
          impactClass: 'correctness',
        }, cell)].filter(Boolean),
      }
    }
    try {
      const text = await runCursor(hunterPrompt(cell, opt, preamble), opt.huntModel, opt)
      const parsed = parseLooseJSON(text)
      const findings = (parsed && Array.isArray(parsed.findings) ? parsed.findings : [])
        .map(f => sanitizeFinding(f, cell)).filter(Boolean)
      eprint(`[hunt ${i + 1}/${cells.length}] ${cell.lens} x ${cell.area}: ${findings.length} candidate(s)`)
      return { cell, findings }
    } catch (e) {
      eprint(`[hunt ${i + 1}/${cells.length}] ${cell.lens} x ${cell.area}: FAILED — ${e.message}`)
      notExamined.push(`hunt failed: ${cell.lens} x ${cell.area}: ${e.message}`)
      return { cell, findings: [] }
    }
  })

  // -- Phase: Verify (mandatory; strong model; one skeptic per candidate) --------------------
  const candidates = []
  for (const r of huntResults) for (const f of r.findings) candidates.push({ finding: f, cell: r.cell })

  const verified = await mapLimit(candidates, opt.concurrency, async ({ finding, cell }, i) => {
    if (opt.dryRun) {
      return { ...finding, verified: { by: 'skeptic-pass', method: 'static-refutation', verdict: 'upheld', note: 'dry-run stub' } }
    }
    try {
      const text = await runCursor(skepticPrompt(finding, cell, skTemplate), opt.verifyModel, opt)
      const v = parseLooseJSON(text)
      const ok = v && typeof v === 'object' && ['upheld', 'refuted', 'uncertain'].includes(v.verdict)
      eprint(`[verify ${i + 1}/${candidates.length}] ${String(finding.title).slice(0, 50)}: ${ok ? v.verdict : 'unparseable->uncertain'}`)
      return {
        ...finding,
        verified: ok
          ? { by: v.by || 'skeptic-pass', method: v.method || 'static-refutation', verdict: v.verdict, note: v.note || '' }
          : { by: 'skeptic-pass', method: 'static-refutation', verdict: 'uncertain', note: 'verifier returned no parseable verdict' },
      }
    } catch (e) {
      eprint(`[verify ${i + 1}/${candidates.length}] ${String(finding.title).slice(0, 50)}: ERROR — ${e.message}`)
      return { ...finding, verified: { by: 'skeptic-pass', method: 'static-refutation', verdict: 'uncertain', note: `verifier errored: ${e.message}` } }
    }
  })

  // -- Emit (merge owns dedupe/cluster/baseline/routing) ------------------------------------
  const filesRead = Array.from(new Set(cells.flatMap(c => c.files || []))).sort()
  const out = {
    schemaVersion: '1.0',
    coverage: {
      plannedCells: cells.length,
      executedCells: cells.length,
      skippedCells: Array.isArray(A.skippedCells) ? A.skippedCells : [],
      filesRead,
      commandsRun: Array.isArray(A.commandsRun) ? A.commandsRun : [],
      notExamined,
    },
    findings: verified,
  }
  eprint(`[hunt-cursor] ${verified.length} findings after verify`)
  process.stdout.write(JSON.stringify(out) + '\n')
  return 0
}

main().then(code => process.exit(code || 0)).catch(e => { eprint(`hunt-cursor.mjs: ${e.stack || e.message}`); process.exit(3) })
