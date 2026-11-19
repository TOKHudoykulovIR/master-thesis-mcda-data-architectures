# Evidence pack — TCO (Total cost of ownership)

**Version** 1.0 · **Assembled** 26 September 2026 · **Coding kit** v1.1, passport M5 · **Register** `source-register.xlsx`

---

## 0. How to use this pack

Rules as in `pack-PORT.md` §0: no scores; tiers P / S / T, with T never carrying a cell alone; web quotations must be spot-checked; all accessed on 26 September 2026.

**Scale being coded (M5).** A relative cost class across the seven configurations for **one reference workload** over **3 years**, covering infrastructure, licensing **and operating personnel**. **5 = lowest cost class.**

| Level | Class |
|---|---|
| 1 | Top-quartile cost among the seven configurations |
| 2 | Above median |
| 3 | Median band |
| 4 | Below median |
| 5 | Bottom-quartile cost |

**Kit rules specific to TCO:**
- class assignment must cite **at least two independent published sources**;
- each source's inclusion or exclusion of **personnel cost** must be stated;
- vendor calculators are context only.

In the tables below, the column **"Personnel?"** records the second rule.

---

## 1. Findings that cut across cells — read before coding

### F1. The kit's hypothesis — cost moves from the invoice to payroll — is supported, but only by interested sources

| Source | Tier | Invoice | Personnel | Personnel? |
|---|---|---|---|---|
| #81 Tlemcani (SLR, 141 studies) | P | — | Indirect expenses such as engineering time and operational overhead "often dominate the direct line items" | Yes, argued, not quantified |
| Merced, Dremio (28 May 2026) | T (author works for a lakehouse vendor) | 10 TB example: storage "$300/month" proprietary vs "$230/month" open; interactive compute "$1,500/month" vs "$800/month (Dremio)" | Engineering overhead "~20 hrs/month" proprietary vs "~40 hrs/month" open; "Without automated compaction, snapshot expiration, and manifest rewriting, open Iceberg tables degrade in performance over time." | Yes |
| MotherDuck (upd. Aug 2026) | T (competing vendor) | — | "If a data engineer with a fully-loaded salary of $150,000 per year spends just four hours a week on warehouse administration, you are paying $15,000 annually"; example admin overhead "$1,250/month" Snowflake vs "$800/month" BigQuery | Yes |
| #105 Espinoza et al. | P | Total cost scored **DWH 80, DL 50, DLH 60** over five years (higher = more favourable), by a financial-sector organisation | Not separated | **No** |
| #104 Espinoza & Maryska | P | DWH rated most favourable on predictable licensing and infrastructure; "DL and DLH carry higher operational complexity and long-term cloud cost" (extraction note, p. 159) | "Skilled personnel" in discussion, not as a cost line | Partial |
| #131 Pamula (abstract) | P | "the cost of incremental data synchronization has been measured to be 95% less than the legacy architecture" — medallion lakehouse on Microsoft Fabric vs legacy warehouse design | Not stated | **No**; one cost component, and the comparison is against a *legacy* design |

**Reading.**
- The two independent academic sources (#104, #105) rate the **warehouse** as the more favourable on cost. They exclude personnel or do not separate it.
- The source reporting a large lakehouse saving (#131) measures one component against a legacy system.
- The only side-by-side figures including personnel (Merced) come from a lakehouse vendor's employee. They show a **lower invoice and double the engineering hours** for the open stack.

**For the coder.** No pair of **independent, disinterested** sources gives a C1 vs C2 class difference that includes personnel. Under the "two sources" rule this is at best a moderate-confidence judgement, and possibly `insufficient`.

**Update to the download list.** The kit's citation of #131 as "measured TCO reduction" **is supported by the abstract**, but only for one component against a legacy baseline. The full text is still useful, but the priority drops from High to Medium.

### F2. Operating-model cost: the expected gap is confirmed

No peer-reviewed or measured source quantifies how an operating model changes TCO on the same platform (kit Part 4 predicted this). Available sources are qualitative, or unsourced figures:

| Source | Tier | Content |
|---|---|---|
| Rollin, Medium (25 Jul 2023) | T | Cost drivers of mesh: "multiple cross-functional teams… data product owners, data product developers, data product testers"; "each data domain might run on separate hardware, potentially increasing overall hardware costs"; per-team monitoring; "Communication overhead might increase". Explicitly no figures |
| Promethium (1 Apr 2026) | T (vendor; **no sources cited**) | Mesh "$4.6M-$11.6M in year one for medium enterprises" vs fabric "$3.5M-$8.8M"; mesh "Phase two domain enablement requires 8-12 FTE platform plus 4-6 FTE per domain team" |
| #70 | P | Separate platforms per department: "When n datasets need to work with m analytical environments, this can create up to n × m replicas, leading to data inconsistencies and increased management costs." |
| G20 Thoughtworks (Jan 2026) | S | A model of "a centralized, cost-effective platform that handles tenancy so well that the value-driving components can be decentralized" |

**Consequence.** Row differences in TCO rest on **mechanism**:
- personnel per domain;
- duplicated infrastructure and replicas;
- coordination overhead;
- a shared platform amortised across domains (hub-and-spoke).

No independent quantification exists. Under the two-source rule, **C3–C6 cannot be class-assigned on quantified evidence**. The coder either assigns on mechanism with low confidence and records it, or codes `insufficient`. Both are legitimate under the kit: `insufficient` becomes midpoint 3 with a full-range uniform in SMAA.

### F3. Invoice-level platform differences look small; pricing models differ

- **Fivetran benchmark** (Dec 2022; TPC-DS 1 TB, untuned; Snowflake, BigQuery, Databricks, Redshift, Synapse): "these warehouses all have excellent price and performance". The managed lakehouse (Databricks) is in the same band as the warehouses at this scale.
- **Pricing mechanics differ:**
  - Snowflake bills credits "per-second billing (with a 60-second minimum each time the warehouse starts)", plus storage "based on a flat rate per terabyte (TB)" [N09a];
  - BigQuery charges on-demand "$6.25 / 1 tebibyte" processed, or slot-hours under editions [N09b];
  - the open stack pays cloud compute and object storage directly.
- Which is cheaper depends on the workload profile. This is why the kit requires **a single declared reference workload**, and why no reference workload has been declared yet (§4).

---

## 2. Sources in this pack

| ID | Source | Tier | Notes |
|---|---|---|---|
| #70 | Miyamoto & Kasuga (2025), Enterprise Data Science Platform | P | Abstract |
| #81 | Tlemcani et al. (2026), SLR | P | Full text on file |
| #102 | Kahn et al. (2022), Research DW migration to public cloud, JAMIA | P | Abstract; full text requested |
| #104, #105 | Espinoza et al. (2025) | P | Full texts on file; **product-level** scoring (MS SQL, Azure, Azure Databricks) |
| #131 | Pamula (2026), Medallion architecture on Microsoft Fabric | P | Abstract; full text requested |
| #46 | Mod (2026), multi-case | P | Abstract; "$12M+ per year in software licensing savings" in one case (telecom), baseline not stated |
| #68 | Gebler et al. (2025) | P | Abstract: data lakes "offer greater flexibility and cost-effective scalability" |
| G20 | Thoughtworks 2026 | S | See pack-TTDP |
| G26 | ardura.consulting, *Data Mesh vs Data Warehouse 2026* | T | In the MLR set; not re-fetched |
| N09a | Snowflake docs — Understanding overall cost · docs.snowflake.com/en/user-guide/cost-understanding-overall | T | Pricing mechanics |
| N09b | Google Cloud — BigQuery pricing · cloud.google.com/bigquery/pricing | T | Prices as of access date |
| N09c | Fivetran, *Cloud Data Warehouse Benchmark*, 19 Dec 2022 · fivetran.com/blog/warehouse-benchmark | S* | Published method; ingestion vendor, not a warehouse vendor; **Garousi appraisal pending** |
| N09d | MotherDuck, *The Data Warehouse TCO* (upd. Aug 2026) · motherduck.com/learn/data-warehouse-tco/ | T | Competing vendor |
| N09e | Merced, *Evaluating the TCO of an Open Lakehouse vs. Proprietary Data Warehouses*, 28 May 2026 · iceberglakehouse.com/posts/open-lakehouse-vs-proprietary-warehouse-tco/ | T | Author at a lakehouse vendor |
| N09f | Rollin, *The Brutal Cost of Data Mesh*, 25 Jul 2023 · medium.com/@hannes.rollin/the-brutal-cost-of-data-mesh-df8cec245506 | T | Qualitative |
| N09g | Promethium, *Data Fabric vs Data Mesh: Real Costs* (1 Apr 2026) · promethium.ai/guides/data-fabric-vs-data-mesh-architecture-comparison-2026/ | T | Vendor; figures unsourced |

---

## 3. Evidence by configuration

| Config | Invoice evidence | Personnel evidence | Row mechanism | Sources | Strength |
|---|---|---|---|---|---|
| **C1** DWH × central | Managed, consumption-priced; the academic sources rate the warehouse cost as most favourable or predictable (#104, #105) | Least administration among warehouses (BigQuery) to moderate (Snowflake) (N09d); lower than open stack (N09e) | One platform, one team, one cost centre | #104, #105, N09a–b, N09c, N09d, N09e | 2 P (product-level, personnel excluded) + T. **Moderate** on invoice, **weak** on personnel |
| **C2** LH × central | Lower storage/compute invoice in vendor examples (N09e); "higher operational complexity and long-term cloud cost" (#104); one component 95% lower vs legacy (#131) | ~2× engineering hours (N09e); maintenance (compaction, snapshot expiry) required | As C1 | #104, #105, #131, #81, N09e | Conflicting P; personnel from T only. **Weak–moderate** |
| **C3** DWH × hub | As C1, shared engine amortised across domains | Hub team + domain teams: no source | Chargeback per domain (profile) | G20 (mechanism) | **No quantified evidence** |
| **C4** LH × hub | As C2, shared platform amortised | Hub platform team + domain teams: no source | "centralized, cost-effective platform that handles tenancy" (G20) | G20 | **No quantified evidence** |
| **C5** DWH × federated | N accounts; replicas/sharing (#70 n×m replicas where platforms differ) | Per-domain roles (N09f); 4–6 FTE per domain (N09g, unsourced) | Duplication + coordination | #70, N09f, N09g | 1 P (mechanism) + T. **Insufficient for class** |
| **C6** LH × federated | Per-domain compute and storage; thin platform | As C5; plus the platform team | As C5 | #70, N09f, N09g | As C5 |
| **C7** fabric | Brownfield: existing platforms plus fabric layer | Fabric team "8-12 FTE… scaling to 15-25 FTE" (N09g, unsourced) | Additive layer | N09g | **T only** |

> **Update 1 Oct 2026 (kit K15).** C7 is redefined as *Hybrid / multi-platform*: lakehouse core plus warehouse serving layer, no fabric layer assumed. Quotations below about a fabric or metadata overlay apply only where such a layer exists; coders treat them as an upper bound for C7, not as its reference profile.

---

## 4. Implications for the coding kit (author decisions, not coding)

1. **Declare the reference workload now.** M5 requires it and it is not yet fixed. It is also needed for CARB. Suggested: *10 TB of managed data, mixed daily ELT plus interactive BI for ~100 analysts, 3-year horizon, one cloud region.* This matches the scale of the only side-by-side example (N09e) and is scenario-neutral. The author confirms or replaces it.
2. **Expect `insufficient` for C3–C6** (F2) unless the coder accepts a mechanism-based assignment. Decide in advance which rule applies, so that both coders apply the same one. **Recommendation:** code `insufficient` for rows without quantified evidence. The SMAA full-range treatment then shows whether the ranking depends on TCO at all, which is a result in itself.
3. **Record source interest.** Every quantified personnel figure comes from a vendor with an interest in the comparison. State this in Chapter 4 alongside the TCO values.
4. **Download list.** Move #131 from High to Medium (F1).

**Decision recorded (29 Sep 2026, kit K12):** the reference workload is **5 TB**, on the technical supervisor's advice, not the 10 TB suggested in §4.1. The other elements stand. N09e's figures are for 10 TB and are used for direction, not class.

**Decision recorded (26 Sep 2026, kit K11):** the author chose inheritance with a symmetric ±1 class uncertainty for rows over the `insufficient` midpoint rule recommended in §4.2, with a directional sensitivity run. The reference warehouse is Business Critical (kit K7), so its higher credit price enters the C1 invoice evidence.

## 5. Open items

- **N09c Fivetran** — Garousi appraisal; open the PDF for per-warehouse cost figures if C1 vs C2 is coded.
- **G26** — not re-fetched; optional.
- **#102 full text** — likely contains cloud cost disclosures for a warehouse migration (C1, a regulated context).
- **Spot-check** of web quotations.

## 6. Spot-check notes (17 October 2026)

All TCO quotations in the sample were found as quoted (Q13 N09e, Q16 N09g: Match). The check recorded two inconsistencies inside the sources themselves. Neither changes a coded cell, because C1 = C2 already rests on K11 (no two independent sources support a class difference).
- **N09e.** The page's lakehouse monthly total (~$3,230) adds up only with ~20 engineering hours, not the ~40 hours its table states. The "double the engineering hours" reading above rests on the table row; the page's own total does not carry it.
- **N09g.** "4-6 FTE per domain team" is the phase-two figure; the steady state given is 3-5 FTE per domain. The page's own range (12-30 FTE for 3-5 domains) does not follow from its components (8-12 + 3-5 × 4-6 = 20-42). The figure is unsourced, as recorded in §2.
