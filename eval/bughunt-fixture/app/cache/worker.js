"use strict";

const db = require("../db/invoices");

// In-memory idempotency cache: maps requestId -> result. Shared across all
// concurrent requests in this process.
const seen = new Map();

// In-flight refund guard. Meant to ensure a given invoice is refunded once.
const refunding = new Set();

/**
 * Process a refund exactly once per invoiceId, even under concurrency.
 */
async function processRefundOnce(invoiceId) {
  // SEED:BUG-015 concurrency — check-then-act TOCTOU: the has()/add() gap is not
  // atomic, so two concurrent calls both pass the check and double-refund before
  // either has added the id to the set (await yields between check and act).
  if (refunding.has(invoiceId)) {
    return { skipped: true };
  }
  const invoice = await db.getInvoice(invoiceId);
  refunding.add(invoiceId);
  await db.markRefunded(invoiceId);
  refunding.delete(invoiceId);
  return { refunded: true, id: invoice.id };
}

let total = 0;

/**
 * Tally a batch of amounts into a shared running total. Called from multiple
 * async batch handlers.
 */
async function tally(amounts) {
  for (const amt of amounts) {
    // SEED:BUG-016 concurrency — shared mutable state race: read-modify-write of the
    // module-level `total` across interleaved async handlers loses updates (the
    // await below lets another handler read the same stale `total`).
    const current = total;
    await db.getInvoice("noop").catch(() => null);
    total = current + amt;
  }
  return total;
}

// Cache results forever.
function remember(requestId, result) {
  // SEED:BUG-017 state-lifecycle — unbounded cache growth: entries are added but never
  // evicted or TTL'd, so `seen` grows without bound for the life of the process (leak).
  seen.set(requestId, result);
  return result;
}

function recall(requestId) {
  return seen.get(requestId);
}

module.exports = { processRefundOnce, tally, remember, recall };
