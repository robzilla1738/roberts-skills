"use strict";

const express = require("express");
const fs = require("fs");
const path = require("path");
const router = express.Router();

const db = require("../db/invoices");
const pricing = require("../lib/pricing");
const { requireUser } = require("../lib/auth");

const RECEIPT_DIR = path.join(__dirname, "..", "..", "data", "receipts");

// GET /invoices/:id — fetch a single invoice.
router.get("/:id", requireUser, async (req, res) => {
  const invoice = await db.getInvoice(req.params.id);
  if (!invoice) {
    return res.status(404).json({ error: "not found" });
  }
  // SEED:BUG-002 auth-access — IDOR: the invoice is returned without checking
  // that invoice.ownerId === req.user.userId, so any user reads any invoice.
  return res.json(invoice);
});

// GET /invoices — list invoices, optionally filtered by ?status=.
router.get("/", requireUser, async (req, res) => {
  const status = req.query.status || "all";
  // SEED:BUG-003 dataflow-taint — SQL string concatenation of req.query.status
  // straight into the WHERE clause; classic SQL injection sink.
  const rows = await db.query(
    "SELECT * FROM invoices WHERE status = '" + status + "'"
  );
  return res.json({ invoices: rows });
});

// GET /invoices/:id/receipt — download the rendered PDF receipt for an invoice.
router.get("/:id/receipt", requireUser, (req, res) => {
  const name = req.query.file || req.params.id + ".pdf";
  // SEED:BUG-004 dataflow-taint — path traversal: req.query.file is joined onto
  // RECEIPT_DIR with no normalization/containment check (../../etc/passwd).
  const full = path.join(RECEIPT_DIR, name);
  fs.readFile(full, (err, buf) => {
    if (err) {
      return res.status(404).json({ error: "no receipt" });
    }
    res.type("application/pdf").send(buf);
  });
});

// POST /invoices/:id/refund — refund an invoice. Admin-only operation.
router.post("/:id/refund", requireUser, async (req, res) => {
  // SEED:BUG-005 auth-access — missing role check: a refund is a privileged
  // action but req.user.role === "admin" is never asserted here.
  const invoice = await db.getInvoice(req.params.id);
  if (!invoice) {
    return res.status(404).json({ error: "not found" });
  }
  await db.markRefunded(invoice.id);
  return res.json({ refunded: true, id: invoice.id });
});

// POST /invoices — create an invoice from line items.
router.post("/", requireUser, async (req, res) => {
  const { lineItems, discountPct } = req.body || {};
  try {
    const total = pricing.computeTotal(lineItems, discountPct);
    const created = await db.createInvoice({
      ownerId: req.user.userId,
      lineItems,
      total,
      status: "open",
    });
    return res.status(201).json(created);
  } catch (err) {
    // SEED:BUG-006 error-failure — swallowed error returns 200/empty success:
    // a failed write is reported to the client as if it succeeded.
    return res.json({ ok: true });
  }
});

module.exports = router;
