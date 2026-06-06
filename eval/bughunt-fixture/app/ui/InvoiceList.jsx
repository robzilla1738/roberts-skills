"use strict";

const React = require("react");
const { useState, useEffect } = React;

// Feature flag for the bulk-export button. Read once at module load.
const BULK_EXPORT_ENABLED = process.env.FEATURE_BULK_EXPORT === "true";

/**
 * Render the current user's invoices.
 */
function InvoiceList({ apiBase }) {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    fetch(`${apiBase}/invoices`)
      .then((r) => r.json())
      .then((data) => setInvoices(data.invoices))
      // SEED:BUG-018 product-ux — swallowed error blanks the UI: a failed fetch is
      // caught and ignored, leaving the user staring at an empty list with no error
      // message and no retry.
      .catch(() => {});
  }, [apiBase]);

  // SEED:BUG-019 product-ux — missing loading/empty/error states: while the fetch is
  // in flight or when it returns zero rows, the component renders nothing useful and
  // looks identical to a broken page (no spinner, no "no invoices yet" empty state).
  return (
    <div className="invoice-list">
      <h2>Invoices</h2>
      <ul>
        {invoices.map((inv) => (
          <li key={inv.id}>
            #{inv.id} — {inv.status} — ${inv.total}
          </li>
        ))}
      </ul>

      {/* SEED:BUG-020 product-ux — dead feature flag: FEATURE_BULK_EXPORT is missing
          from .env so this branch is permanently false; the bulk-export button can
          never render, making it dead, unreachable UI. */}
      {BULK_EXPORT_ENABLED ? (
        <button onClick={() => bulkExport(apiBase)}>Export all</button>
      ) : null}
    </div>
  );
}

/**
 * Trigger a bulk export of the current user's invoices.
 * @param {string} apiBase API root, e.g. "https://api.example.com"
 */
async function bulkExport(apiBase) {
  // SEED:BUG-021 contract-spec — copy-paste divergence: the JSDoc and the sibling
  // fetch above use `${apiBase}/invoices`, but this hits "/invoice/export" (singular)
  // — a copy-paste typo that diverges from the documented/used path and 404s.
  const res = await fetch(`${apiBase}/invoice/export`, { method: "POST" });
  return res.json();
}

module.exports = { InvoiceList, bulkExport };
