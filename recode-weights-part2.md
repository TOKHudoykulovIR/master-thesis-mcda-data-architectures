# Recode v2 — field: Weights, records 51–100

Coded under `coding-scheme-v2.md`. Rule 3 governs: **if the abstract does not explicitly state where the weights came from, the value is `unclear` and coding stops there.**

| # | Short title | v1 | **v2** | Basis in the abstract |
|---|---|---|---|---|
| 51 | Data governance in mesh: Saxo bank | none | **none** | Case study, no weighting |
| 52 | Data integration and storage strategies | n/a | **n/a** | Review paper |
| 53 | Data Lakes vs DW, library analytics | none | **none** | Comparative discussion |
| 54 | Data management within mesh framework | none | **none** | Conceptual |
| 55 | Data Mesh Adoption: readiness | none | **none** | Multi-case readiness assessment; no criteria weighting |
| 56 | Data Mesh vs Data Space: governance | literature | **literature** | "structured literature review subsequently complemented by expert interviews" — stated |
| 57 | Data Mesh Architecture: theory to practice | none | **none** | Tutorial |
| 58 | Data Mesh: principles and catalog | none | **none** | Conceptual |
| 59 | Data ownership revisited | none | **none** | Empirical study of accountabilities |
| 60 | Data Products: overcoming boundaries | none | **none** | Framework |
| 61 | Databricks Lakeguard | none | **none** | Systems paper |
| 62 | Dataspaces: concepts and architectures | n/a | **n/a** | Review |
| 63 | Decentralized governance in mesh platform | none | **none** | Conceptual model |
| 64 | Delta Sharing | none | **none** | Protocol paper |
| 65 | Benchmark-driven MCDM, rank reversal | author | **unclear** | "A weighted aggregation mechanism then combines these normalized scores"; who sets the weights is not stated |
| 66 | Lakehouse for SA training authority | none | **none** | Case study |
| 67 | FlowCaLiSe fog-cloud lakehouse | none | **none** | Architecture proposal |
| 68 | Clinical data infrastructure comparison | author | **unclear** | Three architectures compared; the abstract names no weighting procedure or source |
| 69 | Iceberg multi-platform interoperability | none | **none** | Empirical study |
| 70 | Enterprise data science platform | none | **none** | Architecture proposal |
| 71 | Enterprise data strategy: mesh | none | **none** | Overview |
| 72 | Enterprise digital management, data lake | none | **none** | Strategy discussion |
| 73 | TPC-DS on open table formats | n/a | **n/a** | Benchmark |
| 74 | Cloud platforms in a fuzzy environment | author/practice | **unclear** | "selection of attributes… based on experience and best practices" describes attribute *selection*, not weight derivation |
| 75 | Cloud continuum, math programming | unclear | **unclear** | MCDM via mathematical programming; source not stated |
| 76 | Open-source data fabric platforms | n/a | **n/a** | Review |
| 77 | Data residency compliant architecture | none | **none** | Recommendation framework, no weighting |
| 78 | Monolithic PLM to federated mesh | none | **none** | Transformation approach |
| 79 | On-premises to cloud, Chilean bank | none | **none** | Case study |
| 80 | From Data Mesh to Intermesh | none | **none** | Platform approach |
| 81 | From ETL to Modern Data Stack (SLR) | literature/author | **literature** | Criteria derived inductively from a 141-study corpus; stated in the abstract |
| 82 | Future of database system architectures | n/a | **n/a** | Positional overview |
| 83 | Governing data lakehouses | none | **none** | Governance model |
| 84 | Government compliance for data fabric | none | **none** | Book chapter, descriptive |
| 85 | Hathi: MCDM capacity planning | author | **unclear** | MCDM-based approach to configuration selection; weight source not stated |
| 86 | HHO algorithm, cloud provider | unclear | **unclear** | Mathematical model with metaheuristic; source not stated |
| 87 | Implementing federated governance in mesh | none | **none** | Architecture discussion |
| 88 | AHP-IOWA, POWA, cloud provider | author | **unclear** | AHP with ordered weighted averaging operators named; who supplies the pairwise judgments is not stated |
| 89 | Interoperability frameworks: fabric and mesh | none | **none** | Book chapter |
| 90 | Introduction to data lakes | n/a | **n/a** | Review chapter |
| 91 | FAIR principles for data mesh | n/a | **n/a** | Review/analysis |
| 92 | Key lessons from microservices for mesh | none | **none** | Conceptual |
| 93 | LakeHelm: zero-shot lakehouse advisor | none (learned) | **none** | Configurations learned, not weighted by anyone |
| 94 | Lakehouse (Armbrust et al.) | none | **none** | Position paper |
| 95 | 8RA cloud-edge, digital sovereignty | none | **none** | Position paper |
| 96 | Managing data in a big financial institution | none | **none** | Industrial experience report |
| 97 | Heterogeneous data, graph MCDM | unclear | **unclear** | MCDM model over a criteria graph; source not stated |
| 98 | Master and reference data in data lakes | n/a | **n/a** | Book chapter |
| 99 | M-Data-Fabric | none | **none** | Systems paper |
| 100 | Object-based multi-cloud data lake | n/a | **n/a** | Empirical performance study |

---

## Shift from v1 to v2, records 51–100

| Value | v1 | **v2** | Change |
|---|---|---|---|
| none | 34 | 33 | −1 |
| **unclear** | 4 | **7** | **+3** |
| author | 5 | **0** | **−5** |
| literature | 2 | 2 | — |
| n/a | 5 | 8 | +3 |

Smaller movement than in the first batch, for a structural reason: records 51–100 are domain-heavy. Thirty-three of fifty perform no weighting at all, so rule 1 disposes of them before rule 3 can apply. The `author` category again empties — all five v1 assignments rested on inference from a named method.

Three v1 codings were corrected on grounds other than rule 3. Record 74 was coded `author/practice` from the phrase *"based on experience and best practices"*, which in fact describes how the **attributes** were chosen, not how weights were derived — a misreading, now `unclear`. Record 93 (LakeHelm) was coded `none (learned)`, a value outside the vocabulary; it is a system that learns configurations rather than weighting criteria, so plain `none` is correct. Record 81 was coded `literature/author`; the abstract states derivation from the corpus, so `literature` alone is right, with the author-assigned per-archetype weighting a full-text detail.

---

## Running totals, records 1–100

| Value | v1 | **v2** |
|---|---|---|
| none | 56 | 55 |
| **unclear** | 12 | **26** |
| **author** | 11 | **0** |
| n/a | 6 | 12 |
| panel (n unstated) | 4 | 3 |
| entropy/objective | 3 | 3 |
| literature | 4 | 4 |
| user/consumer input | 3 | 1 |
| single expert | 1 | 0 |
| panel (n stated) | 1 | 0 |

Of the 45 records so far that apply a weighting procedure, **26 do not disclose where the weights came from**, 3 name a group of experts without a count, 3 derive weights objectively by entropy, 4 derive them from literature, and 1 from consumer sentiment. **None states a number of experts in its abstract.**
