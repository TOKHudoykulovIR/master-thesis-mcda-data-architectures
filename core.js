/* Decision core — mirrors engine/topsis.py, engine/promethee.py, engine/matrix.py (secc_floor, K11 TCO),
   engine/frontier.py, engine/smaa.py and engine/ordinal.py. Pure functions, no DOM. */
const CORE = (() => {
  const CRITERIA = ['TTDP', 'AIRD', 'PORT', 'TCO', 'SECC'];
  const CONFIGS = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'];

  // ---- seeded RNG (mulberry32) so a given input always shows the same SMAA numbers
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normal(r) {            // Box–Muller
    let u = 0, v = 0;
    while (u === 0) u = r();
    while (v === 0) v = r();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
  function gamma(r, shape) {      // Marsaglia & Tsang (2000); boost for shape < 1
    if (shape < 1) return gamma(r, shape + 1) * Math.pow(r() || 1e-300, 1 / shape);
    const d = shape - 1 / 3, c = 1 / Math.sqrt(9 * d);
    for (;;) {
      let x, v;
      do { x = normal(r); v = 1 + c * x; } while (v <= 0);
      v = v * v * v;
      const u = r();
      if (u < 1 - 0.0331 * x * x * x * x) return d * v;
      if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
    }
  }
  function dirichlet(r, alpha) {
    const g = alpha.map(a => gamma(r, a));
    const s = g.reduce((p, q) => p + q, 0);
    return g.map(x => x / s);
  }
  /* engine/smaa.py dirichlet_mom: alpha = mean * s, s averaged over criteria of m(1-m)/var - 1 (ddof = 1) */
  function dirichletMoM(W) {
    const n = W[0].length, k = W.length;
    const m = Array.from({ length: n }, (_, j) => W.reduce((p, w) => p + w[j], 0) / k);
    const v = Array.from({ length: n }, (_, j) => W.reduce((p, w) => p + (w[j] - m[j]) ** 2, 0) / (k - 1));
    const s_j = [];
    for (let j = 0; j < n; j++) if (v[j] > 0) { const s = m[j] * (1 - m[j]) / v[j] - 1; if (s > 0) s_j.push(s); }
    const s = s_j.length ? s_j.reduce((p, q) => p + q, 0) / s_j.length : 1e3;
    return m.map(x => x * s);
  }

  // ---- TOPSIS, vector normalisation, all criteria benefit-type (engine/topsis.py closeness)
  function closeness(X, w) {
    const m = X.length, n = w.length;
    const norm = Array(n).fill(0);
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) norm[j] += X[i][j] * X[i][j];
    for (let j = 0; j < n; j++) norm[j] = Math.sqrt(norm[j]);
    const V = X.map(row => row.map((x, j) => (norm[j] === 0 ? 0 : x / norm[j]) * w[j]));
    const ideal = Array(n).fill(-Infinity), anti = Array(n).fill(Infinity);
    for (const row of V) row.forEach((v, j) => { if (v > ideal[j]) ideal[j] = v; if (v < anti[j]) anti[j] = v; });
    return V.map(row => {
      let dp = 0, dm = 0;
      row.forEach((v, j) => { dp += (v - ideal[j]) ** 2; dm += (v - anti[j]) ** 2; });
      dp = Math.sqrt(dp); dm = Math.sqrt(dm);
      return dp + dm === 0 ? 0.5 : dm / (dp + dm);
    });
  }
  /* engine/topsis.py closeness(method='minmax'), all criteria benefit-type (Stage 2 plan A12) */
  function closenessMinMax(X, w) {
    const n = w.length;
    const lo = Array.from({ length: n }, (_, j) => Math.min(...X.map(r => r[j])));
    const hi = Array.from({ length: n }, (_, j) => Math.max(...X.map(r => r[j])));
    const V = X.map(row => row.map((x, j) => ((x - lo[j]) / (hi[j] - lo[j] || 1)) * w[j]));
    const ideal = Array(n).fill(-Infinity), anti = Array(n).fill(Infinity);
    for (const row of V) row.forEach((v, j) => { if (v > ideal[j]) ideal[j] = v; if (v < anti[j]) anti[j] = v; });
    return V.map(row => {
      let dp = 0, dm = 0;
      row.forEach((v, j) => { dp += (v - ideal[j]) ** 2; dm += (v - anti[j]) ** 2; });
      dp = Math.sqrt(dp); dm = Math.sqrt(dm);
      return dp + dm === 0 ? 0.5 : dm / (dp + dm);
    });
  }
  /* engine/promethee.py net_flows(pref='vshape'): V-shaped preference, threshold = the criterion's range (A11) */
  function prometheeNet(X, w) {
    const m = X.length, n = w.length, s = w.reduce((p, q) => p + q, 0) || 1;
    const p = Array.from({ length: n }, (_, j) => Math.max(...X.map(r => r[j])) - Math.min(...X.map(r => r[j])));
    const phi = Array(m).fill(0);
    for (let a = 0; a < m; a++) for (let b = 0; b < m; b++) {
      if (a === b) continue;
      let pi = 0;
      for (let j = 0; j < n; j++) if (p[j] > 0) pi += (w[j] / s) * Math.min(1, Math.max(0, (X[a][j] - X[b][j]) / p[j]));
      phi[a] += pi / (m - 1); phi[b] -= pi / (m - 1);
    }
    return phi;
  }
  /* The leaders (all tied for first) under TOPSIS, TOPSIS with min–max normalisation and PROMETHEE II. */
  function methodCheck(model, w) {
    const top = sc => { const mx = Math.max(...sc); return model.configs.filter((_, i) => sc[i] >= mx - 1e-9); };
    return { topsis: top(closeness(model.X, w)), minmax: top(closenessMinMax(model.X, w)),
             promethee: top(prometheeNet(model.X, w)) };
  }

  /* engine/ordinal.py sample_region: uniform on {w : w[best] largest, w[worst] smallest}. A uniform simplex draw is
     sorted; the largest value goes to best, the smallest to worst, the middle values to the others in random order. */
  function sampleRegion(r, best, worst, n) {
    const u = dirichlet(r, Array(n).fill(1)).sort((a, b) => a - b);
    const w = Array(n).fill(0);
    w[best] = u[n - 1]; w[worst] = u[0];
    const mid = u.slice(1, n - 1);
    for (let i = mid.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [mid[i], mid[j]] = [mid[j], mid[i]]; }
    let t = 0;
    for (let j = 0; j < n; j++) if (j !== best && j !== worst) w[j] = mid[t++];
    return w;
  }
  /* Mean of that region: expected order statistics of a uniform simplex draw, the middle three sharing equally. */
  function regionCentroid(best, worst, n) {
    const e = k => Array.from({ length: n - k + 1 }, (_, i) => 1 / (k + i)).reduce((p, q) => p + q, 0) / n;
    const midMean = Array.from({ length: n - 2 }, (_, i) => e(i + 2)).reduce((p, q) => p + q, 0) / (n - 2);
    return Array.from({ length: n }, (_, j) => (j === best ? e(1) : j === worst ? e(n) : midMean));
  }

  function ranks(scores) {        // 1 = best; ties share the minimum rank
    return scores.map(v => 1 + scores.filter(s => s > v).length);
  }
  function normalise(raw) {
    const s = raw.reduce((p, q) => p + q, 0);
    return s > 0 ? raw.map(x => x / s) : raw.map(() => 1 / raw.length);
  }

  /* Build the deterministic matrix for the active options.
     matrix: {C1:{TTDP:..}, ...}; opts: {floor, includeC7, c6Blocked} */
  function activeModel(matrix, opts) {
    let configs = CONFIGS.filter(c => opts.includeC7 || c !== 'C7');
    const base = {};
    configs.forEach(c => { base[c] = Object.assign({}, matrix[c]); });
    if (opts.c6Blocked && base.C6) base.C6.TTDP = 1;                       // K9 sensitivity
    let excluded = [];
    if (opts.floor) {                                                       // A10a, S1 only
      excluded = configs.filter(c => base[c].SECC < 3);
      configs = configs.filter(c => base[c].SECC >= 3);
    }
    const X = configs.map(c => CRITERIA.map(k => base[c][k]));
    return { configs, X, excluded, base };
  }

  function rankConfigs(model, w) {
    const c = closeness(model.X, w);
    const r = ranks(c);
    return model.configs.map((cfg, i) => ({ config: cfg, score: c[i], rank: r[i] }))
      .sort((a, b) => a.rank - b.rank || CONFIGS.indexOf(a.config) - CONFIGS.indexOf(b.config));
  }

  /* engine/frontier.py: vary criteria a, b on a grid; others keep their current proportions.
     Returns grid[j][i] (row = b value, col = a value): config index in model.configs, -1 infeasible, -2 tie. */
  function frontier(model, w, a, b, grid = 50) {
    const ia = CRITERIA.indexOf(a), ib = CRITERIA.indexOf(b);
    const rest = CRITERIA.map((_, j) => j).filter(j => j !== ia && j !== ib);
    const restSum = rest.reduce((p, j) => p + w[j], 0);
    const share = rest.map(j => (restSum > 0 ? w[j] / restSum : 1 / rest.length));
    const vals = Array.from({ length: grid }, (_, i) => i / (grid - 1));
    const out = Array.from({ length: grid }, () => Array(grid).fill(-1));
    const ties = {};
    for (let i = 0; i < grid; i++) {
      for (let j = 0; j < grid; j++) {
        const wa = vals[i], wb = vals[j];
        if (wa + wb > 1 + 1e-12) continue;
        const ww = Array(CRITERIA.length).fill(0);
        ww[ia] = wa; ww[ib] = wb;
        rest.forEach((jj, t) => { ww[jj] = (1 - wa - wb) * share[t]; });
        if (ww.reduce((p, q) => p + q, 0) <= 0) continue;
        const c = closeness(model.X, ww);
        const mx = Math.max(...c);
        const top = c.map((v, t) => (v >= mx - 1e-12 ? t : -1)).filter(t => t >= 0);
        out[j][i] = top.length === 1 ? top[0] : -2;
        if (top.length > 1) ties[j * grid + i] = top;
      }
    }
    return { vals, grid: out, ties };
  }

  /* engine/smaa.py run(): SMAA-2 with TOPSIS. weightMode: {type:'uniform'} | {type:'dirichlet', alpha}
     | {type:'ordinal', choices: [[mostIndex, leastIndex], ...]} (engine/ordinal.py, E-O1)
     tcoUncertainty: K11 rows (C3–C7) drawn as clip(v + U[-1,1], 1, 5). Returns acceptability [config][rank-1]. */
  function smaa(model, weightMode, opts) {
    const k = opts.k || 10000, r = rng(opts.seed || 1);
    const m = model.configs.length, n = CRITERIA.length, iT = CRITERIA.indexOf('TCO');
    const derived = model.configs.map(c => !['C1', 'C2'].includes(c));
    const counts = Array.from({ length: m }, () => Array(m).fill(0));
    const firstW = Array.from({ length: m }, () => Array(n).fill(0));
    const firsts = Array(m).fill(0);
    for (let t = 0; t < k; t++) {
      let w;
      if (weightMode.type === 'uniform') w = dirichlet(r, Array(n).fill(1));
      else if (weightMode.type === 'ordinal') {           // engine/ordinal.py: one panellist's region per draw
        const [b, lw] = weightMode.choices[Math.floor(r() * weightMode.choices.length)];
        w = sampleRegion(r, b, lw, n);
      } else w = dirichlet(r, weightMode.alpha);
      let X = model.X;
      if (opts.tcoUncertainty) {
        X = model.X.map((row, i) => {
          if (!derived[i]) return row;
          const copy = row.slice();
          copy[iT] = Math.min(5, Math.max(1, row[iT] + (r() * 2 - 1)));
          return copy;
        });
      }
      const c = closeness(X, w).map(v => v + r() * 1e-12);               // random tie-break
      const order = c.map((v, i) => i).sort((p, q) => c[q] - c[p]);
      order.forEach((i, pos) => { counts[i][pos] += 1; });
      firsts[order[0]] += 1;
      w.forEach((x, j) => { firstW[order[0]][j] += x; });
    }
    return {
      configs: model.configs,
      acceptability: counts.map(row => row.map(x => x / k)),
      firstRank: counts.map(row => row[0] / k),
      centralWeights: firstW.map((row, i) => (firsts[i] ? row.map(x => x / firsts[i]) : null)),
      k,
    };
  }

  /* Exploratory carbon (engine/exploratory.carbon_threshold, Stage 2 E-C3). Carbon intensity enters as a sixth,
     cost-type criterion (lower is better) on the estimate's medians; the five weights are scaled by (1 - t). */
  function closenessMixed(X, w, benefit) {   // engine/topsis.py closeness with benefit flags, vector normalisation
    const n = w.length;
    const norm = Array(n).fill(0);
    X.forEach(row => row.forEach((x, j) => { norm[j] += x * x; }));
    for (let j = 0; j < n; j++) norm[j] = Math.sqrt(norm[j]);
    const V = X.map(row => row.map((x, j) => (norm[j] === 0 ? 0 : x / norm[j]) * w[j]));
    const ideal = [], anti = [];
    for (let j = 0; j < n; j++) {
      const col = V.map(r => r[j]), mx = Math.max(...col), mn = Math.min(...col);
      ideal.push(benefit[j] ? mx : mn); anti.push(benefit[j] ? mn : mx);
    }
    return V.map(row => {
      let dp = 0, dm = 0;
      row.forEach((v, j) => { dp += (v - ideal[j]) ** 2; dm += (v - anti[j]) ** 2; });
      dp = Math.sqrt(dp); dm = Math.sqrt(dm);
      return dp + dm === 0 ? 0.5 : dm / (dp + dm);
    });
  }
  const BEN6 = [true, true, true, true, true, false];
  function carbonScores(model, w5, carbon, t) {
    const X6 = model.X.map((row, i) => row.concat([carbon[model.configs[i]]]));
    return closenessMixed(X6, w5.map(x => x * (1 - t)).concat([t]), BEN6);
  }
  function carbonRank(model, w5, carbon, t) {
    const c = carbonScores(model, w5, carbon, t), r = ranks(c);
    return model.configs.map((cfg, i) => ({ config: cfg, score: c[i], rank: r[i] }))
      .sort((a, b) => a.rank - b.rank || CONFIGS.indexOf(a.config) - CONFIGS.indexOf(b.config));
  }
  /* Leaders for t = 0, 0.01, …, tMax. The first place "changes" at the smallest t where no configuration that led
     at t = 0 is still among the leaders (a tie at t = 0 resolved by carbon is not a change). */
  function carbonPath(model, w5, carbon, tMax = 0.6) {
    const path = [];
    for (let i = 0; i <= Math.round(tMax * 100); i++) {
      const t = i / 100, c = carbonScores(model, w5, carbon, t), mx = Math.max(...c);
      path.push({ t, leaders: model.configs.filter((_, j) => c[j] >= mx - 1e-12) });
    }
    const first = path[0].leaders;
    const ch = path.find(p => !p.leaders.some(x => first.includes(x)));
    return { path, first, change: ch ? ch.t : null, after: ch ? ch.leaders : null };
  }

  return { CRITERIA, CONFIGS, rng, dirichlet, dirichletMoM, closeness, closenessMinMax, prometheeNet, methodCheck,
           sampleRegion, regionCentroid, ranks, normalise, activeModel,
           rankConfigs, frontier, smaa, closenessMixed, carbonScores, carbonRank, carbonPath };
})();
if (typeof module !== 'undefined') module.exports = CORE;
