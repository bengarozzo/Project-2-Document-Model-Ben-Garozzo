# DS 4320 Project 2: Clinical Drug Trials Document Database

## Executive Summary
This project builds a MongoDB Atlas document database of recent clinical drug trials collected from the ClinicalTrials.gov API (2024–2025). The database is designed around nested trial documents (conditions, sponsor, status, enrollment, phases, and outcomes-related fields) to support analysis of how trial characteristics vary by phase and status, including enrollment patterns, sponsor types, conditions studied, and availability of reported results.

## Name
Ben Garozzo

## NetID
huk5pd

## DOI
[WRITE HERE]

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
Analyze recent (2024–2025) clinical drug trials to understand how trial phase and trial status relate to enrollment, conditions studied, sponsor characteristics, and results/outcomes availability using a MongoDB document model built from ClinicalTrials.gov API data.

### Motivation
Clinical trial registries are publicly accessible, but the data is complex, nested, and difficult to analyze without a structured secondary dataset. A document database enables direct preservation of nested fields (e.g., multiple conditions, multiple phases, sponsor details, status timelines, and results metadata) while supporting fast filtering and aggregation for questions about which trials are recruiting, how enrollment differs by phase, and where results are (or are not) reported.

### Rationale for Refinement
The refined problem focuses on actionable, measurable dimensions that appear consistently in ClinicalTrials.gov metadata and are well-suited to document modeling: phase, status, enrollment, conditions, sponsor, and outcomes/results indicators. Restricting the time window to 2024–2025 supports a “recent trials” view and reduces concept drift across long historical periods while still yielding a large enough dataset for comparative analysis.

### Press Release Headline + Link
Recent Clinical Drug Trials (2024–2025): What Phase, Status, and Enrollment Reveal About Today’s Trial Landscape — [`press_release.md`](press_release.md)

---

## Domain Exposition
### Terminology Table
| Term | Definition |
|------|-----------|
| Clinical trial | A research study that prospectively assigns participants to interventions to evaluate health outcomes. |
| NCT ID | The ClinicalTrials.gov identifier for a study (e.g., `NCT01234567`). |
| Phase | Trial stage describing development progress (e.g., Early Phase 1, Phase 1, Phase 2, Phase 3, Phase 4). |
| Overall status | Current recruitment/state of the study (e.g., Recruiting, Active, Completed, Terminated). |
| Enrollment | Number of participants targeted or actually enrolled; may be estimated or actual. |
| Sponsor | Organization responsible for initiating and managing the study (lead sponsor and collaborators). |
| Condition | Disease/health topic studied (often multiple per trial). |
| Intervention | Treatment/strategy being tested (e.g., Drug, Biological, Device). |
| Results posted | Indicator that results information is available on ClinicalTrials.gov for the study. |
| Primary outcome | The main outcome(s) used to evaluate intervention effects; may be described textually. |

### Domain Description
ClinicalTrials.gov publishes structured trial metadata with nested substructures (e.g., identification, status module, sponsor module, conditions module, outcomes module). A document model is appropriate because a single trial naturally contains arrays and nested objects (multiple conditions, multiple phases, multiple outcome measures, sponsor/collaborator entities, and multiple location records). This project uses a MongoDB collection of trial documents to support phase/status-driven analyses of enrollment, conditions, sponsor types, and results/outcomes availability for recent trials.

### Background Readings
The `background_reading/` folder contains short notes summarizing key references about ClinicalTrials.gov data, trial phases/status definitions, and considerations when using registry data to build secondary datasets for analysis.

### Readings Summary Table
| Title | Description | Link |
|------|-------------|------|
| ClinicalTrials.gov API overview | Notes on API endpoints, fields, and pagination limits used for acquisition. | [`background_reading/01_clinicaltrials_api_notes.md`](background_reading/01_clinicaltrials_api_notes.md) |
| Trial phases and what they mean | Summary of phase definitions and common caveats. | [`background_reading/02_trial_phase_background.md`](background_reading/02_trial_phase_background.md) |
| Recruitment status definitions | Summary of overall status categories and interpretation. | [`background_reading/03_trial_status_background.md`](background_reading/03_trial_status_background.md) |
| Enrollment fields (estimated vs actual) | Notes on how enrollment appears in registry data and uncertainty implications. | [`background_reading/04_enrollment_field_notes.md`](background_reading/04_enrollment_field_notes.md) |
| Bias and limitations of registry data | Notes on coverage, reporting biases, and missingness patterns. | [`background_reading/05_registry_bias_limitations.md`](background_reading/05_registry_bias_limitations.md) |

---

## Data Creation
### Data Acquisition (Provenance)
Data is collected from the ClinicalTrials.gov API by querying for interventional studies with a study start date constrained to 2024–2025 (inclusive). The raw API responses are stored as JSON in `data/raw_clinical_trials_2024_2025.json`. A cleaning step then standardizes key fields, flattens only the minimal metadata needed for analysis while preserving nested structures (arrays and objects), and outputs `data/clean_clinical_trials_2024_2025.json`. The cleaned documents are then loaded into MongoDB Atlas as the `clinical_trials` collection.

### Code Table
| File | Description | Link |
|------|-------------|------|
| `pipeline/pull_trials.py` | Pulls trials from ClinicalTrials.gov API (2024–2025) and writes raw JSON. | [`pipeline/pull_trials.py`](pipeline/pull_trials.py) |
| `pipeline/clean_trials.py` | Cleans/normalizes raw JSON into analysis-ready nested documents. | [`pipeline/clean_trials.py`](pipeline/clean_trials.py) |
| `pipeline/load_trials.py` | Loads cleaned JSON documents into MongoDB Atlas (`clinical_trials` collection). | [`pipeline/load_trials.py`](pipeline/load_trials.py) |
| `mongosh/setup_collection.js` | Creates DB/collection and indexes for common query patterns. | [`mongosh/setup_collection.js`](mongosh/setup_collection.js) |
| `mongosh/sample_queries.js` | Example document-model queries/aggregations for analysis. | [`mongosh/sample_queries.js`](mongosh/sample_queries.js) |
| `pipeline/analysis.ipynb` | Analysis notebook (reads from MongoDB, produces figures). | [`pipeline/analysis.ipynb`](pipeline/analysis.ipynb) |

### Rationale for Decisions
- The project uses a document model to preserve the original nested structure of ClinicalTrials.gov modules (e.g., arrays for `conditions` and `phases`, and nested objects for `sponsor` and `results` indicators).
- The time window is limited to 2024–2025 to focus on a “recent trials” secondary dataset and to reduce confounding due to changes in reporting practices over long periods.
- Cleaning standardizes categorical fields (phase/status) and coerces enrollment to numeric when possible while retaining uncertainty metadata (e.g., estimated vs actual).
- Indexes are created for common filters (phase, overall status, conditions, sponsor name/type, and study start year) to support fast queries and aggregations.

### Bias Identification
- Registry data may be incomplete, inconsistently reported, or updated over time, especially for outcomes and results posting.
- Enrollment values can be missing or may be estimated rather than actual.
- Conditions and sponsor names can vary due to free-text entry and inconsistent naming conventions.
- Trials in certain therapeutic areas or sponsor types may be over/under-represented relative to the broader research landscape.

### Bias Mitigation
- Track missingness explicitly for critical fields (phase, status, enrollment, conditions, sponsor, results posted) and report it in the analysis.
- Preserve raw text fields alongside standardized fields when normalization is lossy (e.g., sponsor name).
- Use conservative cleaning rules and avoid “inventing” values; prefer `null` with a documented reason over imputation.
- Where possible, use multiple fields for corroboration (e.g., enrollment value + enrollment type) and flag ambiguous records for exclusion from certain computations.

---

## Metadata
### Implicit Schema Guidelines
Each MongoDB document represents a single clinical trial and preserves nested structure:
- Top-level identifiers: `nct_id`, `brief_title`, `study_type`
- Time window fields: `study_start_date`, `study_start_year`
- Nested status object: `status.overall_status`, `status.why_stopped`, `status.last_update_posted`
- Arrays for multi-valued concepts: `phases[]`, `conditions[]`
- Nested sponsor object: `sponsor.lead.name`, `sponsor.lead.class`, `sponsor.collaborators[]`
- Nested enrollment object: `enrollment.count`, `enrollment.type` (e.g., Estimated/Actual)
- Nested outcomes/results indicators: `results.has_results`, `outcomes.primary[]` (when available)

### Data Summary
| Component | Description |
|----------|-------------|
| Population | Interventional clinical trials with study start dates in 2024–2025 pulled from ClinicalTrials.gov API. |
| Unit of analysis | One MongoDB document per trial (identified by `nct_id`). |
| Storage | MongoDB Atlas collection `clinical_trials`. |
| Raw extract | `data/raw_clinical_trials_2024_2025.json` (API-derived). |
| Clean dataset | `data/clean_clinical_trials_2024_2025.json` (standardized nested documents). |
| Outputs | Publication-quality charts in `docs/` and narrative analysis in `pipeline/analysis.md`. |

### Data Dictionary
| Feature | Type | Description | Example |
|--------|------|-------------|---------|
| `nct_id` | string | ClinicalTrials.gov identifier for the trial. | `"NCT01234567"` |
| `brief_title` | string | Short public title of the study. | `"Study of Drug X in Condition Y"` |
| `study_type` | string | Study type (e.g., Interventional). | `"Interventional"` |
| `study_start_date` | string (ISO) | Study start date if available. | `"2024-06-15"` |
| `study_start_year` | int | Derived year from start date used for filtering. | `2024` |
| `phases` | array[string] | Trial phase(s), standardized labels. | `["Phase 2"]` |
| `status.overall_status` | string | Current/last known study status. | `"Recruiting"` |
| `enrollment.count` | int | Enrollment count when parseable. | `120` |
| `enrollment.type` | string | Enrollment type (Estimated/Actual/Unknown). | `"Estimated"` |
| `conditions` | array[string] | Condition(s) studied. | `["Diabetes Mellitus, Type 2"]` |
| `sponsor.lead.name` | string | Lead sponsor organization name. | `"National Institutes of Health (NIH)"` |
| `sponsor.lead.class` | string | Sponsor class if available (e.g., INDUSTRY, NIH, OTHER). | `"NIH"` |
| `results.has_results` | boolean | Whether results are posted on ClinicalTrials.gov. | `false` |
| `outcomes.primary` | array[object] | Primary outcome measures when available. | `[{"measure":"HbA1c change","time_frame":"24 weeks"}]` |

### Uncertainty Quantification
| Feature | Source of Uncertainty | Explanation |
|--------|----------------------|-------------|
| `enrollment.count` | Estimated vs actual; missingness | Many trials report enrollment as estimated at registration; some never update to actual. |
| `study_start_date` | Updates over time; incomplete records | Start dates can be revised; some records have partial/absent date data. |
| `results.has_results` | Reporting lag and posting behavior | Results may be posted later than study completion; absence is not proof of no results. |

---

## Data Stored in Mongo Atlas
- **MongoDB database**: `ds4320_project2` (configured via environment variables)
- **Collection name**: `clinical_trials`
- **Dataset size**: Over 1,000 trial documents (2024–2025 window)
- **Credentials policy**: MongoDB Atlas credentials and grader access will be submitted in Canvas only (not stored in this repository and not shared on GitHub). The pipeline reads `MONGODB_URI` from environment variables.

---

## Problem Solution Pipeline
- **Notebook (.ipynb)**: [`pipeline/analysis.ipynb`](pipeline/analysis.ipynb)
- **Markdown version**: [`pipeline/analysis.md`](pipeline/analysis.md)

### Data Preparation
The analysis queries MongoDB Atlas (`clinical_trials`) into a pandas DataFrame with selected nested fields (phase, overall status, enrollment, sponsor class/name, conditions, and results indicator). Cleaning steps in Python standardize categorical values and compute derived fields (e.g., `study_start_year`, missingness flags, and grouped phase labels).

### Model Implementation
The project uses descriptive modeling and simple predictive baselines to support the refined problem:
- Aggregations by phase/status (counts, proportions, and enrollment summaries)
- Optional baseline classification (e.g., predict `results.has_results` or `status.overall_status` from phase/enrollment/sponsor class) using scikit-learn with transparent metrics

### Analysis Rationale
The refined question is fundamentally comparative (by phase and status). MongoDB’s document model supports filtering and aggregation across nested arrays (e.g., conditions, phases) and nested objects (sponsor/enrollment/results) without forcing a relational decomposition that would inflate row counts and complicate interpretation.

### Visualization
Figures are generated in the analysis notebook and saved as publication-quality charts in `docs/`:
- `docs/trial_status_by_phase.png`
- `docs/enrollment_by_phase.png`

### Visualization Rationale
Phase- and status-stratified plots provide a clear, high-signal view of trial composition and enrollment scale. All figures are generated with consistent labeling, readable fonts, and appropriate axis formatting for submission-quality presentation.

### How the Pipeline Solves the Problem
The pull → clean → load steps produce a stable secondary dataset in MongoDB Atlas that preserves nested clinical trial structure while standardizing analysis-critical fields. The analysis then uses MongoDB queries and aggregations to measure how phase and status relate to enrollment, conditions, sponsor characteristics, and outcomes/results availability for recent trials, directly answering the refined problem definition.

