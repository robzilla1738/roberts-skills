"use strict";

const Database = require("better-sqlite3");

const DB_PATH = (process.env.DATABASE_URL || "sqlite:./data/invoices.db").replace(
  /^sqlite:/,
  ""
);

// A single shared connection for normal reads/writes.
const conn = new Database(DB_PATH);

// Run an arbitrary SQL string (used by the list route).
async function query(sql) {
  return conn.prepare(sql).all();
}

async function getInvoice(id) {
  return conn.prepare("SELECT * FROM invoices WHERE id = ?").get(id);
}

// Fetch every invoice plus its line items, for the admin dashboard.
async function listWithLineItems() {
  // SEED:BUG-012 resource-performance — unbounded result set: selects the entire
  // table with no LIMIT/pagination, so the dashboard loads all invoices into memory.
  const invoices = conn.prepare("SELECT * FROM invoices").all();

  // SEED:BUG-013 resource-performance — N+1 queries: one extra query per invoice to
  // load its line items instead of a single JOIN or a batched IN (...) query.
  for (const inv of invoices) {
    inv.lineItems = conn
      .prepare("SELECT * FROM line_items WHERE invoice_id = ?")
      .all(inv.id);
  }
  return invoices;
}

// Export every invoice as CSV to a temp file. Opens its own connection.
async function exportAll(outPath) {
  // SEED:BUG-014 state-lifecycle — connection/handle leak: a second DB handle is
  // opened but never closed (no conn2.close()), leaking the handle on every export.
  const conn2 = new Database(DB_PATH, { readonly: true });
  const rows = conn2.prepare("SELECT * FROM invoices").all();
  const fs = require("fs");
  const out = fs.openSync(outPath, "w");
  for (const r of rows) {
    fs.writeSync(out, `${r.id},${r.total},${r.status}\n`);
  }
  // out is also never fs.closeSync'd, compounding the leak.
  return rows.length;
}

async function createInvoice(data) {
  const stmt = conn.prepare(
    "INSERT INTO invoices (owner_id, total, status) VALUES (?, ?, ?)"
  );
  const info = stmt.run(data.ownerId, data.total, data.status);
  return { id: info.lastInsertRowid, ...data };
}

async function markRefunded(id) {
  return conn
    .prepare("UPDATE invoices SET status = 'refunded' WHERE id = ?")
    .run(id);
}

module.exports = {
  query,
  getInvoice,
  listWithLineItems,
  exportAll,
  createInvoice,
  markRefunded,
};
