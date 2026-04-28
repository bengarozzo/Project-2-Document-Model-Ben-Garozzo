# ClinicalTrials.gov API Notes (v2)

## What the API provides
ClinicalTrials.gov provides a public API for retrieving study records and selected fields needed for secondary dataset construction. Records are organized as studies with nested modules (identification, status, sponsor, conditions, outcomes, and more).

## Key concepts for this project
- The project collects **interventional** studies with a **study start date** in **2024–2025**.
- The raw pull should preserve enough of the nested structure to enable document modeling (conditions, phases, sponsor information, status, enrollment, and results/outcomes indicators).

## Practical considerations
- Requests may be paginated; the pipeline must iterate through pages until completion.
- Not all studies contain all fields; missingness is expected and must be preserved as `null` rather than imputed.
- Some fields are free text (e.g., condition names, sponsor names) and may vary across records.

