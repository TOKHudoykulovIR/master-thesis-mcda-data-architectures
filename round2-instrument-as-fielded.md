# Delphi Round 2 — the instrument as built

**Recorded** 7 October 2026; corrected the same day after an independent check against the screenshots. **Basis:**
- the author's preview screenshots of version C, taken on 4 October 2026: set 1 (13 images, before the profile was added) and set 2 (3 images, after the profile and the carbon-question subtitle were added, showing the opening page, the feedback page and the end of the first scenario section);
- the author's statement of the scenario order in all three versions (4 October 2026).

Corrections the author was asked to make after set 2 — removing a repeated sentence (§4), making P1–P3 required (§3), adding the subtitle to every (g) question (§5), removing names from titles (§2) — are **not seen in any screenshot**. On 7 October 2026 the author stated that all of them were made in all three versions before distribution. They are recorded below as the author's statement. Versions A and B were built after C; the author was advised to make them by duplicating C and moving the scenario sections ⟦unverified that this was done⟧. They were not seen in screenshots. They carry the set-2 changes only if they were made after those changes ⟦unverified⟧.

**Not for publication.** §1 pairs panellists' names with their codes. This file is a working record and stays out of the published thesis materials (§3.14: names are never published).

This file records what panellists saw. Where it differs from the build guide (`delphi-round2-msforms-build.md`) or from earlier plans, the difference is listed in §6. Anything not verified is marked ⟦unverified⟧.

---

## 1. Versions

*Section omitted from the public release.*

## 2. Opening page

**Title:** `Expert Panel — Round 2: Prioritising the criteria`. In set 1 the title of version C was "Expert Panel — Round 2: Prioritising the criteria (Yevhen, Ievgen)". By set 2 the names were removed from version C. The author states that no version was distributed with names in its title (7 Oct). A title with names would reveal two panellists to the others who received that version, contrary to the form's own statement that responses are anonymous to other panellists.

**Description:**
> Thank you for completing Round 1. This round is the core of the study: you will tell us how important each evaluation criterion is for three types of organisation. It needs no preparation.
> How your answers are used. Your responses are anonymous to other panellists and are reported only in aggregate. The researcher can see your name only in order to link your answers across rounds; names are never published. Anonymised responses will be archived with the thesis materials.

The opening page contains:
- **no consent item;**
- **no statement** that participation is voluntary or that a panellist may withdraw;
- **no statement of the expected duration.**

---

## 3. About you (profile)

Section description:
> A few questions about your experience. They let us describe the panel accurately and check whether priorities differ with experience.

| # | Question | Options | Type |
|---|---|---|---|
| P1 | Your current role | Data / Solution / Enterprise Architect · Lead or Principal Data Engineer · Head of Data, Data Platform or Analytics · Other (free text) | Single choice |
| P2 | Years of experience in data architecture or data platform engineering | Less than 3 years · 3 to less than 5 years · 5 to 10 years · More than 10 years | Single choice |
| P3 | Have you personally taken part in a decision to select a data platform or to migrate to one? | No · Yes, as a contributor to the evaluation · Yes, as the decision owner or co-owner | Single choice |

**Required status.** The 4 October screenshot showed P1–P3 as optional. The author states that they were made required in all three versions (7 Oct).

---

## 4. What Round 1 told us — and the five criteria (information only)

> **Six panellists took part. In brief:**
> • Five criteria met the relevance threshold and are kept.
> • Carbon intensity was rated of low relevance in general and is no longer part of the main comparison. One short question per scenario asks about it separately.
> • No new criterion reached the threshold for inclusion; operational reliability came closest.
> • Some of you named hybrid estates — a warehouse and a lakehouse used together — as missing. The hybrid option has been redefined accordingly.
> • All three scenarios passed the realism and emphasis checks and are unchanged. This time you will rate all three.

The hybrid bullet is quoted as it was meant to read after correction. The screenshots show two other states:
- **set 1:** "Several of you pointed out that hybrid estates — a warehouse and a lakehouse used together — are common." That was inaccurate: panellists named hybrid estates as missing, not as common;
- **set 2 (the latest seen):** the corrected wording, but with its last sentence repeated ("…as missing. The hybrid option has been redefined accordingly. The hybrid option has been redefined accordingly.").

The author states that the repetition was removed in all three versions before distribution (7 Oct). The set-1 wording was therefore not distributed.

> **5 CRITERIA** (AI readiness, Portability and Total cost of ownership sharpened using your Round 1 answers; the other two unchanged)
> **TTDP** — Time-to-data-product. The median elapsed time from a formalised request to a data product running in production — where "in production" means it is discoverable in the catalogue, has a stable access point, has declared quality checks, is documented, uses a standard interface, and has access control applied. Lower is better.
> **AIRD** — AI and GenAI readiness. How much of the AI lifecycle the platform supports natively, without separately integrated tools. Scored from 1 (tabular data only; machine learning runs outside the platform on exported data) to 5 (unstructured data, feature pipelines, model training and serving, and vector search are all native, and retrieval for GenAI respects the same access rules as the source data). Whether those access rules exist and can be audited is assessed under Security and compliance; this criterion assesses whether AI workloads can use the data where it lives. Higher is better.
> **PORT** — Portability and lock-in. How easily data and workloads can move to another engine or platform. Scored from 1 (proprietary formats and catalogue end to end; leaving means rewriting the pipelines and exporting all data) to 5 (open table format and open catalogue; several engines read and write the same data; leaving costs mainly operational effort). The one-off cost of a future exit belongs here; Total cost of ownership covers only the three-year running cost. Higher is better.
> **TCO** — Total cost of ownership. Total three-year cost of running the platform for a comparable workload: infrastructure, licences, and the people needed to operate it. It excludes the one-off cost of a future migration, which is part of Portability. Lower cost is better.
> **SECC** — Security and compliance. What the architecture can enforce and prove: isolation between tenants and domains, granularity of access control, completeness of audit trails, coverage of compliance mappings, and data residency and sovereignty options. Higher is better.

---

## 5. Each scenario section (repeated three times, in the version's order)

**Heading:** `Scenario k of 3 — <scenario name>`

**Description:** "Imagine you are advising this organisation on its data architecture." + vignette + "Answer the questions below for THIS organisation, not for your own current employer or client."

**Vignettes:** as in the build guide §5.3, with one difference. The S1 text reads "with 12K employees" where the guide reads "12,000 employees".

**Questions per scenario** (15 in total; on the form they are numbered continuously after P1–P3, so 45 scenario questions and 48 questions in all):

| Item | Text | Type |
|---|---|---|
| (a) | For this organisation, which criterion is the MOST important? | Single choice of the five criteria; required |
| (b) | For this organisation, which criterion is the LEAST important? | Same; required |
| (c) block heading | How much MORE important is your most important criterion than each criterion below? Give 1 to the criterion you chose as most important. Scale: 1 = equal · 3 = moderately more · 5 = strongly more · 7 = very strongly more · 9 = extremely more | Heading text, not a question |
| (c1)–(c5) | … than TTDP — Time-to-data-product / … than AIRD — AI and GenAI readiness / … than PORT — Portability and lock-in / … than TCO — Total cost of ownership / … than SECC — Security and compliance | Five Rating questions: 9 levels, numbers, end labels "Equal" and "Extremely more"; required |
| (d) block heading | How much MORE important is each criterion below than your least important criterion? Give 1 to the criterion you chose as least important. The value for your most important criterion should equal the value you gave your least important criterion in the block above. Scale: 1 = equal · 3 = moderately more · 5 = strongly more · 7 = very strongly more · 9 = extremely more | Heading text, not a question |
| (d1)–(d5) | TTDP — Time-to-data-product … than my least important / AIRD — AI readiness … / PORT — Portability … / TCO — Total cost of ownership … / SECC — Security and compliance … | Five Rating questions, as (c); required |
| (e) | What drove your ranking for this organisation? (optional, one or two sentences) | Text; optional |
| (f) | One more question about this organisation. Carbon intensity — the CO₂ emitted by the data platform per unit of work it delivers — was kept out of the main comparison after Round 1. For THIS organisation, how does it compare with the criterion you chose as MOST important? | Single choice: Carbon intensity matters less · Equally important · Carbon intensity matters more; required |
| (g) | By how much? — subtitle: If you chose "Equally important" above, select 1. Otherwise: 2 = slightly · 5 = strongly · 9 = extremely (less or more, as you chose above). | Rating, 9 levels, end labels "Equal" and "Extremely"; required; **no branching** (the rating is visible before any direction is chosen) |

*The subtitle of (g) is seen only in the first scenario section of version C (set 2, question 18). In set 1 the three (g) questions had no subtitle. The author states that it was added to all three (g) questions in all three versions (7 Oct).*

**Coding of (f)–(g)** (Stage 2 plan E-C1, revision of 7 Oct; `engine.exploratory.code_carbon_answer`). The direction answer decides:
- "less" with rating *k* ≥ 2 gives *a* = *k*;
- "more" with *k* ≥ 2 gives *a* = 1/*k*;
- "equally important" with 1 gives *a* = 1.

A rating of 1 with "less" or "more", or a rating above 1 with "equally important", is coded *a* = 1 and counted as inconsistent. The count is reported per scenario, with no recontact.

**Notes on the BWM items.**
- The form does not enforce the BWM structure. A panellist can rate the chosen best criterion above 1 in (c), or give different best-to-worst values in (c) and (d). These are the conditions checked by Stage 2 rule A1.
- Labels in block (d) are shortened for AIRD and PORT in version C as seen on 4 October. The criterion order is the same in (c) and (d).
- In set 1, items (c1)–(c5) of the **third section of version C (S2, High-growth start-up; questions 33–37)** showed 1 selected in every row. Block (d) of the same section and block (c) of the other two sections showed no selection, which points to clicks made in preview rather than a default value. ⟦unverified⟧

---

## 6. Differences from the build guide and earlier plans

| # | Planned (guide of 1 Oct; Stage 2 draft; Chapter 3 draft) | As built | Consequence |
|---|---|---|---|
| D1 | Consent item (Q1) with exit on "No" | **Removed** (author's decision) | No recorded consent in either round; Chapter 3 §3.14 corrected |
| D2 | Statement that participation is voluntary, right to withdraw (with a contact), ITPU/EPAM affiliation | **Not in the form** | All three declared in §3.14 |
| D3 | "It takes about 25 minutes" | **Removed from the form** | The form states no duration. The invitation text actually used was not recorded and is no longer available. The Round 1 questionnaire document told panellists that Round 2 would take "the same 45 minutes" ⟦whether the fielded Round 1 form said so is unverified⟧ |
| D4 | Profile Q2–Q9: role, experience, decision participation, number of decisions, platform types, operating models, clouds, industries | **Three questions** (P1–P3); number of decisions, platform types, operating models, clouds and industries left out (author's decision, 4 Oct) | A8 is still computable. The composition quotas and hands-on recency cannot be checked at all, and the industry concentration of the panel is unknown |
| D5 | Experience bands "Less than 3 · 3–4 · 5–10 · More than 10" | "Less than 3 years · 3 to less than 5 years · 5 to 10 years · More than 10 years" | Removes the gap between 4 and 5 years; the five-year threshold is unchanged |
| D6 | Two Likert grids per scenario (5 rows × 9 columns) | **Ten Rating questions** per scenario. The author found that the Likert question type would not take more than seven columns | Same information; each value is one numeric column in the export (confirmed by the test export, 7 Oct). The intermediate scale labels moved from the grid columns into the block heading. The (d) heading now reads "should equal the value … in the block above" (planned: "should match … in the previous question") |
| D7 | Carbon strength: choice 2–9, shown only after "less" or "more" (branching) | **Rating 1–9, always shown and required**, with the instruction to select 1 for "Equally important" | Inconsistent combinations are possible; coding rule fixed in Stage 2 E-C1 (revision of 7 Oct) |
| D8 | — | S1 vignette: "12K employees" | Wording only |
| D9 | Thank-you message (guide §7) | ⟦unverified⟧ | — |
| D10 | — | Set 1 showed a numbering typo in the first rationale question ("13. 14. What drove…"); not present in set 2 | None |
| D11 | Title without names | Names of the two version-C panellists in the title in set 1; removed before distribution in all versions (author's statement) | None, on the author's statement |

---

## 7. Export structure (from the author's test export of one version, 7 October 2026)

- **Layout.** One row per response, 54 columns:
  - six metadata columns: ID, start time, completion time, e-mail, name, last-modified time. Forms names these columns in the account's language (Russian here);
  - the three profile questions;
  - three blocks of 15 scenario questions, in the order the version presents them. Repeated question texts are distinguished only by a numeric suffix ("…2", "…3"). **The export does not name the scenario or the version**, so each file must be kept labelled with its version.
- **Values.** Ratings are exported as integers and choices as their option text.
- **Subtitle check.** In the version tested, all three (g) headers carry the subtitle about selecting 1. This confirms the author's statement in §5 for that version.
- **What the test exposed.** The form lets a respondent choose the same criterion as MOST and LEAST important. This led to Stage 2 amendment 1.
- **Fixture.** The header row, without answers, is kept as `round2/fixtures/export-headers.json` for the import tests.

