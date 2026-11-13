
# Broker Entry Data Cleaning & Reconciliation

### GaiAnQi Global Trading | Trade Compliance Analytics Portfolio

An automated Python pipeline that standardizes synthetic customs
broker submissions, identifies data-quality exceptions, maintains
an audit trail, and reconciles broker entry lines against a
centralized customs entry dataset.

## Executive Summary

GaiAnQi Global Trading is a fictional importer used across a
connected portfolio of international trade analytics projects.

This project simulates a common trade compliance challenge:
receiving customs entry data from multiple brokers with
inconsistent file layouts, formatting conventions, and data quality.

The pipeline transforms these submissions into a standardized
dataset and identifies records requiring further investigation.

## Results

| Metric | Result |
|---|---:|
| Broker submissions | 3 |
| Incoming records | 4,909 |
| Cleaned records | 4,894 |
| Exact duplicates removed | 15 |
| Cells standardized | 13,096 |
| Cleaning review records | 87 |
| Reconciliation review records | 106 |
| Successfully reconciled records | 4,788 |
| Reconciliation match rate | 97.83% |

Results reflect the current deterministic synthetic dataset.

## Pipeline

1. Generate synthetic submissions for three customs brokers.
2. Read broker-specific field mappings and file formats.
3. Standardize dates, country codes, HTS formatting, currencies,
   numeric fields, and other data elements.
4. Detect exact duplicates and retain records requiring review.
5. Produce standardized data and auditable quality reports.
6. Reconcile broker records against reference customs entry lines.
7. Publish refreshed results through GitHub Actions.

## Data Quality Controls

The pipeline includes:

- Required-field validation
- Broker-specific schema mapping
- Country-code normalization
- HTS formatting normalization
- Date and numeric standardization
- Duplicate detection
- Conflicting-key detection
- Missing-value reporting
- Cell-level change logging
- Exception reporting

Blank optional fields are distinguished from required-field
validation failures.

## Reconciliation

Broker entry lines are compared against reference customs records
using entry identifiers and relevant transaction attributes.

Comparison fields include:

- Product identifier, when supplied
- HTS code
- Quantity
- Entered value
- Country of origin

The process distinguishes formatting differences from substantive
data discrepancies.

Records requiring review are not automatically classified as
customs violations.

## Key Outputs

| File | Purpose |
|---|---|
| `cleaned_entries.csv` | Standardized broker records |
| `exceptions.csv` | Cleaning exceptions |
| `quality_issues.csv` | Field-level quality findings |
| `change_log.csv` | Standardization audit trail |
| `removed_duplicates.csv` | Removed duplicate records |
| `quality_summary.json` | Cleaning performance metrics |
| `data_quality_report.md` | Data-quality summary |
| `reconciliation_results.csv` | Line-level reconciliation |
| `reconciliation_summary.csv` | Reconciliation metrics |

Generated outputs are located in `data/processed/`.

## Automation

GitHub Actions runs the following scripts:

- `src/generate_broker_data.py`
- `src/clean.py`
- `src/reconcile.py`

The workflow supports manual execution and a monthly refresh.

## Connected Portfolio

This project forms the third stage of the GaiAnQi Global Trading
analytics portfolio:

**1. Strategic Sourcing Intelligence**

Supplier performance, purchasing exposure, sourcing concentration,
and procurement analytics.

https://github.com/gkarnelle/Strategic-Sourcing-Intelligence

**2. Global Trade Data Analysis**

Shipment and customs entry analytics using interconnected
synthetic trade datasets.

https://github.com/gkarnelle/Global-Trade-Data-Analysis

**3. Broker Entry Data Cleaning & Reconciliation**

Broker data standardization, exception detection, auditability,
and customs entry reconciliation.

Together, these projects demonstrate the relationship between
procurement data, international shipments, customs entries,
and broker reporting.

## Important Disclaimer

All company names, transaction records, broker submissions,
and analytical results are fictional or synthetic.

HTS values are illustrative. This project demonstrates data
engineering, analytical controls, and reconciliation methods,
not legal classification determinations or guaranteed
regulatory compliance.

Exceptions require appropriate human review.
