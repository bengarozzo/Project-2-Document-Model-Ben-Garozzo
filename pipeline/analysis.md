# DS 4320 Project 2 Analysis: Clinical Trial Completion (2024–2025)

## Goal

Analyze recent (2024–2025) clinical trials to identify which characteristics are associated with **trial completion** using a MongoDB document database and a predictive model.

## Data Source and Storage

- Source: ClinicalTrials.gov API (public registry)
- Storage: MongoDB Atlas
  - Collections:
    - `raw_clinical_trials`
    - `clean_clinical_trials`
- Local artifacts (not stored in GitHub):
  - Raw pull: `data/raw_clinical_trials_2024_2025.json`
  - Cleaned data: `data/clean_clinical_trials_2024_2025.json`

## Document Model (High Level)

Each document represents one trial (`nct_id`) and preserves nested structure:

- `phases[]`, `conditions[]`
- `overall_status`
- `enrollment_count`, `enrollment_type`
- `lead_sponsor`, `lead_sponsor_class`
- `interventions[]`, `outcomes[]`
- derived features:
  - `num_interventions`
  - `num_conditions`
  - `num_primary_outcomes`
  - `num_secondary_outcomes`

## Methods

1. Query MongoDB data into a pandas DataFrame.
2. Clean and standardize fields (phase, status, enrollment).
3. Create derived variables:
  - `status_group` (Active, Completed, Stopped)
  - `phase_group` (Early, Mid, Late, Post)
  - `trial_duration_days` (when available)
4. Build a logistic regression model to estimate the probability that a trial is completed.
5. Evaluate model performance using accuracy, confusion matrix, and ROC AUC.
6. Generate an interactive visualization linking model predictions to trial characteristics.

## Model Summary

- Model: Logistic Regression (with class balancing)
- Target: `is_completed`
- Features:
  - enrollment size
  - phase group
  - sponsor type
  - study complexity (interventions, outcomes, conditions)
- Performance:
  - Accuracy: ~0.68
  - ROC AUC: ~0.81
- Interpretation:
  - Smaller, simpler trials are more likely to complete
  - Larger, more complex trials tend to remain active
  - No single feature determines completion

## Key Visualization

- `docs/model_completion_probability_dashboard.html`

This interactive chart shows:

- Enrollment size vs predicted completion probability
- Actual completion status
- Differences across conditions and study designs

## Key Insight

Trial completion is strongly associated with **study size and complexity**. Smaller trials tend to complete more quickly, while larger trials are more likely to remain active due to longer timelines.

## Reproducibility Notes

- MongoDB credentials are not stored in this repository
- Set `MONGO_URI` in your environment or `.env` file
- Run:
  - `load_trials.py` → pull and load data
  - `clean_trials.py` → clean and structure data
  - `analysis.ipynb` → run analysis and model