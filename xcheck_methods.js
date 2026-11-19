// Cross-check of the method check (min–max TOPSIS, PROMETHEE II) and the ordinal sampler against the engine.
const C = require('../src/core.js');
const { DATA } = require('../src/data.js');
const M = DATA.matrix;
const W = [[0.2,0.2,0.2,0.2,0.2],[0.1,0.1,0.2,0.1,0.5],[0.35,0.3,0.1,0.15,0.1],[0.05,0.1,0.6,0.1,0.15],[0.3,0.05,0.25,0.1,0.3]];
const mdl = C.activeModel(M, { floor: false, includeC7: true });
const out = { minmax: W.map(w => C.closenessMinMax(mdl.X, w)), promethee: W.map(w => C.prometheeNet(mdl.X, w)),
  leaders: W.map(w => C.methodCheck(mdl, w)), centroid: C.regionCentroid(4, 0, 5) };
// region sampler: every draw must put best largest and worst smallest
const r = C.rng(5); let bad = 0;
for (let i = 0; i < 20000; i++) { const w = C.sampleRegion(r, 4, 0, 5); if (Math.max(...w) !== w[4] || Math.min(...w) !== w[0]) bad++; }
out.regionViolations = bad;
// E-O1 with the panel's choices, as in round2_analysis (floor in S1, cost uncertainty on)
const K = C.CRITERIA, CH = {
  S1: [['SECC','AIRD'],['SECC','PORT'],['SECC','TTDP'],['SECC','TTDP']],
  S2: [['TTDP','PORT'],['TTDP','PORT'],['TTDP','PORT'],['TTDP','TCO']],
  S3: [['AIRD','TTDP'],['PORT','AIRD'],['PORT','AIRD'],['PORT','TCO']] };
out.eo1 = {};
for (const s of ['S1','S2','S3']) {
  const m = C.activeModel(M, { floor: s === 'S1', includeC7: true });
  const res = C.smaa(m, { type: 'ordinal', choices: CH[s].map(([b, w]) => [K.indexOf(b), K.indexOf(w)]) }, { k: 40000, seed: 11, tcoUncertainty: true });
  out.eo1[s] = Object.fromEntries(res.configs.map((c, i) => [c, res.firstRank[i]]));
}
console.log(JSON.stringify(out));
