# Evidence pack — SECC (Security and compliance posture)

**Version** 1.0 · **Assembled** 26 September 2026 · **Coding kit** v1.1, passport M6 (+ S1 gating rule) · **Register** `source-register.xlsx`

---

## 0. How to use this pack

The rules of `pack-PORT.md` §0 apply here unchanged:
- the pack contains no scores;
- sources are tiered P / S / T, and a tier-T source never carries a cell alone;
- web quotations were taken with a page-reading tool and must be spot-checked;
- all URLs were accessed on 26 September 2026.

Kit v1.1 amendments K3 and K6 apply: the warehouse profiles stay on native storage, and an old primary source is used for the mechanism it describes, not for the current state of products.

**Scale being coded (M6).**

| Level | Mechanism the evidence must show |
|---|---|
| 1 | Coarse-grained access control only; fragmented audit logs; no formal compliance mappings |
| 2 | Role-based access; partial audit trails; platform-level certifications only |
| 3 | Fine-grained (row/column) controls; centralised audit; major certifications mapped (SOC 2 / ISO 27001 class); single-region residency control |
| 4 | Level 3 + policy-as-code / attribute-based control; lineage-integrated audit; multi-region residency options; strong isolation between domains/tenants |
| 5 | Level 4 + **uniform policy enforcement across all engines and domains, including federated topologies**; end-to-end provable auditability; sovereignty options (customer-managed keys, sovereign-region deployment) |

**S1 gating rule (kit M6).** In scenario S1, a configuration coded **below 3** is excluded before ranking. A score of 2 versus 3 therefore changes the S1 result, not only the S1 score. Code the 2/3 boundary with particular care and record the reason.

---

## 1. Findings that cut across cells — read before coding

### F1. Fine-grained policy and multi-engine openness pull against each other

Level 5 requires *uniform policy enforcement across all engines*. The evidence shows that row and column policies do not travel with open-format data by default, because engines receive **storage credentials** and must enforce the policy themselves.

| Where | What the source says | Tier |
|---|---|---|
| Open lakehouse, the problem stated | Before Lakeguard, "fine-grained access control could only be enforced for SQL workloads, while big data processing with frameworks such as Apache Spark relied on coarse-grained governance at the file level with cluster-bound data access." [#61] | P (vendor-authored) |
| Unity Catalog (managed lakehouse variant) | "You cannot use Iceberg REST catalog or Unity REST APIs to access tables with row filters or column masks."; "OpenSharing providers cannot share tables with table-level row filters or column masks." [N07e] | T |
| Apache Polaris (open catalog) | RBAC on catalogs, namespaces and tables, with privileges such as `TABLE_READ_DATA` and `TABLE_WRITE_DATA`; principals receive "short-lived read-only storage credentials" or "short-lived read+write storage credentials". Row- and column-level policy is not documented in Polaris; advanced authorisation is delegated to external policy decision points such as OPA. [N07f] | S |
| Trino (open engine) | Enforces row filters and column masks supplied by OPA: filters act as an additional `WHERE` clause; "only a single column mask may be returned for a given column" [N07g] | T |
| Snowflake as the catalog | "Tables protected by fine-grained data policies, such as masking and row access policies, can be accessed with external engines", with a documented configuration to **enforce** those policies when Spark queries them [N02d] | T |
| BigQuery Storage Read API | "Row access policies that incorporate subqueries aren't compatible with the BigQuery Storage Read API. The BigQuery Storage Read API only supports simple filter predicates." [N07k] | T |

**Consequence for coding.**
- **Warehouse (single engine).** Enforcement is uniform by construction, because every query goes through the one engine.
- **Open lakehouse.** Uniform enforcement holds only where each engine enforces the catalog's policy.
  - Unity Catalog blocks external access to protected tables rather than enforcing on the external engine.
  - Polaris leaves row and column enforcement to the engines.
  - Snowflake has extended its own policies to Spark as an external engine.

This is the **same trade-off seen from the SECC side as PORT F1**: the more engines may write and read, the harder uniform fine-grained policy becomes. The coder should not double-count it, but should also not treat the two criteria as independent here.

### F2. Erasure leaves data behind for a documented window on both platforms

This is context, not an M6 anchor: erasure belongs to the Governance Friction candidate (GOVF), which is re-admitted only if Round 1 triggers rule R4. It is recorded because S1 is a regulated bank.

- **Legal requirement.** GDPR Art. 17(1): the controller shall erase personal data "without undue delay"; Art. 17(2) extends this to informing other controllers of "any links to, or copy or replication of, those personal data" [G27].
- **Iceberg.** A deleted row's data file "may be deleted from the file system when the snapshot in which it was deleted is garbage collected, assuming that older snapshots have also been garbage collected" [N01a]. Physical erasure waits for snapshot expiry, which is an operator action.
- **Snowflake.** Time Travel is configurable "from 0 up to 90 days" (Enterprise). Fail-safe then provides "a (non-configurable) 7-day period during which historical data may be recoverable by Snowflake" [N07h, N07i].
- **Hub-and-spoke on Databricks.** The hub provides "GDPR processes across domains (e.g. right to be forgotten requests)" [G05].

### F3. The operating model matters more for SECC than for any other coded criterion

SECC is the only criterion so far with a **body of row-specific evidence**: the data mesh governance literature. That literature proposes mechanisms for federated policy — computational governance, contracts, platform automation — and reports that the transition is hard. It does **not** demonstrate uniform enforcement across independently operated domains in production.

| Source | Tier | What it shows |
|---|---|---|
| #133 (15 interviews) | P | "organizations have difficulties with the transition toward federated data governance associated with the data mesh concept" |
| #2 | P | Fabric: "a centralized governance model… ideal for organizations seeking uniform governance policies"; mesh "requires strong coordination mechanisms to ensure data consistency, security, and interoperability across domains" |
| #63 | P | Approaches "to drive governance through platform means", "drawn from concrete experiences of implementing a fully-functional data mesh platform" |
| #136 | P | "Governance tasks, such as ensuring data protection compliance, are notoriously challenging to automate"; proposes contract-based verification of declassification |
| #87 | P | Formal definition of federated computational governance, with a **blockchain-based prototype** as validation |
| #30 | P | 8 design decisions and 104 options for federated computational governance, from 49 grey sources and 6 practitioner interviews (abstract only) |
| #51 | P | Saxo Bank pilot: "DG solution involves change management and alignment of incentives and mere technology is not enough" |

---

## 2. Sources in this pack

| ID | Source | Tier | Notes |
|---|---|---|---|
| #2 | Mehta et al. (2025), Governance in data fabric vs data mesh | P | Abstract |
| #4, #84 | Data fabric architecture (2022); government compliance for a data fabric | P | Abstract / title only |
| #5 | Javeri et al. (2026), Federated metadata for lakehouse AI | P | Abstract |
| #30 | Tonnarelli et al. (2026), Design decisions for federated computational governance | P | Abstract; **full text requested** |
| #49 | Oppold et al. (2025), Data contracts at ZEISS SMT, experience report | P | Abstract |
| #51 | Joshi et al. (2021), Saxo Bank case | P | Abstract; open preprint available |
| #57 | Kumara et al. (2024), Data mesh from theory to practice | P | Abstract; 3 case organisations |
| #59 | Fadler & Legner (2022), Data ownership revisited | P | Abstract; 4 cases |
| #61 | Grund et al. (2025), Databricks Lakeguard | P | Abstract; vendor-authored |
| #63 | Wider et al. (2023), Decentralised governance in a mesh platform | P | Abstract; open on arXiv |
| #66, #83 | Lakehouse governance frameworks (2024, 2026) | P | Abstracts |
| #77 | Singi et al. (2021), Data-residency-compliant architecture | P | Abstract; full text requested |
| #87 | Dolhopolov et al. (2024), Federated governance in data mesh | P | Abstract; MDPI open |
| #96 | Sienkiewicz & Wrembel (2021), Data in a big financial institution | P | Abstract |
| #133 | Bode et al. (2024), Industry insights from data mesh | P | Abstract; IEEE Access open |
| #136 | Wider et al. (2024), Automating federated governance | P | Abstract; full text requested |
| #140 | Fannouch et al. (2026), Trustworthy DataOps, medallion lakehouse under mesh | P | Abstract |
| #142 | Chandra et al. (2025), Unity Catalog | P | Abstract; vendor-authored |
| G05 | Databricks, *Building a Data Mesh Based on the Databricks Lakehouse, Part 2* (19 Oct 2022) · databricks.com/blog/building-data-mesh-based-databricks-lakehouse-part-2 | T | |
| G27 | GDPR Art. 17 · gdpr-info.eu/art-17-gdpr/ | P | Regulatory text |
| N01a | Iceberg table spec (see PORT) | P | |
| N02d | Snowflake docs, external engines via Horizon (see PORT) | T | |
| N02f | Snowflake docs, Secure Data Sharing (see PORT) | T | |
| N07a | Snowflake docs — Row access policies · docs.snowflake.com/en/user-guide/security-row-intro | T | |
| N07b | Snowflake docs — Tag-based masking policies · …/user-guide/tag-based-masking-policies | T | |
| N07c | Snowflake docs — Access History · …/user-guide/access-history | T | |
| N07d | Snowflake docs — Tri-Secret Secure · …/user-guide/security-encryption-manage | T | |
| N07e | Databricks docs — Row filters and column masks · docs.databricks.com/aws/en/tables/row-and-column-filters | T | |
| N07f | Apache Polaris — Access control · polaris.apache.org/in-dev/unreleased/managing-security/access-control/ | S | Open-source project docs (same status as G11) |
| N07g | Trino docs — OPA access control · trino.io/docs/current/security/opa-access-control.html | T | |
| N07h | Snowflake docs — Time Travel · …/user-guide/data-time-travel | T | |
| N07i | Snowflake docs — Fail-safe · …/user-guide/data-failsafe | T | |
| N07j | Snowflake docs — Regulatory compliance · …/user-guide/intro-compliance | T | |
| N07k | Google Cloud — Row-level security intro · docs.cloud.google.com/bigquery/docs/row-level-security-intro | T | |
| N07l | Google Cloud — Column-level access control · docs.cloud.google.com/bigquery/docs/column-level-security-intro | T | |
| N07m | Google Cloud — CMEK · docs.cloud.google.com/bigquery/docs/customer-managed-encryption | T | |
| N07n | Snowflake docs — Regions · …/user-guide/intro-regions | T | |

---

## 3. Evidence by configuration

### C1 — Cloud DWH × centralised

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| N07a | T | "Snowflake supports row-level security through the use of row access policies to determine which rows to return in the query result."; policies restrict even "the object owner… who normally has full access to the underlying data"; "A single policy can be set on different tables and views at the same time." | Overview | Product | Fine-grained row control, including segregation of duties (level 3) |
| N07b | T | "Policy administrators can write a policy once, assign a policy to a tag once, and… have the policy apply to many objects."; columns protected "based on the tag string value of the tag assigned to the column" | Overview | Product | Attribute/tag-based policy (level 4) |
| N07l | T | Column access via policy tags checked "at query time, whether a user has proper access"; dynamic data masking | Overview | Product (BigQuery) | Fine-grained column control (level 3) |
| N07c | T | Access History records "a direct link between the user (i.e. query operator), the query, the table or view, the column, and the data"; column lineage "from the source column to the target column in a write operation"; "Access History requires Enterprise Edition (or higher)." | Overview | Product | Centralised, lineage-integrated audit (level 4) |
| N07j | T | "SOC 1 Type II", "SOC 2 Type II", "ISO-27001", "PCI DSS", "HITRUST CSF", "FedRAMP (Moderate and High)", "C5", "K-FSI"… | Compliance | Product | Major certifications mapped (level 3); sector-specific ones for finance |
| N07n | T | "Each Snowflake account is hosted in a single region."; "any data in an account in a region remains in the region unless users explicitly choose to copy, move, or replicate the data." | Regions | Product | Single-region residency control (level 3); multi-region = separate accounts (level-4 option) |
| N07d | T | Tri-Secret Secure: "the combination of a Snowflake-maintained key and a customer-managed key creates a composite master key"; "If you experience a security breach, you can disable access to your key and halt all data operations" | Encryption | Product | Customer-managed keys (level-5 sovereignty component) — **Business Critical edition only** [N07o] |
| N07m | T | BigQuery CMEK: "you control and manage key encryption keys in Cloud KMS" | Overview | Product (BigQuery) | Customer-managed keys |
| #68 | P | "clinical data warehouses offer strong data governance, stability, and structured reporting, making them well suited for environments that require strict compliance" | Abstract | Pattern | Warehouse pattern associated with strong governance |
| F1 | — | Single engine → uniform enforcement by construction; Snowflake extends policies to Spark when it is the catalog (N02d) | — | Pattern + product | Level-5 "all engines" component, **within the warehouse's own engine** |

**Mechanisms not shown / open.**
- "End-to-end provable auditability" (level 5) has no source beyond Access History.
- Edition dependency [N07o, verified 26 Sep 2026]:
  - **Enterprise** adds row access policies, masking policies, tag-based masking, Access History and Time Travel up to 90 days.
  - **Business Critical** adds customer-managed keys (Tri-Secret Secure), private connectivity, support for PHI/HIPAA and **PCI DSS** data, and cross-account failover/failback.
  - The reference profile must state the edition assumed (kit K7).

**Evidence strength:** 1 P (pattern), 9 T across two vendors that concur. The mechanisms are well documented, but only by vendors. This is kit Part 1's "T never alone" case: the P source supports the pattern, and the T sources supply the mechanisms.

---

### C2 — Open lakehouse × centralised

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| N07f | S | RBAC with catalog roles and privileges on "Catalogs, namespaces, Iceberg tables, views, and policies"; short-lived storage credentials vended per privilege | Access control | Pattern (open catalog) | Role-based access at table level (level 2); fine-grained control **not in the catalog** |
| N07g | T | OPA supplies row filters and column masks to Trino | OPA plugin | Product (OSS engine) | Fine-grained control **per engine** (level 3 for that engine) |
| #61 | P | Fine-grained control historically "could only be enforced for SQL workloads", while Spark "relied on coarse-grained governance at the file level"; Lakeguard enforces "row-level filters, and column masks across all of an enterprise's data and AI workloads" | Abstract | Product (Databricks) | The problem is architectural (file-level credentials); the fix is a product |
| #142 | P | Existing lakehouse catalogs "exhibit key limitations, including inconsistent governance, narrow interoperability"; UC "provides consistent governance" | Abstract | Pattern (open-source catalog, vendor-authored) | Consistent governance claimed at the catalog level |
| N07e | T | Unity Catalog ABAC: "ABAC policies attach at the catalog or schema level and apply automatically to tables and columns based on governed tags." — but protected tables are **not accessible** via Iceberg REST or OpenSharing | Row filters page | Product (managed variant) | Tag-based policy (level 4) **at the cost of multi-engine access** (F1) |
| #83, #66, #6, #140 | P | Governance models and frameworks designed for lakehouses (e.g. #140: "shift-left compliance and improved auditability") | Abstracts | Pattern | Governance is designed in, not inherited from the platform |
| N01a | P | Physical erasure after snapshot garbage collection (F2) | Spec | Pattern | Context only |

**Mechanisms not shown / gaps.**
- **Certifications.** A self-operated open stack has no certification of its own. Certification rests on the cloud provider and the operator. No source located states how organisations map SOC 2 or ISO 27001 controls to a self-assembled lakehouse. The managed variant's certifications were not fetched.
- **Residency and keys.** Object storage sits in a customer-chosen region under customer-controlled keys by construction. No source quoted; this is inference from the profile.
- **Uniform enforcement across engines (level 5)** is not shown for the open catalog alone (F1).

**Evidence strength:** 6 P (2 vendor-authored; 4 framework designs), 1 S, 2 T. Coverage is good for the **problem** and thin for **how the reference stack solves it** without a vendor catalog.

---

### C3 — Cloud DWH × hub-and-spoke

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| G05 | T | Hub provides "GDPR processes across domains (e.g. right to be forgotten requests)" and "data cataloging, lineage, audit, and access control" | Blog | Product context (Databricks), pattern-level claim | Central policy plane and central compliance processes in hub-and-spoke |
| #59 | P | Three ownership types identified across 4 cases: "data, data platform, and data product ownership" | Abstract | Pattern | Separates platform ownership (hub) from product ownership (spokes) — the accountability split of hub-and-spoke |
| #96 | P | Financial institutions "follow strict data governance policies as well as country and international regulations"; "dozens to a few hundreds of data sources… integrated in multiple data warehouses" | Abstract | Pattern | S1-type context: central governance over many warehouses |

**Platform evidence:** as C1. One account means one policy engine and one audit log.

**Row-specific mechanism.** Domain isolation inside one account relies on roles and schemas, not separate tenants. Level 4's "strong isolation between domains/tenants" is therefore a judgement for the coder. No source compares role-based isolation with account-level isolation.

**Evidence strength:** 2 P, 1 T specific to the row; inherits C1.

---

### C4 — Open lakehouse × hub-and-spoke

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| G05 | T | As C3 — hub-provided GDPR processes, audit, access control; domains in separate workspaces ("Self-serve compute resources and orchestration (within Databricks Workspaces)") | Blog | Product context | Central policy plane + workspace isolation between domains (level 4 isolation component) |
| #5 | P | "read-through federation model, centralized access control, and lineage-aware metadata management" | Abstract | Pattern | Central policy plane over lakehouse |
| #140 | P | Trust gates "operated under a Data Mesh model", embedding "policy and regulatory compliance, and lineage/observability" in promotion | Abstract | Pattern | Policy-as-code in pipelines (level 4) |
| #49 | P | Data contracts "help us find a balance between a centralized and decentralized data management strategy" over five years at ZEISS SMT | Abstract | Pattern (experience report) | Contracts as the central-standard mechanism |

**Platform evidence:** as C2, including the F1 tension. **One hub-owned catalog** is the setting in which a single policy plane is feasible.

**Evidence strength:** 3 P, 1 T specific to the row; inherits C2.

---

### C5 — Cloud DWH × federated

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| N07n | T | "Each Snowflake account is hosted in a single region." | Regions | Product | Per-domain accounts give per-domain residency and **hard tenant isolation** (level 4 isolation component) |
| N02f | T | Sharing "uses Snowflake's services layer and metadata store"; "no actual data is copied" | Sharing | Product | Cross-domain access under the provider's control, without copies |
| #133 | P | Difficulties "with the transition toward federated data governance" | Abstract | Pattern | Federated governance is hard in practice |
| #2 | P | Mesh "requires strong coordination mechanisms to ensure data consistency, security, and interoperability across domains" | Abstract | Pattern | Same |
| #51 | P | Saxo Bank: "mere technology is not enough" | Abstract | Pattern (regulated bank, pilot) | Governance in a federated bank setting relies on organisational interventions |

**Mechanisms not shown / gaps.**
- **Audit becomes per account.** Access History is an account-level view (inference). No source shows a consolidated audit across domain accounts, so "centralised audit" (level 3) is a judgement.
- **Policy consistency across accounts.** No source shows whether row and masking policies are defined once and applied across domain accounts, or duplicated per account.
- **Shared data.** No source fetched on whether the provider's row and masking policies are enforced on the consumer side of a share. **Open item.**

**Evidence strength:** 3 P (pattern-level, about federated governance in general), 2 T. The level-3 threshold for S1 depends on the centralised-audit judgement, so this cell is a likely point of disagreement between coders.

---

### C6 — Open lakehouse × federated

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #63 | P | Governance "through platform means", from "implementing a fully-functional data mesh platform" | Abstract | Pattern | Computational governance in the platform (level 4) |
| #87 | P | "federated computational governance", validated by "a blockchain-based implementation of a mesh platform" | Abstract | Pattern (prototype) | Formalised uniform policy across domains — **prototype, not production** |
| #136 | P | "Governance tasks, such as ensuring data protection compliance, are notoriously challenging to automate"; contract-based verification of declassification | Abstract | Pattern | Level-5 mechanism proposed, with the difficulty stated |
| #30 | P | 8 design decisions, 104 options for federated computational governance | Abstract | Pattern | Design space mapped; outcome not measured |
| #57 | P | Federated and automated governance among key components; findings from case studies at "three organizations in the Netherlands and Germany" | Abstract | Pattern | Practice exists; detail in full text |
| #133 | P | Transition to federated governance is difficult (15 interviews) | Abstract | Pattern | Counter-evidence to easy uniformity |
| F1 | — | Separate domain catalogs → the fine-grained policy of one catalog does not reach another's engines | — | Pattern | Level-5 "uniform across engines and domains" **not shown** |

**Evidence strength:** 6 P, all at the pattern level, several design or prototype studies, none measuring enforcement outcomes. This is the **richest row-specific evidence** in the matrix so far, and it points to mechanisms proposed rather than demonstrated.

---

### C7 — Hybrid / multi-platform (was: data fabric overlay)

> **Update 1 Oct 2026 (kit K15).** C7 is redefined as *Hybrid / multi-platform*: lakehouse core plus warehouse serving layer, no fabric layer assumed. Quotations below about a fabric or metadata overlay apply only where such a layer exists; coders treat them as an upper bound for C7, not as its reference profile.

| Source | Tier | Quotation | Location | Pattern / product | Mechanism shown |
|---|---|---|---|---|---|
| #2 | P | "Data Fabric provides a centralized governance model that integrates data across diverse sources using automation, metadata management, and AI-driven quality controls. This approach ensures consistency, compliance, and real-time data observability"; "its reliance on centralized control can create bottlenecks" | Abstract | Pattern | Central policy plane across platforms (claimed) |
| #4 | P | Metadata centralised instead of data, to "avoid the problems of data privacy disclosure" | Abstract | Pattern | Privacy by not moving data |
| #84 | P | Government compliance for a web-driven data fabric (title; abstract not quoted) | — | Pattern | Compliance focus exists in fabric literature |

**Mechanisms not shown.** Whether a fabric policy plane is **enforced** in the underlying warehouse and lakehouse engines, or only declared in metadata. F1 applies to every engine the fabric spans.

**Evidence strength:** 3 P, conceptual. **Thin.**

---

## 4. Implications for the coding kit (author decisions, not coding)

1. **Edition assumption.** State the edition in the C1, C3 and C5 profiles: Enterprise or Business Critical. Access History, 90-day Time Travel and periodic rekeying depend on it. Recommended: **Enterprise**, as the modal regulated-enterprise tier. For S1, note that customer-managed keys may require a higher tier; the docs fetched do not say. **Decided 26 Sep 2026 (kit K7): Business Critical**, with Enterprise as a sensitivity run — the recommendation above was revised after checking edition features [N07o].
2. **Record the SECC–PORT dependence (F1)** in Chapter 4 and in the SMAA discussion. If the two criteria are negatively correlated across configurations, weights on both partly cancel, and that should be explained, not discovered.
3. **Evidence inventory (Part 4).** The kit expected SECC S for C1 and M elsewhere.
   - C1: well documented but all T for mechanisms. The expected strength holds only if T sources concurring from two vendors are accepted.
   - C2: M.
   - C3, C4: M.
   - C5: M, at the pattern level only.
   - C6: M, rich but mostly design studies.
   - C7: thin.

## 5. Open items

- **Consumer-side enforcement of provider policies on Snowflake shares** — affects C5.
- **Certifications of the managed lakehouse variant and of the cloud object stores** — affects C2, C4, C6. A source is needed if the coder is to go beyond inference.
- **Full texts #30, #136, #77** (To download).
- **Spot-check** of web quotations.
