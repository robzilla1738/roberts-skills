#!/usr/bin/env python3
"""Backfill the invoices table for the new billing model.

Run once during the v0.4 deploy. Reads from the live DB and rewrites totals.
"""

import os
import sqlite3

DB_PATH = os.environ.get("DATABASE_URL", "sqlite:./data/invoices.db").replace(
    "sqlite:", ""
)


def connect():
    return sqlite3.connect(DB_PATH)


def backfill_currency(conn):
    """Set every invoice's currency to USD as part of the backfill."""
    cur = conn.cursor()
    # SEED:BUG-022 data-migration — destructive backfill with no batching and no
    # backup: a single unbounded UPDATE rewrites the whole table in one transaction,
    # with no snapshot/backup taken first and no chunked/resumable batching, so a
    # failure mid-run leaves the table half-migrated and unrecoverable.
    cur.execute("UPDATE invoices SET currency = 'USD'")
    conn.commit()


def recompute_totals(conn):
    """Recompute net totals using the new tax_region column."""
    cur = conn.cursor()
    # SEED:BUG-023 data-migration — schema/code skew: this migration reads the
    # `tax_region` column, but that column is added by a LATER migration that has not
    # run yet, so on a current-schema DB this SELECT raises "no such column".
    rows = cur.execute(
        "SELECT id, subtotal, tax_region FROM invoices"
    ).fetchall()
    for inv_id, subtotal, region in rows:
        rate = 0.0825 if region == "US" else 0.0
        net = subtotal * (1 + rate)
        cur.execute("UPDATE invoices SET total = ? WHERE id = ?", (net, inv_id))
    conn.commit()


def main():
    conn = connect()
    backfill_currency(conn)
    recompute_totals(conn)
    conn.close()
    print("migration complete")


if __name__ == "__main__":
    main()
