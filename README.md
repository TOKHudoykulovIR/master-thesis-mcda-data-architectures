# Beyond Performance Benchmarks — data and code

Materials of the master's thesis *Beyond Performance Benchmarks: A Multi-Criteria Decision Analysis Framework for Evaluating Modern Data Architectures* (Toxir Xuduykulov, IT Park University, December 2026). Release **v1.1** (v1.0 was the same material as a single archive).

The repository holds what a reader needs to check the thesis: the record-level coding of the literature review, the evidence and the coding sheet behind every score, the anonymised Delphi responses, and the code that turns them into the published tables.

## Where each result comes from

| Thesis | Files |
|---|---|
| Table 1 (criteria coverage), Table 2 (origin of weights), Section 1.3 (methods) | `extraction/recode-*.md` (record-level coding of the 143 studies), `extraction/reduced-extraction-part1..3.md`, `extraction/coding-scheme-v2.md` |
| Table 7 (evidence tiers), Table 26 (anchored scales) | `matrix/matrix-coding-kit-v1.md` |
| Table 20 (performance matrix) | `matrix/matrix-frozen-2026-10-19.json`; freeze record with SHA-256 in `matrix/MATRIX-FROZEN-2026-10-19.md` |
| Table 27 (score, justification and sources of every cell) | `matrix/coding-sheet-coder1.xlsx` (sheet *Cells*, column *Sources (IDs + tier)*); every source ID resolves in `evidence/source-register.xlsx` (sheets *Corpus*, *Grey*, *Added sources*: link, tier, access date) |
| Quotations behind the scores | `evidence/pack-*.md` (one pack per criterion; no scores) |
| Tables 14–16 (Delphi Round 1) | `round1/round1-responses.json`, `round1/round1_analysis.py`, `round1/round1-results.*`, `round1/round1-analysis-report.md` |
| Tables 17–19 (Round 2 responses, weights, Kendall's W, most/least choices) | `round2/imports/2026-10-19-AB-corrected/round2-responses.json`, `round2/analysis/round2-analysis.json` |
| Tables 21–22 (rankings, acceptability, sensitivity runs), frontier maps | `round2/round2_analysis.py` → `round2/analysis/` |
| Table 22, the two runs added after review; notes to Tables 21–22 | `round2/review_checks.py` (not part of the analysis plan) |
| Table 23 and Section 4.5 (exploratory carbon) | `carb/` and `engine/engine/exploratory.py` |
| Section 3.3 (decision engine, 51 tests) | `engine/` |
| Section 3.4 (Architecture Decision Explorer) | `explorer/dist/architecture-decision-explorer.html` (open in a browser; no server); sources in `explorer/src/`, cross-checks in `explorer/test/` |
| Analysis rules fixed in advance, with dated amendments | `analysis-plan/` |
| Round 2 form as fielded | `round2/round2-instrument-as-fielded.md` (section 1 omitted) |

## Reproduce

Python 3.10 or later with NumPy, SciPy, Matplotlib, openpyxl and scikit-learn (versions used: `requirements.txt`).

```bash
pip install -r requirements.txt
cd engine && python -m unittest discover -s tests          # 51 tests
cd ../round2 && python -m pytest -q                         # importer and analysis tests
python round2_analysis.py --responses imports/2026-10-19-AB-corrected/round2-responses.json --closed 2026-10-20 \
       --out /tmp/out.json --report /tmp/out.md --plots /tmp/plots    # reproduces analysis/round2-analysis.json
python review_checks.py                                      # the checks added after review
cd ../round1 && python round1_analysis.py                    # Round 1 results (writes round1-results.*)
```

Random draws use fixed seeds, so the numbers reproduce exactly. The analysis refuses to run if the matrix differs from the frozen one.

## What is not included

Panellists are identified by codes (R01–R06). Their names and e-mail addresses, the key linking codes to names, the raw survey exports, written corrections and recontact messages are withheld. No client or project information was collected.

## Licence

Code (`*.py`, `*.js`, `explorer/`): MIT licence, see `LICENSE`. Data and documents: CC BY 4.0, see `LICENSE-DATA.md`.

## Citation

See `CITATION.cff`. Please cite the thesis and this release: https://github.com/TOKHudoykulovIR/master-thesis-mcda-data-architectures (tag `v1.1`).
