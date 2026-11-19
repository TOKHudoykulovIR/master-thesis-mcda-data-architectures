"""Compare the Explorer carbon add-on (test/js_carbon.json) with the engine (exploratory.carbon_threshold, topsis)."""
import json, sys, numpy as np
sys.path.insert(0, '/mnt/user-data/outputs/engine')
from engine import CRITERIA_EXPLORATORY, CONFIGS, topsis
from engine.matrix import PerformanceModel, secc_floor
from engine.exploratory import carbon_threshold
js = json.load(open('test/js_carbon.json'))
fz = json.load(open('/mnt/user-data/outputs/matrix/matrix-frozen-2026-10-19.json'))['matrix']
est = json.load(open('/mnt/user-data/outputs/carb/carb-summary.json'))['results_p5_p50_p95']
m6 = PerformanceModel({c: {**{k: float(v) for k, v in fz[c].items()}, 'CARB': est[c]['R2'][1]} for c in CONFIGS},
                      criteria=CRITERIA_EXPLORATORY)
W = {'equal': [.2] * 5, 'security': [.1, .15, .15, .15, .45], 'speed': [.35, .3, .1, .15, .1], 'portability': [.1, .15, .45, .15, .15]}
md = 0
for k, w in W.items():
    for mdl, key in ((m6, k), (secc_floor(m6)[0], k + '_floor')):
        c = topsis.closeness(mdl.X(), np.append(np.array(w) * 0.8, 0.2), mdl.benefit())
        md = max(md, np.abs(c - np.array(js[key]['scores20'])).max())
        e = carbon_threshold(mdl, w)
        # engine breaks a tie at t = 0 by index; the Explorer counts a change only when no t = 0 leader remains
        print(f"{key:18s} engine first={e['first_at_zero']} threshold={e['threshold']} | explorer first={js[key].get('first')} change={js[key]['change']}")
print('max abs diff in closeness at t = 0.2:', md)
