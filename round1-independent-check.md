# Round 1 — record of the independent check

**Date** 1 October 2026 · **Checker** a separate LLM instance (a subagent with a fresh context), instructed to work read-only and to write its own code. **Not** a second human coder.

This file records what the check covered, what it found, and what was changed in response, so that Chapter 3 (§3.13) and the Round 1 report can cite it.

## What the checker was given

- The 22 result screenshots from Microsoft Forms.
- The transcription (`round1-responses.json`).
- The Stage 1 rules (`analysis-plan/stage1-round1-analysis-plan.md`).
- The Round 1 report, the Stage 2 plan, the Round 2 form document, the coding kit and the project README.

It was told not to import or run `round1_analysis.py`. It recomputed every rule with its own script before comparing its results with the report.

## What it found

**Transcription.** The checker compared every value in the 22 screenshots with the JSON and found **no mismatch**. The comparison covered:
- 72 Part A ratings;
- B1, B3 and B4;
- 18 realism answers;
- 18 emphasis lists;
- closest-scenario answers;
- all free text.

**Recomputation.** All figures and decisions matched the report:
- R1–R3 (medians, IQRs, decisions) under four quartile definitions;
- R05 treatments;
- R4–R6 counts;
- R7 shares;
- E1 and E2;
- R8 shares;
- the R10 closest-scenario counts;
- R05's Spearman ρ = −0.984;
- the Latin-square balance.

**Coding of open answers.** Two A7 codes were read differently:
- R02's reliability answer as *Data Contract and Quality Accountability*;
- R05's partner answer as a facet of portability.

Neither reading brings any construct to the R4 threshold.

**Points of interpretation and wording raised, and the response:**

| Raised | Response |
|---|---|
| R7 count is 3 only if R06's answer is counted as "missing"; strictly 2 | Both readings reported; C7 redefinition recorded as Stage 1 amendment 8 |
| R7 does not provide for redefining a configuration | Recorded as a deviation (amendment 8) |
| TCO definition changed although its clarity did not require it | Recorded as amendment 9 |
| TTDP and SECC definitions shortened in the Round 2 form | Restored to the Round 1 wording |
| AIRD, PORT, TCO wording differed between report and form | Made identical |
| R05 correlation stated for "Part A" ratings; holds for relevance only | Corrected; correction rule fixed before R05 answers (amendment 5) |
| "+0.98 when reversed" is not independent evidence | Removed as evidence |
| PORT *contested* flag depends on R05, yet was fed back to the panel | Removed from the Round 2 feedback |
| 83% in S3 is a manipulation check, not a valuation of carbon | Wording corrected in the report, amendment 6 and the Stage 2 plan |
| "Hybrid is the norm" and "panel concentrated in finance" unsupported | Withdrawn |
| "Rules applied as written" and "written before data collection" overstated | Corrected: written before launch (author's statement, 4 Oct), responses not viewed before 1 Oct; departures listed |
| Qualified-subgroup definition inconsistent; profile bands could not identify ≥ 5 years | A8 and the form's experience bands corrected |
| Ethics status not declared in the outputs | Declared in the report and the Stage 2 plan |
| Revised H3 had no specified test | Verdict rule stated in Stage 2 A7 |
| TCO per-criterion α not meaningful with two cells | Stage 2 A9 and kit K18 |

The checker's scratch scripts were kept in the session's scratch area. They were not kept with the thesis materials.
