# Evidence pack — AIRD (AI and GenAI readiness)

**Version** 1.0 · **Assembled** 26 September 2026 · **Coding kit** v1.0, passport M3 · **Register** `source-register.xlsx`

---

## 0. How to use this pack

Same rules as `pack-PORT.md` §0. The main ones:
- **no scores** in the pack;
- tiers **P / S / T**, with T never carrying a cell alone;
- web quotations were obtained with a page-reading tool and must be spot-checked;
- all URLs accessed **26 September 2026**.

**Scale being coded (M3).**

| Level | Mechanism the evidence must show |
|---|---|
| 1 | Structured/tabular only; ML outside the platform via manual exports; no vector capability |
| 2 | Unstructured storable but not first-class; ad-hoc feature pipelines; no native ML lifecycle; no vector support |
| 3 | Native unstructured handling; supported feature-engineering patterns; partial ML lifecycle (training **or** serving); basic vector storage/search |
| 4 | Full ML lifecycle (experiment → registry → serving); production feature-platform patterns; native vector search; catalog exposes machine-readable APIs |
| 5 | Level 4 plus **governed RAG** (retrieval over governed data **with policy enforcement**); agents discover and access data through the semantic layer **under the same access controls**; unified governance across structured and unstructured data |

**Kit clarification for level 5 (v1.0).** Governed RAG requires that retrieval from a vector index respects the same access policies as the governed source. In practice this means an index maintained from the governed store by change data capture, with an explicit consistency boundary (Srivastava, 2026). A vector store populated by export does not meet level 5.

---

## 1. Findings that cut across cells — read before coding

### F1. On levels 1–4 the two managed platforms have converged; the literature has not caught up

The corpus's platform contrast rests mainly on Armbrust et al. (2021):
- unstructured data *"data warehouses could not store and query at all"*;
- *"Reading this data via ODBC/JDBC is inefficient, and there is no way to directly access the internal warehouse proprietary formats."* [#94]

The reference warehouse products now document each level-4 mechanism:

| Mechanism | Snowflake | BigQuery (cross-check) |
|---|---|---|
| Unstructured data | stages, directory tables, `FILE` type [N05c] | object tables, with row-level policies extending to the objects [N05h] |
| Feature platform | Feature Store with incremental refresh and point-in-time joins [N05d] | — (not fetched) |
| Registry → serving | Model Registry; inference in warehouse or on containers [N05b] | registration to Vertex AI Model Registry and endpoint deployment [N05i] |
| Vector search | Cortex Search [N05a] | `VECTOR_SEARCH` with ANN indexes [N05g] |
| Machine-readable semantic access | semantic views via Cortex Analyst; MCP servers exposing Cortex Search and semantic views [N05e, N05f] | — |

**One gap in the warehouse column: experiment tracking.** The Snowflake Model Registry page does not mention it [N05b]. The level-4 chain "experiment → registry → serving" is documented from registry onward only.

**Consequence.** The age of #94 matters. As evidence of the architectural mechanism it stands: proprietary storage does not give external ML libraries direct access. As evidence that warehouses cannot handle unstructured data or ML, it is superseded for the reference products.

### F2. Level 5 as written is not met natively by any reference implementation located

The CDC-maintained index exists on both platforms:
- Snowflake: Cortex Search *"refresh cycle processes only the rows that changed since the last refresh"* [N05a];
- Databricks: Delta Sync index built on the source table's change data feed [N06b].

**Policy inheritance does not:**

| Implementation | What the source says | Tier |
|---|---|---|
| Snowflake Cortex Search | *"Cortex Search Services perform searches with owner's rights"* [N05a]. Snowflake's own guide: *"we are following recommended best practice of using explicit filters on the client-side query to filter for access controls. These filters are based on user attributes that are obtained from the authentication flow"*, because *"Cortex Search Services runs with Owner's Rights by design."* [N05j, updated 20 Dec 2025] | T |
| Snowflake Cortex Search | Independent test: *"CORTEX Search runs with owners' rights, not callers', meaning it executes queries using the permissions of the privileged role that created the service"*; *"If misconfigured, CORTEX can allow a user to go around SELECT and still see plaintext values."* Snowflake committed to *"offering caller's rights execution context for specific Snowflake use cases"* [N05k, 29 Apr 2025] | S* |
| Databricks Vector Search (managed lakehouse variant) | *"Row and column level permissions are not supported. However, you can implement your own application level ACLs using the filter API."* [N06b] | T |
| BigQuery vector search | Neither the vector-search page nor the row-level-security interaction page says whether row-level or column-level policies apply to `VECTOR_SEARCH` or vector indexes [N05g, N05l] | T — **undetermined** |

- **No release note was located** showing caller's-rights execution for Cortex Search: searched release notes through September 2026, including the 12 Mar 2026 Cortex Search update, which lists no access-control change.
- **Agents.** Cortex Agents require *"privileges on the objects used by the agent's tools"* [N05e], so the caller's privileges gate which tools an agent may call. A search tool that itself runs with owner's rights still returns owner-scoped results.

**Consequence for coding.** In 2026, policy-inheriting retrieval is achieved by **application-level filtering** layered on the platform, not by the platform. Whether that meets level 5 is the coder's judgement. If it does not, **no configuration reaches level 5**: the top anchor does not discriminate, and that is itself a result (§4).

### F3. For the open stack, "native" depends on where the profile draws its boundary

The C2 reference components are: object storage, open table format, open catalog, Spark and SQL engines, dbt/Spark transforms, Airflow-class orchestration, catalog-level access control. **No ML lifecycle layer and no vector index are listed.**

The level-4 mechanisms exist as open-source components that attach to this stack:
- MLflow: tracking → registry → serving [N06c];
- Feast: offline and online feature store with point-in-time retrieval [N06d];
- open-source Unity Catalog: governs unstructured files and AI assets alongside tables [N06a, #142].

**Iceberg, Spark and Trino provide no vector index themselves** (no source states one).

**Author decision:** does the C2/C4/C6 reference profile include an ML-lifecycle layer of the MLflow class? If yes, those components count as within the configuration. If no, the open stack scores on what Spark and the open catalog provide alone. The managed variant (Databricks) bundles all of them, but it is a product, not the profile.

### F4. The operating model affects AIRD only through governance unification

No source compares AI readiness across operating models on the same platform. Row-specific sources are:
- #46 (multi-case): organisations that embed data contracts and a tiered lakehouse *"can deploy production ML capabilities months ahead"*;
- #5: federated metadata *"with centralized access control"* as the enabler for AI on lakehouses;
- #28: conceptual.

The level-5 component *"unified governance across structured and unstructured data"* is harder to show where each domain runs its own account or catalog (C5, C6). No source located demonstrates or refutes it.

---

## 2. Sources in this pack

| ID | Source | Tier | Notes |
|---|---|---|---|
| #5 | Javeri et al. (2026), Federated metadata architecture for lakehouse AI | P | Abstract |
| #6, #7 | Governance-centric / governed lakehouse architectures (2026) | P | Abstracts; lakehouse + governance for AI; #7 has a measured testbed |
| #20 | Gholivand et al. (2025), Hybrid data warehousing for CSPs | P | Abstract |
| #28 | Inala et al. (2026), Hybrid data products and agentic AI | P | Abstract; conceptual |
| #32 | Srivastava (2026), Selection framework for AI-ready data platforms | P | Full text on file |
| #46 | Mod (2026), Cloud-native modernisation as AI readiness, multi-case | P | Abstract |
| #53 | Alimardanova et al. (2025), Data lakes vs warehouses | P | Abstract |
| #61 | Grund et al. (2025), Databricks Lakeguard, SIGMOD Companion | P | Abstract; vendor-authored |
| #68 | Gebler et al. (2025), Clinical data architectures for AI, JMIR | P | Abstract; rapid review |
| #94 | Armbrust et al. (2021), Lakehouse, CIDR | P | Full text; vendor-authored; **dated — see F1** |
| #111 | Mishra et al. (2025), AI-driven data platforms review | P | Abstract |
| #129 | Mazumdar et al. (2023), The Data Lakehouse | P | Abstract |
| #142 | Chandra et al. (2025), Unity Catalog, SIGMOD Companion | P | Abstract; vendor-authored |
| N05a | Snowflake docs — Cortex Search overview · docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview | T | |
| N05b | Snowflake docs — Model Registry · …/developer-guide/snowflake-ml/model-registry/overview | T | |
| N05c | Snowflake docs — Unstructured data · …/user-guide/unstructured-intro | T | |
| N05d | Snowflake docs — Feature Store · …/developer-guide/snowflake-ml/feature-store/overview | T | |
| N05e | Snowflake docs — Cortex Agents · …/user-guide/snowflake-cortex/cortex-agents | T | |
| N05f | Snowflake release note 7 Aug 2026 — Native Apps: Cortex Agents and MCP servers GA · …/release-notes/2026/other/2026-08-07-native-apps-agents-mcp-ga | T | |
| N05j | Snowflake developer guide — Access controls for RAG (Cortex Search), updated 20 Dec 2025 · snowflake.com/en/developers/guides/getting-started-with-access-controls-for-cortex-search/ | T | Vendor's own statement of the limitation |
| N05k | Cyera Research, *Unexpected behavior in Snowflake's Cortex AI*, 29 Apr 2025 · cyera.com/blog/unexpected-behavior-in-snowflakes-cortex-ai | S* | Independent first-hand test; **Garousi appraisal pending** (*) |
| N05g | Google Cloud — Vector search intro · docs.cloud.google.com/bigquery/docs/vector-search-intro | T | |
| N05h | Google Cloud — Object tables · docs.cloud.google.com/bigquery/docs/object-table-introduction | T | |
| N05i | Google Cloud — Managing models in Vertex AI · docs.cloud.google.com/bigquery/docs/managing-models-vertex | T | |
| N05l | Google Cloud — Row-level security with other features · docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features | T | Silent on vector search |
| N06a | Unity Catalog OSS · unitycatalog.io | T | Open-source project site |
| N06b | Databricks docs — Vector Search · docs.databricks.com/aws/en/vector-search/vector-search | T | |
| N06c | MLflow docs — Model Registry · mlflow.org/docs/latest/ml/model-registry/ | T | Open-source project documentation |
| N06d | Feast docs · docs.feast.dev | T | Open-source project documentation |

---

## 3. Evidence by configuration

### C1 — Cloud DWH × centralised

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #94 | P | "Reading this data via ODBC/JDBC is inefficient, and there is no way to directly access the internal warehouse proprietary formats." | §2 | Pattern (dated) | External ML libraries lack direct access to native storage |
| #94 | P | "more and more datasets were completely unstructured, e.g., video, audio, and text documents, which data warehouses could not store and query at all." | §1 | Pattern — **superseded for reference products (F1)** | Historical level-1/2 position |
| #53 | P | Warehouses "may lack flexibility for unstructured data or real-time analytics" | Abstract | Pattern | Same position, 2025, library analytics context |
| #68 | P | "clinical data warehouses offer strong data governance, stability, and structured reporting… However, they are limited in terms of real-time processing and scalab[ility]" | Abstract | Pattern | Governance strength, analytics limits |
| N05c | T | "Both external (external cloud storage) and internal (i.e. Snowflake) stages support unstructured data." "Directory tables store a catalog of staged files in cloud storage." "The FILE data type represents a file stored in an internal or external stage." | Overview | Product | Native unstructured handling (level 3) |
| N05h | T | "setting a row-level access policy on an object table restricts a user or group's access to the object metadata in selected rows, and also to the objects represented by those rows." | Object tables | Product (BigQuery) | Unstructured under the same row-level policies (level-5 component, unstructured governance) |
| N05d | T | "The Snowflake Feature Store refreshes the features in the feature view for you, incrementally and efficiently"; "Backfill and point-in-time correct features with ASOF JOIN" | Overview | Product | Production feature platform (level 4) |
| N05b | T | "The Model Registry lets you securely manage models and their metadata in Snowflake…"; inference "in a Snowflake virtual warehouse"; serving "in Snowpark Container Services for GPU-based inference" | Overview | Product | Registry → serving (level 4); **experiment tracking not documented** |
| N05i | T | "`MODEL_REGISTRY`: register the model to the Model Registry"; deploy to endpoints | Registration | Product (BigQuery) | Registry → serving via Vertex AI |
| N05a | T | "The two primary use cases for Cortex Search are retrieval augmented generation (RAG) and enterprise search."; incremental refresh of changed rows | Overview | Product | Native vector/hybrid search; CDC-style index maintenance |
| N05a, N05j, N05k | T, T, S* | Owner's-rights execution; access control by application-level filters (F2) | — | Product | **Level-5 policy inheritance not shown** |
| N05g | T | "When a vector index is used, the VECTOR_SEARCH and AI.SEARCH functions use the Approximate Nearest Neighbor search technique" | Overview | Product (BigQuery) | Native vector search; policy behaviour undocumented (F2) |
| N05e, N05f | T | Cortex Agents use "Cortex Analyst … using a semantic view" and Cortex Search; MCP server "exposes app-owned objects such as Cortex Search services, semantic views, procedures, and UDFs as MCP tools"; consumers control access "with caller grants" | Overview; release note | Product | Machine-readable semantic access for agents (level 4–5 component) |

**Evidence strength:** 4 P, all at the pattern level and partly dated. Current capability rests on T only (two vendors concur). Under the kit, T never carries a cell alone. The P evidence points lower than the T evidence: **a conflict for the coder** — see F1 on dating.

---

### C2 — Open lakehouse × centralised

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #94 | P | "The use of open formats also made data lake data directly accessible to a wide range of other analytics engines, such as machine learning systems."; declarative DataFrame APIs that map "data preparation computations into Spark SQL query plans" | §1, §3.4 | Pattern | Direct ML access to governed tables; unstructured in the lake |
| #32 | P | Reference architecture "that integrates lakehouse storage, feature processing, and semantic retrieval layers as the unified substrate for modern analytics, machine learning, and Retrieval-Augmented Generation applications" | Abstract, §IX | Pattern | Level-4 components as one substrate |
| #32 | P | RAG over managed enterprise data requires "relational system of record plus vector store as semantically indexed read replica, synchronised by CDC, with an explicitly governed consistency boundary" (extraction note) | §IX-C | Pattern | Defines the level-5 mechanism; does not show policy inheritance |
| #129 | P | Warehouses "lead to proliferation of data copies… restricting access to engines, tools, and capabilities beyond what the vendor offers"; lakehouse provides "additional capabilities" | Abstract | Pattern | Open access for ML tools |
| #111 | P | "The rise of Data Lakes and Lakehouse architectures allows organizations to manage structured and unstructured data more efficiently." | Abstract | Pattern | Unstructured handling |
| #142 | P | "there is growing demand to govern a broader range of assets beyond tabular data, such as unstructured data and AI models… we introduce Unity Catalog (UC), an open and universal Lakehouse catalog"; "core APIs and both server and client implementations have been available as open source since June 2024." | Abstract | Pattern (open-source catalog, vendor-authored) | One catalog for tables, files and models (level-5 component) |
| #61 | P | Lakeguard "enforces fine-grained data access policies, row-level filters, and column masks across all of an enterprise's data and AI workloads" | Abstract | Product (Databricks) | Policies on data and AI **workloads** — not on vector indexes (see N06b) |
| N06a | T | "Manage unstructured data, such as images and documents, and Gen AI tools with a single, universal catalog."; "Apache 2.0 licensed" | Home | Pattern (OSS) | Unified catalog available outside Databricks |
| N06c | T | Registry version control; "Each registered model version is linked to the MLflow run… that produced it"; tracking and serving components | Model Registry | Pattern (OSS) | Experiment → registry → serving (level 4), **if in profile (F3)** |
| N06d | T | "open-source feature store"; "an offline store for historical feature extraction… an online store for serving features at low-latency"; "point-in-time correct feature sets" | Intro | Pattern (OSS) | Production feature platform (level 4), **if in profile (F3)** |
| N06b | T | Delta Sync index on "Delta Lake tables, streaming tables, or managed tables using Iceberg v3 or above", maintained through change data feed; "Row and column level permissions are not supported." | Vector Search | Product (managed variant) | CDC-maintained index shown; **policy inheritance not shown** (F2) |

**Evidence strength:** 7 P (2 vendor-authored), several T.
- Strongest on the architectural argument: direct ML access, one catalog for tables, files and models.
- Level-4 components are documented as open source (F3 decides whether they count).
- Level 5 is not shown (F2).

---

### C3 — Cloud DWH × hub-and-spoke

**No source located addresses AI readiness of a hub-and-spoke warehouse as distinct from a centralised one.** Platform evidence from C1 applies: same engine, same AI services.

Row-relevant mechanism, from F4: the hub owns the engine, catalog and access-control framework (profile). Governance therefore stays unified, and so do the conditions for the level-5 component "unified governance across structured and unstructured data".

**Evidence strength:** none specific; inherits C1.

---

### C4 — Open lakehouse × hub-and-spoke

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #46 | P | Organisations "embedding these patterns right from the program's beginning can deploy production ML capabilities months ahead of those that treat AI enablement as a post-migration task"; patterns are "the data contract, the event-driven integration backbone, the tiered data Lakehouse architecture, and the versioned inference API" | Abstract | Pattern (multi-case) | Shared lakehouse platform with contracts accelerates ML delivery |
| #5 | P | "a read-through federation model, centralized access control, and lineage-aware metadata management" to enable "scalable, secure, and compliant AI analytics" | Abstract | Pattern | Central policy plane over lakehouse AI (hub function) |
| #7 | P | Governed medallion lakehouse with "governance and metadata management… explicit promotion contracts"; "a 72% reduction in infrastructure provisioning time" | Abstract | Pattern (testbed) | Governed, AI-ready lakehouse with platform tooling |

**Platform evidence:** as C2.

**Evidence strength:** 3 P specific to the row (one multi-case, one testbed, one design); inherits C2.

---

### C5 — Cloud DWH × federated

**No source located on AI readiness of separate warehouse accounts per domain.** Platform evidence from C1 applies per domain.

**Mechanism relevant to level 5** (F4, inference, not in a source): AI services (search index, semantic views, agents) are objects inside one account. An agent or retrieval index spanning domains must reach data in other accounts through sharing. The pack found no source on whether AI services operate over shared data under the consumer's policies. **Gap.**

**Evidence strength:** none specific; inherits C1.

---

### C6 — Open lakehouse × federated

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #28 | P | "Architectures facilitating hybrid data products, like data mesh and data fabric, address the increasing complexity of data integration and sharing across silos. At the same time, demand for agentic AI solutions… is on the rise." | Abstract | Pattern (conceptual) | Data products as the unit agents consume |
| #5 | P | Federated metadata with centralised access control (see C4) | Abstract | Pattern | Suggests AI governance needs a central policy plane even in a federated estate |

**Platform evidence:** as C2.

**Gap:** no source demonstrates unified governance of structured and unstructured data, or governed retrieval, across independently operated domain workspaces.

**Evidence strength:** 2 P, conceptual or design only; inherits C2. **Thin on the row-specific question.**

---

### C7 — Hybrid / multi-platform (was: data fabric overlay)

> **Update 1 Oct 2026 (kit K15).** C7 is redefined as *Hybrid / multi-platform*: lakehouse core plus warehouse serving layer, no fabric layer assumed. Quotations below about a fabric or metadata overlay apply only where such a layer exists; coders treat them as an upper bound for C7, not as its reference profile.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #32 | P | Edge case: high-cardinality time series joined to relational dimensions "resolves to a lakehouse ingestion pattern unifying governance in a single storage substrate" (extraction note) | §IX-C | Pattern | Hybrid estates tend to consolidate AI workloads onto one governed substrate |
| #20 | P | Hybrid architecture that "enables seamless integration and processing of structured, semi-structured, and unstructured data" | Abstract | Pattern (design) | Unstructured handling in a hybrid estate |
| #28 | P | Data mesh and fabric as architectures for hybrid data products and agentic AI | Abstract | Pattern (conceptual) | — |

**Mechanisms not shown:**
- whether the fabric's unified metadata layer exposes machine-readable APIs that agents use across platforms;
- whether retrieval through the fabric honours source policies.

**Evidence strength:** 3 P, design or conceptual. **Thin.**

---

## 4. Implications for the coding kit (author decisions, not coding)

1. **Level-5 attainability (F2).** Record in the kit that no reference implementation located in September 2026 enforces source-table policies on vector retrieval natively; policy-inheriting retrieval is built with application-level filters. Two options:
   - **(a) Keep level 5 as written.** It is then likely unattained, and the AIRD column compresses to levels 1–4.
   - **(b) Add a sentence** that level 5 is met when the platform supplies the CDC-maintained index and the means (attribute filters bound to the authenticated identity) to enforce the source policy at query time. This option admits an application-level mechanism.

   Either is defensible; the choice must be made **before** coding and declared.
2. **Profile boundary for the open stack (F3).** State whether the C2/C4/C6 reference profiles include an MLflow-class lifecycle layer and a Feast-class feature store. The C1 warehouse has the equivalents built in, so omitting them from C2 would compare a product suite against a bare stack.
3. **Dating rule.** Add to Part 1: *"Where a primary source's factual claim about a product class is contradicted by current documentation of the reference implementation, the primary source is used for the mechanism it describes, not for the current state of the class."* F1 needs it; PORT F1 needed it too.
4. **Evidence inventory (Part 4).** The kit expected AIRD S for C2, C4, C6 and M elsewhere.
   - C2 holds at S for levels 1–4.
   - C4 is supported (3 row-specific P).
   - C3 and C5 have no row-specific evidence.
   - C6 and C7 are thin.
   - Level 5 is unsupported everywhere.

## 5. Open items

- **N05k** needs a Garousi appraisal to confirm S tier; until then treat it as T.
- **Behaviour of BigQuery vector search under row-level policies** is undetermined. A targeted check of the `VECTOR_SEARCH` reference page, or a statement from Google, would settle it.
- **Snowflake caller's-rights execution for Cortex Search**, promised in April 2025: re-check release notes before coding.
- **Spot-check** of web quotations (plan step 5).
