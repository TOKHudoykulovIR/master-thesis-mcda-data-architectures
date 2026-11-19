# Delphi Round 1 — analysis report

**Date** 1 October 2026 · **Rules** `analysis-plan/stage1-round1-analysis-plan.md` (R1–R10) · **Data** `round1-responses.json` · **Computation** `round1_analysis.py` → `round1-results.json`, `round1-results.md`

*Revised 4 and 7 October 2026: R05 status corrected (§3.2); hybrid reading of R06 and the PORT–TCO pair qualified (§4, §5); §9 item 5 updated after the Round 2 profile was reduced.*

This report applies the Stage 1 rules to the Round 1 data and records every decision taken, with the figures behind it. Departures from the plan are listed in §2 and entered as dated amendments in the plan file.

---

## 1. Summary of decisions

| Item | Outcome | Rule |
|---|---|---|
| Responses analysed | **6** (7 submissions; 1 was the researcher's own test and is removed) | — |
| Criteria retained for Round 2 | **TTDP, AIRD, PORT, TCO, SECC** | R2 |
| Criterion excluded | **CARB** — median relevance 2.5 (< 3.0) | R2 |
| Criterion flagged as contested | PORT (median 4.0, IQR 1.5) — only with R05's ratings as recorded | R2 |
| Definitions revised | AIRD (median clarity 3.0), PORT (3.5) under R3; boundary sentence added to TCO outside R3 | R3, amendment 9 |
| Criteria re-admitted | None (highest count: operational reliability, 2 of the 3 required) | R4 |
| Overlap / dependence triggers | None (highest count: PORT–TCO, 2 in each question) | R5, R6 |
| Configuration set | Not reviewed (B1: 83% *Mostly*). **C7 redefined** after *hybrid / multi-platform* was named in B2 by 3 panellists (2 on a strict reading) | R7, amendment 8 |
| Vignettes | **All three pass** the manipulation check; none revised | R8 |
| Expectations | E1 met (100% *Yes* or *Partly*); E2 met (100%) | — |
| Round 2 assignment | **Amended:** all six panellists rate all three scenarios, in a balanced order | R10, amendment 7 |
| Carbon in Round 2 | Not in the criteria set. **One exploratory question per scenario**, asked after the weighting and outside it | R2, amendment 6 |

---

## 2. Field period, sample and status of the plan

**Field period.** Launched 21 September 2026, closed 1 October 2026 (10 days). The plan's minimum of 10 complete responses was not reached. The plan required a single seven-day extension in that case; **none was applied**, and analysis proceeds with the responses available.

**Sample.** Seven submissions were received. Form ID 1 was the researcher's own test and is removed. **n = 6**, all EPAM employees, all with complete Part A ratings. Open questions were optional, and 2–5 panellists answered each.

**Instrument as fielded.** The Microsoft Forms build omitted the free-text comment fields that the questionnaire document placed under each criterion, each scenario and B3/B4. R3 therefore revises definitions using the open answers to A7–A9, B2 and the closing comment. No per-criterion comments exist.

**Status of the plan.** The Stage 1 plan was written before Round 1 was launched, and no response was viewed before 1 October. It was **not sent** to the supervisor and will not be, so no external time-stamp exists. The thesis reports the rules as fixed by the author before the responses were viewed, without independent verification. The rules were applied as written except where amendments 2–9 record otherwise. The one rule whose outcome ran against the author's design — R2 excluding carbon intensity, the criterion the framework was built to foreground — was applied.

**Ethics.** Round 1 was run without formal ethics approval. The study specification had called for university ethics review, and the departure from it is declared. It is not a deviation from this plan.

**Deviations, entered as amendments 1–9 in the plan file:**

| # | Deviation | Effect on decisions |
|---|---|---|
| 1 | Plan not sent; no external time-stamp | None on the analysis; it weakens the pre-specification claim |
| 2 | n = 6 against a minimum of 10; the required extension not applied (author's decision not to wait) | Every decision rests on six responses; the 3-of-n thresholds in R4–R7 equal 50% of the panel |
| 3 | Quartile definition not fixed in the plan | Type 7 used. All common definitions are reported (§3); no retention decision depends on the choice |
| 4 | Comment fields omitted from the form | R3 uses the open answers only |
| 5 | One respondent's relevance ratings appear reversed (§3.2) | Primary analysis uses the data as recorded; no retention decision changes under either alternative; a correction rule is fixed in the amendment |
| 6 | Exploratory carbon question added to Round 2 | Outside the criteria set and after the weighting; enters no primary analysis |
| 7 | R10 replaced: all three scenarios for everyone, balanced order | 6 raters per scenario instead of 4; within-panellist comparisons become fully paired |
| 8 | C7 redefined rather than an eighth configuration added (§5) | Changes the profile coders score for C7; C1–C6 unaffected |
| 9 | TCO definition given a boundary sentence although its clarity (4.0) did not require revision | Wording only; aligns TCO with the revised PORT |

---

## 3. Part A — criteria (R1, R2, R3)

**R1.** All six responses are complete on Part A. None is excluded.

### 3.1 Results (data as recorded; quartiles type 7)

| Criterion | Relevance ratings | Median | IQR | R2 decision | Clarity median | R3 |
|---|---|---|---|---|---|---|
| CARB | 2, 1, 3, 5, 2, 3 | **2.5** | 1.0 | **Excluded from Round 2** | 3.0 | moot |
| TTDP | 5, 4, 5, 1, 5, 5 | 5.0 | 0.75 | Retained | 4.0 | — |
| AIRD | 4, 4, 4, 3, 5, 4 | 4.0 | 0.0 | Retained | **3.0** | **Revise** |
| PORT | 4, 2, 5, 2, 4, 4 | 4.0 | 1.5 | **Retained, contested** | **3.5** | **Revise** |
| TCO | 5, 4, 5, 1, 5, 5 | 5.0 | 0.75 | Retained | 4.0 | — |
| SECC | 5, 4, 5, 1, 5, 5 | 5.0 | 0.75 | Retained | 4.0 | — |

*Order of ratings: R02, R03, R04, R05, R06, R07.*

**Quartile definitions.** CARB is excluded and PORT is contested under all four definitions checked (type 7, type 6, type 8, Tukey hinges). Under type 6 and type 8, TTDP, TCO and SECC would also be flagged *contested*. That flag comes entirely from R05's ratings of 1, discussed in §3.2. Retention is unaffected.

### 3.2 Data-quality check — R05 (not a plan rule)

R05's relevance profile is almost the mirror image of the panel's:
- Spearman ρ between R05's relevance ratings and the other five panellists' medians is **−0.98**. Every other panellist correlates at +0.82 or above.
- R05 rated TTDP, cost and security "1 = not at all relevant", yet selected *Cost* and *Security & compliance* among the emphasised criteria in the scenarios, and TTDP in all three.
- R05's clarity ratings are 1 on every criterion. A constant clarity profile is not by itself unusual: R04 rated every criterion 4.

A reversed reading of the scale is the most likely explanation, but it is not certain. R05 had not been asked as of 4 October 2026 (an earlier version of this report said he had; that was wrong).

**Correction rule, fixed before his answer (amendment 5):**
- The data are corrected only if R05 confirms in writing that he read 1 as the highest.
- The correction then applies to all twelve Part A ratings, relevance and clarity alike, because they share one grid and one scale.
- The as-recorded analysis stays in the thesis alongside the corrected one.

| Treatment | CARB | TTDP | AIRD | PORT | TCO | SECC | Clarity revisions |
|---|---|---|---|---|---|---|---|
| As recorded (primary) | 2.5 · excluded | retained | retained | retained, **contested** | retained | retained | AIRD, PORT |
| R05 reversed | 2.0 · excluded | retained | retained | retained | retained | retained | AIRD |
| R05 excluded | 2.0 · excluded | retained | retained | retained | retained | retained | AIRD |

**What depends on R05:** only the *contested* flag on PORT and the R3 revision of PORT. If only the relevance ratings were reversed, PORT clarity would stay at 3.5 and still require revision. The PORT definition is revised in any case, because of the PORT–TCO boundary raised in A8/A9 (§4).

**R03 — a minor inconsistency.** R03 rated S1 unrealistic but chose it as the scenario closest to their own experience. Both answers are kept as given. Under the amended R10 the closest-scenario answer only sets the order of presentation.

### 3.3 Carbon intensity — what the data say

- **General relevance is low.** Five of six panellists rated it 1–3. The only 5 is R05's, which is probably reversed.
- **The S3 vignette carried its carbon signal.** Five of six (83%) selected carbon among the criteria the S3 vignette emphasises, more than any other criterion. In S1 and S2 nobody selected it. This is a manipulation check: it shows the vignette communicates its intended context. It does not measure how much weight practitioners would give carbon there, and the question did not ask for a ranking.
- **Practitioners notice the measurement problem.** R02's closing comment: "The criteria need operational measurement definitions for managed and serverless platforms, where energy and infrastructure metrics aren't exposed." This is the condition that made carbon an *estimated* criterion in this thesis (kit K1).

**Reading.** Panellists do not see carbon as weighing in the platform decisions they have experienced. Whether they would weigh it where a mandate exists is open: the S3 result shows only that they recognise the mandate in the text. R2 measures general relevance, so a criterion that could matter only in mandated contexts fails it. This is reported as a finding about current practice. It is not a reason to override the rule. The exploratory Round 2 question (amendment 6) measures what R8 cannot: the weight panellists give carbon in each context.

---

## 4. Open questions (R4, R5, R6)

Coding of every answer is in Appendix A.

**R4 — missing criteria (A7).** Constructs named:

| Construct | Status | A7 mentions | Also named elsewhere |
|---|---|---|---|
| Operational reliability (SLA, recovery, incident rate, pipeline success, freshness) | new | **2** (R02, R04) | — |
| Cognitive Load and Talent Risk | pre-listed | 1 (R02, secondary) | R03 in B2 |
| Platform-partner ecosystem | new | 1 (R05) | — |
| Organisational politics | new | 0 | R05 in B2 |

Re-admission requires three. **None is re-admitted**, including if mentions outside A7 were counted (maximum 2). Operational reliability is the nearest. It is reported as a candidate for future work and noted as partly a service-quality attribute, close to the performance criteria the thesis places outside its depth. R06's A7 answer is a proposed trade-off question, not a criterion.

**R5 — overlap (A8).**
- PORT–TCO: 2 (R04, R06).
- TTDP–TCO (people cost): 1.
- AIRD–SECC (governed catalogue access): 1.

Not triggered. The PORT–TCO overlap is real in the wording. PORT's definition included "the cost class of a migration", while TCO's did not say whether exit cost was in or out. Both definitions now state the boundary (§6).

**R6 — dependence (A9).**
- PORT–TCO: 2 (R04, R06).
- AIRD–SECC: 1.
- AIRD–TTDP: 1.

R02's "TTDP trades off against Security" describes a trade-off between performances, not preferential dependence, and is not counted. Not triggered. The PORT–TCO dependence ("portability matters more when long-term cost is high") is recorded in the threats to validity, because it is the one pair named in both questions by more than one panellist (AIRD–SECC was named in both by R02 alone).

---

## 5. Part B — configurations (R7) and expectations

| Question | Yes (fully) | Mostly | Partly | No | Share counted |
|---|---|---|---|---|---|
| B1 coverage | 0 | 5 | 1 | 0 | 83% fully or mostly → **no review** |
| B3 separation (E1) | 3 | — | 3 | 0 | 100% yes or partly → **E1 met** |
| B4 middle row (E2) | 3 | — | 3 | 0 | 100% yes or partly → **E2 met** |

Both expectations are met on the counting fixed in the plan. *Yes* alone is 50% in each case, and the thesis reports both shares.

**B2.** *Hybrid / multi-platform* appears in three answers:
- R02: "Missing: hybrid/multi-platform, i.e. a lakehouse as the core with a warehouse as the serving layer, or Snowflake and Databricks coexisting."
- R04: "The main missing configuration is a hybrid/multi-platform architecture… both warehouse and lakehouse technologies, sometimes across multiple cloud providers…"
- R06: "The main configurations which I saw previously is a hybrid architecture."

R02 and R04 call it missing. R06 names it in the *missing or wrong* field without saying *missing*. Counted as a mention, the R7 threshold of three is met; on a strict reading the count is two and R7 does not trigger. Both readings are reported.

**Decision (amendment 8): no new configuration; C7 redefined.** C7 already stood for warehouse and lakehouse coexisting. It was presented as *Hybrid / Data Fabric*, defined by a unifying metadata and governance layer. None of the three answers mentions such a layer. R02 and R04 describe the coexistence itself; R06's "hybrid" is unspecified (it could mean cloud and on-premises). The two specific answers suggest the label and the overlay requirement hid the option.

R7 foresees only *adding* a configuration. Changing an existing one is therefore a decision outside the rule, declared as a deviation. In substance it replaces the configuration the panel saw: a fabric overlay, whose boundary was the overlay itself. The new configuration is defined by the coexistence of two platforms.

- **Definition.** C7 is now *Hybrid / multi-platform*: an open lakehouse and a cloud warehouse in one estate, layered (lakehouse core, warehouse serving layer) or side by side. A shared catalogue or fabric layer may span them but is not assumed.
- **Coded reference profile (kit K15).** The layered form. It is the more specific of the two descriptions given, and the one the derived C7 values fit. The side-by-side form is covered by the definition but not coded separately; this is a limitation.

Adding an eighth configuration would duplicate C7's core and add cells with no evidence base. C7 stays outside the grid for the rank-reversal test. Its derived values are unaffected: TCO is the mean of C1 and C2 (K11), and CARB is half warehouse, half lakehouse. Multi-cloud (R04) is a different dimension from platform paradigm and stays out of scope.

---

## 6. Revised definitions for Round 2 (R3)

**AIRD — AI and GenAI readiness** *(revised; clarity 3.0)*
> How much of the AI lifecycle the platform supports natively, without separately integrated tools. Scored from 1 (tabular data only; machine learning runs outside the platform on exported data) to 5 (unstructured data, feature pipelines, model training and serving, and vector search are all native, and retrieval for GenAI respects the same access rules as the source data). Whether those access rules exist and can be audited is assessed under Security and compliance; this criterion assesses whether AI workloads can use the data where it lives. Higher is better.

**PORT — Portability and lock-in** *(revised; clarity 3.5, plus the PORT–TCO boundary)*
> How easily data and workloads can move to another engine or platform. Scored from 1 (proprietary formats and catalogue end to end; leaving means rewriting the pipelines and exporting all data) to 5 (open table format and open catalogue; several engines read and write the same data; leaving costs mainly operational effort). The one-off cost of a future exit belongs here; Total cost of ownership covers only the three-year running cost. Higher is better.

**TCO — Total cost of ownership** *(one sentence added; clarity 4.0, so R3 does not require it, but the boundary must read the same from both sides)*
> Total three-year cost of running the platform for a comparable workload: infrastructure, licences, and the people needed to operate it. It excludes the one-off cost of a future migration, which is part of Portability. Lower cost is better.

TTDP and SECC are unchanged and are shown to the panel in their Round 1 wording. The TCO sentence is a change outside R3 (amendment 9). These definitions are consistent with the anchored scales in the coding kit (M3; M4 as amended by K2); the kit records the boundaries in K17.

---

## 7. Part C — scenarios (R8, R10)

| Scenario | Intended criterion | Share selecting it | Realism: Yes / Mostly / No | No-share | R8 |
|---|---|---|---|---|---|
| S1 Regulated finance | SECC | **100%** | 4 / 1 / 1 | 17% | **Pass** |
| S2 High-growth start-up | TTDP or AIRD | **100%** (TTDP) | 3 / 3 / 0 | 0% | **Pass** |
| S3 Sustainability-mandated | CARB | **83%** | 1 / 4 / 1 | 17% | **Pass** |

**Emphasis profiles (share of panellists):**
- S1: SECC 100%, AIRD 83%, PORT 50%, TCO 50%, TTDP 17%, CARB 0%.
- S2: TTDP 100%, TCO 100%, AIRD 83%, PORT 17%, CARB 0%, SECC 0%.
- S3: CARB 83%, PORT 67%, TTDP 33%, SECC 33%, AIRD 17%, TCO 17%.

All three vignettes pass and are not revised. S3 is kept although its intended criterion is excluded from the weighting. Its second design signal — architectural longevity, carried by PORT — remains. The exploratory carbon question (amendment 6) is asked in every scenario, so the panel's view of carbon in S3 is still recorded.

**Missing contexts (C4).**
- A legacy-heavy enterprise in modernisation: 2 (R04, R06).
- A regulated scale-up: 1 (R02).

No rule applies. These are reported as limits to the scenario set. S1 already includes a migration under way, and S3 a history of costly migrations.

**R10 — assignment.** Closest scenario: S1 ×4, S2 ×1, S3 ×1. Under the rule as written, each panellist would rate their own scenario plus one other. That gives 4 raters per scenario against the target of 8, and only partial pairing between scenarios.

**Amended (amendment 7):**
- Every panellist rates **all three** scenarios.
- To keep order from being confounded with scenario, the form exists in three versions forming a Latin square, with two panellists each:
  - A: S1 → S2 → S3 (R03, R05);
  - B: S2 → S3 → S1 (R02, R06);
  - C: S3 → S1 → S2 (R04, R07).
- Each scenario appears in each position twice. Panellists whose closest scenario is S2 or S3 open with it. Four panellists chose S1, but only version A opens with it and it holds two, so two of them meet S1 second or third.

---

## 8. Consequences for Stage 2

- **Criteria set:** five benefit-type criteria; BWM over five.
- **H3** ("CARB weighs more in S3") **cannot be tested** in the primary analysis. It is replaced by a hypothesis on PORT, derived from the vignette's second design signal. An exploratory carbon analogue is reported.
- **CARB estimate:** retained for the exploratory analyses:
  - carbon weight from the extra question;
  - ranking with carbon added;
  - the carbon weight at which each scenario's first-ranked configuration would change.
- **Statistics at n = 6:**
  - the A7 permutation test becomes exact over (3!)⁶ = 46,656 within-panellist assignments;
  - A6 clustering can only form two clusters of three;
  - the R9 qualification subgroup is likely below five and therefore descriptive.

## 9. What Round 1 contributes beyond the rules

1. **Carbon: low general relevance.** Five of six rated it 3 or below for the decisions they have seen. The S3 vignette nonetheless made it salient (83% selected it there). How much weight it would carry in a mandated context is measured in Round 2 (exploratory). This bears directly on the literature-practice gap the thesis starts from.
2. **Hybrid estates were the configuration most often named as missing** (3 of 6, or 2 on a strict reading). Prevalence was not measured, and B4 (all *Yes* or *Partly* that hub-and-spoke is the most common pattern) does not suggest that single-platform configurations are rare.
3. **Operational reliability** is the leading unmet criterion (2 of 6).
4. **Portability is contested only if R05's ratings stand as recorded.** Two panellists tie its value to expected long-term cost.
5. **Four of six chose S1 as the scenario closest to their experience.** That was a forced choice among three stylised vignettes, and one of the four rated S1 unrealistic. Industry experience is not measured: the Round 2 profile was limited to role, experience and decision participation (author's decision, 4 Oct 2026). Nothing is said about concentration.

---

## Appendix A — coding of every open answer

| Q | Respondent | Answer (verbatim, abridged where marked) | Code |
|---|---|---|---|
| A7 | R02 | "Operational reliability/operability: pipeline success rate, freshness-SLA; secondarily skills/talent availability (time-to-hire for the stack)." | NEW: operational reliability; CLTR |
| A7 | R04 | "Reliability, resilience and operational robustness… availability/SLA, failure recovery time, recovery point/time objectives, incident frequency and the operational effort…" | NEW: operational reliability |
| A7 | R05 | "…the role of the service-provider partnership… the shape of any solution is largely determined by who the company chooses to partner with." | NEW: platform-partner ecosystem |
| A7 | R06 | "…Which improvement would matter more to your decision: A) a 30% lower three-year TCO, or B) a 30% shorter time-to-data-product?" | Not a criterion (proposed trade-off question) |
| A8 | R02 | "C2 and C5 on people cost; C3 and C6 on governed, machine-readable catalog access." | TTDP–TCO; AIRD–SECC |
| A8 | R04 | "…overlap between C5 (TCO) and C4 (Portability), because migration/exit costs are partly reflected in both…" | PORT–TCO |
| A8 | R06 | "…C4 and C5, because migration effort and proprietary dependencies can create future costs." | PORT–TCO |
| A9 | R02 | "AI readiness depends on Security…; Time-to-Data-Product trades off against Security." | AIRD–SECC (dependence); TTDP–SECC trade-off, not counted |
| A9 | R04 | "C3 (AI readiness) and C2 (Time-to-Data-Product) are somewhat dependent… C4 (Portability) can also become more important when the expected long-term cost… is high." | AIRD–TTDP; PORT–TCO |
| A9 | R06 | "…interaction between C4 and C5. Portability becomes more important when the expected long-term cost… is high…" | PORT–TCO |
| B2 | R02 | "Missing: hybrid/multi-platform, i.e. a lakehouse as the core with a warehouse as the serving layer, or Snowflake and Databricks coexisting." | Hybrid / multi-platform |
| B2 | R03 | "An additional criterion could [be] expertise of the available team or easiness of forming a team with the desired skills" | Not a configuration (CLTR) |
| B2 | R04 | "…hybrid/multi-platform architecture… both warehouse and lakehouse technologies, sometimes across multiple cloud providers…" | Hybrid / multi-platform |
| B2 | R05 | "I've worked for a project where politics [matters]." | Not a configuration (organisational politics) |
| B2 | R06 | "The main configurations which I saw previously is a hybrid architecture." | Hybrid / multi-platform (named; not stated as missing — strict reading excludes it) |
| C4 | R02 | "Regulated scale-up, e.g. healthtech/insurtech…" | Regulated scale-up |
| C4 | R04 | "…a large enterprise undergoing major cloud/data-platform modernization or migration…" | Legacy-heavy enterprise in modernisation |
| C4 | R06 | "…the typical big company: tight budget, lots of legacy systems, and no one dominant reason to change." | Legacy-heavy enterprise in modernisation |
| Other | R02 | "The criteria need operational measurement definitions for managed and serverless platforms, where energy and infrastructure metrics aren't exposed." | Measurement of CARB (supports K1) |
| Other | R06 | "The framework is clear and covers things architects usually leave unspoken. Its biggest plus is that it looks at long-term impact, not just speed and cost." | General endorsement |

The coding was drafted with LLM assistance and accepted by the author. A separate LLM instance re-derived it independently. It disagreed on two A7 codes: R02's reliability answer could be read as Data Contract and Quality Accountability, and R05's partner answer as a facet of portability. Neither reading brings any construct to three mentions. No second human coder was used; this is a limitation.
