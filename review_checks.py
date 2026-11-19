"""Checks added after the review of the thesis draft (November 2026). They are NOT part of the analysis plan.

Reproduces:
  - Table 21 note: closeness from unrounded and from two-decimal group weights;
  - Section 4.4: C4 vs C6 in S3 under other random seeds (identical scores, so the gap is sampling noise);
  - Table 22, run 'Delivery speed equal': TTDP set to 2 for every configuration;
  - Table 22, run 'Coded values of the reset cells': C1, C2, C7 x TTDP = 1; C4 x TTDP = 5; C4 x SECC = 4;
  - Section 4.4: C5 vs C3 on the same weight draws, among the warehouse configurations and among all seven.

Usage (from this folder):  python review_checks.py
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'engine'))
import round2_analysis as RA
from engine import CRITERIA, CONFIGS, ordinal, smaa
from engine.matrix import secc_floor
from engine.topsis import closeness_batch

frozen = RA.load_frozen_matrix(os.path.join(HERE, '..', 'matrix', 'matrix-frozen-2026-10-19.json'))
ent = RA.enterprise_cells(os.path.join(HERE, '..', 'matrix', 'coding-sheet-coder1.xlsx'))
model, _ = RA.build_models(frozen, ent)
data = json.load(open(os.path.join(HERE, 'imports', '2026-10-19-AB-corrected', 'round2-responses.json'), encoding='utf-8'))
an = json.load(open(os.path.join(HERE, 'analysis', 'round2-analysis.json'), encoding='utf-8'))
gw = {s: an['scenarios'][s]['weights']['group_geometric'] for s in ['S1', 'S2', 'S3']}


def eo1(m, scenario, seed=ordinal.SEED, floor=None):
    keep, _ = ordinal.usable_choices(RA._choices(data, scenario))
    floor = (scenario == 'S1') if floor is None else floor
    mm = secc_floor(m)[0] if floor else m
    res = ordinal._summary(smaa.run(mm, ordinal.weight_sampler_ordinal(keep, len(m.criteria)), k=10_000, seed=seed))
    return {c: round(float(v), 4) for c, v in sorted(res['first_rank'].items(), key=lambda x: -x[1]) if v >= 0.005}


def topsis(m, w, floor=False):
    mm = secc_floor(m)[0] if floor else m
    c = closeness_batch(mm.X()[None], np.asarray(w, float)[None], mm.benefit())[0]
    return {k: round(float(v), 4) for k, v in sorted(zip(mm.configs, c), key=lambda x: -x[1])}


print('1. Closeness: unrounded vs two-decimal group weights')
for s in ['S1', 'S2', 'S3']:
    w = [gw[s][k] for k in CRITERIA]
    print(' ', s, 'unrounded', topsis(model, w, s == 'S1'))
    print(' ', s, '2 dp     ', topsis(model, list(np.round(w, 2)), s == 'S1'))

print('2. S3, C4 vs C6 under other seeds')
for seed in [ordinal.SEED, 1, 2, 3, 4]:
    r = eo1(model, 'S3', seed=seed)
    print(' ', seed, 'C4', r.get('C4'), 'C6', r.get('C6'))

print('3. Delivery speed equal (TTDP = 2 for all)')
mt = model.copy()
for c in CONFIGS:
    mt.base[c]['TTDP'] = 2.0
for s in ['S1', 'S2', 'S3']:
    print(' ', s, eo1(mt, s))

print('4. Coded values of the five reset cells')
for label, cells in [('all five', [('C1', 'TTDP', 1), ('C2', 'TTDP', 1), ('C7', 'TTDP', 1), ('C4', 'TTDP', 5), ('C4', 'SECC', 4)]),
                     ('C4 x SECC only', [('C4', 'SECC', 4)]), ('C4 x TTDP only', [('C4', 'TTDP', 5)])]:
    ms = model.copy()
    for c, k, v in cells:
        ms.base[c][k] = float(v)
    for s in ['S1', 'S2', 'S3']:
        print(' ', label, s, eo1(ms, s))

print('5. S1: C5 closer to the ideal than C3 on the same weight draws')
keep, _ = ordinal.usable_choices(RA._choices(data, 'S1'))
W = ordinal.weight_sampler_ordinal(keep, 5)(np.random.default_rng(7), 20000)
for label, cfgs in [('warehouses (C1, C3, C5)', ['C1', 'C3', 'C5']), ('all seven', CONFIGS)]:
    m = model.subset(cfgs)
    C = closeness_batch(np.broadcast_to(m.X(), (len(W),) + m.X().shape), W, m.benefit())
    i3, i5 = m.configs.index('C3'), m.configs.index('C5')
    print(' ', label, round(float((C[:, i5] > C[:, i3]).mean()), 3))
