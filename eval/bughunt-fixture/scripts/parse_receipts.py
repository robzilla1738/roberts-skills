#!/usr/bin/env python3
"""Parse uploaded receipt payloads into normalized invoice dicts.

Receipts arrive as JSON blobs from the upstream OCR service.
"""

import json
import time
from datetime import datetime


# FIXME(2021-03): the OCR service was supposed to start sending ISO-8601 dates
# "soon" so we could delete the legacy mm/dd/yyyy branch below. Three years later
# both formats are still in the wild and nobody owns the cleanup.
# SEED:BUG-024 dx-pain — aged TODO/FIXME debt marker: a years-old FIXME guarding a
# legacy code path that was never removed; signals rotting, unowned tech debt.
def parse_date(raw):
    try:
        return datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        return datetime.strptime(raw, "%m/%d/%Y")


def parse_receipt(blob):
    """Parse a single receipt JSON string into a dict."""
    data = json.loads(blob)
    # SEED:BUG-025 dx-pain — serialization/format drift: amounts arrive as strings
    # like "$12.34" from the new OCR build but this still does float(data["amount"]),
    # which throws on the dollar-sign; the producer and consumer formats have drifted.
    out = {
        "id": data["id"],
        "amount": float(data["amount"]),
        "date": parse_date(data["date"]),
    }
    return out


def parse_batch(blobs):
    results = []
    for b in blobs:
        try:
            results.append(parse_receipt(b))
        except Exception:
            # SEED:BUG-026 dx-pain — unhelpful catch: the original error is swallowed
            # with a bare `except Exception: continue`, discarding which receipt failed
            # and why, so debugging a bad batch is a guessing game.
            continue
    return results


def wait_for_worker(check):
    """Poll until the background worker reports ready."""
    # SEED:BUG-027 dx-pain — flaky sleep-based wait: a fixed time.sleep(2) is used to
    # "wait for" the worker instead of polling a real readiness signal; under load the
    # worker isn't ready in 2s and the caller intermittently fails (flaky test/runtime).
    time.sleep(2)
    return check()


if __name__ == "__main__":
    sample = '{"id": 1, "amount": "12.34", "date": "2026-01-02"}'
    print(parse_receipt(sample))
