
"""Reconcile cleaned broker submissions against GaiAnQi reference data."""

import csv
import io
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
BASE = (
    "https://raw.githubusercontent.com/"
    "gkarnelle/Global-Trade-Data-Analysis/main/v2/data/"
)

def fetch(filename):
    with urlopen(BASE + filename, timeout=30) as response:
        return list(csv.DictReader(
            io.StringIO(response.read().decode("utf-8-sig"))
        ))

def money(value):
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None

def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

entries = fetch("customs_entries.csv")
lines = fetch("customs_entry_lines.csv")

reference = {}
for line in lines:
    key = line["entry_line_id"]
    if key in reference:
        raise ValueError(f"Duplicate reference entry line: {key}")
    reference[key] = line

entry_ids = {row["entry_id"] for row in entries}

with (PROCESSED / "cleaned_entries.csv").open(
    newline="", encoding="utf-8"
) as handle:
    broker_rows = list(csv.DictReader(handle))

results = []

for row in broker_rows:
    entry_id = row["entry_number"]
    line_number = row["entry_line_number"]

    # Match the canonical entry-line identifier.
    try:
        line_id = f"{entry_id}-{int(line_number):02d}"
    except (ValueError, TypeError):
        line_id = ""

    issues = []

    if entry_id not in entry_ids:
        issues.append("unknown_entry_id")

    ref = reference.get(line_id)

    if ref is None:
        issues.append("unmatched_entry_line")
    else:
        if row["part_number"] and row["part_number"] != ref["product_id"]:
            issues.append("product_mismatch")

        if row["hts"] != ref["illustrative_hts_code"]:
            issues.append("hts_mismatch")

        if money(row["quantity"]) != money(ref["quantity_entered"]):
            issues.append("quantity_mismatch")

        if money(row["value"]) != money(ref["entered_value_usd"]):
            issues.append("entered_value_mismatch")

        if row["coo"] != ref["origin_code"]:
            issues.append("origin_mismatch")

    if row["validation_status"] == "needs_review":
        issues.append("broker_quality_review")

    results.append({
        "record_id": row["record_id"],
        "broker": row["broker"],
        "entry_id": entry_id,
        "entry_line_id": line_id,
        "product_id": row["part_number"],
        "reference_match": "yes" if ref else "no",
        "reconciliation_status": "needs_review" if issues else "matched",
        "discrepancy_codes": "; ".join(dict.fromkeys(issues)),
    })

PROCESSED.mkdir(parents=True, exist_ok=True)

fields = [
    "record_id", "broker", "entry_id", "entry_line_id",
    "product_id", "reference_match",
    "reconciliation_status", "discrepancy_codes",
]
write_csv(PROCESSED / "reconciliation_results.csv", fields, results)

counts = Counter(row["reconciliation_status"] for row in results)

summary = [
    {"metric": "broker_rows_reconciled", "value": len(results)},
    {"metric": "matched_rows", "value": counts["matched"]},
    {"metric": "rows_needing_review", "value": counts["needs_review"]},
    {"metric": "reference_entry_lines", "value": len(lines)},
]

write_csv(
    PROCESSED / "reconciliation_summary.csv",
    ["metric", "value"],
    summary,
)

print("GaiAnQi broker reconciliation complete")
for item in summary:
    print(f"{item['metric']}: {item['value']:,}")
