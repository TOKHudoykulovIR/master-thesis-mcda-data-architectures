# Coding scheme v2 — tightened definitions

*Supersedes the field definitions in `validation-instructions.md` and the starred-field guidance in `extraction-form.md` for the reduced extraction. Produced after the first validation round returned κ < 0.60 on seven of eleven fields.*

---

## Why v2 exists

The first validation compared LLM-assisted coding of 30 records against independent human coding. Three failure modes were diagnosed, and each is addressed below by a change to the definition rather than by asking coders to try harder.

**Failure 1 — inference where the abstract is silent.** In the Weights field the automated coder assigned `author` to records whose abstracts said only that a weighted method was applied. The human coder assigned `unclear`. Agreement 43%, κ = 0.25. The definition permitted inference; v2 forbids it.

**Failure 2 — two readings of "addresses a criterion".** TCO and PORT were coded by one coder when the criterion appeared as a substantive concern and by the other only when it was used as a dimension of evaluation. κ = 0.25 and 0.24. v2 fixes the stricter reading and states the test.

**Failure 3 — contribution versus topic in Type.** κ = 0.57, with disagreements concentrated on papers that survey literature in order to propose something, and on papers reporting one organisation's experience. v2 supplies a decision order.

Two fields passed and are unchanged: **AIRD** (κ = 1.00) and **SECC** (κ = 0.80). **Arch** at 0.73 is retained with one clarification. **CARB** and **TTDP** showed 97% and 90% agreement with unstable κ because the categories are rare; their definitions are tightened for precision, not because coders disagreed often.

---

## The governing rule

> **Code what the abstract states. Where the abstract does not state it, code the designated "not stated" value. Do not infer from what is likely, conventional in the field, or implied by the method used.**

This rule overrides every other consideration, including the appearance of an incomplete dataset. The counts of `unclear` and `n/a` are reported results in their own right: a corpus in which 40% of records do not disclose their weight source is a finding about the literature's reporting practices, not a gap in the extraction.

---

## Field definitions

### Type

Code the **form of the contribution**, not the subject matter. Apply the first rule that matches, in order:

1. Does the work report measurements, experiments, or systematically collected primary data? → `empirical`
2. Is performance evaluation the primary contribution? → `benchmark`
3. Does it propose or apply a decision method to a selection problem? → `method`
4. Does it propose an architecture, model, framework or methodology as its artefact? → `framework`
5. Does it report one organisation's implementation or experience, without proposing a general artefact? → `case study`
6. Does it survey a body of literature, tools or practice as its contribution? → `review`
7. Otherwise — discusses, defines or compares without artefact, data or survey → `conceptual`

*The ordering resolves the two known ambiguities.* A paper that reviews literature **in order to propose** a reference architecture reaches rule 4 before rule 6 → `framework`. A paper that describes one organisation's deployment **and** reports measurements from it reaches rule 1 first → `empirical`.

*Where a work is a framework demonstrated on a single case,* rule 4 applies — the case is a demonstration vehicle, not the contribution.

### Arch

Multiple values permitted, comma-separated: `DWH` · `LH` · `DL` · `MESH` · `FABRIC` · `CLOUD` · `DB` · `none`

**Test:** would removing this architecture from the paper change its contribution? If yes, code it. If it appears as background, motivation, or a single passing reference, do not.

*Clarification added in v2:* code `none` when the work addresses data management, governance or decision methods **without** a specific architectural object — for example a governance framework for Spark workloads that names no architecture, or a general MCDM method demonstrated on an abstract problem. `none` is a legitimate and expected value, not a failure to find something.

*`CLOUD` covers cloud services, providers, instances and platforms generally.* `DB` covers database engines and paradigms. A paper selecting among cloud providers is `CLOUD` even if one provider happens to offer a lakehouse.

### OpModel

`CENT` · `HUB` · `FED` · `n/a`

**Test:** does the abstract state something about **who owns, governs or is accountable for the data**?

- `FED` — domains, business units or organisations own their own data and platforms. Applies where the abstract describes decentralised ownership, domain-oriented ownership, or federated governance.
- `CENT` — a single team or unit owns the platform and all data products, stated as such.
- `HUB` — an explicit middle position: central platform provision with domain-owned products, or an explicit distinction between logical and physical decentralisation.
- `n/a` — the abstract says nothing about ownership or governance topology.

*Change in v2:* **naming data mesh is not sufficient for `FED`.** The abstract must say something about ownership, decentralisation or federated governance. A paper that mentions data mesh as context while studying, say, blockchain metadata catalogues is `n/a`. This resolves the disagreement on record 55, where mesh was the object of study but the abstract described readiness assessment rather than ownership.

*Expect `n/a` to dominate.* Roughly three-quarters of the corpus says nothing about operating models. That is itself the finding.

### The six criteria

For each, code `yes` or `no`.

> **Universal test, new in v2:** code `yes` only where the criterion functions as **a dimension on which something is evaluated, compared, measured or selected**. Code `no` where it appears as motivation, background, a design goal, or a property mentioned in passing.

The phrase to apply is *"is this criterion something the paper uses to judge between options, or to measure an outcome?"* — not *"does the paper care about this?"*

**CARB** — energy consumption, carbon, emissions or environmental impact.
`yes` where energy or emissions are measured, modelled, or used as a criterion.
`no` where sustainability motivates the work without being measured or evaluated.
*Boundary case, decided in v2:* a work that selects a storage technology **for** life-cycle assessment purposes is `no` — the carbon being assessed belongs to the products under study, not to the storage architecture. Record 119 is coded `no` on this rule.

**TTDP** — speed of delivering data products or capabilities.
`yes` for time-to-value, delivery agility, implementation timeframe, development cycle length, or ease of adoption framed as time.
`no` for query latency, processing speed, ingestion throughput or runtime performance. **These are system performance, not delivery time, and the distinction is the single most common error.**
*Boundary case, decided in v2:* "shortening the software development cycle" is `yes`. "Reducing query response time" is `no`.

**AIRD** — support for AI and ML workloads.
`yes` for ML lifecycle support, feature pipelines, vector search, embeddings, RAG, model training or serving, or AI-readiness as a platform property.
`no` where machine learning is a technique the authors use inside their own method — a paper applying K-means to cluster cloud instances is `no`.
*Unchanged from v1; this field achieved perfect agreement.*

**PORT** — ability to leave, substitute or operate across engines.
`yes` for vendor lock-in, open formats, portability, migration cost, exit cost, or interoperability **between query engines over the same data**.
`no` for interoperability between organisations, between clinical systems, between IoT devices, or semantic interoperability of data models. **These are a different sense of the word and were the main source of disagreement.**
*Test:* is the concern *"can I move or use something else?"* — or *"can these two systems talk to each other?"* Only the first is PORT.

**TCO** — cost as an evaluation dimension.
`yes` where cost, pricing, licensing, or economic return is **a criterion in the evaluation**, or where cost is measured or modelled.
`no` where cost appears as motivation ("cloud costs are rising"), as a claimed benefit of the proposed artefact ("our approach is cost-efficient"), or as a single contextual mention.
*Change in v2:* a paper claiming its own solution is cheaper is `no` unless cost is evaluated as a dimension. This was the main source of disagreement — the liberal reading coded a claimed benefit as a criterion.

**SECC** — security, compliance, governance, privacy, auditability, data residency.
`yes` where any of these is a substantive concern of the work.
*Unchanged from v1; this field reached κ = 0.80. Note that SECC remains deliberately broader than the other criteria, because governance is the dominant theme of the domain-side literature and the breadth is informative.*

### Method

`AHP` · `ANP` · `BWM` · `TOPSIS` · `PROMETHEE` · `ELECTRE` · `fuzzy-variant` · `weighted scoring` · `other` · `none` · `n/a`

**Decision order, new in v2:**

1. Does the work perform no multi-criteria decision procedure at all? → `none`. *This applies to most architecture papers and is the expected value.*
2. Is it a review, benchmark or tool description where a decision method would not apply? → `n/a`
3. Does it name a standard MCDA technique? → code that technique. Where several are combined, list them comma-separated, most central first.
4. Is the technique a fuzzy, neutrosophic, intuitionistic or grey variant of a named method? → code the base method **and** `fuzzy-variant`, e.g. `TOPSIS, fuzzy-variant`.
5. Is it a plain weighted sum with no MCDA technique? → `weighted scoring`
6. Is it a bespoke, metaheuristic, optimisation-based or otherwise non-standard multi-criteria procedure? → `other`

*Change in v2:* rule 4 replaces the v1 practice of coding either the base method or `fuzzy-variant` inconsistently. Both are now recorded, which preserves the methods inventory while keeping the base-method tally comparable.

*`none` versus `n/a`:* `none` means a decision could have been supported but was not; `n/a` means the question does not arise. A mesh reference architecture is `none`. A survey of data catalogue tools is `n/a`.

### Weights — *the field the gap claim rests on*

`author` · `single expert` · `panel(n)` · `panel (n unstated)` · `literature` · `equal` · `entropy/objective` · `user/consumer input` · `none` · `unclear` · `n/a`

**Decision order, new in v2 — apply strictly in sequence:**

1. Is no weighting performed anywhere in the work? → `none`
2. Is the work a review, benchmark or tool description? → `n/a`
3. **Does the abstract explicitly state where the weights came from?** If not → `unclear`. **Stop here. Do not proceed to the categories below on the basis of inference.**
4. If it does state a source, code it:
   - Authors assigned the weights themselves → `author`
   - One named expert or decision-maker → `single expert`
   - A group of experts **with the number stated** → `panel(n)`, writing the number
   - Experts, stakeholders or decision-makers as a group, **number not stated** → `panel (n unstated)`
   - Derived from prior literature → `literature`
   - All criteria weighted equally by construction → `equal`
   - Computed from the data by entropy, CRITIC or similar → `entropy/objective`
   - Derived from users, consumers, providers or reviews → `user/consumer input`

**Rule 3 is the change.** In v1 the automated coder reached rule 4 by inference; agreement was 43%. The instruction is now explicit: an abstract stating *"weights are assigned to each criterion"* without saying by whom is `unclear`, not `author`.

**Where both subjective and objective weights are combined** — as in an AHP-plus-entropy hybrid — code both, comma-separated, subjective first: `panel(3), entropy/objective`. In v1 this was coded inconsistently as one or the other.

*Why this matters.* The thesis claims that no prior work elicits weights from practitioners across organisations. That claim survives whether a record is `author` or `unclear` — neither reports a panel. But the reported breakdown must be accurate, and a `author` count inflated by inference would be indefensible if an examiner checked three abstracts at random.

---

## Recoding procedure

**Fields to recode across all 143 records:** Type, OpModel, TTDP, PORT, TCO, Method, Weights.

**Fields retained from v1:** AIRD, SECC, CARB, Arch. CARB is retained despite low κ because the single disagreement (record 119) is resolved by the boundary rule above; apply that rule to the eight CARB-positive records and adjust if needed.

**Order of work.** Recode field by field rather than record by record. Holding one definition in mind across 143 abstracts produces more consistent coding than switching between eleven definitions on each record — and it makes the pass through Weights, the most consequential field, a single focused session.

**Expected direction of change.** The `unclear` count in Weights should rise substantially and `author` should fall. The `yes` counts for TCO and PORT should fall as the stricter test is applied. If these do not move, the recoding has not been done differently from v1.

**Validation of v2.** Draw a **fresh** random sample of 30 records with a different seed — reusing the first sample would measure recall of the earlier exercise rather than agreement. Code independently, compute κ per field, and apply the same pre-specified thresholds: ≥0.75 accept, 0.60–0.75 review the responsible field, <0.60 recode manually.

**What goes in the protocol.** A dated amendment in Appendix C recording that the first validation returned κ below threshold on seven fields, that the scheme was revised as documented here, and that the corpus was recoded and revalidated. In the thesis, §2.2.6 describes the extraction procedure, the LLM assistance, both validation rounds and their κ values. An iteration that is documented is a strength; one that is concealed is a liability.

---

## Amendments after Round 2

Two provisions were added following the second validation round. Both are recorded here rather than silently folded into the definitions above, so that the sequence remains inspectable.

**A1 — the criteria test applies to all six criteria.** In the first recoding pass the strict test was applied to TCO, PORT and TTDP but not to AIRD and SECC, which had passed Round 1 and were therefore left untouched. This produced an internal inconsistency: three criteria on the strict reading, three on the loose one. Round 2 detected it — both fields fell from high to low agreement, not because coders disagreed about abstracts but because they were applying different definitions. AIRD and SECC were subsequently recoded on the strict test, falling from 31 to 12 and from 76 to 44 records respectively.

*The general lesson, worth stating in the thesis:* when a rule shared by several fields is revised, every field governed by it must be recoded, including fields that passed validation under the old rule. Passing validation under a superseded definition is not evidence of correctness under the new one.

**A2 — Weights is derivative of Method.** The two fields were coded independently, which permitted contradictory pairs. The rule:

| Method | Weights |
|---|---|
| `none` — no decision procedure applied | `none` — no weights exist |
| `n/a` — review, benchmark, tool description | `n/a` |
| any method applied, source disclosed | the disclosed source |
| any method applied, source not disclosed | `unclear` |

The final row is the one that matters. A method that ranks alternatives on multiple criteria necessarily involves weights, whether stated or implicit; an abstract's silence establishes non-disclosure, not absence. Three contradictory pairs in the automated coding were corrected under this rule.

## Residual disagreement after Round 2

Mean agreement across eleven fields is 83%. Four fields retain κ between 0.41 and 0.50 — PORT, TCO, SECC and Weights — with disagreements concentrated on abstracts where a criterion is mentioned but its status as an evaluation dimension is arguable. These are judgment calls on ambiguous source material rather than divergent application of the rules, and further tightening of the definitions would not resolve them without making the scheme arbitrary.

Three fields show high agreement with uninformative κ: CARB, TTDP and AIRD contain one or two positive cases in a sample of thirty, where a single disagreement collapses the coefficient while agreement stands at 87–97%. Percent agreement is the meaningful figure for these fields and κ is reported for completeness.

The findings Chapter 2 advances hold under both coders' assignments; residual disagreement affects coverage percentages by a few points and no substantive claim. See `validation-report.md`.
