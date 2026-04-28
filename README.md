# DS 4320 Project 2: Clinical Trial Completion Analysis (Document Model)

## Executive Summary
This project builds a MongoDB Atlas document database of recent clinical trials (2024–2025) collected from the ClinicalTrials.gov API. The database preserves the nested structure of trial data and supports both exploratory analysis and predictive modeling. The primary goal is to identify patterns associated with whether a clinical trial reaches completion. Using a document model and a logistic regression classifier, the project analyzes how study characteristics such as enrollment size, phase, sponsor type, and study complexity relate to trial completion outcomes.

## Name
Ben Garozzo

## NetID
huk5pd

## DOI
https://doi.org/10.5281/zenodo.19868760

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
| File | Description | Link |
|------|-------------|------|
| `pipeline/load_trials.py` | Pulls and loads raw data into MongoDB | [`pipeline/load_trials.py`](pipeline/load_trials.py) |
| `pipeline/clean_trials.py` | Cleans and standardizes data | [`pipeline/clean_trials.py`](pipeline/clean_trials.py) |
| `pipeline/analysis.ipynb` | Performs analysis and modeling | [`pipeline/analysis.ipynb`](pipeline/analysis.ipynb) |
| `mongosh/setup_collection.js` | Creates indexes | [`mongosh/setup_collection.js`](mongosh/setup_collection.js) |
| `mongosh/sample_queries.js` | Example queries | [`mongosh/sample_queries.js`](mongosh/sample_queries.js) |

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

### Data Dictionary

| Feature | Type | Description | Example |
|--------|------|-------------|---------|
| `nct_id` | object | Unique identifier for each clinical trial | "NCT07168200" |
| `brief_title` | object | Short title of the trial | "A Phase III Clinical Study..." |
| `official_title` | object | Full descriptive title of the trial | "A Randomized, Controlled..." |
| `source_condition` | object | Broad condition category used for grouping | "cancer" |
| `overall_status` | object | Current trial status | "RECRUITING" |
| `start_date` | object | Trial start date | "2025-10-17" |
| `primary_completion_date` | object | Expected or actual primary completion date | "2028-04" |
| `completion_date` | object | Expected or actual full completion date | "2028-12" |
| `study_type` | object | Type of study | "INTERVENTIONAL" |
| `phases` | object | List of trial phases | ["PHASE3"] |
| `enrollment_count` | int64 | Number of participants in the trial | 720 |
| `enrollment_type` | object | Indicates if enrollment is estimated or actual | "ESTIMATED" |
| `conditions` | object | List of conditions studied | ["Cervical Cancer"] |
| `keywords` | object | Keywords associated with the study | ["immunotherapy"] |
| `lead_sponsor` | object | Name of the lead sponsor | "NIH" |
| `lead_sponsor_class` | object | Sponsor type classification | "INDUSTRY" |
| `brief_summary` | object | Short summary of the trial | "This study evaluates..." |
| `interventions` | object | List of interventions in the trial | [{...}] |
| `arm_groups` | object | Study arms or treatment groups | [{...}] |
| `primary_outcomes` | object | Primary outcome measures | [{...}] |
| `secondary_outcomes` | object | Secondary outcome measures | [{...}] |
| `num_interventions` | int64 | Number of interventions | 2 |
| `num_arm_groups` | int64 | Number of study arms | 2 |
| `num_primary_outcomes` | int64 | Number of primary outcomes | 1 |
| `num_secondary_outcomes` | int64 | Number of secondary outcomes | 6 |
| `num_conditions` | int64 | Number of conditions studied | 1 |
| `healthy_volunteers` | bool | Whether healthy volunteers are allowed | False |
| `sex` | object | Eligible participant sex | "ALL" |
| `minimum_age` | object | Minimum participant age | "18 Years" |
| `is_fda_regulated_drug` | bool | Whether the trial involves an FDA-regulated drug | False |
| `is_fda_regulated_device` | bool | Whether the trial involves an FDA-regulated device | False |
| `has_results` | bool | Whether results have been reported | False |

### Data Dictionary: Quantification of Uncertainty for Numerical Features

| Feature | Metric | Value | Interpretation |
|--------|--------|------:|----------------|
| `enrollment_count` | Missing values | 0 / 1476 = 0.0% | All trials contain enrollment values, but these are often estimated. |
| `enrollment_count` | Mean | 216.0 | Mean is much higher than median due to large outlier trials. |
| `enrollment_count` | Median | 80.5 | Typical trial size is relatively small. |
| `enrollment_count` | Standard deviation | 800.0 | High variability indicates wide differences in study scale. |
| `enrollment_count` | Maximum | 18000 | Extreme outliers introduce uncertainty in averages. |
| `trial_duration_days` | Missing values | 443 / 1476 = 30.0% | Missing duration mainly from ongoing trials. |
| `trial_duration_days` | Median | 1141 | Represents typical planned duration among completed/planned trials. |
| `num_interventions` | Mean | 2.29 | Most trials involve 1–3 interventions. |
| `num_interventions` | Standard deviation | 1.49 | Moderate variation in study complexity. |
| `num_primary_outcomes` | Mean | 1.81 | Most trials define one main outcome. |
| `num_primary_outcomes` | Standard deviation | 1.87 | Some trials define multiple primary endpoints. |
| `num_secondary_outcomes` | Mean | 6.36 | Trials often track multiple secondary outcomes. |
| `num_secondary_outcomes` | Standard deviation | 6.72 | High variability indicates inconsistent reporting. |
| `num_conditions` | Mean | 2.01 | Most trials focus on one or two conditions. |
| `num_conditions` | Standard deviation | 1.92 | Some trials include many conditions. |
| `is_completed` | Completed trials | 181 / 1476 = 12.3% | Strong class imbalance due to recent dataset (most trials still active). |

These numerical summaries show that uncertainty in this dataset is driven primarily by missing completion information and highly variable enrollment sizes, both of which are a result of using a recent (2024–2025) trial cohort.

### Engineered Features

| Feature | Type | Description | Example |
|--------|------|-------------|---------|
| `status_group` | object | Simplified trial status (Active, Completed, Stopped, Unknown) | "Active" |
| `phase` | object | Primary phase extracted from phases list | "PHASE3" |
| `phase_group` | object | Grouped phase category (Early, Mid, Late, Post, Unknown) | "Late" |
| `trial_duration_days` | float | Duration between start and completion dates | 1141 |
| `is_completed` | int64 | Binary target variable (1 = completed, 0 = not completed) | 1 |

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
This project frames trial completion as a binary classification problem. Logistic regression is used because it is interpretable and allows direct understanding of how trial characteristics influence completion probability. The goal is not to maximize prediction accuracy, but to identify meaningful relationships between study design and outcomes.

### Visualization
- Interactive Plotly dashboard (`docs/model_completion_probability_dashboard.html`)
- Shows predicted completion probability vs enrollment

### Visualization Rationale
The visualization directly connects model predictions with real trial characteristics, allowing users to explore how trial size and complexity relate to completion.

### How the Pipeline Solves the Problem
The pipeline creates a structured dataset, analyzes it, and builds a model that identifies key factors associated with trial completion. It transforms raw registry data into actionable insight.
