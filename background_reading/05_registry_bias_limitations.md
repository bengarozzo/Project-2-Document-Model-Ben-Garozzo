# Bias and Limitations of Registry Data

## Coverage and reporting bias
ClinicalTrials.gov is a major registry, but reporting practices vary by sponsor, geography, and study type. Some fields (especially outcomes/results) may be incomplete or absent.

## Missingness is informative
Missing results/outcomes fields may reflect:
- Studies that are ongoing or recently completed
- Delayed posting behavior
- Differences in sponsor incentives and compliance patterns

## Implication for this project
The secondary dataset preserves missingness (uses `null` rather than imputation) and quantifies missingness rates in the analysis so conclusions reflect data limitations.

