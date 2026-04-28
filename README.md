# DS 4320 Project 2: Clinical Trial Completion Analysis (Document Model)

## Executive Summary
This project builds a MongoDB Atlas document database of recent clinical trials (2024–2025) collected from the ClinicalTrials.gov API. The database preserves the nested structure of trial data and supports both exploratory analysis and predictive modeling. The primary goal is to identify patterns associated with whether a clinical trial reaches completion. Using a document model and a logistic regression classifier, the project analyzes how study characteristics such as enrollment size, phase, sponsor type, and study complexity relate to trial completion outcomes.

## Name
Ben Garozzo

## NetID
huk5pd

## DOI
[ADD BEFORE SUBMISSION]

## Press Release
[`press_release.md`](press_release.md)

## Pipeline
[`pipeline/`](pipeline/)

## License
MIT License — [`LICENSE`](LICENSE)

---

## Problem Definition
### General Problem
Clinical drug trials

### Specific Problem
Identify which characteristics of recent (2024–2025) clinical trials are associated with whether a trial reaches completion using a document database and predictive modeling.

### Motivation
Clinical trials are expensive, time-consuming, and uncertain. Many trials remain active for years or fail to complete, slowing down medical progress. Researchers often lack clear guidance on which design choices make trials more likely to succeed. By analyzing real trial data, this project aims to identify structural patterns that are associated with completion.

### Rationale for Refinement
The refined problem focuses on predicting and explaining trial completion using measurable and consistently available metadata (e.g., enrollment, phase, sponsor, and outcomes). The 2024–2025 time window ensures the dataset reflects current trial design practices while still providing enough data for meaningful analysis. This also introduces a realistic constraint: many trials are still ongoing, which affects interpretation and highlights dataset limitations.

### Press Release Headline + Link
Why Do Some Clinical Trials Finish… and Others Don’t? — [`press_release.md`](press_release.md)

---

## Domain Exposition
### Terminology Table
| Term | Definition |
|------|-----------|
| Clinical trial | A research study that tests medical interventions in humans. |
| NCT ID | Unique identifier for each trial on ClinicalTrials.gov. |
| Phase | Stage of trial development (Phase 1–4). |
| Overall status | Current state (Recruiting, Completed, Terminated, etc.). |
| Enrollment | Number of participants in the study. |
| Sponsor | Organization responsible for the trial. |
| Condition | Disease being studied. |
| Intervention | Treatment being tested. |
| Primary outcome | Main measure used to evaluate success. |

### Domain Description
ClinicalTrials.gov provides structured but deeply nested data. A document model is ideal because each trial naturally contains nested fields such as conditions, interventions, outcomes, and sponsor details. This project uses MongoDB to store and query this structure efficiently, allowing analysis without flattening the data into a rigid relational schema.

### Background Readings
Located in `background_reading/`

### Readings Summary Table
| Title | Description | Link |
|------|-------------|------|
| API Overview | How data is collected | [`background_reading/01_clinicaltrials_api_notes.md`](background_reading/01_clinicaltrials_api_notes.md) |
| Trial Phases | Meaning of phases | [`background_reading/02_trial_phase_background.md`](background_reading/02_trial_phase_background.md) |
| Status Definitions | Recruitment states | [`background_reading/03_trial_status_background.md`](background_reading/03_trial_status_background.md) |
| Enrollment Notes | Estimated vs actual | [`background_reading/04_enrollment_field_notes.md`](background_reading/04_enrollment_field_notes.md) |
| Bias Notes | Limitations of registry data | [`background_reading/05_registry_bias_limitations.md`](background_reading/05_registry_bias_limitations.md) |

---

## Data Creation
### Data Acquisition (Provenance)
Data was collected from the ClinicalTrials.gov API for interventional studies from 2024–2025. Raw JSON responses were stored and then cleaned to extract relevant fields while preserving nested structure. Cleaned documents were inserted into MongoDB Atlas.

### Code Table
| File | Description |
|------|-------------|
| `pipeline/load_trials.py` | Pulls and loads raw data into MongoDB |
| `pipeline/clean_trials.py` | Cleans and standardizes data |
| `pipeline/analysis.ipynb` | Performs analysis and modeling |
| `mongosh/setup_collection.js` | Creates indexes |
| `mongosh/sample_queries.js` | Example queries |

### Rationale for Decisions
- Document model preserves nested structure
- Focus on recent data for relevance
- Avoid over-cleaning to preserve original meaning
- Use simple model for interpretability

### Bias Identification
- Many trials are still ongoing
- Enrollment often estimated
- Reporting is inconsistent
- Certain conditions (e.g., cancer) are overrepresented

### Bias Mitigation
- Avoid imputing missing values
- Explicitly analyze missingness
- Interpret results as associations, not causation
- Acknowledge temporal limitations

---

## Metadata
### Implicit Schema Guidelines
Each document represents one trial:
- `nct_id`
- `source_condition`
- `overall_status`
- `phases[]`
- `enrollment_count`
- `lead_sponsor_class`
- `interventions[]`
- `outcomes[]`

### Data Summary
| Component | Description |
|----------|-------------|
| Dataset size | 1,476 trials |
| Time range | 2024–2025 |
| Conditions | Cancer, Diabetes, Heart Disease |
| Storage | MongoDB Atlas |
| Unit | One document per trial |

### Data Dictionary (partial)
| Feature | Type | Description |
|--------|------|-------------|
| `nct_id` | string | Trial ID |
| `source_condition` | string | Condition group |
| `overall_status` | string | Trial status |
| `phase` | string | Trial phase |
| `enrollment_count` | int | Number of participants |
| `num_interventions` | int | Count of interventions |
| `num_conditions` | int | Count of conditions |

### Uncertainty Quantification
| Feature | Uncertainty |
|--------|------------|
| Enrollment | Often estimated |
| Status | Changes over time |
| Completion | Many trials still ongoing |

---

## Data Stored in Mongo Atlas
- Database: `clinical_trials_project`
- Collection: `raw_clinical_trials`, `clean_clinical_trials`
- Size: 1,476 documents
- Access provided via Canvas

---

## Problem Solution Pipeline
### Data Preparation
MongoDB data is queried into pandas. Fields are cleaned, categorized, and transformed into analysis-ready features.

### Model Implementation
A logistic regression model predicts whether a trial is completed using:
- enrollment
- phase
- sponsor type
- study complexity features

### Analysis Rationale
The goal is not to predict future outcomes, but to identify patterns associated with early completion. The model is interpretable and highlights structural relationships in the data.

### Visualization
- Interactive Plotly dashboard (`docs/model_completion_probability_dashboard.html`)
- Shows predicted completion probability vs enrollment

### Visualization Rationale
The visualization directly connects model predictions with real trial characteristics, allowing users to explore how trial size and complexity relate to completion.

### How the Pipeline Solves the Problem
The pipeline creates a structured dataset, analyzes it, and builds a model that identifies key factors associated with trial completion. It transforms raw registry data into actionable insight.