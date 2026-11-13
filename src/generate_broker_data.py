
"""Generate fictional broker submissions from GaiAnQi customs entries."""

import csv
import io
import json
import random
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

BASE = (
    "https://raw.githubusercontent.com/"
    "gkarnelle/Global-Trade-Data-Analysis/main/v2/data/"
)

rng = random.Random(42)

def fetch(filename):
    with urlopen(BASE + filename, timeout=30) as response:
        content = response.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(content)))

entries = fetch("customs_entries.csv")
lines = fetch("customs_entry_lines.csv")

mappings = json.loads(
    (ROOT / "config" / "broker_mappings.json").read_text(
        encoding="utf-8"
    )
)

entry_lookup = {r["entry_id"]: r for r in entries}

if len(entry_lookup) != len(entries):
    raise ValueError("Duplicate entry IDs in reference data")

if any(r["entry_id"] not in entry_lookup for r in lines):
    raise ValueError("Entry line references unknown entry ID")

if len({r["entry_line_id"] for r in lines}) != len(lines):
    raise ValueError("Duplicate reference entry line IDs")

countries = {
    "CN": "China",
    "MX": "Mexico",
    "CA": "Canada",
    "DE": "Germany",
    "VN": "Vietnam",
    "KR": "South Korea",
}

broker_files = list(mappings)
submissions = {name: [] for name in broker_files}

for index, line in enumerate(lines):
    entry = entry_lookup[line["entry_id"]]

    if line["entry_date"] != entry["entry_date"]:
        raise ValueError("Entry date mismatch in reference data")

    if line["origin_code"] != entry["origin_code"]:
        raise ValueError("Origin mismatch in reference data")

    broker_file = broker_files[index % len(broker_files)]
    config = mappings[broker_file]

    date = datetime.strptime(line["entry_date"], "%Y-%m-%d")
    origin = line["origin_code"]

    # Entry-line suffix is used as the demo broker line number.
    line_number = line["entry_line_id"].rsplit("-", 1)[-1]

    standard = {
        "tax_id": "123456789",
        "importer_name": "GaiAnQi Global Trading",
        "entry_number": line["entry_id"],
        "entry_line_number": str(int(line_number)),
        "entry_date": date.strftime(config["date_formats"][0]),
        "coo": origin,
        "coe": origin,
        "hts": line["illustrative_hts_code"],
        "part_number": line["product_id"],
        "description": f"Synthetic product {line['product_id']}",
        "quantity": line["quantity_entered"],
        "unit_of_measure": "PCS",
        "value": line["entered_value_usd"],
        "currency": "USD",
        "supplier": entry["supplier_id"],
        "manufacturer": "",
        "duty_amount": "",
    }

    # Controlled, reproducible broker data-quality scenarios.
    if index % 101 == 0:
        standard["part_number"] = ""

    if index % 137 == 0:
        standard["coo"] = ""

    if index % 173 == 0:
        standard["value"] = ""

    if index % 211 == 0:
        standard["quantity"] = "-5"

    if index % 251 == 0:
        standard["value"] = str(
            round(float(line["entered_value_usd"]) + 125, 2)
        )

    # Translate canonical fields into each broker's own headers.
    row = {
        source_col: standard[target_col]
        for source_col, target_col in config["columns"].items()
    }

    submissions[broker_file].append(row)

# Add a few exact duplicate submissions for testing.
for filename, rows in submissions.items():
    rows.extend(dict(row) for row in rows[:5])

for filename, rows in submissions.items():
    config = mappings[filename]
    path = RAW / filename

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(config["columns"]),
            delimiter=config.get("delimiter", ","),
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{filename}: {len(rows):,} synthetic submission rows")

print(f"Reference customs entries: {len(entries):,}")
print(f"Reference entry lines: {len(lines):,}")
print("Broker submissions generated successfully.")
