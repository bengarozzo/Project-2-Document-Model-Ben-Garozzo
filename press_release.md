# Why Do Some Clinical Trials Finish… and Others Don’t?

## Hook
Every year, thousands of clinical trials begin with the goal of advancing medicine. But many never reach completion. What separates the trials that finish from the ones that stall?

## Problem Statement
Clinical trials are critical for developing new treatments, yet they are often slow, expensive, and uncertain. Many trials remain active for years or fail to complete, delaying important medical progress. One of the biggest challenges is that researchers do not always know which design choices make a trial more likely to succeed. Without this understanding, studies may be overcomplicated, underfunded, or unrealistic in scope. This project focuses on identifying the key structural factors that are associated with whether a trial reaches completion.

## Solution Description
To address this problem, we built a data pipeline using clinical trial data from ClinicalTrials.gov and stored it in a MongoDB database. We then analyzed features such as enrollment size, number of interventions, study phase, and disease type. A statistical model was used to estimate the probability that a trial is completed based on these characteristics. Rather than predicting distant future outcomes, the goal is to identify patterns associated with trials that complete earlier and more efficiently. These insights can help researchers design better trials and allocate resources more effectively.

## Chart
[Interactive Model Visualization](docs/model_completion_probability_dashboard.html)

This chart visualizes each clinical trial as a point. The x-axis shows enrollment size (on a log scale), and the y-axis shows the model’s predicted probability of completion. Color indicates whether the trial is actually completed, and shape represents the disease type.

Several clear patterns emerge from this visualization:

- **Smaller trials are more likely to be completed.** Trials with lower enrollment counts tend to cluster at higher predicted probabilities, suggesting that simpler studies are easier to execute and finish.
- **Larger trials are less likely to be completed (at least in the short term).** As enrollment increases, predicted completion probability drops sharply. Many large trials remain active, reflecting their longer timelines and greater complexity.
- **Completed trials tend to appear in the upper portion of the chart.** This shows that the model is effectively identifying characteristics associated with completed studies.
- **There is still significant overlap between completed and non-completed trials.** This indicates that no single factor determines success, and completion depends on a combination of features such as design complexity, funding, and domain.

Overall, the chart shows that trial completion is strongly tied to study size and complexity, but also highlights the inherent uncertainty in clinical research.

## Data
All data is stored in a MongoDB Atlas database and sourced from the ClinicalTrials.gov API. The dataset includes over 1,400 interventional clinical trials from 2024–2025, covering cancer, diabetes, and heart disease studies. Because the dataset is recent, many trials are still ongoing, so the analysis reflects early completion patterns rather than final long-term outcomes.