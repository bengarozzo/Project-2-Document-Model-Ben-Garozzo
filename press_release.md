# Recent Clinical Drug Trials (2024–2025): What Phase, Status, and Enrollment Reveal

## Hook
ClinicalTrials.gov contains thousands of newly registered drug trials every year, but the information is nested, inconsistent, and difficult to summarize without building a structured secondary dataset.

## Problem Statement
Stakeholders (patients, clinicians, researchers, and policy analysts) need a clear, data-driven view of recent clinical drug trials: which phases dominate the current landscape, which statuses are most common, how enrollment differs by phase, what conditions are being studied, who is sponsoring the work, and whether results/outcomes information is being posted.

## Solution Description
This project creates a MongoDB Atlas document database of 2024–2025 clinical drug trials collected from the ClinicalTrials.gov API. Each trial is stored as a single nested document that preserves arrays (conditions, phases, outcome measures) and nested objects (status, sponsor, enrollment, results indicators). The analysis queries the `clinical_trials` collection to produce phase/status summaries, enrollment comparisons, and outcomes/results indicators that directly answer the refined problem.

## Chart
- Trial status by phase: `docs/trial_status_by_phase.png`
- Enrollment by phase: `docs/enrollment_by_phase.png`

