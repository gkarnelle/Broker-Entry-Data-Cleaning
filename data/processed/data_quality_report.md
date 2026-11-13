# Data quality report

Synthetic demonstration data only.

| Metric | Count |
|---|---:|
| Input rows | 4909 |
| Output rows | 4894 |
| Exact duplicates removed | 15 |
| Conflicting rows retained | 0 |
| Rows needing review | 87 |
| Allowed blank part numbers | 49 |
| Changed cells | 13096 |

## Completeness

Before counts use all input rows; after counts use retained rows. Nulls are not imputed. Counts may fall when duplicate rows are removed.

| Field | Nulls before | Nulls after |
|---|---:|---:|
| tax_id | 0 | 0 |
| importer_name | 0 | 0 |
| entry_number | 0 | 0 |
| entry_line_number | 0 | 0 |
| entry_date | 0 | 0 |
| coo | 37 | 36 |
| coe | 0 | 0 |
| hts | 0 | 0 |
| part_number | 50 | 49 |
| description | 0 | 0 |
| quantity | 0 | 0 |
| unit_of_measure | 0 | 0 |
| value | 28 | 28 |
| currency | 0 | 0 |
| supplier | 0 | 0 |
| manufacturer | 4909 | 4894 |
| duty_amount | 4909 | 4894 |

## Interpretation

Blank part numbers are allowed and do not by themselves create an exception. Conflicting versions are retained; no broker is assumed authoritative. Passed means the configured structural rules passed, not that customs accuracy was verified. Invalid nonblank values remain visible in the cleaned output with review flags. Quality issues and change logs include input rows subsequently removed as duplicates.
