# Analysis plan — Stage 2: elicitation, aggregation, ranking, robustness and validation

*Draft, revised 1 October 2026 with the Round 1 outcomes, and on 7 October 2026 to match the Round 2 instrument as built (`round2/round2-instrument-as-fielded.md`; previous text in `_archive-2026-10-07/`). The pre-Round-1 draft is archived as `_archive-2026-10-01/stage2-full-analysis-plan-pre-round1.md`. Intended to be fixed before Round 2 was launched; Round 2 was launched on 4 October 2026, before that happened.*

> **Revision of 7 October 2026.** Changes: no consent item (D1); profile of three questions (D4, D5); comparison vectors collected as rating questions rather than grids (D6); carbon strength rated 1–9 without branching, with a coding rule for contradictory answers (D7, E-C1); participation in A8 defined. **Round 2 was launched on 4 October 2026** (author's statement), before this revision. The plan therefore cannot be described as fixed before launch, and the thesis says so (Ch3 §3.11.1). No response had been viewed by 7 October 2026 (author's statement).

> **Amendments.** Three, at the end of this file: 1 (7 Oct 2026, checks and import), 2 (17 Oct 2026, validation replaced by an evaluation against the requirements), 3 (19 Oct 2026, no recontacts, panellists' own corrections, no Round 3, SMAA only where five valid responses exist, exploratory ordinal SMAA E-O1).

**How this plan is fixed.** The plan is not publicly registered; the OSF registration originally intended was dropped by the author's decision. It is **not sent** to the supervisor (author's decision, 4 Oct 2026), so it has no external time-stamp. It is meant to be fixed by the author before Round 2 is launched and before any matrix cell is coded. If Round 2 was launched first, the plan is fixed before any Round 2 response is viewed, and the thesis states which of the two applies. After that date the file is not edited; any later change is recorded as a dated amendment at the end of this document and reported in the thesis. The thesis reports these rules as fixed by the author without external verification, as it does for Stage 1.

---

## Title

Beyond Performance-Only Evaluation: an empirically grounded multi-criteria framework for selecting data architecture configurations — Stage 2 analysis plan: Round 2 elicitation and full analysis

## Description

Second of two analysis plans for a master's thesis study (ITPU, in collaboration with EPAM). Stage 1 fixed the rules for Delphi Round 1. It was written before any Round 1 response was viewed, but it was not sent to the supervisor, so no external time-stamp exists (Stage 1 amendment 1). Round 1 has been analysed under its rules (`round1/round1-analysis-report.md`). The outcomes are summarised below and determine the criteria, configurations and scenarios used here.

This plan fixes, before any Round 2 response is viewed (and, if it is fixed before launch, before any is collected):
- how criteria weights are elicited, checked and aggregated;
- when the Delphi terminates;
- how the configuration-by-criterion matrix is coded;
- how configurations are ranked;
- how robustness is assessed;
- which expectations are tested;
- what counts as successful validation;
- which carbon analyses are exploratory.

**At the date this plan is fixed, no Round 2 responses exist and no matrix cell has been coded.**

### Round 1 outcomes carried into this plan

| Item | Outcome under Stage 1 rules |
|---|---|
| Complete Round 1 responses | **6** (minimum 10 not reached; extension not applied — Stage 1 amendment 2) |
| Criteria retained (R2) | TTDP (median 5.0, IQR 0.75), AIRD (4.0, 0.0), PORT (4.0, 1.5, **contested**), TCO (5.0, 0.75), SECC (5.0, 0.75) |
| Criterion excluded (R2) | **CARB** (median 2.5, IQR 1.0) |
| Criteria re-admitted (R4) | None; highest count: operational reliability, 2 |
| Definitions revised (R3) | AIRD (clarity 3.0), PORT (3.5); boundary sentence added to TCO outside R3 (Stage 1 amendment 9) |
| Configuration set (R7) | Not reviewed (B1: 83% *Mostly*). **C7 redefined** as *Hybrid / multi-platform* (kit K15; Stage 1 amendment 8) after 3 mentions in B2, 2 on a strict reading |
| Vignettes passing the manipulation check (R8) | S1 pass (SECC 100%, *No* 17%); S2 pass (TTDP 100%, *No* 0%); S3 pass (CARB 83%, *No* 17%) |
| Vignettes revised | None |
| Expectations E1, E2 | Both met (100% *Yes* or *Partly*; *Yes* alone 50% each) |
| Round 2 assignment (R10) | All six panellists rate all three scenarios, in a Latin-square order (Stage 1 amendment 7) |
| Carbon in Round 2 | One exploratory question per scenario, after the weighting (Stage 1 amendment 6) |

The analysis below is written for the **five-criterion** case.

---

## Hypotheses

Three groups. None is a condition for any other; all are reported regardless of outcome.

### H — priorities differ by organisational context

These test whether the panel's weights respond to the scenarios in the directions the vignettes were written to elicit. They are necessary for the scenario design to be meaningful, not substantive findings about architectures.

- **H1.** In S1 (regulated finance), SECC receives the highest group weight.
- **H2.** In S2 (high-growth start-up), TTDP or AIRD receives the highest group weight.
- **H3 (revised 1 Oct 2026).** In S3 (sustainability-mandated), PORT receives a higher group weight than in S2.

*On H3.* The original H3 — CARB weighs more in S3 than in S1 and S2 — cannot be tested, because CARB was excluded from the weighting. The revision uses the vignette's second design signal, architectural longevity, which was written into S3 before Round 1. It narrows the comparison to S2. S2 was designed with PORT as a minor concern. S1 was designed with PORT elevated, so no S3–S1 difference is predicted. The author had seen the Round 1 emphasis shares for PORT (S3 67%, S1 50%, S2 17%) when revising, and the thesis says so. The original direction is reported in exploratory form (E-C1).

### P — practitioner propositions about which configurations win

Stated before any ranking is computed, so that the results can confirm or contradict what practice expects. Tested on first-rank acceptability from the SMAA (see *Analysis plan*, A14).

- **P1.** In S1, a warehouse configuration (C1 or C3) has the highest first-rank acceptability.
- **P2.** In S2, the federated configurations (C5, C6) together have first-rank acceptability below 10%.
- **P3.** In S3, a lakehouse configuration (C2, C4 or C6) has the highest first-rank acceptability.
- **P4 — the central question of the thesis.** In at least one scenario, a hub-and-spoke configuration (C3 or C4) has higher first-rank acceptability than every centralised and every federated configuration.

### R — robustness expectations

- **R-a.** The TOPSIS and PROMETHEE II rankings agree at Kendall's τ-b ≥ 0.7 in each scenario.
- **R-b.** Adding or removing C7 changes the relative order of C1–C6 in no scenario.

---

## Design plan

**Study type.** A Delphi study with a conditional third round *(not held: amendment 3, point 4)*, combined with a multi-criteria decision analysis whose performance values are coded from documented evidence. Carbon intensity, estimated from published benchmark runs, enters only exploratory analyses.

**Two independent inputs.** Criteria weights are *preferences* and are elicited from the panel. Performance values are *facts* about configurations and are coded from evidence by two coders. Neither input is derived from the other, and no person contributes to both.

**Blinding.** Panellists do not see the performance matrix. Coders do not see the elicited weights until coding is complete and agreement has been computed.

---

## Sampling plan

**Round 2 sample.** The six panellists who completed Round 1. Each rates **all three scenarios** (Stage 1 amendment 7).

**Instrument.** A Microsoft Forms questionnaire in three versions that differ only in scenario order. The orders form a 3 × 3 Latin square, with two panellists per version, so that each scenario is rated first, second and third by two panellists each:
- A: S1 → S2 → S3;
- B: S2 → S3 → S1;
- C: S3 → S1 → S2.

Each version contains:
- a statement of how answers are used (no consent item);
- a profile section of three questions;
- a short summary of the Round 1 results;
- a criteria reference section;
- for each scenario, one Best-Worst Method section — two choice questions and two blocks of five 1–9 rating questions — followed by an optional rationale and the exploratory carbon question.

Responses are linked to Round 1 by respondent name, recorded by the form and never published.

**Minimum for analysis.** Five valid responses per scenario. A scenario with fewer is reported descriptively, without SMAA. *(Applies to all three scenarios: no version-C response was received, amendment 3, points 2–3.)*

**Field period.** Ten to fourteen days, with reminders on days 4 and 8.

---

## Variables

**Elicited, per panellist per scenario:**
- best criterion;
- worst criterion;
- best-to-others vector (1–9 for each of the five criteria);
- others-to-worst vector (1–9 for each);
- optional free-text rationale.

**Exploratory, per panellist per scenario.** Whether carbon intensity matters less than, as much as, or more than the panellist's most important criterion, and by how much (1–9; panellists are told to choose 1 for "equally important").

**Profile, per panellist:**
- role;
- years of experience (less than 3; 3 to less than 5; 5 to 10; more than 10);
- participation in a platform selection or migration decision (none / contributor / decision owner or co-owner).

The number of decisions, platform types, operating models, clouds and industries are not collected; the panel's composition against the specification's quotas cannot be checked.

**Coded, per configuration per criterion.** A performance value on the criterion's anchored scale, with its evidence record. The carbon estimate is computed, not coded, and is used only in the exploratory analyses.

---

## Analysis plan

### Weights

**A1 — Attention check.** A scenario response fails if any of the following holds:
- the best criterion is not rated 1 in the best-to-others vector;
- the worst criterion is not rated 1 in the others-to-worst vector;
- the best-to-worst value differs between the two vectors by more than 1.

A failing response triggers one recontact asking the panellist to confirm or correct the specific item. Unresolved failures are excluded for that scenario; the number is reported.

**A2 — Individual weights.** Computed by the linear Best-Worst Method (Rezaei, 2016), solved as a linear programme. Where the vectors disagree on best-to-worst by exactly 1, the best-to-others value is used.

**A3 — Consistency.**
- Assessed by the input-based consistency ratio of Liang, Brunelli & Rezaei (2020), with the threshold tabulated there for five criteria on a nine-point scale.
- A response above the threshold triggers one recontact identifying the comparison pair contributing most to the inconsistency. Revised responses replace the originals.
- Responses remaining above the threshold are **retained** in the primary analysis and **excluded** in a sensitivity analysis; both results are reported.

**A4 — Aggregation.** Group weights per scenario are the geometric mean of individual weight vectors, renormalised to sum to one. Arithmetic-mean aggregation is reported as a sensitivity check.

**A5 — Consensus and termination.** Agreement per scenario is measured by Kendall's W over the panellists' criterion rankings. *(Round 3 not held; W reported descriptively: amendment 3, point 4.)*

| Outcome after Round 2 | Action |
|---|---|
| W ≥ 0.5 in every scenario | Delphi terminates |
| W < 0.5 in any scenario | Round 3 for that scenario: panellists see the anonymised group weights and their own, and may revise |

After Round 3 the Delphi terminates regardless of W. Stability between Rounds 2 and 3 is reported as the mean absolute change in group weight per criterion.

**A6 — Dissensus.** *(Not run: no Round 3; amendment 3, point 4.)* If W < 0.5 persists after Round 3 in any scenario, the individual weight vectors for that scenario are clustered by k-means on centred log-ratio-transformed weights. k is chosen from 2 to 4 by mean silhouette, with a minimum cluster size of three. With six panellists, only k = 2 (three and three) is admissible. Clusters are reported as *priority profiles*, and each is carried separately into the ranking and SMAA. Dissensus is a finding, not a failure.

**A7 — Weights across scenarios (H1–H3).** Descriptive comparison of group weights, plus one exact permutation test per criterion comparing the three scenarios, with Holm correction across the five criteria. No multivariate test is performed; the panel is too small to support one. H1–H3 are judged by the direction of the group weights (A4); the permutation tests for the criteria they involve (SECC, TTDP, AIRD, PORT) are reported alongside and qualify the strength of that judgement.

**A8 — Panel qualification (Stage 1 rule R9).** A1–A7 are repeated for the subgroup meeting the protocol's original criteria: personal participation in a platform selection or migration decision (answer *contributor* or *decision owner or co-owner*), **and** at least five years' experience (bands 5 to 10, or more than 10). The specification asked for a decision leader or *substantial* contributor; the profile cannot separate substantial from minor contributions, so the subgroup approximates the original criterion. A panellist with either profile answer missing is asked once; if it is still missing, they are left out of the subgroup and the number is reported. If the subgroup has fewer than five members, the comparison is descriptive only. A participation-only subgroup is reported alongside as supplementary.

### Performance matrix

**A9 — Coding.** Each cell of the 7 × 5 matrix is scored independently by two coders against the anchored scale in the metric passport for that criterion. The coders use the evidence packs assembled from the literature review corpus and the multivocal component. Evidence is graded primary, secondary or tertiary; no cell may rest on tertiary evidence alone. Each coder records, per cell, the score, the sources and the anchor level judged met.

Inter-coder agreement is computed per criterion by Krippendorff's α (ordinal). **Threshold: α ≥ 0.7.** Following Krippendorff (2004), values from 0.70 to below 0.80 are reported as supporting tentative conclusions only. PORT, AIRD, SECC and TTDP have only 6–7 non-calibration cells each, so a pooled α across all non-calibration cells is reported alongside as supplementary (kit K14). A cell either coder marks *insufficient* is left out of α and reported separately, with the cells on which the coders disagreed about sufficiency; each α is reported with the number of cells it uses. TCO has two coded cells (C1, C2; K11); no per-criterion α is computed for it, and its cells enter the pooled α.
- A criterion below the threshold has its anchored scale reviewed for ambiguity, the revision documented, and the criterion recoded by both coders. Agreement is reported before and after.
- Remaining disagreements are resolved by discussion. The pre-resolution scores are retained for A14.

**TTDP** is coded on an anchored scale from five architectural determinants of delivery time: queue position, hand-offs, provisioning, endpoint tooling and platform dependency. It is not coded as elapsed days, because the literature review found no study reporting elapsed delivery time for data products. The scale scores a class of expected delivery speed; no claim is made about absolute durations.

**Criterion boundaries (kit K17).**
- The one-off cost of a future exit or migration is scored under PORT only. TCO is the three-year running cost of the reference workload.
- SECC scores the policy regime. AIRD scores whether AI workloads can use governed data natively.

**C7 (kit K15)** is coded as *Hybrid / multi-platform*: a lakehouse core and a warehouse serving layer in one estate, with no fabric layer assumed.

**Descriptive checks on the coded matrix (added 4 Oct 2026, from Chapter 4).** After coding, the spread of each criterion across C1–C7 is reported as a discriminance check, and the Spearman rank correlations across configurations of SECC with PORT, AIRD with PORT, AIRD with SECC and TTDP with SECC are reported. With seven configurations these are descriptive; they test no hypothesis and change no rule.

**Cells both coders mark as having insufficient evidence** are scored at the scale midpoint, with the full range carried into SMAA as uniform uncertainty, and are listed in the thesis.

**Exception — TCO (kit K11):**
- C1 and C2 differ only if two independent sources support the difference, each stating whether personnel cost is included.
- C3–C6 inherit their platform column's value, and C7 takes the mean of C1 and C2. Each carries a symmetric shift of −1 to +1 class, sampled in A14.
- A midpoint would impose an ordering between rows and platforms that the evidence does not contain.

**Reference workload and edition.**
- The reference workload is 5 TB of managed data, daily batch ELT plus interactive BI for about 100 analysts, over a 3-year horizon, in AWS eu-central-1 (kit K12; confirmed by the technical supervisor).
- The cloud-warehouse profiles are coded at Snowflake Business Critical, for SECC and TCO alike (kit K7).

The full coding procedure, anchored scales and reference profiles are fixed in `matrix-coding-kit-v1.md` (**version 1.3**), version-frozen at the date this plan is fixed.

*Contingency, declared now.* If a second coder cannot be secured, the matrix is single-coded, no α can be reported, and this is stated as a limitation of the performance values in the thesis.

*Contingency in force (7 October 2026).* No second coder was secured; the author codes the matrix alone. Consequences:
- there are no calibration discussions, no α and no disagreement resolution;
- a cell the author marks *insufficient* is treated as a cell both coders mark insufficient would be (midpoint, full-range uncertainty);
- sensitivity run 2 of A14 (coder disagreement) cannot be performed and is dropped;
- no substitute reliability check, such as recoding after an interval, is planned (author's decision, 7 Oct). Adding one later would be a dated amendment;
- blinding: the author codes and freezes the matrix before viewing any Round 2 response (see *Blinding* above).

### Ranking

**A10 — Primary method: TOPSIS.** Vector normalisation; Euclidean distance to the ideal and anti-ideal solutions; one ranking per scenario, using the group weights from A4. All five criteria are scored on anchored scales oriented so that 5 is the most favourable outcome, and are therefore benefit-type.

**A10a — SECC admissibility floor in S1.** Two predecessor works argue that security and compliance act as gating conditions, and that compensatory aggregation can mask a fatal gap behind a high aggregate.
- In S1 only, any configuration scoring below 3 on SECC is excluded from the ranking before A10, A11 and A14 are applied. Level 3 is the first anchor at which fine-grained controls, centralised audit and major certification mappings are all present.
- In S2 and S3 security is treated as a genuine trade-off and remains compensatory.
- A sensitivity run for S1 without the floor is reported.

**A11 — Cross-check: PROMETHEE II.**
- Type III (V-shape) preference function per criterion, with the preference threshold *p* equal to the range of that criterion across configurations. Net flows determine the ranking.
- Agreement with TOPSIS is reported as Kendall's τ-b per scenario (R-a).
- A sensitivity run uses the Type I (usual) preference function.

**A12 — Normalisation sensitivity.** TOPSIS is rerun with min–max normalisation. Rank changes are reported.

**A13 — Rank reversal (R-b).** Rankings are computed with C1–C6 only and with C1–C7. Any change in the relative order of C1–C6 is reported with the mechanism that produced it.

### Robustness

**A14 — SMAA.** *(Runs only where a scenario has five valid responses: at most S1. Exploratory E-O1 for all scenarios: amendment 3, points 3 and 5.)* For each scenario, a Dirichlet distribution is fitted to the individual weight vectors by the method of moments. 10,000 weight vectors are drawn, and each is combined with the performance matrix through TOPSIS. Reported per scenario:
- **rank acceptability indices** — the share of draws in which each configuration takes each rank;
- **central weight vectors** — the mean weights under which each configuration ranks first;
- **confidence factors** — the share of draws in which a configuration ranks first when weights are fixed at its central vector.

Uncertainty in the performance matrix enters the primary run in two places fixed by A9:
- cells with insufficient evidence are sampled across the full scale;
- derived TCO rows are sampled across their ±1 class shift.

**Five sensitivity runs:**
1. Weights resampled by bootstrap from the observed individual vectors, rather than drawn from the fitted Dirichlet.
2. Matrix values sampled uniformly between the two coders' pre-resolution scores, for every cell on which they initially disagreed. *(Dropped under the single-coder contingency, A9.)*
3. C6 re-scored on TTDP at level 1 ("domains blocked on missing baseline capability"), removing the reference profile's assumption that the self-serve platform exists (kit K9).
4. The warehouse cells C1, C3, C5 and C7 re-coded on SECC and TCO under Snowflake Enterprise edition (kit K7).
5. TCO shifted directionally: federated rows dearer by 0 to 2 classes, hub rows −1 to +1, hybrid dearer by 0 to 1 (kit K11).

A conclusion that changes under either of the last two runs is reported as dependent on the edition or on the cost assumption.

**A15 — Priority frontier maps.** For each scenario, two-dimensional maps are drawn by varying the weights of two criteria over their full range, rescaling the remaining weights proportionally to their group values, and recording the first-ranked configuration at each point on a 50 × 50 grid. Maps for all criterion pairs are produced. The main text reports the pair formed by the scenario's two highest-weighted criteria; the rest go in an appendix.

**A16 — Tests of P1–P4.** *(Only partly possible: amendment 3, point 3. Exploratory examination against E-O1: point 5.)* Each proposition is judged against first-rank acceptability from A14 exactly as worded. A proposition is *supported*, *not supported*, or *indeterminate*. It is indeterminate where the leading configuration's acceptability exceeds the next by fewer than five percentage points.

### Exploratory — carbon intensity

Carbon intensity was excluded from the weighting by Stage 1 rule R2. S3 was written around a carbon mandate, and 83% of panellists recognised it in the Round 1 manipulation check. That shows the vignette carried its signal, not how much weight carbon would receive, which is what E-C1 measures. The analyses below are **exploratory**. They change no primary result and are reported in a separate section.

**E-C0 — The estimate.** CARB values are **estimated, not measured** (kit K1, K16). Platform values are computed from published benchmark runs: runtime and configuration converted to energy with Cloud Carbon Footprint coefficients, multiplied by the grid intensity of AWS eu-central-1, plus embodied emissions by the CCF method. The workload is the reference workload of A9, and three candidate functional units are used. Every uncertain input is sampled over a declared range. The script `carb/carb_estimate.py` and the table `carb/carb-assumptions.md` (v0.2) are version-frozen at the date this plan is fixed. The operating-model effect is an assumed overhead range, so CARB comparisons within a platform column are reported as indeterminate.

**E-C1 — The panel's carbon judgement.** In each scenario the carbon question is coded as a ratio *a*:
- *a* = 1 for "equally important";
- *a* = *k* for "less important by *k*";
- *a* = 1/*k* for "more important by *k*", with *k* from 2 to 9.

The direction answer decides. A rating of 1 with "less" or "more", or a rating above 1 with "equally important", is coded *a* = 1 and counted as inconsistent; the count is reported per scenario. There is no recontact for this question.

The panellist's carbon weight is their best criterion's weight divided by *a*. The six weights are renormalised to sum to one. Group carbon weights are formed as in A4. They are compared across scenarios descriptively and with the A7 permutation scheme. The original H3 direction — carbon weighs more in S3 than in S1 and S2 — is reported in this exploratory form.

**E-C2 — Ranking with carbon.** TOPSIS and SMAA (A10, A14) are rerun with the six-criterion weights from E-C1, with CARB as a cost-type criterion on the functional unit R₂, sampled from the estimate's joint draws. They are rerun once more with the estimate's provisioning-floor draws (`carb-assumptions.md` §4a, R3b). P1–P4 are not re-judged on these runs; changes in first-rank acceptability are reported.

**E-C3 — Carbon threshold.** For each scenario, the smallest carbon weight *t* at which the TOPSIS first-ranked configuration changes is computed. *t* runs from 0 to 0.6 in steps of 0.01, with the primary group weights scaled by (1 − *t*). It is reported next to the group carbon weight from E-C1. This shows whether the panel's own valuation of carbon would be enough to change the recommendation.

**E-C4 — Functional unit and platform discrimination.** E-C2 is repeated with CARB per pipeline run (R₁) and per data product per month (R₃). CARB is described as discriminating between platform columns only if one column is lower in at least 80% of draws. The median difference between the columns is reported alongside, because that rule carries no magnitude condition.

### Implementation specifications

Fixed with the computational core (`engine/`, revised 1 Oct 2026) because the rules above leave them open:

- **A7 permutation scheme.** Each panellist rated all three scenarios, so labels are permuted *within* panellists over all 3! = 6 orders. The statistic is the variance of the scenario means. All assignments are enumerated when their number is at most 65,536; with six panellists this is (3!)⁶ = 46,656, so the test is exact. The smallest attainable p is 6/46,656 ≈ 0.00013. Above the limit, 100,000 Monte Carlo permutations are used and this is reported.
- **A14 Dirichlet precision.** Estimated per criterion by the method of moments and averaged across criteria. Ties in SMAA ranks are broken at random.
- **A10a.** The SECC floor applies to the coded value. A cell coded `insufficient` (base 3) passes it.
- **A15.** Ties for first place are shown as ties, not resolved.
- **A16.** P1, P3 and P4 compare the best configuration inside the claimed set with the best outside it; for P4 the comparison set is C1, C2, C5 and C6. P2 is judged against its 10% threshold without an indeterminate band. A configuration excluded by the S1 floor counts as acceptability 0.
- **E-C1.** The best criterion is the one the panellist selected as best in that scenario, after any A1 recontact.

### Validation (RQ4)

*Withdrawn by amendment 2 (17 October 2026). Kept below as originally fixed.*

**A17 — Expert assessment.** Three to five data architects who took no part in Rounds 1–3 review, for each scenario, the frontier maps and rank acceptability results. They rate on a 1–5 scale:
- *validity* — "the results reflect how these choices play out in practice";
- *usefulness* — "I would use this in an architecture decision".

**Threshold, fixed now:** the framework is judged valid and useful if **at least 70% of assessors rate each dimension 4 or higher.** Falling short on either is reported as such, with the assessors' comments.

**A18 — Retrospective case.** One past EPAM platform decision, anonymised. Weights are elicited from one or more participants in that decision with the same BWM instrument, applied to a scenario description of that organisation at the time. The framework's output is compared with the configuration the organisation actually chose.

**Consistency criterion, fixed now:**
- The recommendation is *consistent* with the actual decision if the chosen configuration has the highest or second-highest first-rank acceptability under the case's elicited weights.
- Otherwise it is *discordant*, and the discordance is analysed: whether it reflects a criterion the framework omits, a weight the case participants would revise, or a decision the participants themselves regard as mistaken.
- A discordant case is reported, not replaced.
- The case is conducted and reported following the case-study guidelines of Runeson & Höst (2009).

---

## Other

**Software and verification.** All computation is in Python (`engine/`; agreement in `matrix/agreement.py`). Before any study data are processed, each method is verified by unit tests:
- linear BWM — Rezaei (2016), as reproduced in Rezaei's BWM tutorial;
- input-based consistency ratio — Liang, Brunelli & Rezaei (2020);
- TOPSIS — Opricovic & Tzeng (2004);
- PROMETHEE II — Zhao, Peng & Li (2013), plus hand calculations. Brans & Vincke's original example could not be obtained.
- Krippendorff's α — Krippendorff (2011).

Property tests cover the remaining components. The tests are run before every analysis run, and the Python and package versions are recorded with the outputs.

**Declared limitations, carried from Stage 1:**
- All panellists are EPAM employees. Their decision experience is likely to span client organisations, which would mitigate but not remove the single-employer limitation; this is the author's assumption and is not recorded by the profile.
- Recruitment did not apply the protocol's decisive criterion; A8 addresses this.
- **The panel has six members against a planned minimum of ten.**
- The Stage 1 rules carry no external time-stamp.
- One Round 1 respondent's relevance ratings appear reversed. No retention decision depends on how they are treated; the *contested* flag on PORT does.
- No stage of the study has formal ethics approval; the study specification had called for university ethics review. Neither round contained a consent item, although the specification required written informed consent.
- C7 is coded in its layered form; the side-by-side hybrid named by one panellist is covered by the definition but not coded separately.
- Carbon intensity, a criterion the framework was designed to include, was excluded by the panel's relevance ratings and is analysed only in exploratory form.

**Deviations.** Any departure from this plan is recorded as a dated amendment with its rationale and reported in the thesis. Analyses not specified here are labelled *exploratory*.

**Data and materials.** Anonymised weight vectors, profile data in aggregated form (three questions), the coded matrix with each coder's scores and evidence records, and all analysis code will be published with the thesis materials.

**Sent to the supervisor on:** not sent. **Fixed by the author on:** 7 October 2026 — after the Round 2 launch (4 October), before any Round 2 response was viewed, and before any matrix cell was coded. **Round 2 launched at that date:** yes (4 October 2026). **Round 2 responses viewed at that date:** none — the author states that the Responses view had not been opened as of 7 October 2026 and will not be opened before the matrix is coded. **Matrix cells coded at that date:** none.

## Amendments

**Amendment 1 — 7 October 2026.** Made after the plan was fixed the same day, before any Round 2 response was viewed and before any matrix cell was coded. The occasion was the author's test export of one form version, in which one criterion was chosen as both MOST and LEAST important and every rating was 1. That export exposed the first gap below. The others were found in a review of the engine and the import code that followed.

1. **A1 — two further failures.** A scenario response also fails A1 if:
   - the same criterion is chosen as best and as worst; or
   - the best-to-worst value is 1 (best rated equal to worst) while any rating other than the best-to-worst pair is above 1.

   The form allows both. Under the previous engine, both passed A1. A best = worst response gave equal weights when every rating was 1, and otherwise weights with no interpretation. The second case is contradictory: if the best criterion is no more important than the worst, every criterion is equally important. Recontact and exclusion follow A1 as written.
2. **A3 — which threshold applies.**
   - **Threshold row.** The threshold is read from Liang, Brunelli & Rezaei (2020), Table 3, in the row for the response's own best-to-worst value and the column for five criteria. "On a nine-point scale" in A3 refers to the rating scale, not to a single row of the table.
   - **Best-to-worst value of 2.** Table 3 has no row for 2. The note to the table states that the threshold "should be 0 in this case, because, when the preferences are ordinal-consistent, the CRI = 0", and that the decision-maker should revise when CR > 0. This threshold is adopted.
   - **Previous behaviour.** Under the previous engine, every response with a best-to-worst value of 2 was marked consistent, whatever its CR. That included CR = 1, and higher values where ratings exceed the best-to-worst value (for example 39.5).
   - **Consequence.** With a best-to-worst value of 2, only the pairs (1, 2) and (2, 1) are consistent. A criterion judged to lie in between, rated (1, 1), gives CR = 0.5, so such flags are expected to be common. They are reported separately from flags under the table rows, and the recontact message explains the constraint rather than implying an error.
   - **Best-to-worst value of 1.** Such a response is consistent only when every rating is 1 (point 1).
3. **E-C1 — anchor of the carbon answer.** The carbon question compares carbon with "the criterion you chose as MOST important" at the time of answering. The anchor is therefore the MOST choice in the response as first submitted, even if an A1 recontact changes it. The carbon weight is the revised weight of that criterion divided by *a*. The first import is archived for this purpose. This replaces the implementation specification "after any A1 recontact" for E-C1.
4. **Import** (`round2/round2_import.py`):
   - **Versions.** Each export is labelled with its version, and its sections are mapped to scenarios by that version's Latin-square order. A file in which no respondent is assigned to its version stops the import as probably mislabelled. A single respondent who answered another version is analysed in the order actually seen and reported.
   - **Identities.** Respondents are matched to codes by e-mail or by first name and surname, through a key kept outside the published materials. The researcher's test rows are removed.
   - **Duplicates.** A respondent's row on the assigned version is kept; among several, the latest is kept. The others are excluded and reported. This rule is applied without looking at values.
   - **Report.** The import report shows counts and flags only, with no ratings, weights or choices.

Implemented in:
- `engine/engine/bwm.py`, with tests in `engine/tests/test_amendment1.py`;
- `round2/round2_import.py`, with tests in `round2/test_round2_import.py`.

**Amendment 2 — 17 October 2026.** Made after the matrix was coded. By the author's statement, no Round 2 response had been viewed by this date.

1. **A17 and A18 withdrawn.** The expert assessment and the retrospective case are not carried out (author's decision). RQ4 is reworded: *To what extent does the framework, applied to the three scenarios, meet the four requirements derived from the review (thesis §2.7.5)?*
2. **A17′ — evaluation against the requirements.** Each requirement is judged *met*, *partly met* or *not met*. *Partly met* applies when the condition holds for some criteria or scenarios but not all, and the exceptions are named.
   - **Commensurable alternatives:** met if all seven configurations are scored on the same criteria, the same anchored scales and the same reference workload, and every cell carries a score or a declared `insufficient`.
   - **Criteria scorable from stated evidence:** met if every coded cell records the mechanism shown and sources that satisfy the tier rule, and every criterion takes at least two different values across the configurations.
   - **Weights with a traceable origin:** met if each scenario's group weights can be recomputed from the archived, anonymised responses with the released code, and the consistency of every response and the panel's agreement are reported.
   - **Outputs that state their conditions:** met if, for each scenario, the first-ranked configuration is reported with its first-rank acceptability, its frontier map and the sensitivity runs that change it.
3. **Known when this amendment was made.** The coded matrix gives all seven configurations the same cost class, so the discrimination condition in the second criterion will record TCO as not discriminating.

**Amendment 3 — 19 October 2026.** Made after versions A and B had been imported (four panellists) and their A1 and A3 flags read, and after the analyst had read the values of the flagged responses to draft the recontact messages. Matrix frozen before that (`matrix/MATRIX-FROZEN-2026-10-19.md`). No weight or ranking had been computed.

1. **No recontact.** The recontacts required by A1 and A3 are not made (author's decision: no time before the deadline for the final product). Drafts were prepared and are archived unsent (`round2/recontact/`).
   - A1 is applied as written for an unresolved failure: the response is excluded for that scenario. Six of the twelve scenario responses in versions A and B failed A1; one was corrected by the panellist (point 6), so five are excluded.
   - A3 is applied as written: responses above the threshold are retained in the primary analysis and excluded in a sensitivity analysis.
   - Every other part of an excluded response (profile, MOST and LEAST choices, rationale, carbon answer) is kept. A carbon weight (E-C1) is not computed where the BWM response is excluded.
2. **Close of Round 2.** Round 2 closes when the two version-C panellists have responded, or on 20 October 2026, whichever comes first. *Outcome:* neither version-C panellist responded, and Round 2 closed on 20 October 2026 (author's statement). Four of the six panellists answered.
3. **Consequence, known when this amendment was made.** From versions A and B, S1 has three valid responses (after the correction in point 6), S2 and S3 two each. With the two version-C panellists, S1 can reach the minimum of five; S2 and S3 at most four. Under the rule *Minimum for analysis*:
   - S2 and S3 are reported descriptively, without SMAA (A14);
   - S1 is analysed by A14 only if both version-C responses are valid for it;
   - A16: P2 and P3 cannot be judged as specified; P1 can if A14 runs for S1; P4 can be found supported in S1 but cannot be rejected, since the other scenarios are not analysed;
   - the SMAA part of E-C2 follows the same minimum; its TOPSIS part and E-C3 are reported descriptively.
   - *Outcome at the close:* S1 three valid responses, S2 and S3 two each. A14 runs for no scenario; P1–P4 cannot be judged as specified in any scenario and are examined only on E-O1 (point 5).
4. **No Round 3.** Round 3 is not held, whatever Kendall's *W* turns out to be (author's decision, made before *W* was computed). A5 is reported descriptively: *W* per scenario over the valid responses, with no termination decision and no stability measure. A6 (priority profiles) is not run: it applies only after Round 3, and its minimum cluster size of three cannot be met.
5. **E-O1 — exploratory SMAA with ordinal weight information.** Added because A14 cannot run for S2 and S3, and for S1 only if both version-C responses are valid. E-O1 is run for all three scenarios, so that they are compared on one basis; where A14 runs for S1, both are reported and A14 is primary. Specified before the version-C responses were received. When it was specified, the analyst had seen the MOST and LEAST choices of the four panellists in versions A and B; no weight, ranking or acceptability had been computed.
   - **Input.** Each panellist's MOST and LEAST choice per scenario (questions (a) and (b)), as given, including scenario responses excluded by A1: these are separate single-choice questions, not part of the comparison blocks that A1 checks. A response with the same criterion as MOST and LEAST gives no ordinal information and is left out.
   - **Weight distribution.** Each draw picks one panellist at random with equal probability, then a weight vector uniformly from that panellist's region: the MOST criterion has the largest weight and the LEAST the smallest, the other three are unordered. Sampling: a uniform draw on the simplex, sorted; the largest value goes to MOST, the smallest to LEAST, the middle three to the other criteria in random order. This is exactly uniform on the region.
   - **Run.** 10,000 draws per scenario, seed 20261019, combined with the frozen matrix through TOPSIS as in A14, with the same matrix uncertainty (A9) and the SECC floor in S1 (A10a). Reported: rank acceptability indices, central weights, confidence factors.
   - **Sensitivity.** (i) Only scenario responses that pass A1. (ii) S1 without the floor. (iii) The matrix variants of A14 runs 3–5 (K9, K7, K11 directional), with the same rule: a conclusion that changes under K7 or K11 is reported as dependent on the edition or the cost assumption. (iv) Reference: weights uniform on the whole simplex (no preference information).
   - **P1–P4.** Examined against E-O1 first-rank acceptability with the A16 rules (indeterminate band of five points; P2 against 10 %; floor-excluded configurations count as 0). Reported as an *exploratory examination*, not as the tests specified in A16.
   - **Descriptive companion.** Counts of MOST and LEAST choices per criterion and scenario.
   - **Basis.** SMAA-2 provides for partial preference information (Lahdelma & Salminen, 2001); simulation-based SMAA represents it as a uniform distribution over the weights satisfying linear constraints (Tervonen et al., 2013, EJOR 224(3), 552–559).
   - **What it cannot show.** The ordinal region says nothing about how much more one criterion matters than another, so acceptabilities are wider than under elicited ratio weights. The equal weight given to each panellist and the uniform distribution inside each region are modelling choices, not data.
6. **Panellists' own corrections.** No recontact is made, but a correction that a panellist sends in writing is applied if it can be matched to one scenario response: it must give 1 to that response's MOST criterion in block 1 and to its LEAST criterion in block 2. The first submission is kept, A1 and A3 are re-run on the corrected vectors, and the E-C1 anchor stays the MOST choice of the first submission (amendment 1, point 3). This follows the Round 1 rule that a panellist's data are changed only on his own written statement (Stage 1 amendment 5).
   - One correction was received: R06, S1, Teams message of 19 October 2026 (`round2/corrections/`). The message names "Scenario 3", the third section of version B, which is S1; the corrected vectors match that section's MOST and LEAST choices and no other's.
   - Effect: R06's S1 response passes A1. A3 still flags it, so it is retained in the primary analysis and excluded in the sensitivity analysis.

Implemented in:
- `engine/engine/ordinal.py`, with tests in `engine/tests/test_ordinal.py` (E-O1);
- `round2/round2_import.py --corrections`, with tests in `round2/test_round2_import.py` (point 6).
- `round2/round2_analysis.py`, with tests on synthetic responses in `round2/test_round2_analysis.py`: the whole Round 2 analysis as amended. It takes the close date of Round 2 as a required argument, checks the frozen matrix against its hash, runs A14 (seed 20261014) only where a scenario has five valid responses, and runs E-O1 (seed 20261019) for every scenario. Written and tested before Round 2 closed; first run on real responses on 1 November 2026, with the close date 20 October 2026 (`round2/analysis/`).
