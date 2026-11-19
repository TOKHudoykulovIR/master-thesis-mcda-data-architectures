# Recode v2 — field: OpModel, records 1–143

Coded under `coding-scheme-v2.md`. **The change from v1:** naming data mesh is no longer sufficient for `FED`. The abstract must say something about ownership, decentralisation or federated governance. Where it does not, the value is `n/a`, even for papers whose subject is data mesh.

Only records receiving a value other than `n/a` are listed. **All 143 records not listed below are coded `n/a`.**

| # | Short title | v1 | **v2** | Evidence in the abstract |
|---|---|---|---|---|
| 2 | Governance in Fabric vs Mesh | CENT, FED | **CENT, FED** | "Data Fabric provides a **centralized governance model**"; mesh contrasted as distributed |
| 4 | Distributed data fabric, metadata KG | n/a | **CENT** | "Instead of storing the full amount of data in a **centralized** data lake, we choose to **centralize** the metadata" |
| 5 | Federated metadata architecture | FED | **HUB** | "read-through **federation** model, **centralized access control**" — federated access under central governance |
| 6 | Governance-centric lakehouse | CENT | **n/a** | Governance processes discussed; no statement about ownership topology |
| 12 | Non-intrusive framework, mesh pipelines | FED | **FED** | "data mesh architectures gain traction in **federated environments**" |
| 16 | Adopting the Data Mesh | FED | **FED** | "establishment of **decentralised data ownership** and domain-oriented data teams" |
| 28 | Hybrid data products, agentic AI | FED | **n/a** | Mesh and fabric named as enabling architectures; nothing stated about ownership |
| 30 | Federated computational governance | FED | **FED** | "**decentralized** data architecture… analytical domain data as **autonomous products**" |
| 31 | Self-serve data platforms in meshes | FED | **FED** | "**shifts the ownership** of the data to the business domains… **federated** and automated governance" |
| 33 | Patterns for Mesh and Data Spaces | FED, HUB | **HUB, FED** | The corpus's clearest statement of both: "**logically decentralized** meshes, in which domains own data products on a **shared platform**" (HUB) and "**physically decentralized** meshes, in which domains operate separate environments" (FED) |
| 34 | Integrating data lakes into DW | CENT | **n/a** | Integration of two architectures; no ownership statement |
| 49 | Data contracts, manufacturing | FED, CENT | **HUB** | "find a **balance between a centralized and decentralized** data management strategy" — an explicit middle position |
| 51 | Data governance in mesh: Saxo bank | FED | **FED** | "data **ownership**" named as one of three governance aspects, in a mesh setting |
| 54 | Data management within mesh framework | FED | **FED** | "responsibility for data is **distributed among domain teams, not centralised** in a single team" |
| 55 | Data Mesh Adoption: readiness | FED | **n/a** | Readiness assessment for adoption; the abstract does not describe ownership arrangements |
| 56 | Data Mesh vs Data Space: governance | FED | **FED** | "data mesh primarily focuses on **domain-oriented decentralization** within a single organization" |
| 57 | Data Mesh Architecture: theory to practice | FED | **FED** | "**shifts the ownership** of the data to the business domains… **federated** governance model" |
| 58 | Data Mesh: principles and catalog | FED | **FED** | "domain-driven approach… **decentralized ownership**, and **federated governance**" |
| 59 | Data ownership revisited | n/a | **n/a** | Data ownership is the topic, but as accountability rights, not as an architectural operating model |
| 60 | Data Products: overcoming boundaries | FED | **n/a** | Distributed platform landscapes described as a problem; no ownership model proposed |
| 63 | Decentralized governance in mesh platform | FED | **FED** | "**decentralized** analytics data management… enable **decentralized data governance**" |
| 70 | Enterprise data science platform | FED | **HUB** | "**centralized data management** with **federated access** from multiple query engines" |
| 71 | Enterprise data strategy: mesh | FED | **FED** | "**distributed domain driven** architectures, **federated governance** and self-serving data infrastructure" |
| 78 | Monolithic PLM to federated mesh | FED | **FED** | "transforming a monolithic PLM landscape into a **federated** Domain and Data Mesh" |
| 80 | From Data Mesh to Intermesh | FED | **FED** | "without **delegating data ownership** to a central authority" |
| 87 | Implementing federated governance in mesh | FED | **FED** | "**decentralized data domains** and **federated computational governance**" |
| 89 | Interoperability frameworks: fabric and mesh | FED | **n/a** | Layers of a data fabric described; mesh introduced conceptually without ownership detail |
| 91 | FAIR principles for data mesh | FED | **FED** | "**decentralizing ownership** and promoting the principle of 'Data as a Product'" |
| 92 | Key lessons from microservices for mesh | FED | **FED** | "Domain-Driven Design… **team autonomy**" as critical components of mesh implementation |
| 95 | 8RA cloud-edge, digital sovereignty | FED | **FED** | "a **federated**, multi-vendor cloud–edge continuum—managed **collaboratively** by hyperscalers, European providers, edge platforms, and telcos" |
| 118 | Data product design in mesh | FED | **n/a** | Data product design methodology; the abstract describes governance features, not ownership topology |
| 121 | Rethinking data democratization | n/a | **CENT** | "a shift toward **centralized data management and specialized teams**" |
| 131 | Medallion architecture in practice | n/a | **CENT** | "**centralized auditing** capabilities" under a unified catalog governance framework |
| 133 | Toward avoiding the data mess | FED | **FED** | "**decentralized, distributed** concept… transition toward **federated data governance**… **shift of responsibility**" |
| 134 | Green data lake management, CTMC | n/a | **CENT** | "a **centralized** data repository platform called Data Lake" |
| 135 | Data Mesh Reference Architecture | FED | **FED** | "**federated governance**… domain architecture, self-serve data platform architecture, and federated governance" |
| 136 | Automating federated data governance | FED | **FED** | "**federated data governance** and **decentralized** data operations" |
| 137 | Lakehouse federation in CPNs | FED | **FED** | "a **federated** approach to achieve data sharing and **federated governance**" |
| 139 | OTE Group telecom data management | FED | **n/a** | "IFIP International Federation" is a publisher name, not an operating model. v1 coding was a false positive on the string "federation" |
| 140 | Trustworthy DataOps, Medallion Lakehouse | FED | **FED** | "operated under a **Data Mesh model**" with distributed pipeline responsibility |

---

## Corpus totals

| Value | v1 | **v2** | Change |
|---|---|---|---|
| `n/a` | 109 | **110** | +1 |
| **FED** | 29 | **24** | **−5** |
| **CENT** | 4 | **5** | +1 |
| **HUB** | 1 | **4** | **+3** |

---

## What changed and why

**Five records lose `FED`.** Records 28, 55, 60, 89 and 118 name data mesh, distributed platforms or federated architectures as context, but their abstracts say nothing about who owns or governs the data. Under the v2 rule, subject matter is not evidence of an operating model. Record 139 was a **false positive** — the string "federation" appeared only in the publisher's name, IFIP International Federation for Information Processing. A useful reminder that keyword-adjacent coding produces errors of this kind, and an argument for coding from sentences rather than term matches.

**`HUB` rises from 1 to 4, and this is the substantive finding.** Three records describe an explicit middle position that v1 collapsed into `FED` or `n/a`:

- **Record 33** states both poles within one paper: *logically decentralized meshes, in which domains own data products on a shared platform* — precisely the hub-and-spoke configuration — and *physically decentralized meshes, in which domains operate separate environments*. This is the only prior work in the corpus that names the distinction this thesis's middle row formalises.
- **Record 70** describes *centralized data management with federated access from multiple query engines* — central ownership of the substrate, federated consumption.
- **Record 49** frames its contribution as finding *a balance between a centralized and decentralized data management strategy* through data contracts.
- **Record 5** combines a *read-through federation model* with *centralized access control*.

**Four records gain `CENT`** where v1 overlooked explicit statements: records 4, 121, 131 and 134 each describe centralised management, auditing or repositories in so many words.

---

## Implications for Chapter 2 and Chapter 4

**The claim about the operating-model axis strengthens, and its wording becomes precise.** Of 143 records, 110 say nothing at all about who owns or governs the data. Twenty-four describe federated ownership, five centralised, and four an explicit middle position. **In every case the operating model is a property of the architecture under discussion — mesh implies federation, a data lake implies centralisation — never a dimension varied independently of the platform choice.** No record in the corpus presents a configuration space in which the same platform can be operated under different ownership models.

**Record 33 deserves explicit treatment in §2.6, not just a row in the tally.** It is the nearest prior work to the middle row of this thesis's grid: it recognises that domains can own data products on a shared platform, distinguishes this from domains operating separate environments, and gives both patterns names. What it does not do is pair either pattern with a platform choice, or treat the distinction as an axis against which architectures are evaluated. Citing it as a precedent — and stating what it stops short of — is considerably stronger than claiming the middle position is unrecognised in the literature.

**A correction to the earlier corpus summary.** The v1 note that "only one record (a mesh paper distinguishing logical from physical decentralisation) approaches a hub-and-spoke position" understated the case: four records do, and one of them names both patterns explicitly. The claim to make is not that nobody sees the middle, but that nobody treats it as a dimension.
