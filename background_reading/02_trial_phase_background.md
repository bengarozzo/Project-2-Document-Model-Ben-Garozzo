# Trial Phases Background

## Phase overview
Clinical drug trials are commonly described using phases that roughly indicate the stage of evaluation:
- Early Phase 1 / Phase 1: Initial safety, dosing, pharmacology
- Phase 2: Preliminary efficacy and continued safety
- Phase 3: Larger confirmatory efficacy and safety
- Phase 4: Post-marketing studies (when applicable)

## Why phase is tricky
- A study can list multiple phases (e.g., "Phase 1/Phase 2").
- Not all interventional studies are phase-labeled (e.g., device studies or missing fields).

## Implication for document modeling
Phase is stored as an **array** (e.g., `phases: ["Phase 2"]`) to preserve multiple values without creating a relational join table.

