# Analysis plan — Stage 1: Round 1 decision rules

> **Status (1 Oct 2026).** This plan was written before any Round 1 response was viewed. It was **not sent** to the supervisor, and no external time-stamp exists. The body below is unchanged from the version written before data collection (copy: `_archive-2026-10-01/stage1-round1-analysis-plan-as-written.md`), except that the bracketed dates are filled. Round 1 was analysed under these rules on 1 Oct 2026 (`round1/round1-analysis-report.md`); departures are listed under *Amendments* at the end.

**How this plan is fixed.** The plan is not publicly registered; the OSF registration originally intended was dropped by the author's decision. Instead, this file is sent by e-mail to the thesis supervisor **before** the data it governs are viewed. The date of that e-mail is the time-stamp. The file is not edited after sending; any later change is recorded as a dated amendment at the end of this document and reported in the thesis. A private, dated record is weaker evidence than a public registration, and the thesis says so.

---

## Title

Beyond Performance-Only Evaluation: an empirically grounded multi-criteria framework for selecting data architecture configurations — Stage 1 analysis plan: Delphi Round 1 decision rules

## Description

This is the first of two dated analysis plans for a master's thesis study (ITPU, in collaboration with EPAM) developing a multi-criteria decision framework for selecting between data architecture configurations, defined as combinations of platform paradigm (cloud warehouse, open lakehouse) and operating model (centralised, hub-and-spoke, federated).

A Delphi panel of practising data architects provides validation of the framework's building blocks (Round 1) and criteria weights (Round 2). **This plan fixes the rules by which Round 1 responses will be analysed and by which the criteria set, configuration set and scenarios will be frozen for Round 2.**

Round 1 was launched on **21 September 2026**. **At the date this plan is sent, no Round 1 responses have been viewed by the researcher.** A second plan, covering Round 2 elicitation, aggregation, ranking, robustness analysis and validation, will be sent after the Round 1 analysis and before Round 2 is launched.

## Hypotheses

Round 1 is a validation round and tests no hypothesis about the substantive framework. Two expectations are recorded here so that they can be reported as met or not met:

**E1.** A majority of respondents (>50%) will answer *Yes* or *Partly* to B3, which asks whether separating the platform choice from the operating model matches how such decisions are made in practice. This expectation is recorded because the literature review found the separation stated explicitly in practitioner sources.

**E2.** A majority of respondents (>50%) will answer *Yes* or *Partly* to B4, which asks whether the hub-and-spoke configurations represent the most common pattern in practice.

Neither expectation governs a design decision. Both are reported regardless of outcome.

---

## Design plan

**Study type.** Delphi consensus study, Round 1 of two (a conditional third round is specified in the Stage 2 plan).

**Instrument.** A questionnaire administered in Microsoft Forms with three parts:

- **Part A — criteria.** Six criteria (C1 carbon intensity, C2 time-to-data-product, C3 AI and GenAI readiness, C4 portability and lock-in exposure, C5 total cost of ownership, C6 security and compliance posture), each rated for *relevance* and *clarity* on a 1–5 scale; open questions A7 (missing criteria), A8 (overlapping criteria), A9 (dependence between criteria).
- **Part B — configurations.** Seven configurations; B1 coverage (Yes fully / Mostly / Partly / No), B2 missing or unrealistic configurations (open), B3 separation of platform and operating model (Yes / Partly / No), B4 realism of the hub-and-spoke row (Yes / Partly / No).
- **Part C — scenarios.** Three organisational vignettes (S1 regulated finance, S2 high-growth start-up, S3 sustainability-mandated enterprise), each rated for realism (Yes / Mostly / No) with up to three emphasised criteria selected; C4 missing context (open); a final question identifying the scenario closest to the respondent's own experience.

Candidate criteria held in reserve by the researcher were **not shown** to respondents, so that any mention in A7 is unprompted.

---

## Sampling plan

**Recruitment.** Panellists were identified by a recruiter within EPAM Systems against a written description: experienced data architecture or data platform engineers, with hands-on involvement with data platforms, available for two short questionnaires.

**Declared deviations from the study protocol.** Two, recorded here before any data were viewed:

1. **Panel composition.** The protocol specified at least 30% of panellists from outside EPAM. **All panellists are EPAM employees.** The panel's decision experience nonetheless spans multiple client organisations, since EPAM is a consultancy delivering platform work for external clients; this mitigates but does not remove the single-employer limitation, which is declared in the thesis.
2. **Selection criteria.** The protocol specified as decisive criterion personal participation in at least one real platform selection or migration decision, and a threshold of five years' experience. **The description used in recruitment did not include either.** Participants' experience will be established by a profile section at the start of Round 2 (see *Analysis plan*, rule R9).

**Target and minimum.** Target: 12–15 complete responses. **Minimum for analysis: 10.** If fewer than 10 complete responses have been received at the end of the field period, the period is extended once by seven days; analysis then proceeds with the responses available, and the shortfall is reported.

**Field period.** Ten to fourteen days from launch, with reminders on days 4 and 8.

---

## Variables

**Measured variables.** For each of C1–C6: relevance (1–5) and clarity (1–5). B1, B3, B4 and scenario realism as ordered categories. For each scenario, the set of criteria selected as emphasised. The scenario identified as closest to own experience. Open-text responses to A7, A8, A9, B2 and C4.

---

## Analysis plan

All rules are applied mechanically to the data. Every decision taken under them is reported with the underlying figures.

**R1 — Completeness.** A response missing more than 20% of the Part A rating items is excluded from the criterion statistics in R2 and R3, and retained for all other analyses. The number excluded is reported.

**R2 — Criterion retention, on relevance.** For each criterion, the median and interquartile range of relevance ratings are computed.

| Median | IQR | Decision |
|---|---|---|
| ≥ 4.0 | ≤ 1.0 | **Retained** |
| ≥ 4.0 | > 1.0 | Retained; flagged as contested and reported as such |
| 3.0 – 3.9 | any | Retained; definition reviewed before Round 2 |
| < 3.0 | any | **Excluded from Round 2** |

**R3 — Criterion wording, on clarity.** A criterion with median clarity below 4.0 has its definition revised before Round 2, using the comments given. Clarity never determines retention.

**R4 — Re-admission of candidate criteria.** Open responses to A7 are coded by the researcher against a construct list prepared before viewing responses: Governance Friction (effort and time to fulfil data-subject and regulatory requests), Cognitive Load and Talent Risk (skills required to operate the platform, availability of those skills), Data Contract and Quality Accountability, Data Sovereignty. Any construct not on the list is coded as new. A construct is **re-admitted** to the criteria set for Round 2 if it is named independently by **three or more respondents**. The total number of criteria in Round 2 may not exceed **eight**; if more than two constructs qualify, those with the most mentions are admitted and ties are broken by the researcher with the reasoning recorded. The coding of every A7 response is published.

**R5 — Overlap.** If three or more respondents identify the same pair of criteria as overlapping in A8, the means–ends relationship between that pair is re-examined and the outcome reported. This may lead to a definition being narrowed; it does not by itself remove a criterion.

**R6 — Dependence.** If three or more respondents identify the same pair as preferentially dependent in A9, this is reported as a threat to the additive aggregation model and carried into the threats to validity. It does not change the design.

**R7 — Configurations.** If fewer than 50% of respondents answer *Yes, fully* or *Mostly* to B1, the configuration set is reviewed before Round 2. A configuration named as missing in B2 by three or more respondents is considered for addition, with the decision and reasoning reported. B3 and B4 are reported as proportions against expectations E1 and E2 and do not change the design.

**R8 — Scenarios (manipulation check).** Each vignette was written to emphasise specific criteria: S1 — C6 security and compliance; S2 — C2 time-to-data-product and C3 AI readiness; S3 — C1 carbon intensity. A vignette **passes** if its intended criterion (for S2, either of the two) is among the emphasised criteria selected by **at least 60%** of respondents, **and** fewer than 30% rate it *No* on realism. A vignette that fails either condition is revised before Round 2 using the comments given, and the revision is reported.

**R9 — Sensitivity to panel qualification.** Because the recruitment description omitted the protocol's decisive criterion (see *Sampling plan*), a profile section at the start of Round 2 will ask each panellist whether they have personally participated in a platform selection or migration decision, in what role, and their years of experience. **Round 2 weights will be reported for the full panel and, separately, for the subgroup meeting the protocol's original criteria.** If the subgroup contains fewer than five panellists, the comparison is reported descriptively only. This analysis is registered now so that the treatment of the deviation is fixed before any weights are seen.

**R10 — Scenario assignment for Round 2.** Each panellist is assigned the scenario they identified as closest to their experience, plus a second scenario assigned round-robin so that each scenario is rated by as close to an equal number of panellists as possible, with a target of at least eight per scenario.

---

## Other

**Relationship to Stage 2.** The criteria set, configuration set and scenario texts resulting from R2–R8 will be reported in the Stage 2 plan, which will be sent before Round 2 launches and will reference this plan.

**Data.** Anonymised Round 1 responses and the A7 coding will be published with the thesis materials. Panellists are anonymous to one another; the researcher holds names to link responses across rounds.

**Sent to the supervisor on:** not sent (see status note at the top). **Round 1 responses first viewed:** 1 October 2026.

## Amendments

All dated 1 October 2026, recorded after Round 1 responses were viewed. Each is reported in the thesis.

1. **Plan not sent.** The plan was not e-mailed to the supervisor and will not be. It was written before Round 1 was launched (21 Sep), and no response was viewed before 1 Oct; no third party can verify either point. The thesis states this, and does not describe Stage 1 as pre-registered or externally dated.
2. **Sample and field period.** Seven submissions were received; one was the researcher's own test and is removed. **n = 6.** The field period ran from 21 Sep to 1 Oct 2026, ten days. The minimum of 10 was not reached, and the single seven-day extension required by *Sampling plan* was **not applied**, by the author's decision not to wait further. Analysis proceeds with six responses.
3. **Quartile definition (R2).** The plan did not fix one. Type 7 (linear interpolation; the R and NumPy default) is used. Type 6, type 8 and Tukey hinges are reported alongside. No retention decision depends on the choice. The *contested* flag for TTDP, TCO and SECC appears under type 6 and type 8 only, and arises solely from R05's ratings (amendment 5).
4. **Comment fields (R3).** The Forms build omitted the per-criterion and per-scenario comment fields. Definitions are revised under R3 using the open answers to A7–A9, B2 and the closing comment.
5. **Suspected scale reversal, R05 (data quality; no rule).** R05's **relevance** ratings correlate at ρ = −0.98 with the other panellists' medians; every other panellist is at +0.82 or above. His clarity ratings are constant (all 1). The primary analysis uses the data as recorded, and reversed and excluded treatments are reported. No retention decision differs between treatments; the PORT *contested* flag and the PORT R3 revision do.

   **Correction rule, fixed before R05 answers.** The data are corrected only if R05 confirms in writing that he read 1 as the highest. The correction then applies to all twelve Part A ratings, which share one grid and one scale. The as-recorded analysis is reported alongside.
6. **Carbon intensity (R2).** R2 excludes CARB from Round 2 (median relevance 2.5). The exclusion is applied: CARB is not in the Round 2 criteria set, the weighting or the primary ranking. **Addition:** in each Round 2 scenario, *after* the Best-Worst items, one exploratory question asks how carbon intensity compares with the panellist's most important criterion (BWM 1–9 scale, either direction). *Rationale:* R2 measures relevance in general. The framework weights criteria per context, and S3 was written around a carbon mandate, which 83% of panellists recognised in the R8 check. R8 shows only that the vignette carried its signal; it does not measure the weight carbon would receive. The question measures that weight without letting it enter the primary analysis. It is placed after the weighting so that it cannot influence it.
7. **Scenario assignment (R10).** With six panellists, the rule as written gives four raters per scenario against a target of eight. **Replaced:** every panellist rates all three scenarios. Order follows a 3 × 3 Latin square across three form versions (S1-S2-S3, S2-S3-S1, S3-S1-S2), two panellists each, so that each scenario appears in each position twice. A panellist is placed on the version opening with their closest scenario while that version has room. The closest-scenario answer is otherwise used only for description.

8. **C7 redefined (R7).** *Hybrid / multi-platform* appears in three B2 answers. Two call it missing, and the third names it without saying so, so the R7 threshold is met on a lenient reading and not on a strict one.
   - R7 foresees only adding a configuration. C7 was instead redefined, from *Hybrid / Data Fabric*, defined by a unifying overlay, to *Hybrid / multi-platform*, defined by the coexistence of a lakehouse and a warehouse with no overlay assumed.
   - In substance this replaces the configuration the panel saw in Round 1. The panel does not rate configurations in Round 2.
   - Reasoning: report §5; coded reference profile: kit K15.
9. **Definition change outside R3.** TCO (median clarity 4.0) receives one sentence excluding the one-off cost of a future migration, so that its boundary with the revised PORT reads the same from both sides. TTDP and SECC are shown unchanged.
