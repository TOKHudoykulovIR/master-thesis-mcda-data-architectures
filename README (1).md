# Engine — computational core of the framework

Implements the Stage 2 analysis plan (`../analysis-plan/stage2-full-analysis-plan.md`), rules A1–A16 and the
exploratory carbon analyses E-C1–E-C4, in plain Python (NumPy, SciPy, scikit-learn, Matplotlib). Custom code rather
than a library, so that every step can be defended line by line.

**Design after Delphi Round 1 (1 Oct 2026).**
- **Five primary criteria** (`CRITERIA`: TTDP, AIRD, PORT, TCO, SECC). CARB was excluded from the weighting by Stage 1 rule R2. It appears only in `CRITERIA_EXPLORATORY` (primary + CARB, last) and in `exploratory.py`.
- Every panellist rates **all three scenarios**, and the A7 permutation test permutes each panellist's three labels.
- The previous version is archived in `../_archive-2026-10-01/engine-pre-round1/`.

## Run

```bash
cd engine
python -m unittest discover -s tests      # 51 tests
python demo_synthetic.py                  # end-to-end run on SYNTHETIC data -> demo_output/
```

`demo_output/` is produced from an **invented** panel (six panellists × three scenarios), **random placeholder** matrix
values and **invented** carbon answers. It shows that the pipeline works end to end; it is **not** a result and must
not be read or cited as one. The exploratory part uses the carbon estimate's joint draws (`../carb/carb-draws.npz`).

## Map from the analysis plan to code

| Rule | What | Where |
|---|---|---|
| A1 | Attention check | `bwm.attention_check` |
| A2 | Linear BWM; best-to-worst mismatch of 1 resolved to best-to-others | `bwm.reconcile`, `bwm.linear_bwm` |
| A3 | Input-based CR and thresholds (Liang et al. 2020, Table 3); pair to recontact; consistent-only sensitivity | `bwm.consistency_ratio`, `bwm.cr_threshold`, `pipeline` (`W_consistent`) |
| A4 | Geometric-mean aggregation; arithmetic sensitivity | `aggregate.geometric_mean`, `aggregate.arithmetic_mean` |
| A5 | Kendall's W (tie-corrected); Round 3 decision; stability | `aggregate.kendalls_w`, `delphi_decision`, `stability` |
| A6 | Priority profiles: k-means on clr weights, k by silhouette, minimum cluster size 3 | `stats.priority_profiles` (called only if W < 0.5 persists after Round 3) |
| A7 | Exact permutation test per criterion across scenarios (labels permuted within each panellist: 3! orders each, (3!)^6 = 46,656 assignments), Holm correction | `stats.perm_test_scenarios`, `stats.holm`, `pipeline.scenario_tests` |
| A8 | Qualified-subgroup rerun | rerun `pipeline.weights_stage` on the subgroup's responses |
| A9 | Matrix: insufficient cells; TCO rule K11 | `matrix.PerformanceModel` |
| A10 | TOPSIS, vector normalisation; all five primary criteria benefit-type | `topsis.closeness` |
| A10a | SECC floor in S1, plus no-floor run | `matrix.secc_floor`, `pipeline.ranking_stage` |
| A11 | PROMETHEE II, V-shape with p = range; usual-criterion run; Kendall's τ-b | `promethee.net_flows`, `stats.tau_b` |
| A12 | Min–max normalisation | `topsis.closeness(..., 'minmax')` |
| A13 | Rank reversal with and without C7 | `pipeline.ranking_stage` (`order_without_C7`, `R-b_order_stable`) |
| A14 | SMAA-2: Dirichlet (method of moments), 10,000 draws; acceptability, central weights, confidence factors; bootstrap run; matrix variants K7, K9, K11 | `smaa.run`, `matrix.variant_*`, `apply_tco_k11(directional=True)` |
| A15 | Frontier maps, 50 × 50, top-two criteria; ties shown as ties | `frontier.frontier`, `frontier.plot` |
| A16 | H1–H3 (H3 revised: PORT, S3 > S2), P1–P4, R-a, R-b as worded | `hypotheses` |
| E-C1 | Carbon question coded to a ratio (form answer: direction decides; contradictory direction–rating pairs coded 1 and flagged, revision of 7 Oct); carbon weight appended to each panellist's weights | `exploratory.code_carbon_answer`, `exploratory.carbon_ratio`, `exploratory.append_carbon` |
| E-C2 | Ranking and SMAA with carbon added (estimate R₂ draws; provisioning-floor draws) | `pipeline.ranking_stage` on a model over `CRITERIA_EXPLORATORY`; `matrix.variant_carb` |
| E-C3 | Carbon weight at which the first-ranked configuration changes | `exploratory.carbon_threshold` |
| E-C4 | Functional unit and the 80 % rule | R1/R2/R3 draws from `carb-draws.npz`; `carb-summary.json` |
| E-O1 | Exploratory SMAA with ordinal weight information (amendment 3): each draw picks a panellist, then weights uniform on the region where that panellist's MOST criterion is largest and LEAST smallest; sensitivity runs; uniform reference | `ordinal.sample_region`, `ordinal.weight_sampler_ordinal`, `ordinal.run_scenario`, `ordinal.choice_counts` |

Validation (A17–A18) was withdrawn by amendment 2 (17 Oct 2026); the evaluation against the requirements (A17′) is a judgement, not computation. Amendment 3 (19 Oct 2026): A14 runs only where a scenario has five valid responses; E-O1 is run for all scenarios; no Round 3, so `delphi_decision`, `stability` and `stats.priority_profiles` are not used on the real data.

## Tests

| Test | Reference | Status |
|---|---|---|
| Linear BWM, car example | Rezaei (2016), as reproduced in Rezaei's slides *BWM: Best Worst Method* (n.d., slide 25) | **Passes, with one documented discrepancy.** ξ_L = 0.061 and all five weight values are reproduced. The slide prints the weight vector without labels; read in the criterion order of slide 24 it gives comfort = 0.154 and safety = 0.123, and the engine returns them transposed. That reading violates the model's own constraint at the published ξ_L: \|0.431 − 4 × 0.154\| = 0.185 > 0.061. So the printed order, not the solver, is at fault. The test checks the constraint argument explicitly. To confirm against the original paper when the full text is available. |
| Input-based CR, car example | Liang, Brunelli & Rezaei (2020), Omega 96 | Passes: CR = 0.14, below threshold 0.2958. Threshold table transcribed from two independent copies of the paper, which agree |
| TOPSIS, vector normalisation | Opricovic & Tzeng (2004), EJOR 156, Table 3 | Passes: C* = 0.762, 0.722, 0.238 |
| TOPSIS, min–max | Same example, as in the pymcdm library's test suite | Passes: 0.500, 0.617, 0.500 |
| PROMETHEE II, usual criterion | Zhao, Peng & Li (2013), Procedia CS 17 | Passes: φ = 0.1, −0.3, 0.2 (also verified by hand) |
| BWM exact recovery, attention check, reconcile | Property | Passes |
| Kendall's W | Property: W = 1 for identical raters; W = (ρ_s + 1)/2 for two raters (Siegel & Castellan) | Passes on 20 random cases |
| PROMETHEE V-shape | Hand calculation | Passes |
| Dirichlet method-of-moments | Recovery of known α from 200,000 draws | Passes (3%) |
| SMAA | Dominance ⇒ acceptability 1 and confidence 1; acceptability rows and columns sum to 1 | Passes |
| Permutation test | Exact extremes (p = 2/64 at maximal separation, 6 experts; p = 1 when identical) | Passes |
| Holm | Worked values | Passes |
| Frontier | Extremes, infeasible corner, tie | Passes |
| CARB variant | Replaces draws and medians; original model untouched; wrong shape rejected | Passes |
| A7, three labels | Exact p = 6/6⁶ at maximal separation; p = 1 under identity; two-label case unchanged (2/64); Monte Carlo above the limit | Passes |
| H3 revised | PORT direction; carbon direction only in exploratory runs | Passes |
| Exploratory carbon | Ratio coding; appended weight keeps the stated ratio to the best criterion; threshold at t = 0 equals the five-criterion TOPSIS winner | Passes |
| Pipeline | Runs end to end; reproducible under a fixed seed | Passes |
| E-O1 ordinal SMAA | Region constraints hold; exactly uniform on the region (means, spreads and middle-criterion order frequencies agree with rejection sampling from 2,000,000 uniform simplex draws; E[max] = H₅/5, E[min] = 1/25); equal share per panellist; MOST = LEAST dropped; dominance ⇒ acceptability 1; ordinal information moves acceptability as expected; S1 floor; reproducible | Passes (11 tests) |

PROMETHEE has no test against Brans & Vincke's original example: the original was not obtainable. The Zhao et al. example and the hand calculations cover the usual and V-shape functions.

## Implementation choices that the analysis plan did not fix

These are written into the Stage 2 plan (section *Implementation specifications*) before it is sent.

1. **A7 permutation scheme.** Observations are paired within panellists. Each panellist's values are permuted among that panellist's own scenario labels: a swap for two ratings, all six orders for three. This is exact under the null of no scenario effect. All assignments are enumerated when their number, the product of m_i!, is at most 65,536; otherwise 100,000 Monte Carlo permutations are used. With six panellists × three scenarios: 46,656 assignments, exact; smallest attainable p = 6/46,656 ≈ 0.00013. The statistic is the variance of the scenario means.
2. **Dirichlet precision.** Estimated per criterion as m(1 − m)/var − 1 and averaged across criteria (Ronning 1989).
3. **Ties.** In SMAA, ties are broken at random. In frontier maps, ties are shown as ties.
4. **SECC floor** is applied to the coded (deterministic) SECC value. A cell coded `insufficient` has base 3, so it passes the floor.
5. **P1, P3, P4** are judged as the best configuration inside the claimed set versus the best outside it (for P4: against C1, C2, C5 and C6). A difference of fewer than 5 points is *indeterminate*. **P2** is a threshold claim (C5 + C6 < 10%) with no indeterminate band. A configuration excluded by the S1 floor counts as acceptability 0.
6. **Zero weights** in geometric aggregation are floored at 1e-9.
