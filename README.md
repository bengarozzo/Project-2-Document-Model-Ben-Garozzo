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

## Readings Summary Table
| Title | Description | Link |
|------|-------------|------|
| Analysis of Data from Multiclinic Trial | Discusses how clinical trial data is analyzed across multiple sites and the challenges of combining trial data. | [`Analysis of Data from Multiclinic Trial.pdf`](background_reading/Analysis%20of%20Data%20from%20Multiclinic%20Trial.pdf) |
| Clinical Trial Participation _ FDA | Explains clinical trial participation and why representativeness matters for health equity. | [`Clinical Trial Participation _ FDA.pdf`](background_reading/Clinical%20Trial%20Participation%20_%20FDA.pdf) |
| Machine learning for clinical trials in the era of COVID-19 | Explores how machine learning can support clinical trial design, missing data handling, and adaptive trial decisions. | [`Machine learning for clinical trials in the era of COVID-19.pdf`](background_reading/Machine%20learning%20for%20clinical%20trials%20in%20the%20era%20of%20COVID-19.pdf) |
| Machine Learning Predicts Outcomes of Phase III Clinical Trials for Prostate Cancer | Shows how machine learning can predict clinical trial outcomes using merged clinical trial datasets. | [`Machine Learning Predicts Outcomes of Phase III Clinical Trials for Prostate Cancer.pdf`](background_reading/Machine%20Learning%20Predicts%20Outcomes%20of%20Phase%20III%20Clinical%20Trials%20for%20Prostate%20Cancer.pdf) |
| Randomized Clinical Trials of Machine Learning Interventions in Health Care A Systematic Review | Reviews ML-based clinical trials and highlights issues with reporting, bias, transparency, and generalizability. | [`Randomized Clinical Trials of Machine Learning Interventions in Health Care A Systematic Review.pdf`](background_reading/Randomized%20Clinical%20Trials%20of%20Machine%20Learning%20Interventions%20in%20Health%20Care%20A%20Systematic%20Review.pdf) |
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

### Data Dictionary: Quantification of Uncertainty (Numerical)

| Feature | Metric | Value | Interpretation |
|--------|--------|------|---------------|
| `enrollment_count` | % missing | 0% | All trials contain an enrollment value, but many are estimates rather than actual counts. |
| `enrollment_count` | % estimated (vs actual) | ~100% | Nearly all enrollment values are reported as estimated, introducing uncertainty in final trial size. |
| `trial_duration_days` | % missing | ~30% | Missing when completion date is not yet available (ongoing trials). |
| `trial_duration_days` | Std Dev | High (~800+ days) | Large variability reflects wide differences in trial timelines. |
| `num_interventions` | Std Dev | ~1.5 | Moderate variability in study complexity across trials. |
| `num_primary_outcomes` | Std Dev | ~1.8 | Variation in how trials define success metrics. |
| `num_secondary_outcomes` | Std Dev | ~6.7 | High variability indicates inconsistent reporting of secondary measures. |
| `num_conditions` | Std Dev | ~1.9 | Most trials focus on 1–2 conditions, but some are multi-condition studies. |
| `minimum_age` | % missing | ~1.5% | Small number of trials do not report age requirements. |
| `overall_status` | % "Active" | ~82% | Most trials are still ongoing, introducing temporal bias. |
| `is_completed` | Class imbalance | ~12% completed | Strong imbalance impacts model performance and interpretation. |

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