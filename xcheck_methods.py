import json, sys, numpy as np
sys.path.insert(0, '/mnt/user-data/outputs/engine')
from engine import topsis, promethee
from engine.matrix import PerformanceModel
js = json.load(open('test/js_methods.json'))
an = json.load(open('/mnt/user-data/outputs/round2/analysis/round2-analysis.json'))
M = json.load(open('/mnt/user-data/outputs/matrix/matrix-frozen-2026-10-19.json'))['matrix']
model = PerformanceModel({c: {k: float(v) for k, v in M[c].items()} for c in M}); model.apply_tco_k11(3, 3)
X, ben = model.X(), model.benefit()
W = [[0.2]*5,[0.1,0.1,0.2,0.1,0.5],[0.35,0.3,0.1,0.15,0.1],[0.05,0.1,0.6,0.1,0.15],[0.3,0.05,0.25,0.1,0.3]]
d1 = max(np.abs(topsis.closeness(X, w, ben, 'minmax') - np.array(js['minmax'][i])).max() for i, w in enumerate(W))
d2 = max(np.abs(promethee.net_flows(X, w, ben) - np.array(js['promethee'][i])).max() for i, w in enumerate(W))
print('min-max TOPSIS max abs diff:', d1); print('PROMETHEE II max abs diff:', d2)
print('leaders per weight set:', js['leaders'])
print('region violations:', js['regionViolations'], '| centroid (SECC most, TTDP least):', np.round(js['centroid'], 4))
worst = 0
for s in ['S1', 'S2', 'S3']:
    eng = an['scenarios'][s]['E-O1']['main']['first_rank']
    diff = max(abs(eng[c] - js['eo1'][s][c]) for c in eng); worst = max(worst, diff)
    print(s, 'engine', {c: round(v, 3) for c, v in eng.items()}, '| page', {c: round(v, 3) for c, v in js['eo1'][s].items()}, '| max diff', round(diff, 4))
assert d1 < 1e-12 and d2 < 1e-12 and js['regionViolations'] == 0 and worst < 0.02
print('OK')
