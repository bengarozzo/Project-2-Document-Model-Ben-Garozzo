# DS 4320 Project 2 Analysis: Clinical Drug Trials (2024–2025)

## Goal
Analyze recent (2024–2025) clinical drug trials by **phase**, **status**, **enrollment**, **condition**, **sponsor**, and **results/outcomes availability** using a MongoDB document database built from ClinicalTrials.gov API data.

## Data source and storage
- Source: ClinicalTrials.gov API (public registry)
- Storage: MongoDB Atlas collection `clinical_trials`
- Local artifacts:
  - Raw pull: `data/raw_clinical_trials_2024_2025.json`
  - Cleaned documents: `data/clean_clinical_trials_2024_2025.json`

## Document model (high level)
Each document represents one trial (`nct_id`) and preserves nested structures:
- `phases[]`, `conditions[]`
- `status.overall_status`, `enrollment.count`, `enrollment.type`
- `sponsor.lead.{name,class}`
- `results.has_results`
- `outcomes.primary[]` (when present)

## Methods
1. Query MongoDB into a pandas DataFrame with selected nested fields.
2. Standardize categorical fields (phase/status) and validate enrollment as numeric where possible.
3. Compute descriptive summaries:
   - Counts by phase and overall status
   - Enrollment distributions by phase
   - Sponsor class distribution by phase/status
   - Results posted rates by phase/status
4. Produce publication-quality figures saved to `docs/`.

## Key figures
- `docs/trial_status_by_phase.png`: trial status composition across phases
- `docs/enrollment_by_phase.png`: enrollment distribution by phase

## Reproducibility notes
- MongoDB credentials are **not** stored in this repository.
- Set `MONGODB_URI` in your environment (or a local `.env` file ignored by git).

