// Cross-check of the Explorer's carbon add-on against engine/exploratory.carbon_threshold (run: node test/xcheck_carbon.js > test/js_carbon.json)
const C = require('../src/core.js');
const { DATA } = require('../src/data.js');
const med = Object.fromEntries(Object.entries(DATA.carbon.est).map(([c, v]) => [c, v[1]]));
const W = { equal: [.2, .2, .2, .2, .2], security: [.1, .15, .15, .15, .45], speed: [.35, .3, .1, .15, .1], portability: [.1, .15, .45, .15, .15] };
const out = {};
for (const [k, w] of Object.entries(W)) {
  const m = C.activeModel(DATA.matrix, { floor: false, includeC7: true });
  const p = C.carbonPath(m, w, med, 0.6);
  out[k] = { scores20: C.carbonScores(m, w, med, 0.2), first: p.first, change: p.change, after: p.after,
             path: p.path.map(x => x.leaders) };
  const f = C.activeModel(DATA.matrix, { floor: true, includeC7: true });
  out[k + '_floor'] = { scores20: C.carbonScores(f, w, med, 0.2), change: C.carbonPath(f, w, med, 0.6).change };
}
console.log(JSON.stringify(out));
