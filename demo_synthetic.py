"""SYNTHETIC end-to-end run of the engine, in the post-Round-1 design: five primary criteria, six panellists,
each rating all three scenarios; exploratory carbon analyses (E-C1-E-C3) on top.
Every number here is invented to exercise the code path: the panel, the weights, the carbon answers and the
coded matrix values are NOT data and must not be read as results. The CARB values in the exploratory part use
the estimate's joint draws (carb/carb-draws.npz) if present.
Run from the engine folder:  python demo_synthetic.py"""
import json, os
import numpy as np
from engine import CRITERIA, CRITERIA_EXPLORATORY, CONFIGS
from engine.bwm import BWMResponse
from engine.matrix import PerformanceModel, variant_c6_blocked, variant_edition, variant_carb
from engine import pipeline, hypotheses, exploratory
from engine.provenance import environment
from engine.frontier import plot

rng = np.random.default_rng(20261001)
OUT = 'demo_output'; os.makedirs(OUT, exist_ok=True)

# ---- synthetic panel: 6 panellists x 3 scenarios (Stage 1 amendment 7), primary criteria only ---------------
true = {'S1': np.array([.15, .15, .15, .15, .40]), 'S2': np.array([.30, .25, .10, .25, .10]),
        'S3': np.array([.15, .10, .35, .15, .25])}
def to_bwm(w):
    b, wo = int(np.argmax(w)), int(np.argmin(w))
    bo = np.clip(np.rint(w[b] / w), 1, 9); ow = np.clip(np.rint(w / w[wo]), 1, 9)
    bo[b] = 1; ow[wo] = 1; ow[b] = bo[wo]
    return BWMResponse(b, wo, bo, ow)
responses = {s: [] for s in true}; records = {c: [] for c in CRITERIA}; best_of = {}
for e in range(6):
    for s in true:
        w = rng.dirichlet(true[s] * 40); r = to_bwm(w)
        responses[s].append((f'R{e + 2:02d}', r)); best_of[(f'R{e + 2:02d}', s)] = r.best
weights = {s: pipeline.weights_stage(responses[s], CRITERIA) for s in true}
for s, ws in weights.items():
    for eid, w in zip(ws['experts'], ws['W']):
        for j, c in enumerate(CRITERIA):
            records[c].append((eid, s, w[j]))

# ---- synthetic matrix (placeholder scores, drawn at random: NOT coded values) -----------------------------
coded = {c: {k: float(rng.integers(2, 6)) for k in ['TTDP', 'AIRD', 'PORT', 'SECC']} for c in CONFIGS}
base = {c: {'TCO': 3.0, **coded[c]} for c in CONFIGS}
model = PerformanceModel(base)
model.apply_tco_k11(tco_c1=3.0, tco_c2=3.0)                          # K11 (C1 = C2 when evidence conflicts)
model.mark_insufficient('C7', 'PORT')                                 # example of an insufficient cell
variants = {
    'K9 C6 TTDP=1': variant_c6_blocked(model),
    'K7 Enterprise edition': variant_edition(model, {('C1', 'SECC'): 4, ('C3', 'SECC'): 4, ('C5', 'SECC'): 3,
                                                     ('C7', 'SECC'): 3, ('C1', 'TCO'): 3.5}),
}
dirm = model.copy(); dirm.apply_tco_k11(3.0, 3.0, directional=True); variants['K11 directional TCO'] = dirm

# ---- primary ranking per scenario ---------------------------------------------------------------------------
results, fr_for_P, taus = {}, {}, {}
for s in true:
    r = pipeline.ranking_stage(model, weights[s]['group_geometric'], weights[s]['W'], s, variants, k=10_000, seed=7,
                               group_w_arith=weights[s]['group_arithmetic'], W_consistent=weights[s]['W_consistent'])
    va, vb, grid = r.pop('frontier')
    plot(va, vb, grid, r['smaa']['configs'], *r['frontier_pair'], os.path.join(OUT, f'frontier_{s}.png'),
         title=f'{s} (SYNTHETIC) — first-ranked configuration')
    fr_for_P[s] = (r['smaa']['configs'], r['smaa']['first_rank']); taus[s] = r['tau_b_topsis_promethee']
    r.pop('smaa'); results[s] = r

# ---- exploratory carbon analyses (E-C1-E-C3) -----------------------------------------------------------------
carb_path = os.path.join('..', 'carb', 'carb-draws.npz')
if os.path.exists(carb_path):
    d = np.load(carb_path); carb_draws = d['R2']; carb_floor = d['R2_floor'] if 'R2_floor' in d.files else None
else:
    carb_draws = np.column_stack([rng.normal(100 + 30 * i, 10, 4000) for i in range(7)]); carb_floor = None
model6 = PerformanceModel({c: {**model.base[c], 'CARB': float(np.median(carb_draws[:, i]))} for i, c in enumerate(CONFIGS)},
                          criteria=CRITERIA_EXPLORATORY, samplers=model.samplers, carb_draws=carb_draws)
carbon_answer = {'S1': ('less', 7), 'S2': ('less', 8), 'S3': ('less', 2)}   # invented answers, same for everyone
explor, g6_all = {}, {}
for s in true:
    a = exploratory.carbon_ratio(*carbon_answer[s])
    W6 = np.array([exploratory.append_carbon(w, best_of[(eid, s)], a)
                   for eid, w in zip(weights[s]['experts'], weights[s]['W'])])
    g6 = np.exp(np.log(W6).mean(axis=0)); g6 /= g6.sum(); g6_all[s] = g6
    r6 = pipeline.ranking_stage(model6, g6, W6, s, k=4000, seed=11, frontier_grid=10)
    entry = {'group_weight_CARB': round(float(g6[-1]), 3),
             'first_rank_with_carbon': r6['first_rank'],
             'carbon_threshold': {k: v for k, v in exploratory.carbon_threshold(
                 model6, weights[s]['group_geometric']).items() if k != 'path'}}
    if carb_floor is not None:
        rf = pipeline.ranking_stage(variant_carb(model6, carb_floor, 'CARB S7 floor'), g6, W6, s, k=4000, seed=12,
                                    frontier_grid=10)
        entry['first_rank_with_carbon_floor_model'] = rf['first_rank']
    explor[s] = entry
H_explor = hypotheses.H(g6_all, CRITERIA_EXPLORATORY)

summary = {
    'WARNING': 'SYNTHETIC DEMO — invented panel, matrix and carbon answers. Not results.',
    'environment': environment(),
    'weights': {s: {'group_geometric': dict(zip(CRITERIA, np.round(w['group_geometric'], 3))),
                    'kendalls_W': round(w['kendalls_w'], 3), 'n': len(w['W']),
                    'inconsistent': [x['expert'] for x in w['responses'] if not x['consistent']]} for s, w in weights.items()},
    'A7 scenario tests': pipeline.scenario_tests(records, CRITERIA),
    'H': hypotheses.H({s: w['group_geometric'] for s, w in weights.items()}, CRITERIA),
    'P': hypotheses.P(fr_for_P), 'R-a': hypotheses.R_a(taus),
    'ranking': results, 'matrix notes': model.notes,
    'EXPLORATORY carbon (E-C1-E-C3)': explor,
    'EXPLORATORY H3-carbon': H_explor.get('H3-carbon (exploratory; S3: CARB above S1 and S2)'),
}
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(summary), open(os.path.join(OUT, 'summary.json'), 'w'), indent=2, ensure_ascii=False)
print(json.dumps(clean({k: summary[k] for k in ['weights', 'A7 scenario tests', 'H', 'P']}), indent=1, ensure_ascii=False)[:2500])
print('EXPLORATORY:', json.dumps(clean(explor), indent=1)[:1500])
