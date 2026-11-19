# Performance matrix — coding kit v1.3

*Supersedes Parts I and II of `round1-package-draft.md` (v0.3). Revised with the findings of the literature review and multivocal component. What changes here is how configurations are scored against the criteria. The definitions shown to the panel in Round 2 were sharpened after Round 1; the boundaries they state are fixed for coders in K17.*

**Status.** v1.3 (1 Oct 2026, after Delphi Round 1): amendments K1–K18 in Part 7 take precedence over the text of Parts 1–6 where they conflict. K7 and K11 were confirmed by the author on 26 Sep 2026; K12 was confirmed by the technical supervisor on 29 Sep 2026. No item is pending. Round 1 re-admitted no criterion; CARB was excluded from the weighting (K16) and C7 redefined (K15). To be frozen before coding begins and before the Stage 2 plan is fixed.

---

## Part 0 — What changed since v0.3, and why

Seven changes. Three of them alter the analysis plan and are carried into the Stage 2 registration.

| # | Change | Reason | Affects Stage 2? |
|---|---|---|---|
| 1 | **TTDP is coded as an anchored class from delivery determinants, not as median days from case studies** | The literature review found no study in 143 that measures elapsed time to a production data product, and the multivocal search found none in practitioner sources. The v0.3 procedure — median days from maturity-documented cases — has no data to run on. | Yes — scale and direction |
| 2 | **All anchored scales are oriented so that 5 is best** | v0.3 oriented TCO so that 5 = lowest cost, while the Stage 2 draft treated TCO as a cost criterion. Under that combination TOPSIS would have rewarded the most expensive configuration. One convention for all coded criteria removes the error. | Yes — criterion direction |
| 3 | **SECC acquires an admissibility floor in S1** | Two predecessors argue that security and compliance behave as gating conditions, and that compensatory aggregation can mask a fatal gap. Chapter 2 undertakes to address this; v0.3 and the Stage 2 draft did not. | Yes — new gating rule |
| 4 | PORT levels 4 and 5 distinguish read from write portability | The multivocal search found that some engines cannot write to external catalogs; multi-engine operation is broadly real for reads and not for writes. The v0.3 level 5 did not distinguish them. | No |
| 5 | CARB acquires an explicit rule for the operating-model axis | v0.3 said this axis was "coded from evidence" without stating how. The review found no evidence quantifying it. | No, but declared |
| 6 | C3 and C4 profiles use practitioner vocabulary and a hub-service inventory | Hub-and-spoke is a named, mature pattern in practitioner sources and nearly absent from academic ones. Profiles built without that vocabulary would read as unfamiliar to the panel. | No |
| 7 | C5 and C6 profiles record the platform-first dependency | Practitioner sources document domain teams stalled for months awaiting baseline platform capability. This is a property of federated configurations, not of any one implementation. | No |

---

## Part 1 — Coding conventions

**Orientation.** Every coded criterion is scored 1–5 with **5 the most favourable outcome** — lowest cost, fastest delivery, highest portability, strongest security, fullest AI support. CARB alone is carried as an estimated value *(K1: estimated, not measured)* in gCO₂e per functional unit, where lower is better. Consequently, in TOPSIS and PROMETHEE **CARB is the only cost-type criterion; the five coded criteria are benefit-type.**

**Unit of assessment.** A cell scores the **reference profile** in Part 3 — an ideal type — not a vendor's current product and not any particular organisation's deployment. Where evidence concerns a named product, the coder asks whether the finding follows from the architectural pattern or from that product's implementation, and uses it only in the first case.

**Evidence tiers.**

| Tier | What qualifies | May carry a cell alone? |
|---|---|---|
| Primary | Peer-reviewed study, open-standard specification ~~, own pilot measurement~~ *(withdrawn, K1)* | Yes |
| Secondary | Grey source scoring ≥4 on the Garousi appraisal and reporting measurement or documented first-hand experience | Yes, if two independent sources concur |
| Tertiary | Vendor documentation, grey source scoring 3, analyst assertion without disclosed method | **Never alone** |

**Anchor rule.** A level is assigned only when the evidence shows the **mechanism** the anchor describes, not a claim that the outcome is achieved. "Supports governed RAG" is a claim; "retrieval runs through the catalog's access policies" is a mechanism.

**When evidence is insufficient.** The coder records `insufficient` rather than a score. A cell recorded `insufficient` by both coders is resolved by the rule in Part 5, not by guessing.

---

## Part 2 — Metric passports v1.0

### M1 · Carbon intensity (CARB)

**Definition — unchanged.** SCI = ((E × I) + M) / R per ISO/IEC 21031; minimise; gCO₂e per R. Three candidate functional units R₁ per pipeline run, R₂ per terabyte processed per month, R₃ per data product served per month. The choice of R is an object of analysis.

*[Superseded by K1 — the pilot was dropped; platform values are estimated.]* **Platform axis — measured.** Instrumented pilot: one standardised workload on one warehouse engine and one lakehouse engine, same region and data volume, repeated runs. E from resource metrics through the Cloud Carbon Footprint coefficients; I from Electricity Maps for the pilot region; M from CCF embodied estimates. This yields a value for C1 (warehouse) and C2 (lakehouse) under each R.

**Operating-model axis — rule, new in v1.0.** No study in the corpus and no practitioner source found quantifies how an operating model changes the carbon intensity of the same platform. The mechanisms are known — storage replicated across domains, many small compute clusters rather than one large one, per-domain idle capacity — and their direction is not in doubt: federation adds overhead relative to centralisation. Their magnitude is not established anywhere. Therefore:

1. Coders code, per operating model, the **presence and extent of each duplication mechanism** in the reference profile: replicated storage (none / partial / full), compute fragmentation (single pool / per-domain pools / per-domain accounts), idle-capacity exposure (low / medium / high).
2. Each combination maps to an **overhead range** set from whatever quantitative evidence the evidence-pack search locates. If no source quantifies a mechanism, its range is a declared assumption, stated in the thesis as such.
3. CARB for C3–C6 is the platform value multiplied by the operating-model overhead. **The overhead is not a point value: SMAA samples uniformly across the range.**
4. If the ranges are assumptions rather than evidence, CARB comparisons **within** a platform column are reported as indeterminate. Comparisons **between** columns rest on the pilot and stand. *[K1: they now rest on the estimate and stand only if one column is lower in ≥ 80% of draws — Stage 2 plan A9.]*

**C7.** Platform value as an even mix of C1 and C2, plus a fabric overhead range for the metadata and virtualisation layer, sampled in SMAA. Declared as an assumption.

**If no sandbox access.** Platform values from published benchmark energy data at the engine class level; declared. *[K1: this is now the method.]*

### M2 · Time-to-data-product (TTDP) — revised

**Definition — unchanged, as shown to the panel.** Elapsed time from a formalised request to a data product in production meeting the six-property endpoint: discoverable, addressable, trustworthy, self-describing, interoperable, secure.

**Coding — revised.** Because elapsed time is not reported anywhere in the literature, the configuration is scored on the **architectural determinants of delivery time**, which are documented. Five determinants:

| Determinant | Faster | Slower |
|---|---|---|
| D1 Queue position | The team that needs the product builds it | Request enters a central team's backlog |
| D2 Hand-offs | Zero or one team boundary | Two or more (e.g. domain → central modelling → central BI) |
| D3 Provisioning | Self-serve templates provision storage, compute, CI and catalog entry | Tickets to a platform or infrastructure team |
| D4 Endpoint tooling | Catalog, contracts, quality checks and access policy applied by default | Each of the six properties assembled per product |
| D5 Platform dependency | Platform mature and shared | Each domain must first build or wait for baseline capability |

**Anchored scale, 5 = fastest:**

- **1** — Central queue *and* two or more hand-offs; manual provisioning; endpoint properties assembled per product; or domains blocked on missing baseline capability.
- **2** — Central queue with one hand-off, or domain ownership without self-serve provisioning.
- **3** — Either the queue or the hand-offs removed, but not both; partial templating; some endpoint properties by default.
- **4** — Domain builds its own product on self-serve provisioning; at most one hand-off; most endpoint properties by default.
- **5** — Level 4 with all six endpoint properties applied by default through platform tooling, and no dependency on capability the domain must build itself.

**Why this is defensible.** Each determinant is a documented cause of delay: the central bottleneck is the stated motivation of data mesh; platform-first failure is documented across practitioner sources; the endpoint properties are the ones the definition requires. What is lost is calibration to days. The thesis says so: TTDP is scored as a **class of expected delivery speed**, and no claim is made about absolute durations.

**Confound, declared.** Team maturity affects delivery at least as much as architecture does. The scale scores what the architecture makes possible for a competent team, not what a given team achieves.

### M3 · AI and GenAI readiness (AIRD) — anchors unchanged

Levels 1–5 as in v0.3. One clarification from the literature: level 5's "governed RAG" requires that retrieval from a vector store respects the same access policies as the governed source, which in practice means a vector index maintained from the governed store by change data capture with an explicit consistency boundary (Srivastava, 2026). A vector store populated by export does not meet level 5.

### M4 · Portability and lock-in (PORT) — levels 4 and 5 revised

Levels 1–3 as in v0.3.

- **4** — Open table format and open catalog; **multiple engines read the same data** through the catalog; documented exit paths exist.
- **5** — Level 4, **and multiple engines write** through the same open catalog, demonstrated; exit penalty limited to operational effort.

**Why.** Multi-engine operation is asymmetric in practice: some engines, including at least one major warehouse, cannot write to external catalogs, so a deployment may have one writer and several readers. Read portability is broadly demonstrated; write portability is not uniform. Level 5 requires the stronger condition.

### M5 · Total cost of ownership (TCO) — orientation restated

Definition and scale unchanged: relative cost class over three years for a reference workload, including operating personnel. **5 = lowest cost class.** Treated as a benefit-type criterion in the ranking methods, per Part 1.

Personnel cost is the component most often omitted in the literature and most likely to separate configurations: managed warehouses shift cost to the invoice, self-operated lakehouse stacks and federated models shift it to payroll. Class assignment must cite at least two independent sources, and must state whether personnel cost is included in each.

### M6 · Security and compliance (SECC) — gating rule added

Anchors unchanged. **New:** SECC functions both as a compensatory criterion and, in scenario S1, as an admissibility condition.

**Rule.** In S1, any configuration scoring **below 3** on SECC is excluded from the S1 ranking before TOPSIS, PROMETHEE and SMAA are applied. It remains in the S2 and S3 rankings. A sensitivity run without the floor is reported.

**Why 3.** Level 3 is the first at which fine-grained controls, centralised audit and major certification mappings are all present — the minimum a regulated institution under supervisory audit could defend. Below it, a configuration is not a trade-off the bank could accept at some price; it is not an option.

**Why only S1.** In S2 and S3 no regulatory obligation makes a security level non-negotiable; there, security is a genuine trade-off and remains compensatory.

---

## Part 3 — Reference profiles v1.0

Changes from v0.3 only; unchanged text is not repeated.

### C3 — Cloud warehouse × hub-and-spoke

**Vocabulary.** In practitioner sources this is the hub-and-spoke pattern on a warehouse platform: a central hub — also called a centre of excellence or platform team — owns the engine, standards, shared dimensions and tooling; domain spokes own their pipelines and data products inside the hub's guardrails.

**Hub services inventory.** Engine operation and capacity; CI/CD templates; shared conformed dimensions; catalog and lineage; access-control framework and audit; cross-domain regulatory processes, including subject-access and erasure requests.

**Rationale recorded in practice.** Full decentralisation presumes engineering capability most organisations lack; the hub concentrates the scarce skills while the spokes hold domain knowledge. Spokes are expected to take on more ownership as they mature.

### C4 — Open lakehouse × hub-and-spoke

**Vocabulary.** Practitioner sources distinguish two variants, both inside this cell. A *harmonized* mesh: autonomous domains on one shared platform with unified tooling. A *hub-and-spoke* mesh: the hub owns primary shared assets registered in the catalog, spokes operate independently day to day. The reference profile is the harmonized variant; the difference is recorded so that coders do not treat hub-owned shared assets as a departure from C4.

**Hub services inventory.** As C3, plus self-serve publishing to managed storage locations, open-catalog policy plane with domain stewards, data-contract tooling.

**Status of the "modal pattern" claim.** Supported by practitioner sources, which treat this as the standard pragmatic form; not supported by the academic corpus, which records it four times. The thesis states the claim with that attribution.

### C5 — Cloud warehouse × federated

**Addition.** Domains own separate warehouse accounts linked by the engine's native sharing. **Platform-first dependency:** a domain without an established account, pipelines and access model cannot deliver until it has built them; there is no hub to provide them. This affects D5 in TTDP.

### C6 — Open lakehouse × federated

**Addition.** As C5, the platform-first dependency applies: practitioner sources document domain teams stalled for months awaiting baseline platform capability where the thin self-serve platform was not in place first. The reference profile assumes the self-serve platform exists — otherwise the configuration is not the canonical mesh but its failure mode — and the coding notes record that this assumption carries the configuration's TTDP score.

### C1, C2, C7 — unchanged

---

## Part 4 — Evidence inventory

*Expected evidence strength per cell before pack assembly. S strong, M moderate, T thin, — none located. To be confirmed during assembly; a cell's final strength is recorded with its score.*

| | CARB | TTDP | AIRD | PORT | TCO | SECC |
|---|---|---|---|---|---|---|
| **C1** warehouse, central | ~~S *pilot*~~ T *estimated* | M | M | S | M | S |
| **C2** lakehouse, central | ~~S *pilot*~~ T *estimated* | M | S | S | M | M |
| **C3** warehouse, hub | T *derived* | M | M | S | T | M |
| **C4** lakehouse, hub | T *derived* | M | S | S | T | M |
| **C5** warehouse, federated | T *derived* | M | M | M | T | M |
| **C6** lakehouse, federated | T *derived* | M | S | S | T | M |
| **C7** hybrid / fabric | T *assumed* | T | M | M | T | M |

**Reading the table.** Evidence follows the grid's structure. Criteria driven by the platform — AIRD, PORT — are well evidenced down each column and differ little across rows. Criteria driven by the operating model — TTDP, the governance component of SECC — have their evidence in the practitioner literature on mesh and hub-and-spoke. **CARB and TCO are thin wherever the operating model matters**, because no source quantifies the overhead federation adds to either. Those two criteria will carry the widest uncertainty ranges into SMAA, and that should be expected rather than discovered.

### Known sources by criterion

Identifiers: corpus records by number from the reduced extraction; grey sources G01–G29 from the multivocal log.

**CARB.** ~~Own pilot (primary).~~ *(K1: benchmark-based estimate, `carb/`.)* Cloud Carbon Footprint methodology; Electricity Maps. G01 FootPrinter — workload-to-energy attribution, validated against measured traces. Corpus #127 green warehouse schema, #130 multicore query-processor energy, #134 CTMC data-lake energy — component level, usable for mechanism, not for configuration values. G03 on vendor data limitations.

**TTDP.** No source reports elapsed delivery time. Determinant evidence: Dehghani on the central bottleneck; G20–G25 on mesh adoption timescales and platform-first delays; G22 on data product lead time as an aspirational target; G05–G09 on hub services and the capability rationale; corpus #104–105 on implementation timeframe as a criterion.

**AIRD.** Armbrust et al. (2021); Srivastava (2026) on vector, RAG and CDC-maintained indexes; corpus #104–105 practitioner scores on analytics optimisation; corpus #23 semantic fidelity in ML pipelines; corpus #68 comparative evaluation of three architectures for AI research.

**PORT.** Specifications for Iceberg, Delta and Hudi; G11 Polaris; G12–G15 including the write-portability limitation in G14; corpus #1 format comparison, #15 Active Data Lakes, #64 Delta Sharing, #69 Iceberg multi-platform interoperability, #70 multi-engine federated access; Tlemcani et al. (2026) on vendor neutrality; Armbrust et al. on lock-in.

**TCO.** Corpus #131 measured TCO reduction; #104–105 practitioner cost scores; Tlemcani et al. on indirect costs dominating; G26 FinOps context. Personnel cost by operating model: not located — expected gap.

**SECC.** Corpus #61 Lakeguard, #142 Unity Catalog, #77 data residency, #30, #63, #87, #136 federated governance mechanisms, #51 Saxo Bank case; G05 hub-provided GDPR processes; G27–G29 erasure obligations and deletion complexity across distributed estates.

---

## Part 5 — Coding procedure

**Before coding.** Both coders read Parts 1–3 in full. They code three calibration cells together — one strong, one moderate, one thin — and discuss, then code the remaining cells independently. Calibration cells are excluded from the agreement statistic.

**Per cell, each coder records:**

| Field | Content |
|---|---|
| Cell | e.g. C4 × PORT |
| Score | 1–5, or `insufficient` |
| Anchor met | The level whose mechanism the evidence shows |
| Why not higher | The mechanism for the next level that the evidence does not show |
| Sources | Identifiers and tiers |
| Pattern or product | Whether the evidence concerns the architectural pattern or a named product's implementation |
| Confidence | High / medium / low |

**Example.**

| Field | Content |
|---|---|
| Cell | C4 × PORT |
| Score | 4 |
| Anchor met | Open format and open catalog; multiple engines read the same tables through the catalog |
| Why not higher | Multi-engine **write** through the open catalog is not uniformly supported; at least one major engine cannot write to external catalogs (G14) |
| Sources | Iceberg spec (P); G11 Polaris (P); corpus #69 (P); G14 (S) |
| Pattern or product | Pattern — the limitation is engine-side and applies to any open-catalog lakehouse |
| Confidence | High |

**Agreement.** Krippendorff's α (ordinal) per criterion, over non-calibration cells. Threshold 0.7. Below threshold: review the anchors for ambiguity, record the revision, both coders recode that criterion. Pre-resolution scores are kept for the SMAA sensitivity run.

**Cells both coders mark `insufficient`.** Scored at the midpoint 3 with the full range 1–5 carried into SMAA as uniform uncertainty, and listed in the thesis. This is preferable to a guessed value: it lets the analysis show whether the result depends on the missing evidence.

**Blinding.** Coders do not see the elicited weights until coding and the agreement statistic are complete.

---

## Part 6 — What this means for the Stage 2 analysis plan

Three edits to `analysis-plan/stage2-full-analysis-plan.md` (formerly the Stage 2 pre-registration) follow from Part 0 and are made there:

1. **A10:** CARB is the only cost-type criterion; TTDP and TCO are coded with 5 as best and treated as benefit-type.
2. **A10a (new):** the SECC admissibility floor in S1, with a sensitivity run without it.
3. **A9:** TTDP coded from delivery determinants; the CARB operating-model overhead as a sampled range; cells coded `insufficient` by both coders carried as full-range uncertainty.


---

## Part 7 — Amendments v1.1 (26 September 2026)

Decided by the author on 26 September 2026, before any cell was coded, on the evidence in `evidence/pack-PORT.md` and `evidence/pack-AIRD.md`. The v1.0 text is archived as `matrix-coding-kit-v1.0-archive.md`.

**K1 · CARB — no pilot (replaces M1 "Platform axis — measured").** The instrumented pilot is dropped. Platform values for C1 and C2 are **estimated** from published benchmark runs (runtime × instance type) using Cloud Carbon Footprint coefficients for energy and embodied emissions and Electricity Maps or provider data for grid intensity, for each functional unit R₁–R₃. Every assumption is tabulated in `carb-estimate` and each platform value is carried into SMAA as a range, not a point. "Own pilot measurement" is removed from the primary tier (Part 1). The M1 operating-model rule (overhead ranges) is unchanged. If the platform ranges overlap, CARB is reported as non-discriminating between columns.

**K2 · PORT level 5 (replaces the M4 "Why" paragraph).** Multi-engine write through one open REST catalog is demonstrated by several implementations as of 2026, including the reference warehouse in both directions (Snowflake: writes to external catalogs GA Oct 2025; external engines write to Snowflake-managed tables GA May 2026). What remains non-uniform is write access across catalog-ownership boundaries (foreign or shared tables) and table maintenance by non-owning engines. **Level 5 is met when multiple engines write through the estate's own open catalog, demonstrated in documentation or literature.** G14 is retained only as a dated source.

**K3 · C1/C3/C5 boundary kept.** The warehouse profiles remain defined on engine-native storage. The reference warehouse's ability to operate on open-format tables is coded as a documented **exit path** (M4 level-4 wording), not as the profile's storage model. The convergence of the platform axis is declared as a limitation in Chapter 4.

**K4 · AIRD level 5 unchanged, with a recorded expectation.** Level 5 requires the platform to enforce source policies on retrieval. Application-level filtering does not meet it. No reference implementation located in September 2026 does so natively; the level is therefore expected to be unattained, and that outcome is reported as a finding (a 2026 product gap), not corrected by loosening the anchor.

**K5 · Open-stack profiles include an ML layer (amends Part 3, C2/C4/C6).** The reference components of C2, C4 and C6 include an MLflow-class lifecycle layer (tracking, registry, serving) and a Feast-class feature store, open source and attached to the open catalog. Rationale: the warehouse profiles include the equivalents natively; omitting them would compare a product suite with a bare stack.

**K6 · Dating rule (adds to Part 1).** Where a primary source's factual claim about a product class is contradicted by current documentation of the reference implementation, the primary source is used for the **mechanism** it describes, not for the **current state** of the class. The coder records the conflict in the cell notes.

**Evidence inventory (amends Part 4), PORT and AIRD rows as found:** PORT — C3 none row-specific (was S), C7 thin (was M). AIRD — C3 and C5 none row-specific, C6 and C7 thin, level 5 unsupported everywhere. CARB — C1/C2 become *estimated* (was *pilot*).

**K7 · Warehouse edition (amends Part 3, C1/C3/C5/C7; decided 26 Sep 2026, replaces the earlier Enterprise default).** The reference warehouse is **Snowflake Business Critical** [N07o]. Rationale: (1) *capability parity* — the open-lakehouse profiles are credited with cloud-native customer-managed keys and private connectivity, so the warehouse is credited with its equivalents, which exist only from Business Critical upward (same principle as K5); (2) *scenario realism* — S1 is a bank handling card data, and only Business Critical supports PCI DSS data; (3) *consistency across criteria* — the same edition is used for SECC and TCO: Business Critical's higher credit price (~33% above Enterprise) is carried into the TCO class, so capability is not credited without its cost. Standard is excluded: without row and column policies the warehouse would fall below the S1 admissibility floor as an artefact of packaging. **Sensitivity (Stage 2 plan, A14):** SECC for C1, C3, C5 and C7 and TCO for C1 are coded a second time under **Enterprise** (5 extra cells; TCO rows are derived under K11), and all scenarios are re-run with that variant — the case of an organisation, such as S2, that would not buy the top tier.

---

## Part 7 (continued) — Amendments v1.2 (26 September 2026)

Decided on the evidence in `evidence/pack-SECC.md`, `pack-TTDP.md`, `pack-TCO.md` and `carb/carb-assumptions.md`, before any cell was coded.

**K8 · SECC and PORT are not independent (amends M4, M6).** Fine-grained row and column policies do not travel with open-format data: an engine receiving storage credentials must enforce them itself, and one managed catalog blocks external access to protected tables rather than enforcing on the external engine. The more engines may read and write (PORT level 5), the harder uniform policy becomes (SECC level 5). Coders score each criterion on its own anchors and do not adjust one for the other. The dependence is declared in Chapter 4 and examined after coding by the rank correlation of the two columns across configurations; if strongly negative, the SMAA discussion explains that weight on one partly offsets weight on the other.

**K9 · C6 sensitivity run (amends Part 3, C6).** The C6 reference profile assumes the self-serve platform exists. Because platform-first delay is the best-documented failure mode in the practitioner evidence (G20, G21, G10), a sensitivity run re-scores C6 on TTDP at **level 1** (anchor: "domains blocked on missing baseline capability"). Recorded in the Stage 2 analysis plan, A14.

**K10 · TTDP evidence carries an advocacy bias (amends M2).** Most evidence for determinants D1–D2 (central queue, hand-offs) comes from proponents of decentralisation; no counter-study measuring central-team delivery speed was located. This is declared with the TTDP values. A coder who scores C1 and C2 (or C3 and C4) differently on TTDP must cite a D3 or D4 source for the difference; the evidence located does not otherwise separate the platform columns on this criterion.

**K11 · TCO cells without quantified evidence (amends M5 and Part 5 for TCO; decided 26 Sep 2026).** *Platform columns:* C1 and C2 receive different TCO classes only if at least two independent sources, each stating whether personnel cost is included, support the difference; otherwise C1 = C2. *Rows (C3–C6):* each inherits its platform column's value — no operating-model cost effect is assumed in the primary analysis — and SMAA adds a symmetric shift drawn uniformly from −1 to +1 class, clipped to the scale. *C7:* the mean of C1 and C2, with the same ±1. *Why not the Part 5 midpoint rule:* against coded platform values, a midpoint of 3 would silently rank rows above or below their platform (e.g. C3 'dearer' than a C1 coded 4) — an ordering the evidence does not contain. *Why not a directional primary:* assuming federation dearer and hub cheaper would build the expected result of proposition P4 (hub-and-spoke wins) into the input that tests it. **Directional sensitivity (Stage 2 plan, A14):** federated rows shifted dearer by 0 to 2 classes, hub rows by −1 to +1, fabric dearer by 0 to 1; conclusions that differ between the primary and this run are reported as dependent on the cost assumption. Sources with a commercial interest in the comparison are flagged in the cell record whether or not they are used. *Expected consequence, stated in advance:* C1 and C2 evidence conflicts (academic sources favour the warehouse excluding personnel; vendor sources favour the lakehouse invoice but report roughly double engineering hours), so TCO is likely to be non-discriminating; in S2, where TCO weighs heavily, the ranking would then rest on the other criteria, and the thesis says so.

**K12 · Reference workload and region (amends M1, M5; confirmed 29 Sep 2026).** **5 TB of managed data**; daily batch ELT plus interactive BI for about 100 analysts; 3-year horizon; AWS eu-central-1 (Frankfurt). Used by the CARB estimate and as the frame for TCO classes. A change is a parameter change in `carb/carb_estimate.py` and a dated note here. **Volume — confirmed 29 Sep 2026:** the technical supervisor replied that "There is no typical/average configuration… volume isn't that critical… 5 Tb should be quite enough". This replaces the proposed 10 TB. The analyst count was not addressed and stays a declared assumption. Effect (`carb/carb-assumptions.md` v0.2, §6 R3b):
- the primary CARB model is linear in volume, so R₂ and the ranking are unchanged, and R₁ and R₃ are halved;
- a concurrency-sized provisioning floor, tested as a sensitivity, binds at 5 TB. It raises absolute values but keeps the order.

For TCO, the scale is below the only side-by-side cost example (N09e, 10 TB). The coder treats that example's figures as indicative of direction, not of class. **Region — confirmed 29 Sep 2026:** the technical supervisor judged that the choice of region "doesn't really matter for research purposes", noting that Frankfurt is popular for its broader service availability. AWS eu-central-1 is retained. This agrees with the provisional region check in `carb/carb-assumptions.md` §6: the grid factor rescales every configuration, and the order does not change.

**K13 · Evidence inventory, all criteria as found (replaces Part 4 table for coding purposes).**

| | CARB | TTDP | AIRD | PORT | TCO | SECC |
|---|---|---|---|---|---|---|
| **C1** | T *estimated* | M | M (T for current state) | S | conflicting → likely C1 = C2 (K11) | M (mechanisms T, two vendors; Business Critical, K7) |
| **C2** | T *estimated* | M | S (levels 1–4) | S | weak–moderate, conflicting | M |
| **C3** | *assumed overhead* | M | none row-specific | none row-specific | *inherits C1 ±1 (K11)* | M |
| **C4** | *assumed overhead* | M | M (3 P) | S (inherits C2) | *inherits C2 ±1 (K11)* | M |
| **C5** | *assumed overhead* | M (D5) | none row-specific | M | *inherits C1 ±1 (K11)* | M (pattern-level) |
| **C6** | *assumed overhead* | M (D5) | thin | S (inherits C2) | *inherits C2 ±1 (K11)* | M (design studies) |
| **C7** | *assumed overhead* | none | thin | thin | *mean of C1, C2 ±1 (K11)* | thin |

AIRD level 5 is unsupported in every row (K4). CARB within-column comparisons are indeterminate (K1).

**K14 · Coding scope and agreement (amends Part 5; 26 Sep 2026).** Coders score **30 primary cells**: PORT, AIRD, SECC and TTDP for C1–C7, and TCO for C1 and C2. CARB is estimated, not coded (K1), and TCO for C3–C7 is derived (K11). They also score **5 Enterprise-variant cells** (K7). The three calibration cells are C4×PORT (strong; it is also the worked example in Part 5, so it could not count toward agreement anyway), C3×TTDP (moderate) and C7×AIRD (thin). That leaves 6–7 units per criterion for Krippendorff's α, too few for a stable per-criterion estimate. The per-criterion α and its 0.70 threshold stand as specified. **A pooled α across all non-calibration cells is reported alongside as supplementary**, and the thesis states the small-sample limitation. Files: `matrix/coding-sheet-coder1.xlsx`, `coding-sheet-coder2.xlsx`; α is computed by `matrix/agreement.py`, verified against the worked example in Krippendorff (2011) (ordinal α = 0.815).

---

## Part 7 (continued) — Amendments v1.3 (1 October 2026, after Delphi Round 1)

Taken on the Round 1 results (`round1/round1-analysis-report.md`) before any cell was coded. v1.2 is archived as `_archive-2026-10-01/matrix-coding-kit-v1.2.md`.

**K15 · C7 redefined as *Hybrid / multi-platform* (replaces the C7 profile of v0.3; Stage 1 rule R7).** Three of six panellists named *hybrid / multi-platform* as a missing configuration. They described warehouse and lakehouse coexisting, and none of them mentioned a unifying fabric layer.

*Reference profile, coded:*
- an open lakehouse (Iceberg tables in an open REST catalog, Spark/Trino) and the reference warehouse (Snowflake Business Critical, K7) in one estate;
- the lakehouse holds the core data, and the warehouse serves curated data for BI, either by reading the lakehouse's open tables through the catalog or by holding loaded copies;
- governance runs through each platform's native controls, with a central platform team;
- a shared catalogue or fabric layer spanning both platforms **may exist but is not assumed**.

*Ideal-type boundary:* two platform paradigms in one estate. Remove either and the profile reduces to the C1 or C2 column.

*Scope of the definition.* The panel-facing definition also covers side-by-side estates, such as Snowflake and Databricks over separate data. Only the layered form is coded. The side-by-side form is declared as not separately coded (Stage 1 amendment 8).

*Coding consequences:*
- Coders score the profile without a fabric layer. Evidence on fabric overlays in the packs applies only as an upper bound and is so marked.
- TCO stays derived as the mean of C1 and C2 ±1 (K11).
- The CARB estimate keeps its half-and-half structure. Its A13 overhead is relabelled as coexistence overhead (copies between core and serving layer); the values are unchanged.
- C7 stays outside the grid for the rank-reversal test (Stage 2 A13).
- Where earlier text says "fabric" for C7 (M1 "fabric overhead", Part 4 table, K11 directional run "fabric dearer by 0 to 1"), read "hybrid (C7)"; the rules are unchanged.

**K16 · CARB after Round 1 (amends K1, M1).** Stage 1 rule R2 excluded CARB from the Round 2 criteria set (median relevance 2.5). The estimate in `carb/` is retained. It is used only in the exploratory carbon analyses of the Stage 2 plan, not in the primary matrix. CARB was never a coded criterion (K1), so coding scope (K14) is unchanged.

**K17 · Criterion boundaries (amends M3, M4, M5; Stage 1 rule R3).** The Round 2 definitions shown to the panel (report §6) state two boundaries. Coders apply the same ones:
- **PORT / TCO.** The one-off cost of a future exit or migration is scored only under PORT, in the migration-cost component of M4. TCO (M5) is the three-year running cost of the reference workload and excludes it.
- **AIRD / SECC.** SECC scores whether access policies exist, are enforced and can be audited across the estate. AIRD scores whether AI workloads, including GenAI retrieval, can use governed data natively. AIRD level 5 additionally requires retrieval to honour the source policies (K4). This is a capability of the AI path, not a second scoring of the policy regime.

**K18 · Agreement for TCO (amends K14).** TCO has two coded cells (C1, C2); rows C3–C7 are derived (K11). No per-criterion α is computed for TCO, and its two cells enter only the pooled α. The per-criterion α and the 0.70 threshold apply to PORT, AIRD, SECC and TTDP.
