# CARB estimate — assumptions, sources and results

**Version** 0.2 · 29 September 2026 · Script: `carb_estimate.py` (seed 20260926, 10,000 Monte Carlo draws) · Outputs: `carb-results.csv`, `carb-summary.json`, `carb-draws.npz` (joint draws: `R1`, `R2`, `R3` primary; `R2_floor` for the provisioning-floor sensitivity run). Version 0.1 (26 Sep, 10 TB) is in `_archive-2026-09-26/`.

**Status after Delphi Round 1 (1 Oct 2026).** The panel rated carbon intensity low in general relevance (median 2.5 of 5), and Stage 1 rule R2 excluded it from the Round 2 weighting. The estimate is therefore used **only in the exploratory carbon analyses** of the Stage 2 plan, not in the primary ranking (kit K16). Workload scale and region are **confirmed** by the technical supervisor (29 Sep 2026). The script and this table are fixed by the author when the Stage 2 analysis plan is fixed (the plan is not sent; §3.11.1). Any later change is a dated amendment.

**Method.** Software Carbon Intensity (ISO/IEC 21031): **SCI = (E·I + M) / R**. There is no measurement (kit K1). Platform values are estimated from published benchmark runs using Cloud Carbon Footprint (CCF) coefficients. Each uncertain input is a uniform range, so every output is a distribution. SMAA receives the distribution, not a point value.

---

## 1. Parameters

| ID | Parameter | Value | Basis |
|---|---|---|---|
| P1 | Managed data volume | **5 TB** | **Confirmed 29 Sep 2026** by the technical supervisor: "There is no typical/average configuration. My recommendation: volume isn't that critical. You can lower the total bandwidth for the sake of variability. 5 Tb should be quite enough." Replaces the proposed 10 TB |
| P2 | Horizon | 3 years | Kit M5 |
| P3 | Region | AWS eu-central-1 (Frankfurt) | **Confirmed 29 Sep 2026** by the technical supervisor ("doesn't really matter for research purposes"; Frankfurt is common for service availability) |
| P4 | Data products (for R₃) | 20 | Assumption; identical for all configurations |
| P5 | Users | Daily batch ELT plus interactive BI for about 100 analysts | Assumption from the proposal; the technical supervisor did not comment on it. It matters only in the provisioning-floor run (§6, R3b) |
| A1 | Daily work | 20–60 % of managed data per day, in TPC-DS power-run TB-equivalents (1–3 TB-eq at 5 TB) | Assumption. Does **not** cancel in R₂: storage is a fixed daily amount divided by the day's work (correction of 4 Oct 2026, §6 R3c) |
| A2 | ELT share of daily work (R₁) | 30–60 % | Assumption |

## 2. Coefficients

| ID | Coefficient | Value | Source |
|---|---|---|---|
| CCF-1 | CPU power per vCPU, AWS | min 0.74 W, max 3.5 W | CCF methodology [S-CCF] |
| A3 | CPU utilisation during runs | 30–80 % | CCF default is 50 %; range is an assumption |
| CCF-2 | Memory energy | 0.000392 kWh per GB-hour | [S-CCF] |
| CCF-3 | Object storage (HDD) | 0.65 Wh per TB-hour | [S-CCF] |
| A4 | Object-storage replication | ×3 | Assumption (multi-AZ storage); CCF keeps its factors in a separate spreadsheet not retrieved |
| CCF-4 | PUE, AWS | 1.135 | [S-CCF] |
| CCF-5 / A5 | Grid intensity, eu-central-1 | 320–420 g CO₂e/kWh (CCF uses EEA 368) | [S-CCF]; range assumed for year-to-year variation |
| A6 | Embodied, per vCPU-hour | 0.3–1.0 g | Derived from CCF method M = TE·(TR/EL)·(RR/TR), EL = 4 years [S-CCF-E], with TE 1.5–3 t CO₂e per ~96-vCPU server — **assumption; BoaviztAPI not queried** |
| A7 | Embodied, per GB RAM-hour | 0.005–0.02 g | Assumption |

## 3. Platform efficiency — the core input

| Platform | Benchmark | Configuration | Runtime | Source |
|---|---|---|---|---|
| **Cloud DWH (Snowflake)** | TPC-DS 100 TB, power run | 4XL = 128 nodes × 8 vCPU × 16 GB (estimate) | **3,760 s** (Snowflake-reported, pre-clustered data) to **7,276 s** (Databricks-measured on the official dataset) | [S-SF] [S-DB] [S-SEL] |
| **Open lakehouse (Spark + Iceberg on S3)** | TPC-DS 3 TB | 9 × r5d.4xlarge = 144 vCPU, 1,152 GB | **1,535.6 s** (EMR 7.5 optimised runtime) to **5,546.2 s** (open-source Spark 3.5.3 + Iceberg 1.6.1) | [S-EMR] |

**The warehouse range is itself a vendor dispute.** Snowflake reports 3,760 s; Databricks, re-running on the official dataset, reports that it "took 1.9x longer". Both ends are used.

**Snowflake hardware is not disclosed.** The 8-vCPU / 16-GB node is a practitioner estimate: *"Each node has 8 cores/threads, regardless of cloud provider"*; on AWS each node *"is a c5d.2xlarge EC2 instance"* [S-SEL, T tier]. Sensitivity S5 doubles it.

| ID | Adjustment | Value | Basis |
|---|---|---|---|
| A8 | Cross-scale normalisation (100 TB vs 3 TB runs) | ×0.8–1.25, applied to each platform independently | Assumption |
| A9 | Production idle / over-provisioning vs benchmark | Warehouse ×1.05–1.30 (auto-suspend, per-second billing with 60 s minimum [N09a]); lakehouse ×1.20–2.00 (always-on interactive cluster plus ephemeral Spark jobs) | Assumption |
| A10 | Storage retention (Time Travel/Fail-safe; Iceberg snapshots) | ×1.0–1.3, both platforms | Assumption |

## 4. Operating-model overhead (kit M1 rule — declared assumptions, no source quantifies them)

| ID | Operating model | Compute | Storage |
|---|---|---|---|
| — | Centralised (C1, C2) | ×1.00 | ×1.00 |
| A11 | Hub-and-spoke (C3, C4) | ×1.00–1.15 | ×1.00–1.10 |
| A12 | Federated (C5, C6) | ×1.10–1.50 | ×1.00–1.30 |
| A13 | Hybrid / multi-platform (C7): half warehouse + half lakehouse, plus coexistence overhead (copies between lakehouse core and warehouse serving layer; relabelled 1 Oct 2026 under kit K15, values unchanged) | ×1.05–1.20 | ×1.10–1.40 |

## 4a. Provisioning floor — sensitivity only (added in v0.2)

The primary model scales compute with the amount of work. A BI engine is in practice sized for **concurrency**, not for data volume, so at small volumes a fixed floor can dominate. The floor model tests this. It is not part of the primary estimate.

| ID | Assumption | Value | Basis |
|---|---|---|---|
| F1 | Floor capacity | 2–4 nodes × 8 vCPU (16–32 vCPU). Equal for every configuration within a draw. Memory at each platform's baseline ratio: warehouse 2 GB/vCPU, lakehouse 8 GB/vCPU | Assumption, sized for ~100 analysts (P5); **no source** |
| F2 | Active hours of the floor | Warehouse: 8–12 h on working days (auto-suspend). Lakehouse: S7a always on (24 h × 7 d); S7b as the warehouse; floor-model draws `R2_floor`: uniform between the two | Assumption; **no source** |
| — | Structure | ELT stays work-proportional. The BI share of compute becomes max(work-proportional, floor). Operating-model and fabric multipliers apply to the floor as to compute | — |

---

## 5. Results — primary model (median, 5th–95th percentile; 5 TB, Frankfurt)

| Config | R₁ g per daily pipeline run | R₂ g per TB-equivalent processed | R₃ g per data product per month |
|---|---|---|---|
| C1 DWH × central | 144 (116–182) | **95 (67–144)** | 274 (210–373) |
| C2 LH × central | 299 (179–539) | **286 (160–458)** | 809 (420–1,527) |
| C3 DWH × hub | 153 (122–193) | 100 (70–153) | 290 (221–396) |
| C4 LH × hub | 319 (190–580) | 305 (170–493) | 862 (445–1,643) |
| C5 DWH × federated | 170 (132–222) | 115 (80–173) | 331 (244–460) |
| C6 LH × federated | 371 (215–692) | 360 (197–597) | 1,016 (514–1,982) |
| C7 hybrid / multi-platform | 264 (183–415) | 224 (142–333) | 631 (387–1,066) |

Compared with v0.1 (10 TB), R₂ is **identical** and R₁ and R₃ are **halved**. The reason is in §6, R3b.

Absolute values depend on A1 and on the idle model, and should not be quoted as footprints. **Only the relative position is meaningful.**

## 6. What the estimate shows — and what it does not

**R1 · Platform axis.** Under the baseline assumptions the warehouse column is lower-carbon: P(C1 < C2) = 1.00 on R₂. **The direction is not robust** to plausible combinations of assumptions:

| Scenario (lakehouse side unless stated) | P(C1 < C2) | Column lower in ≥ 80 % of draws |
|---|---|---|
| Baseline: memory-optimised r5d nodes, lakehouse idle 1.2–2.0, open-source-to-EMR runtime range | 1.00 | warehouse |
| S1 Compute-optimised lakehouse nodes (2 GB/vCPU, as Snowflake) | 1.00 | warehouse |
| S2 Lakehouse idle equal to warehouse | 1.00 | warehouse |
| S3 S1 + S2 | 0.99 | warehouse |
| S4 S3 + optimised engine only (EMR 7.5 runtime) | 0.82 | warehouse (barely) |
| S5 Snowflake nodes 2× larger than the estimate | 0.995 | warehouse |
| **S6 S4 + S5** | **0.08** | **lakehouse — the order reverses** |
| S7a Provisioning floor; lakehouse engine always on | 1.00 | warehouse |
| S7b Provisioning floor; both engines suspend outside working hours | 1.00 | warehouse |
| **S7c S7b + S6 assumptions** | **0.15** | **lakehouse** — but medians differ by only ~5 % (257 vs 245) |

**Reading.** The warehouse comes out ahead through three effects:
- the vendor's efficient engine;
- smaller memory per vCPU;
- auto-suspend.

A carefully engineered lakehouse, using compute-optimised nodes, no idle clusters and an optimised Spark runtime, closes most of the gap. Against a larger-than-estimated Snowflake node it overtakes the warehouse. The platform difference in CARB therefore depends on **how well the lakehouse is operated** and on **undisclosed warehouse hardware**, more than on the architecture class. This is a finding in its own right, and consistent with G03 on the limits of vendor data.

**Against the Stage 2 decision rule** (A9: CARB is non-discriminating between platform columns only if neither column is lower in at least 80 % of draws), every scenario is discriminating. What changes is the **direction**: warehouse lower in the baseline and S1–S5, S7a and S7b; lakehouse lower in S6 and S7c.

*Correction to v0.1.* Version 0.1 said that S6 would count as non-discriminating. That was wrong: under S6 the lakehouse column is lower in 92 % of draws, so the rule counts it as discriminating in the opposite direction.

*Observation on the rule.* The 80 % rule is a probability criterion with no magnitude condition. Under S7c it would call a ~5 % median difference discriminating, because the shared floor makes the paired draws highly correlated. This affects how the result is worded, not the ranking: TOPSIS and SMAA use the magnitudes.

**R2 · Operating-model axis.** Every within-column ordering (C1 < C3 < C5; C2 < C4 < C6) follows **only from the declared overhead ranges A11–A12**. No source quantifies them (kit M1, K1). Per kit K1 these comparisons are reported as **indeterminate**. They are in the output only so that SMAA can carry the assumed uncertainty.

**R3 · Functional unit** *(corrected 4 Oct 2026)*. The ranking **by median** is identical under R₁, R₂ and R₃ (`ranking_invariant_to_R = true`; the script's check compares median orders only). **R₂ and R₃ order configurations identically in every draw**, by construction: both divide the same daily total by a quantity common to all configurations. **R₁ does not**: its numerator is the ELT share of compute plus the whole day's storage, so it can reorder configurations within a draw. The full ranking under R₁ matches R₂ in 82 % of draws; P(C7 < C2) is 0.98 on R₂ and 0.85 on R₁; P(C3 < C5) 0.98 and 0.95. The earlier statement that the ranking is identical under all three units by construction was wrong for R₁. The choice of functional unit would change rankings only if configurations differed in **what they deliver**. An example would be federated domains producing more data products for the same compute. The estimate does not model that, and no source quantifies it. For the thesis's functional-unit question: *under a fixed workload, R₂ and R₃ cannot reorder configurations; R₁ changes only the acceptability shares of close pairs, through the choice to attribute the whole day's storage to the pipeline run.*

**R3a · Region.** The script was re-run at 5 TB with only the grid range changed. The order of configurations and every probability are unchanged. Absolute values scale with the grid, and a lakehouse on a clean grid falls below a warehouse on a fossil-heavy one. **The grid ranges other than Frankfurt are rough approximations, not yet sourced**; they support the ranking claim only, not the absolute values.

| Region (grid range assumed, g CO₂/kWh) | C1 | C2 | C4 | Floor model C1 / C2 | P(C1 < C2) | P(C1 < C2), scenario S6 |
|---|---|---|---|---|---|---|
| Stockholm, eu-north-1 (15–60) | 21 | 77 | 82 | 81 / 216 | 1.00 | 0.06 |
| **Frankfurt, eu-central-1 (320–420), primary** | 95 | 286 | 305 | 239 / 713 | 1.00 | 0.08 |
| Virginia, us-east-1 (330–450) | 99 | 298 | 319 | 249 / 742 | 1.00 | 0.08 |
| Mumbai, ap-south-1 (650–750) | 167 | 492 | 526 | 397 / 1,209 | 1.00 | 0.09 |

*Medians on R₂, g CO₂e per TB-equivalent.*

**R3b · Data volume (added in v0.2).** The primary model is **linear in data volume**: work (A1) and storage both scale with P1. Therefore:
- R₂ and the ranking are **invariant to volume by construction**, not as an empirical finding;
- R₁ and R₃ scale proportionally.

The provisioning floor (§4a) is the one mechanism that makes volume matter, so it was run at five volumes:

| Volume | R₁ C1 / C2 (primary) | R₂ C1 / C2 (primary) | R₂ C1 / C2 (floor model, ratio) | Floor binds, share of draws (DWH / LH, S7a) | P(C1 < C2): primary / floor model / S7c |
|---|---|---|---|---|---|
| 1 TB | 29 / 60 | 95 / 286 | 902 / 2,905 (3.2) | 1.00 / 1.00 | 1.00 / 1.00 / 0.15 |
| **5 TB (reference)** | 144 / 299 | 95 / 286 | 239 / 713 (3.0) | 1.00 / 1.00 | 1.00 / 1.00 / 0.15 |
| 10 TB | 289 / 598 | 95 / 286 | 157 / 444 (2.8) | 1.00 / 1.00 | 1.00 / 1.00 / 0.15 |
| 50 TB | 1,444 / 2,990 | 95 / 286 | 96 / 290 (3.0) | 0.37 / 0.30 | 1.00 / 1.00 / 0.10 |
| 100 TB | 2,888 / 5,980 | 95 / 286 | 95 / 286 (3.0) | 0.05 / 0.05 | 1.00 / 1.00 / 0.09 |

**Reading.**
- **At 5 TB the floor binds in every draw.** The BI engine sized for 100 analysts, not the data volume, sets the compute. Absolute values are about 2.5 times the primary model's, which are therefore **lower bounds** for this workload.
- **The ranking does not change.** Under the floor model all seven configurations keep the primary order (C1 < C3 < C5 < C7 < C2 < C4 < C6), and the median C2/C1 ratio stays near 3.
- **What the floor changes is the source of the platform gap.** Below ~50 TB the gap comes mainly from suspend behaviour and memory per node rather than engine efficiency. Under the lakehouse-favourable assumptions (S7c) the two platforms become nearly equal.
- The technical supervisor's view that volume "isn't that critical" holds for the ranking. It does not hold for absolute values.

The floor-model draws (`R2_floor`) are carried into the Stage 2 plan as a sensitivity run in A14, so the full ranking is tested against them.

**R3c · Daily work share A1 and storage share** *(added 4 Oct 2026)*. With A1 fixed at 20 % and at 60 %, C1's median R₂ is 149 g and 74 g, and the C2/C1 ratio of medians is 2.3 and 3.6; the median order of all seven configurations is unchanged at both ends. Object-storage energy is about 60 % of the median R₂ of the warehouse configurations (C1 62 %, C3 61 %, C5 59 %), about 20 % for the lakehouse configurations and 33 % for C7. Storage is modelled identically for both platforms (CCF-3, A4, A10), so the absolute platform gap is a compute difference, and the ratio is diluted by a common term that rests on A1 and A4. Reproduce by fixing A1 in a copy of the script.

**R4 · Limitations.**
- The two benchmarks differ in scale (100 TB vs 3 TB) and date (2021 vs 2024).
- Warehouse hardware is inferred, not disclosed.
- BigQuery cannot be cross-checked, because slot consumption per run is not published.
- Embodied emissions use a derived range, not BoaviztAPI output.
- **The primary model is linear in volume.** Its idle model (A9) is proportional, while at 5 TB a concurrency floor dominates. Primary absolute values are lower bounds; the floor is tested in S7 and in the floor-model run.
- **The floor parameters (F1, F2) and the user count (P5) have no source.**
- A1 does not cancel in R₂ (see R3c). It left the median order unchanged in the runs made.

---

## 7. Sources

| ID | Source | Tier |
|---|---|---|
| S-CCF | Cloud Carbon Footprint, Methodology · cloudcarbonfootprint.org/docs/methodology/ | S (open methodology) |
| S-CCF-E | Cloud Carbon Footprint, Embodied emissions · cloudcarbonfootprint.org/docs/embodied-emissions | S |
| S-SF | Snowflake, *Industry Benchmarks and Competing with Integrity*, 12 Nov 2021 · snowflake.com/en/blog/industry-benchmarks-and-competing-with-integrity/ | T (vendor, disputed) |
| S-DB | Databricks, *Snowflake Claims Similar Price/Performance… But Not So Fast!*, 15 Nov 2021 · databricks.com/blog/2021/11/15/snowflake-claims-similar-price-performance-to-databricks-but-not-so-fast.html | T (competing vendor) |
| S-SEL | Woodward, *Choosing the right warehouse size in Snowflake*, select.dev, 27 Nov 2022 · select.dev/posts/snowflake-warehouse-sizing | T (practitioner estimate) |
| S-EMR | AWS Big Data Blog, *Amazon EMR 7.5 runtime for Apache Spark and Iceberg…*, 27 Dec 2024 · aws.amazon.com/blogs/big-data/amazon-emr-7-5-runtime-for-apache-spark-and-iceberg-can-run-spark-workloads-3-6-times-faster-than-spark-3-5-3-and-iceberg-1-6-1/ | T (vendor; open-source baseline reported by the vendor) |
| N09a | Snowflake docs, Understanding overall cost (billing mechanics) | T |
| G03 | Teads Engineering, carbon footprint of a cloud-hosted platform (vendor-data limitation) | T |
| TS-2 | Technical supervisor, e-mail replies of 29 Sep 2026 on region and workload scale | Personal communication |

**All benchmark inputs are tier T.** Under kit Part 1 this is acceptable for an *estimate declared as such* (K1), not for a measured value. The thesis must say so wherever CARB values appear.
