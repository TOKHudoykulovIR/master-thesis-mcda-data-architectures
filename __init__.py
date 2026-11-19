"""Computational core for the thesis framework (Stage 2 analysis plan, rules A1–A16, exploratory E-C1–E-C4).

After Delphi Round 1 (1 Oct 2026) the primary criteria set has five members: CARB was excluded from the
Round 2 weighting by Stage 1 rule R2 and is used only in the exploratory carbon analyses.
Criteria order used throughout: CRITERIA (primary) and CRITERIA_EXPLORATORY (primary + CARB, last).
Configurations: CONFIGS."""
CRITERIA = ['TTDP', 'AIRD', 'PORT', 'TCO', 'SECC']
CRITERIA_EXPLORATORY = CRITERIA + ['CARB']
CONFIGS = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7']
# The coded criteria are benefit-type (5 = best, A10). CARB, used only in exploratory runs, is cost-type.
BENEFIT = {'CARB': False, 'TTDP': True, 'AIRD': True, 'PORT': True, 'TCO': True, 'SECC': True}
