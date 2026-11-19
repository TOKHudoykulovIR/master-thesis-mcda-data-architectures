# Recode v2 — field: Weights, records 1–50

Coded under `coding-scheme-v2.md`, decision order applied strictly. Rule 3 governs: **if the abstract does not explicitly state where the weights came from, the value is `unclear` and coding stops there.**

| # | Short title | v1 | **v2** | Basis in the abstract |
|---|---|---|---|---|
| 1 | Iceberg / Delta / Hudi comparison | author | **unclear** | A weighted model and ranking algorithms are described; the abstract does not say who set the weights |
| 2 | Governance in Fabric vs Mesh | none | **none** | Comparative discussion, no weighting |
| 3 | MCDM in software engineering | n/a | **n/a** | Review of methods |
| 4 | Distributed data fabric on metadata KG | none | **none** | Architecture proposal |
| 5 | Federated metadata architecture | none | **none** | Architecture proposal |
| 6 | Governance-centric lakehouse | none | **none** | Roadmap and principles |
| 7 | Governed lakehouse DataOps | none | **none** | Reference architecture |
| 8 | Group MCDM, Best-Only Method | panel (n unstated) | **panel (n unstated)** | "Group decision-making among experts" is explicit; no count given |
| 9 | Markov chain MCDM, cloud | user/consumer input | **unclear** | Phase 1 is "determining criteria weights"; the source is not stated. User feedback refines the *ranking*, not the weights |
| 10 | Cloud deployment options | author | **unclear** | A multi-criteria approach over cost, scalability, performance; weight source not stated |
| 11 | Multi-layer Delta lakehouse | none | **none** | Architecture review and design |
| 12 | Non-intrusive framework, mesh pipelines | none | **none** | Framework, no weighting |
| 13 | Secure IoT cloud platform, entropy | entropy/objective | **entropy/objective** | Entropy distance approach named in the title and abstract |
| 14 | IF-AHP-Entropy-ELECTRE, data fabric | panel(3) | **unclear, entropy/objective** | Entropy is explicit. The abstract names IF-AHP for subjective weights but does not state who provided the judgments — the panel of three is in the full text only |
| 15 | Active Data Lakes | none | **none** | Systems paper |
| 16 | Adopting the Data Mesh | none | **none** | Case study |
| 17 | Fuzzy sentiments + QoS | user/consumer input | **user/consumer input** | Weights derived from consumer sentiment mining; explicitly stated |
| 18 | Cloud ranking protocol, fuzzy | unclear | **unclear** | MCDM named, source not stated |
| 19 | Enhanced MCDM, cloud provider | entropy/objective | **entropy/objective** | "The entropy technique is utilized to determine the weight of the criteria" |
| 20 | Hybrid data warehousing for CSPs | none | **none** | Architecture proposal |
| 21 | Cloud provider through SLAs | unclear | **unclear** | SLA-based selection; weight source not stated |
| 22 | Group decision, AI cloud platforms | panel (n unstated) | **panel (n unstated)** | Explicitly a multiple-criteria *group* decision-making process |
| 23 | Polyglot semantic control plane | none | **none** | Systems paper |
| 24 | Best Only Method + RE-TOPSIS | author | **unclear** | Two MCDM approaches combined; weight source not stated |
| 25 | Data lake architecture models | none | **none** | Overview |
| 26 | AHP for ranking cloud databases | author | **unclear** | AHP framework proposed; indexing is "based on user's needs" but the weight source is not stated |
| 27 | Performance parameters, AHP | author | **unclear** | AHP named; weight source not stated |
| 28 | Hybrid data products, agentic AI | none | **none** | Architecture discussion |
| 29 | Scalable governed pipelines | none | **none** | Experimental evaluation, no weighting |
| 30 | Federated computational governance | literature | **literature** | Decisions derived from a grey-literature review and interviews; stated |
| 31 | Self-serve data platforms in meshes | literature | **literature** | Same authors, same method, stated |
| 32 | Architectural evolution and selection | single expert | **unclear** | Weighted compatibility scoring described; the abstract does not say the architect assigns weights — that is full-text detail |
| 33 | Patterns for Mesh and Data Spaces | none | **none** | Pattern comparison |
| 34 | Integrating data lakes into DW | none | **none** | Conceptual comparison |
| 35 | Big data platform at a hospital | panel (n unstated) | **unclear** | A Rembrandt system application is named; the abstract does not state who supplied the judgments |
| 36 | BoaviztAPI | n/a | **n/a** | Assessment method, no criteria weighting |
| 37 | QoE/QoS with PROMETHEE-II | consumer/provider input | **unclear** | A centralised QoE repository is proposed; whether stakeholder data sets the weights is not stated |
| 38 | Green cloud computing SLR | n/a | **n/a** | Systematic review |
| 39 | Cloud instance selection, K-Means + AHP | author | **unclear** | AHP and parallel K-means named; weight source not stated |
| 40 | Cloud provider, accountability and security | unclear | **unclear** | Interval-valued fuzzy TOPSIS; source not stated |
| 41 | Cloud prioritization, INS + TOPSIS | expert judgments | **panel (n unstated)** | "help users and experts express their evaluations"; experts explicit, count absent |
| 42 | Cloud provider, fuzzy TOPSIS | unclear | **unclear** | Source not stated |
| 43 | Cloud ranking, GRA / TOPSIS / SAW | unclear | **unclear** | Three techniques compared; source not stated |
| 44 | Cloud selection, fuzzy MARCOS | unclear | **unclear** | "After establishing the relevant indicators"; who establishes them is not stated |
| 45 | Cloud selection, fuzzy ANP | unclear | **unclear** | Source not stated |
| 46 | Cloud-native modernization | none | **none** | Multiple-case study |
| 47 | Data catalog tools, multivocal review | n/a | **n/a** | Review |
| 48 | Data catalogs in mesh and data spaces | none | **none** | Analytical paper |
| 49 | Data contracts, manufacturing | none | **none** | Case study |
| 50 | Data fabrics for multi-domain systems | none | **none** | Comparative discussion |

---

## Shift from v1 to v2, records 1–50

| Value | v1 | **v2** | Change |
|---|---|---|---|
| none | 22 | 22 | — |
| **unclear** | 8 | **19** | **+11** |
| author | 6 | **0** | **−6** |
| single expert | 1 | 0 | −1 |
| panel (n unstated) | 4 | 3 | −1 |
| panel (n stated) | 1 | 0 | −1 |
| entropy/objective | 3 | 3 | — |
| user/consumer input | 3 | 1 | −2 |
| literature | 2 | 2 | — |
| n/a | 1 | 4 | +3 |

The `author` category empties entirely in this batch. Every v1 assignment of `author` rested on inference: an abstract naming AHP or a weighted model, with no statement of who supplied the weights. Under rule 3 all become `unclear`.

Two panel assignments also fall. Record 14 (Zhou & Chen) is the corpus's only `panel(3)` — but that figure comes from the full text, not the abstract. **For internal consistency the reduced extraction now codes it `unclear`; the full extraction retains `panel(3)` with the full text as its basis.** Record 35 loses its panel coding for the same reason.

This matters for how the Chapter 2 claim is phrased. It can no longer be *"only one record reports a panel with a stated size"* if that fact is established from full texts while the tally is built from abstracts. Two defensible framings:

1. **Abstract-level claim:** of N records applying a weighting method, none states the number of experts consulted in its abstract; k state that a group of experts was involved without giving a count; the remainder do not disclose the source at all.
2. **Full-text claim, restricted:** among the five works read in full, one reports a panel of three internal directors of the buying organisation.

Both are true and checkable. Mixing them is not. Recommend using framing 1 for the corpus-level tally and framing 2 when discussing the closest works in §2.6.

**Reporting note.** The rise of `unclear` from 8 to 19 is itself a finding about the literature: more than half of the records that apply a multi-criteria method do not disclose where their weights came from. That is a reporting-practice observation worth a sentence in §2.5.2, independent of the gap argument.
