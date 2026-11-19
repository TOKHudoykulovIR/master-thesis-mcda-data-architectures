# Evidence pack — PORT (Portability and lock-in)

**Version** 1.0 · **Assembled** 26 September 2026 · **Coding kit** v1.0, passport M4 · **Register** `source-register.xlsx`

---

## 0. How to use this pack

**This pack contains no scores.** It contains quotations, where each one came from, how strong the source is, and which anchor mechanism the quotation shows. Scores are assigned by the coders, independently, on the coding sheet.

**Scale being coded (M4).**

| Level | Mechanism the evidence must show |
|---|---|
| 1 | Proprietary formats and catalog end-to-end; exit = full pipeline rewrite plus bulk-export cost; single-engine only |
| 2 | Data exportable via standard interfaces, but pipeline logic, semantics and catalog proprietary; high rework |
| 3 | Open table format at the core; compute engine substitutable with moderate rework; catalog proprietary |
| 4 | Open table format **and** open catalog; **multiple engines read** the same data through the catalog; documented exit paths exist |
| 5 | Level 4, **and multiple engines write** through the same open catalog, demonstrated; exit penalty limited to operational effort |

**Reference implementations.** Cloud DWH = Snowflake (primary), BigQuery (cross-check). Open lakehouse = Apache Iceberg + Spark/Trino on object storage; Databricks cited as the managed variant. A cell scores the **reference profile**, not a product: for each product quotation the "Pattern / product" column says whether the finding follows from the architectural pattern or from one vendor's implementation.

**Tiers** (kit Part 1). **P** primary — peer-reviewed or open specification. **S** secondary — grey source with Garousi ≥4 reporting measurement or first-hand experience; carries a cell only if two independent S sources concur. **T** tertiary — vendor documentation, analyst assertion; never carries a cell alone.

**How quotations were obtained.** Corpus abstracts are copied verbatim from the Zotero export. Web pages were retrieved with a page-reading tool instructed to return exact sentences; the tool can occasionally trim or merge sentences. Every web quotation carries its URL and must be spot-checked against the live page before coding (plan step 5). Quotations marked † were checked twice against a second page of the same source and agree.

**Access date for all URLs:** 26 September 2026.

---

## 1. Findings that cut across cells — read before coding

### F1. The write-asymmetry rationale in the coding kit is out of date

The kit (M4, "Why") justifies level 5 by G14: *"Certain engines (for instance, Snowflake) do not support writing to external catalogs. You might end up in a situation where only one engine can write to the Iceberg table, and the other engine can only read."* G14 is dated **17 March 2025**.

Snowflake has since shipped write support in both directions, both generally available:

- **17 Oct 2025** — Snowflake writes to Iceberg tables owned by an **external** REST catalog: *"Write operations for externally managed Iceberg tables"* and *"Catalog-linked databases that connect to external Iceberg REST catalogs"* moved to GA, with *"INSERT, UPDATE, DELETE, MERGE"* [N02c].
- **26 May 2026** — **external engines** write to Snowflake-managed Iceberg tables: *"You can read and write to Snowflake-managed Iceberg v2 and v3 tables from any external query engine that supports the open Iceberg REST protocol, such as Apache Spark™."* [N02e] †

**Internal contradiction in the vendor's own documentation.** The general Iceberg page still says *"Third-party clients can't append to, delete from, or upsert data to Iceberg tables that use Snowflake as the catalog"* [N02a]. The Horizon-specific page [N02d] and the dated release note [N02e] say the opposite and are later and more specific. The coder should treat N02a's sentence as stale.

**What remains asymmetric** — restrictions now depend on **which catalog owns the table**, not on which engine is used:

| Situation | Restriction | Source |
|---|---|---|
| Unity Catalog **foreign** Iceberg tables (owned by another catalog) | external clients read only | N04b |
| Unity Catalog **Delta** tables exposed as Iceberg | external clients read only | N04b |
| Unity Catalog, any external client | *"can't run table maintenance operations, such as expiring snapshots and removing orphan files"* | N04b |
| BigQuery via its Iceberg REST catalog endpoint | *"You can't create or modify tables … using BigQuery data definition language (DDL) or data manipulation language (DML) statements."* | N03c |
| Snowflake-managed tables written from external engines | no CTAS; *"Equality deletes aren't supported"*; *"Writing to shared Iceberg tables isn't supported"*; no rollback | N02d |
| Snowflake writing to Unity-managed tables | vended credentials *"work for reads only"*; writes need a manually configured external location | N04c (Aug 2025, may be superseded) |

**Consequence for coding.** At the level of the architectural pattern, multi-engine **write** through one open REST catalog is now demonstrated by several independent implementations (Polaris, Unity Catalog managed Iceberg, Snowflake Horizon, Trino and Spark as writers). What is not uniform is write access **across catalog ownership boundaries** and table maintenance by non-owning engines. Whether that meets "multiple engines write through the same open catalog, demonstrated" is the coder's judgement. The kit's M4 "Why" paragraph should be amended either way (§4).

### F2. The platform axis is converging

The reference warehouse now reads and writes open-format tables in open catalogs (F1), so a Snowflake estate can sit at the lakehouse end of PORT. The C1 profile excludes this by definition: *"engine-native proprietary storage & table format"*, *"Ideal-type boundary. Excludes … any lakehouse-format sidecars."* C1, C3 and C5 are therefore coded on **native** storage; the Iceberg path counts as a documented **exit path** for those cells, not as their storage model.

This is an **author decision to record in the thesis**, not a coding question: either keep the ideal-type boundary (the grid stays analysable, but the warehouse column describes a shrinking share of real estates) or add a variant. The pack assumes the boundary is kept.

### F3. The operating model changes PORT only through the sharing mechanism

No source located compares portability across operating models on the same platform. The one mechanism in the evidence that differs by row is **how domains share data with each other**: C5 relies on the warehouse's native sharing, which is platform-bound (C5 evidence below); C6 can use open protocols. C3 and C4 share within one engine or one catalog and add no sharing layer. The coder decides whether that mechanism is large enough to move a cell by a level.

### F4. Portability has a measured performance cost

#70 reports that federated access through an open lakehouse removed data copies and cut operational steps by 33–44% against BigQuery/Snowflake native tables, while *"query latency may increase by up to a factor of 2.6 compared with native tables."* This bears on the "switch penalty" component of level 5 only indirectly; it is recorded so that it is not double-counted under PORT and TCO.

---

## 2. Sources in this pack

| ID | Source | Tier | Notes |
|---|---|---|---|
| #1 | Lakkireddy (2026), Iceberg/Delta/Hudi comparison, JAIT | P | Abstract; Spark-only experiments |
| #15 | Ginter & Leis (2026), Active Data Lakes, PVLDB | P | Abstract |
| #33 | Papp & Bub (2026), Patterns for Data Mesh and Data Space | P | Abstract |
| #60 | Schneider et al. (2025), Data Products across platforms, GI | P | Abstract; industry perspective |
| #64 | Puttaswamy et al. (2025), Delta Sharing, PVLDB 18, p. 5197 | P | Full text; **authors are Databricks employees** — vendor interest in the comparison with warehouses |
| #69 | Shafiq et al. (2026), Iceberg multi-platform interoperability | P | **Abstract only** — full text requested (To download, High) |
| #70 | Miyamoto & Kasuga (2025), Enterprise Data Science Platform | P | Abstract; production deployment |
| #73 | Guimaraes & Araujo (2026), TPC-DS on open table formats, SciTePress | P | Full text |
| #81 | Tlemcani et al. (2026), ETL to Modern Data Stack SLR | P | Full text on file |
| #93 | Xu et al. (2026), LakeHelm, PVLDB | P | Abstract |
| #94 | Armbrust et al. (2021), Lakehouse, CIDR | P | Full text; authors from Databricks |
| #99, #4, #89, #76 | Data fabric papers | P | Abstracts; C7 only |
| #105 | Espinoza et al. (2025), evaluation framework, QIP | P | Full text on file; scores are practitioner judgements on **products** |
| #137 | Xin et al. (2025), FedLakehouse | P | Abstract |
| N01a | Apache Iceberg table specification — raw.githubusercontent.com/apache/iceberg/main/format/spec.md | P | Open specification |
| N01b | Iceberg REST Catalog OpenAPI — raw.githubusercontent.com/apache/iceberg/main/open-api/rest-catalog-open-api.yaml | P | Open specification |
| G11 | Apache Polaris — polaris.apache.org | S | Open-source project site |
| G14 | olake.io, *Why move to Apache Iceberg* (17 Mar 2025) — olake.io/iceberg/move-to-iceberg/ | S | Write limitation now superseded (F1) |
| G15 | Jericó, *From Delta Lake to Apache Iceberg: migration blueprint* (Dec 2025) — matheusjerico.medium.com/… | S | Located; not quoted in this version |
| G12 | Databricks, *Open Table Formats Explained* — databricks.com/blog/open-table-formats | T | Located; not quoted — spec evidence suffices |
| G13 | Dremio, *Apache Iceberg vs Delta Lake* — dremio.com/blog/apache-iceberg-vs-delta-lake/ | T | Located; not quoted |
| N02a | Snowflake docs, Iceberg tables — docs.snowflake.com/en/user-guide/tables-iceberg | T | Contains a stale sentence (F1) |
| N02b | Snowflake docs, catalog-linked database — …/tables-iceberg-catalog-linked-database | T | |
| N02c | Snowflake release note, 17 Oct 2025 — …/release-notes/2025/other/2025-10-17-iceberg-external-writes-cld-ga | T | |
| N02d | Snowflake docs, external engines via Horizon — …/tables-iceberg-query-using-external-query-engine-snowflake-horizon | T | |
| N02e | Snowflake release note, 26 May 2026 — …/release-notes/2026/other/2026-05-26-tables-iceberg-query-using-external-query-engine-snowflake-horizon-writes-ga | T | |
| N02f | Snowflake docs, Secure Data Sharing — …/user-guide/data-sharing-intro | T | |
| N02g | Snowflake docs, unloading data — …/user-guide/data-unload-overview | T | |
| N03a | Google Cloud docs, Iceberg managed tables in BigQuery — docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery | T | |
| N03b | Google Cloud docs, exporting table data — docs.cloud.google.com/bigquery/docs/exporting-data | T | |
| N03c | Google Cloud docs, BigLake metastore Iceberg REST catalog — docs.cloud.google.com/biglake/docs/blms-rest-catalog | T | |
| N04a | Trino docs, Iceberg connector — trino.io/docs/current/connector/iceberg.html | T | Open-source project documentation |
| N04b | Databricks docs, Iceberg REST access to Unity Catalog — docs.databricks.com/aws/en/external-access/iceberg | T | |
| N04c | Databricks Community technical blog, *Iceberg interoperability Databricks ↔ Snowflake* (14 Aug 2025) — community.databricks.com/…/ba-p/128406 | T | Vendor community; dated |

---

## 3. Evidence by configuration

### C1 — Cloud DWH × centralised

*Profile:* managed warehouse on engine-native proprietary storage and table format; engine-native catalog; one central team.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #94 | P | "commercial warehouses lock data into proprietary formats that increase the cost of migrating data or workloads to other systems." | §1 Introduction | Pattern | Proprietary storage format; migration cost (levels 1–2) |
| #94 | P | "there is no way to directly access the internal warehouse proprietary formats." | §2 Motivation | Pattern | No direct multi-engine access to native storage |
| #64 | P | "data warehouses store data in proprietary formats, and thus do not give direct data access to external tools." | §1 | Pattern (vendor-authored) | As above |
| #70 | P | "Traditional data warehouses require copying data into vendor-specific environments, while direct data access across different analytics platforms remains technically challenging." | Abstract | Pattern | Single-engine access to native data |
| N02g | T | "Use the COPY INTO <location> command to copy the data from the Snowflake database table into one or more files in a Snowflake or external stage." | Overview | Product | Bulk export through a standard interface (level-2 mechanism) |
| N03b | T | Export formats CSV, JSON, Avro, Parquet; "BigQuery can export up to 1 GB of logical data size to a single file…"; "The only supported export location is Cloud Storage." | Export overview | Product | Bulk export to open file formats, with constraints (level 2) |
| #105 | P | Practitioner scores for "support for open formats": DWH 50, DL 80, DLH 80 | p. 99, Table 4 | **Product** (MS SQL vs Azure Databricks) | Relative judgement, warehouse roughly half the lakehouse |
| N02a–N02e | T | Snowflake reads and writes Iceberg tables in external catalogs (F1) | — | Product | **Exit path** to open format exists; outside C1 storage model (F2) |

**Next-level mechanism not shown.** Level 3 requires an open table format at the core — excluded by the C1 profile. **Gap:** no source quantifies the rework of pipeline logic (SQL dialect, stored procedures, engine-specific features) on exit; the level-2 wording "high rework" is therefore supported by mechanism (#94, #64) but not by a measured rework figure.

**Evidence strength:** 4 P (2 vendor-authored), 3 T. Mechanism well documented; exit cost not quantified.

---

### C2 — Open lakehouse × centralised

*Profile:* object storage; open table format; open catalog; Spark and SQL engines on the same tables; one central team.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| N01a | P | "Serializable isolation -- Reads will be isolated from concurrent writes and always use a committed snapshot of a table's data." | Goals | Pattern | Open format with concurrent writers by design |
| N01a | P | "Writers create table metadata files optimistically, assuming that the current version will not be changed before the writer's commit. Once a writer has created an update, it commits by swapping the table's metadata file pointer from the base version to the new version." | Optimistic concurrency | Pattern | Multi-writer commit protocol defined in the open spec (level-5 precondition) |
| N01b | P | "Commit updates to a table. Commits have two parts, requirements and updates. Requirements are assertions that will be validated before attempting to make and commit changes." | `updateTable` | Pattern | Open catalog API coordinates writes from any client (level 4–5) |
| G11 | S | "It implements Iceberg's REST API, enabling seamless multi-engine interoperability across a wide range of platforms, including Apache Doris™, Apache Flink®, Apache Spark™, Dremio® OSS, StarRocks, and Trino." | Home page | Pattern (open-source catalog) | Open catalog; multiple engines |
| N04a | T | "The connector provides read access and write access to data and metadata in Iceberg"; supports INSERT, UPDATE, DELETE, MERGE; catalogs include "a REST catalog" | Iceberg connector | Product (OSS) | A second engine writes through the same open catalog type |
| N04b | T | "The Apache Iceberg REST catalog lets supported clients, such as Apache Spark, Apache Flink, and Trino, read from and write to Unity Catalog-registered Iceberg tables on Databricks." | Overview | Product (managed variant) | Multi-engine write through an open REST catalog — **with the ownership restrictions in F1** |
| N02d / N02e | T | External engines read and write Snowflake-managed Iceberg tables through the Horizon REST API (F1) | — | Product | A warehouse engine is now among the writers |
| #70 | P | "Experimental results demonstrate that major cloud data warehouses and programming environments can directly query EDSP-managed datasets. We implemented and deployed EDSP in an enterprise production environment, confirming interoperability across multiple query engines." | Abstract | Pattern | **Multi-engine read, demonstrated in production** (level 4) |
| #69 | P | "Experimental setups include accessing Snowflake-managed Iceberg tables in Databricks and vice versa… The results show that Iceberg reduces the complexity of data management by automating metadata handling and synchronization" | Abstract | Pattern | Cross-platform read in both directions; **write not stated in abstract** — full text pending |
| #73 | P | "Iceberg's engine-agnostic design enables Trino, Flink, and Hive integration—critical for heterogeneous cloud environments." | Body (section not recorded) | Pattern | Engine substitutability (assertion in paper; experiments were Spark-only) |
| #93 | P | "The lakehouse architecture decouples system design into interoperable subsystems—execution engines (e.g., Spark, Trino, Presto) and table formats (e.g., Delta Lake, Iceberg, Hudi)—giving users flexibility to mix and match." | Abstract | Pattern | Engine and format substitutability |
| #81 | P | Vendor neutrality discussed in 48 of 141 studies; open table formats identified as the mechanism insulating against lock-in | §5.1 | Pattern | Corroborates open-format mechanism across the literature |
| G14 | S | "If you ever decide to leave a particular vendor, your data remains in open file formats, and your Iceberg table metadata can still be read by other platforms." | Lock-in section | Pattern | Documented exit path (level 4) |
| #105 | P | DLH 80 on open-format support | p. 99 | Product | Relative judgement |

**Qualifications recorded in the evidence.**

- **Physical data independence traded for interoperability.** #15: "Apache Parquet is the de facto standard file format for relational data in data lakes. This standardization is fundamental to interoperability, but it comes at the cost of physical data independence because query engines integrate tightly with Parquet." Portability of **engines** is bought with lock-in to a **file format**.
- **Format choice is itself a commitment.** #1 finds workload-dependent trade-offs between Iceberg, Delta and Hudi. Migration between formats is documented (G15), and interoperability layers exist (G12, UniForm), so the switch penalty between formats is operational rather than a rewrite.
- **Maintenance is not portable everywhere.** N04b: external clients cannot expire snapshots or remove orphan files on Unity-managed tables; the owning engine keeps that role.

**Next-level mechanism.** Level 4 mechanisms are shown by P and S sources. Level 5 turns on F1: multi-engine write through one open catalog is demonstrated by several implementations; ownership-boundary and maintenance restrictions remain.

**Evidence strength:** 8 P, 2 S, several T. The strongest-evidenced cell in the PORT column.

---

### C3 — Cloud DWH × hub-and-spoke

*Profile:* as C1, plus per-domain schemas or databases inside one shared engine account.

**No source located addresses portability of the hub-and-spoke model on a warehouse as distinct from the centralised model.** The platform evidence for C1 applies unchanged: same engine, same native storage, same catalog. Per F3, hub-and-spoke adds no inter-domain sharing layer — domains share within one account.

**Decision left to the coder:** whether PORT for C3 equals C1 (platform-driven criterion, kit Part 4 reading) or differs for a reason the coder can source.

**Evidence strength:** none specific to the cell; inherits C1.

---

### C4 — Open lakehouse × hub-and-spoke

*Profile:* as C2, plus self-serve platform; shared open catalog with a central policy plane and domain stewards.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #33 | P | "It identifies two complementary Data Mesh patterns: logically decentralized meshes, in which domains own data products on a shared platform, and physically decentralized meshes, in which domains operate separate environments and federate discovery and access." | Abstract | Pattern | The C4 variant is "logically decentralized": one shared platform and catalog |
| N04b | T | Managed Iceberg tables: external clients read and write; foreign tables: read only | Requirements table | Product | Ownership rule for writes (managed vs foreign). *Inference, not in the source:* with one hub-owned catalog every domain table is "managed", so the F1 restrictions would not arise inside the estate |

**Platform evidence:** as C2.

**Row-specific mechanism.** A single hub-owned catalog means every domain writes through the same open catalog — the configuration in which the level-5 mechanism is best demonstrated (F1). **Gap:** no source measures C4 against C2 on portability.

**Evidence strength:** inherits C2; 1 P specific to the row.

---

### C5 — Cloud DWH × federated

*Profile:* separate warehouse accounts per domain, same engine class, linked by the engine's native sharing; thin or no central platform.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| N02f | T | "With Secure Data Sharing, no actual data is copied or transferred between accounts. All sharing uses Snowflake's services layer and metadata store." | How sharing works | Product | Inter-domain integration runs through a proprietary service |
| N02f | T | "Any full Snowflake account can both provide and consume imported data." Reader accounts: "a reader account can only consume data from the provider account that created it." | Consumers | Product | Sharing confined to the vendor's platform |
| #64 | P | "All data warehouses discussed above restrict sharing to be only within their system/cloud," which forces providers to "maintain ETL pipelines to copy and update data to different clouds." | §10 Related work | Pattern (vendor-authored) | Native warehouse sharing is platform-bound |
| #60 | P | "industrial practice shows that analytics architectures of large enterprises are not organized centrally, but instead consist of many differently shaped data platforms that are operated by separate business units… Due to this heterogeneity, the sharing of data between different business units becomes difficult from both a technical and organizational perspective." | Abstract | Pattern | Federated platform ownership complicates interoperability |
| #33 | P | "physically decentralized meshes, in which domains operate separate environments and federate discovery and access." | Abstract | Pattern | C5 is the physically decentralised variant |
| N02d | T | "Writing to shared Iceberg tables isn't supported" | Limitations | Product | Even the open-format path does not extend to shared tables |

**Row-specific mechanism (F3).** Inter-domain integration depends on a proprietary sharing service on top of proprietary storage. Exit therefore means re-establishing every inter-domain link in addition to migrating each domain. **Gap:** no source quantifies this additional exit cost.

**Evidence strength:** 3 P (1 vendor-authored), 2 T sources. Mechanism clear; magnitude not quantified.

---

### C6 — Open lakehouse × federated

*Profile:* domain-owned lakehouse workspaces on shared open storage and catalog standards; data products with contracts; thin self-serve platform; computational governance.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #64 | P | "The client can then take the list of access tokens and read files in parallel at massive bandwidth, without streaming through the sharing server"; open-source connectors account for "about 40% of the recipients", using "15+ different connectors" | §3.4, §8.5 | Pattern (open protocol, vendor-authored) | Open cross-platform sharing protocol, demonstrated at scale |
| #64 | P | "Even though writes are possible, we limit URLs to be read-only in Delta Sharing." | §4.1.1 | Pattern | Cross-domain sharing is **read**; writes stay with the owning domain |
| N01b | P | Iceberg REST commit API (see C2) | — | Pattern | Open catalog interface usable across domain workspaces |
| #137 | P | "FedLakehouse is proposed, which achieves federated data management among heterogeneous lakehouses and relational databases. Providing a unified data access view…" | Abstract | Pattern | Federated access across separately operated lakehouses (research prototype) |
| #33 | P | Physically decentralised mesh (see C5) | Abstract | Pattern | C6 as the open-standard physically decentralised variant |
| #30 | P | "federated computational governance, in which data governance policies are defined and enforced at the domain level while respecting organization-wide standards" | Abstract | Pattern | Shared standards across domains; **portability detail only in full text** (To download, High) |

**Platform evidence:** as C2.

**Row-specific mechanism (F3).** Inter-domain sharing can run on an open protocol (Delta Sharing) or a shared open catalog. The evidence shows cross-domain **read** portability; **write** stays with the owning domain by design. If domains run **separate** catalogs, the ownership restrictions in F1 (foreign tables read-only, maintenance by owner only) apply between domains. **Gap:** no source examines portability across several independently operated open catalogs.

**Evidence strength:** 5 P (1 vendor-authored, 1 prototype); inherits C2.

---

### C7 — Hybrid / multi-platform (was: data fabric overlay)

> **Update 1 Oct 2026 (kit K15).** C7 is redefined as *Hybrid / multi-platform*: lakehouse core plus warehouse serving layer, no fabric layer assumed. Quotations below about a fabric or metadata overlay apply only where such a layer exists; coders treat them as an upper bound for C7, not as its reference profile.

*Profile:* coexisting warehouse and lakehouse; unified metadata/catalog layer; federated query and virtualisation; central policy plane.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #89 | P | "We will first introduce the concept of a Data Fabric which is becoming the de facto standard framework for enterprise data interoperability." | Abstract | Pattern | Fabric positioned as interoperability layer (assertion) |
| #4 | P | "Instead of storing the full amount of data in a centralized data lake, we choose to centralize the metadata into the data warehouse." | Abstract | Pattern | Metadata-centred overlay; underlying stores unchanged |
| #99 | P | M-Data-Fabric "realizes the overall use of different data sources rather than reuse according to the process of metadata identification, analysis, integration… and knowledge map construction." | Abstract | Pattern | Metadata overlay across heterogeneous sources |
| #137 | P | Unified access view over heterogeneous lakehouses and relational databases (see C6) | Abstract | Pattern | Federated query layer |
| #70 | P | Latency up to 2.6× against native tables under federated access (F4) | Abstract | Pattern | Cost of the virtualisation path |

**Mechanisms not shown.** Portability of each underlying platform is unchanged by the overlay: the warehouse part carries C1 evidence, the lakehouse part C2 evidence. **Gap:** no source was located on whether the fabric layer — metadata graph, virtualisation engine, policy plane — is itself portable, or on the lock-in it introduces. The C7 cell will rest on mechanism inference plus the C1/C2 evidence.

**Evidence strength:** 5 P, all abstracts, mostly conceptual or prototype. **Thin.**

---

## 4. Implications for the coding kit (author decisions, not coding)

1. **Amend M4 "Why"** (kit v1.0, Part 2): replace the G14-based statement with F1. Suggested text: *"Multi-engine write through one open REST catalog is demonstrated by several implementations as of 2026. What remains non-uniform is write access across catalog-ownership boundaries (foreign or shared tables) and table maintenance by non-owning engines. Level 5 requires multi-engine write within the estate's catalog, demonstrated."*
2. **Keep or revise the C1/C3/C5 ideal-type boundary** in view of F2. Keeping it is defensible; the convergence should be stated in Chapter 4 as a limitation of the platform axis.
3. **Update the evidence inventory** (Part 4): PORT expected strengths hold for C1, C2 and C4. **C3 has no row-specific evidence** (was S). **C7 is thin** (was M).
4. **Update the known-sources list** for PORT: G14 is now a superseded source; add N01a, N01b, N02c–N02f, N04b.

## 5. Open items

- **#69 full text** — needed to see whether the Snowflake ↔ Databricks experiments covered writes.
- **#30 full text** — needed for C6 portability detail.
- **Spot-check** of web quotations against live pages (plan step 5).

## 6. Spot-check notes (17 October 2026)

All PORT quotations in the sample were found as quoted (Q01, Q02, Q03, Q14, Q15: Match).
- **N03c** has moved to docs.cloud.google.com/lakehouse/docs/set-up-lakehouse-iceberg-rest-catalog (BigLake renamed Lakehouse on 20 April 2026). The quoted limitation continues "…using BigQuery data definition language (DDL) or data manipulation language (DML) statements"; the quotation in §1 already ends with that tail. Register updated.
- **#69 full text** located (author's homepage, Tampere University). Its performance experiments measure query latency only; a step that updates data in Databricks and checks it in Snowflake is described, but no result is reported. The full text therefore shows cross-platform reads, not writes. For the write mechanism of PORT level 5, the pack relies on the open specifications and engine documentation (N01a, N01b, N04a, N04b), not on #69.
