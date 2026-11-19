# Evidence pack — TTDP (Time-to-data-product)

**Version** 1.0 · **Assembled** 26 September 2026 · **Coding kit** v1.1, passport M2 (determinant coding) · **Register** `source-register.xlsx`

---

## 0. How to use this pack

The rules of `pack-PORT.md` §0 apply here too:
- no scores;
- P / S / T tiers, and T never carries a cell alone;
- web quotations must be spot-checked;
- URLs were accessed on 26 September 2026.

**How TTDP is coded (kit M2).** TTDP is not coded from elapsed days. It is coded from five **architectural determinants of delivery time**; the evidence below is arranged by determinant first (§3), then summarised per configuration (§4).

| Determinant | Faster | Slower |
|---|---|---|
| D1 Queue position | The team that needs the product builds it | Request enters a central team's backlog |
| D2 Hand-offs | Zero or one team boundary | Two or more |
| D3 Provisioning | Self-serve templates provision storage, compute, CI and catalog entry | Tickets to a platform or infrastructure team |
| D4 Endpoint tooling | Catalog, contracts, quality checks and access policy applied by default | Each of the six properties assembled per product |
| D5 Platform dependency | Platform mature and shared | Each domain must first build or wait for baseline capability |

**Anchors.**
- **1** Central queue and two or more hand-offs, with manual provisioning and endpoint assembled per product; or domains blocked on missing capability.
- **2** Central queue with one hand-off; or domain ownership without self-serve.
- **3** Either the queue or the hand-offs removed, but not both; partial templating.
- **4** The domain builds on self-serve provisioning, with at most one hand-off and most endpoint properties applied by default.
- **5** Level 4 with all six properties applied by default and no dependency on capability the domain must build itself.

**Declared confound (kit).** The scale scores what the architecture makes possible for a **competent team**, not what a given team achieves.

---

## 1. Findings that cut across cells — read before coding

### F1. No source reports elapsed delivery time for a data product — confirmed

The kit's premise holds after a second search. The nearest quantities are these; none is a data-product lead time:

| Source | What it gives | Tier |
|---|---|---|
| G22 (Monte Carlo, 29 Feb 2024) | A practitioner's warning against "trying to establish a lead time of delivering a data product within a day" — lead time as a target, with no measured value | T |
| G21 (Thoughtworks, 27 Mar 2024) | "These initial data product teams are stuck for months at a time, waiting for the platform to develop baseline capabilities"; recommends a first use case of "two to three data products… over the course of six months" | S |
| G20 (Thoughtworks, 16 Jan 2026) | "We've seen teams spend over a year just trying to map the existing landscape before delivering a single new data product." | S |
| #7 | "a 72% reduction in infrastructure provisioning time, from 3 hours to 50 minutes" in a governed lakehouse testbed | P |
| G24 (dev.to, dated 1 Jun 2026 on the page) | "This process took about 18 months." — the context (whole transition or one product) must be read on the page before use | S |
| G04 (DORA) | Change lead time: "The amount of time it takes for a change to go from committed to version control to deployed in production." Software only; no benchmark bands on the current page | S |

**Consequence.** Delivery speed is scored as a class on D1–D5, as the kit specifies. The figures above are illustrations for the thesis text, **not calibration for the scale**.

### F2. The operating-model evidence is consistent in direction, but two-sided for federation

- **D1 and D2** favour decentralisation. The central team is a queue [Dehghani 2019], and hand-offs cost flow [Team Topologies].
- **D5** penalises decentralisation without a platform. Teams are "stuck for months" [G21], and domains lack the skills [G07, G24].
- **The practitioner literature converges on hub-and-spoke as the resolution.** The hub, or centre of excellence, owns the platform and guardrails, and spokes "progressively assume greater ownership" [G10].
- G10 also states the trade-off plainly: "Pure mesh approaches reverse the trade-off, enabling local flexibility and faster iteration while allowing standard fragmentation, duplicated pipelines, and inconsistent metadata."

This is why the kit's C6 profile **assumes the self-serve platform exists** (Part 3). Without it, C6 is the failure mode, not the canonical mesh, and its D5 would sit at the slow end.

### F3. The platform axis has little evidence on delivery time

- **D3 and D4 are the determinants where platform could matter.** A managed warehouse ships provisioning and discovery features; an assembled lakehouse needs them built.
- **What was found.**
  - Snowflake's internal marketplace provides publishing, discovery and access control for data products across accounts, which bears on D4 [N08a].
  - #7 measures provisioning time on a lakehouse with infrastructure-as-code (D3).
  - No source compares D3 or D4 across the two platforms.
- **Do not conflate** pipeline **latency** with delivery **time**. #29 measures the effect of governance strictness on end-to-end pipeline latency, a runtime property, not how long it takes to deliver a product.

---

## 2. Sources in this pack

| ID | Source | Tier | Notes |
|---|---|---|---|
| N08b | Dehghani, *How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh*, martinfowler.com, 20 May 2019 · martinfowler.com/articles/data-monolith-to-mesh.html | S | Originating practitioner text |
| N08c | Dehghani, *Data Mesh Principles and Logical Architecture*, martinfowler.com, 3 Dec 2020 · martinfowler.com/articles/data-mesh-principles.html | S | |
| N08d | Team Topologies, *Key concepts* · teamtopologies.com/key-concepts | S | Practitioner framework (Skelton & Pais) |
| N08e | Thoughtworks, *Drive data and AI success with Team Topologies and Data Mesh*, 4 Mar 2025 · thoughtworks.com/insights/blog/data-strategy/team-topologies-data-mesh | T | Consultancy blog |
| N08a | Snowflake docs — Organizational listings / Internal Marketplace · docs.snowflake.com/en/user-guide/collaboration/listings/organizational/org-listing-about | T | |
| G04 | DORA metrics guide · dora.dev/guides/dora-metrics/ | S | Software construct |
| G06 | Kaushikk, *Implementing Data Mesh on Databricks: Harmonized and Hub & Spoke*, 21 Apr 2024 · rajanieshkaushikk.com/2024/04/21/harmonized-hub-spoke/ | S | |
| G07 | Strengholt, *Data Mesh: The Balancing Act of Centralization and Decentralization* — IIA republication, 24 Apr 2023 (iianalytics.com/community/blog/data-mesh-the-balancing-act-of-centralization-and-decentralization), of the Towards Data Science original, Mar 2022 | S | Attribution resolved: same article, author Strengholt |
| G10 | Angélil & Migon (2026), *Beyond the Data Mesh Illusion*, arXiv:2605.27131 | S | Preprint |
| G20 | Thoughtworks, *The state of data mesh in 2026*, 16 Jan 2026 · thoughtworks.com/en-us/insights/blog/data-strategy/the-state-of-data-mesh-in-2026-from-hype-to-hard-won-maturity | S | |
| G21 | Thoughtworks, *10 recommendations for a successful enterprise data mesh implementation*, 27 Mar 2024 · thoughtworks.com/en-us/insights/articles/recommendations-for-a-successful-data-mesh-implementation | S | |
| G22 | Monte Carlo, *How To Implement Data Mesh: Top Tips From 4 Data Leaders*, 29 Feb 2024 · montecarlo.ai/blog-how-to-implement-data-mesh | T | |
| G24 | Watson, *What I Learned From Running a Data Mesh*, dev.to · dev.to/ben_watson_data/what-i-learned-from-running-a-data-mesh-213f | S | Page date 1 Jun 2026 (possibly an update) |
| #7 | Fannouch et al. (2026), Governed lakehouse DataOps, healthcare testbed | P | Abstract |
| #16 | Ramchandani & Mackinnon (2023), Adopting the data mesh, case | P | Abstract |
| #29 | Bhatt & Gadiraju (2026), Governed pipelines — latency | P | Abstract; **latency, not TTDP** |
| #31 | Van Eijk et al. (2024), Design decisions for self-serve platforms | P | Abstract; open on arXiv |
| #34 | Herden (2020), Integrating data lakes into DW architectures | P | Abstract |
| #46 | Mod (2026), Cloud-native modernisation, multi-case | P | Abstract |
| #55 | Ramos et al. (2024), Data mesh adoption readiness, multi-case | P | Abstract |
| #60 | Schneider et al. (2025), Data products across platforms | P | Abstract |
| #118 | Karkošková (2025), Data product design methodology | P | Abstract |
| #133 | Bode et al. (2024), 15 interviews on data mesh | P | Abstract |
| #135 | van der Werf et al. (2025), Data mesh reference architecture | P | Abstract; archetypes |

---

## 3. Evidence by determinant

### D1 — Queue position

| Source | Tier | Quotation | Direction |
|---|---|---|---|
| N08b | S | "the long response time to satisfy the data consumer needs has historically been a point of organizational friction"; "frustrated consumers fighting for a spot on top of the data platform team backlog and an over stretched data platform team" | Central backlog = slow |
| G24 | S | "we quickly reached data overload… The small team of analysts and engineers were expected to be subject matter experts on every possible domain" | Central team saturates |
| #60 | P | Enterprises run many business-unit platforms "for reasons such as an improved time to market, flexibility and customer orientation" | Decentralised ownership is adopted for time to market |
| #34 | P | Data warehouses hit limits "due to lack of agility, flexibility and system complexity" | Central warehouse pattern associated with low agility |
| G06 | S | Hub-and-spoke "May limit domain-specific agility due to central control; potential bottlenecks in data processing and innovation at the spoke level" | A residual queue remains at the hub for hub-owned assets |

### D2 — Hand-offs

| Source | Tier | Quotation | Direction |
|---|---|---|---|
| N08b | S | "the whole pipeline i.e. the monolithic platform, is the smallest unit that must change to cater for a new functionality"; engineers "siloed from the operational units of the organization" | Stage-organised teams = multiple hand-offs |
| N08d | S | Stream-aligned teams have "no hand-offs to other teams for any purpose"; "Nothing kills productivity faster than one team waiting on another team" | Hand-offs cost flow |
| N08e | T | "Reduce bottlenecks in centralized data teams"; address "the complexities of data handovers through clear documentation and data contracts" | Contracts reduce hand-off cost |

### D3 — Provisioning

| Source | Tier | Quotation | Direction |
|---|---|---|---|
| N08c | S | "the only way that teams can autonomously own their data products is to have access to a high-level abstraction of infrastructure that removes complexity and friction" | Self-serve provisioning is the precondition for domain delivery |
| #31 | P | "designing and implementing a self-serve data platform is challenging"; catalog of design decisions from 43 grey sources and 6 expert interviews | Self-serve is achievable but a design effort in itself |
| #7 | P | "a 72% reduction in infrastructure provisioning time, from 3 hours to 50 minutes" with infrastructure-as-code in a governed lakehouse | Measured D3 gain from templating (testbed) |
| N08e | T | "Create platform teams that provide boilerplates and standardized tools to reduce cognitive load." | Templates via a platform team |

### D4 — Endpoint tooling

| Source | Tier | Quotation | Direction |
|---|---|---|---|
| N08c | S | The platform should "lower the current cost and specialization needed to build data products"; "decreased lead time" named as a measure that data is delivered as a product | Default tooling lowers per-product assembly |
| N08a | T | Internal Marketplace: "Publishing data products in the Internal Marketplace ensures teams access consistent datasets"; teams "discover, trust, and apply resources"; access "managed by account targeting and Role-Based Access Control" | Discoverability, addressability and access policy by default on the warehouse platform |
| #118 | P | Data products with "governance, marketplace accessibility, global search capabilities, and data discovery"; "Data contracts, implemented in YAML" | Endpoint properties delivered through a methodology and contracts |
| #46 | P | Organisations embedding "the data contract… the tiered data Lakehouse architecture, and the versioned inference API" from the start "can deploy production ML capabilities months ahead" | Default contracts and tiers accelerate delivery (multi-case) |

### D5 — Platform dependency

| Source | Tier | Quotation | Direction |
|---|---|---|---|
| G21 | S | "These initial data product teams are stuck for months at a time, waiting for the platform to develop baseline capabilities"; recommends "core MVP capabilities to be 'just good enough'" | Platform-first delay, documented |
| G20 | S | "We've seen organizations spend a year in 'analysis paralysis,' trying to define the perfect, immutable domain boundaries."; teams spending "over a year just trying to map the existing landscape before delivering a single new data product"; a model with "a centralized, cost-effective platform that handles tenancy so well that the value-driving components can be decentralized" | Delay before the first product; a central platform as enabler |
| G10 | S | "pure implementations frequently underdeliver—teams inherit new responsibilities without the platform maturity, tooling, or coordination mechanisms needed to exercise them effectively"; staged path in which "The CoE retains platform integrity and governance automation, while spokes progressively assume greater ownership" | Federation without a platform is slow; hub-and-spoke as the maturity path |
| G07 | S | "Not all organizations have 500+ data engineers. Not all organizational teams are familiar with complex data modeling techniques, change data capture, Kubernetes, and Python notebooks."; enabling teams "sometimes even take ownership of data pipeline management for situations when a domain team lack necessary skills" | Skills are a dependency; a central enabling team fills the gap |
| G24 | S | Domain teams "reluctant to own their own data… requiring new skillsets that they don't possess"; "a successful data mesh is created by distributing ownership while centralising standards, tooling and discoverability" | First-hand account: hub-type centralisation of tooling |
| #133 | P | Organisations have difficulties with "the shift of responsibility for the development, provision, and maintenance of data products"; recommends "a cross-domain steering unit" and "small dedicated teams" | Transition cost; a central steering unit |
| #55 | P | Readiness factors for data mesh adoption (TOE framework, multi-case) | Adoption depends on organisational readiness |
| #16 | P | Case reports mesh "accelerating data-driven decision-making processes" | Positive outcome claim (abstract; no measure) |

---

## 4. Summary by configuration

The profile fixes the determinant states. The evidence column shows which sources support each state. Coders assign the level.

| Config | D1 queue | D2 hand-offs | D3 provisioning | D4 endpoint tooling | D5 platform dependency | Evidence (row-specific) |
|---|---|---|---|---|---|---|
| **C1** DWH × central | Central backlog | Typically ≥2 (source → central modelling → BI) | Central team provisions; the managed platform makes provisioning itself fast | Warehouse-native catalog and marketplace (N08a); applied by the central team | Mature, shared | N08b, G24, #34 (D1–D2); N08a (D4) |
| **C2** LH × central | Central backlog | As C1 | Central team provisions; templating possible (#7) | Open catalog; properties assembled by the central team | Mature, shared | N08b, G24 (D1–D2); #7 (D3) |
| **C3** DWH × hub | Domain builds; hub-owned shared assets queue at the hub (G06) | 0–1 (spoke → hub for shared assets) | Hub templates (profile) | Hub-provided; marketplace across schemas | Hub supplies the platform | G06, G10, G07, G24, N08e |
| **C4** LH × hub | As C3 | As C3 | Hub self-serve templates (profile; #7, #31) | Hub-provided contracts and catalog (#118, #46) | Hub supplies the platform | G06, G10, G07, G24, #31, #46, #118 |
| **C5** DWH × federated | Domain builds | 0 within the domain; cross-domain via sharing | **Each domain sets up its own account**; no hub (profile) | Per domain; organizational listings across accounts exist (N08a) | **Platform-first dependency** (kit C5 addition) | G21, G20, G10, G07, #133 |
| **C6** LH × federated | Domain builds | 0 within the domain | Thin self-serve platform — **assumed to exist** (kit C6) | Contracts and policy-as-code (profile) | Low **if** the platform exists; otherwise the failure mode (G21) | G21, G20, G10, #31, #133, #16 |
| **C7** fabric | Mixed | Fabric adds a metadata/virtualisation layer | Mixed | Unified discovery via fabric (claimed) | Brownfield: existing platforms | **No row-specific source located** |

> **Update 1 Oct 2026 (kit K15).** C7 is redefined as *Hybrid / multi-platform*: lakehouse core plus warehouse serving layer, no fabric layer assumed. Quotations below about a fabric or metadata overlay apply only where such a layer exists; coders treat them as an upper bound for C7, not as its reference profile.

**Evidence strength by row.**
- **C1, C2:** moderate. The D1 and D2 evidence is the core argument of the data mesh literature itself, which gives it an **advocacy bias** that should be recorded. The platform difference between C1 and C2 is barely evidenced (F3).
- **C3, C4:** moderate and consistent. Practitioner sources converge on hub-and-spoke as the pragmatic form.
- **C5, C6:** moderate on D5 (platform-first delay is well documented) and thin on outcomes.
- **C7:** none.

---

## 5. Implications for the coding kit (author decisions, not coding)

1. **Advocacy bias.** Most D1–D2 evidence comes from proponents of decentralisation (Dehghani, Thoughtworks). Add a sentence to M2 recording this, and note that no counter-study measuring central-team delivery speed was located.
2. **C6 assumption.** The kit already states that C6 assumes the self-serve platform exists. The evidence (G21, G20, G10) supports making a **sensitivity run** in SMAA explicit: C6 with D5 at the slow end. This matches the kit's existing C6 note.
3. **Platform axis (F3).** Record that TTDP is expected to differ little between C1 and C2, and between C3 and C4, on evidence. A coder who separates them must cite a D3 or D4 source.
4. **Evidence inventory (Part 4).** The kit expected M for C1–C6 and T for C7, and this holds.

## 6. Open items

- ~~G07 attribution~~ — resolved: the IIA post is a republication of Strengholt's article (MLR log, URL appendix).
- **G24 "about 18 months"** — read the context on the page.
- **G23** (promethium.ai, five-phase roadmap with durations) was not re-fetched. Optional; it is tertiary.
- **Spot-check** of web quotations.
