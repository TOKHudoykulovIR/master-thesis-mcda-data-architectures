"""End-to-end orchestration of the Stage 2 analysis plan (A1–A16) for one or more scenarios."""
import numpy as np
from . import bwm, aggregate, topsis, promethee, smaa, stats, hypotheses
from .frontier import frontier
from .matrix import secc_floor


def weights_stage(responses, criteria):
    """responses: list of (expert_id, BWMResponse) for ONE scenario. Implements A1–A5 (flags; recontacts are manual)."""
    rows, report = [], []
    for eid, r in responses:
        e = bwm.evaluate(r)
        report.append({'expert': eid, 'attention_ok': e['attention_ok'], 'attention_reasons': e['attention_reasons'],
                       'CR': round(e['CR'], 4), 'threshold': e['threshold'], 'consistent': e['consistent'],
                       'recontact_criterion': criteria[e['recontact_pair']] if not e['consistent'] else None,
                       'xi_L': round(e['xi_L'], 4)})
        if e['attention_ok']:                  # A1: unresolved failures excluded
            rows.append((eid, e['weights'], e['consistent']))
    W = np.array([w for _, w, _ in rows])
    W_consistent = np.array([w for _, w, ok in rows if ok])
    return {'experts': [eid for eid, _, _ in rows], 'W': W, 'W_consistent': W_consistent,
            'group_geometric': aggregate.geometric_mean(W), 'group_arithmetic': aggregate.arithmetic_mean(W),
            'group_consistent_only': aggregate.geometric_mean(W_consistent) if len(W_consistent) else None,
            'kendalls_w': aggregate.kendalls_w(W), 'responses': report}


def _order(configs, scores):
    return [configs[i] for i in np.argsort(-np.asarray(scores), kind='stable')]


def ranking_stage(model, group_w, W, scenario, variants=None, k=10_000, seed=0, frontier_grid=50,
                  group_w_arith=None, W_consistent=None, run_smaa=True):
    """A10–A15 for one scenario. variants: {name: PerformanceModel} for the A14 matrix sensitivity runs.
    group_w_arith: A4 sensitivity (arithmetic aggregation). W_consistent: A3 sensitivity (inconsistent responses excluded).
    run_smaa=False: deterministic parts only (A10–A13, A15), for a scenario below the minimum of five valid responses
    (Stage 2 plan, amendment 3)."""
    out = {'scenario': scenario}
    m_full = model
    if scenario == 'S1':                                           # A10a
        model, excluded = secc_floor(model)
        out['secc_floor_excluded'] = excluded
    X, ben, cfg = model.X(), model.benefit(), model.configs
    c_vec = topsis.closeness(X, group_w, ben, 'vector')
    c_mm = topsis.closeness(X, group_w, ben, 'minmax')
    ph_v = promethee.net_flows(X, group_w, ben, 'vshape')
    ph_u = promethee.net_flows(X, group_w, ben, 'usual')
    out['topsis'] = dict(zip(cfg, np.round(c_vec, 4)))
    out['order_topsis'] = _order(cfg, c_vec)
    out['order_topsis_minmax'] = _order(cfg, c_mm)                  # A12
    out['order_promethee_vshape'] = _order(cfg, ph_v)               # A11
    out['order_promethee_usual'] = _order(cfg, ph_u)
    out['tau_b_topsis_promethee'] = stats.tau_b(c_vec, ph_v)        # R-a
    if group_w_arith is not None:                                   # A4 sensitivity
        out['order_topsis_arithmetic_weights'] = _order(cfg, topsis.closeness(X, group_w_arith, ben, 'vector'))
    if 'C7' in cfg:                                                 # A13 / R-b
        m6 = model.subset([c for c in cfg if c != 'C7'])
        out['order_without_C7'] = _order(m6.configs, topsis.closeness(m6.X(), group_w, ben, 'vector'))
        out['R-b_order_stable'] = hypotheses.R_b(out['order_without_C7'], out['order_topsis'])
    out['variants'] = {}
    if not run_smaa:
        top2 = [model.criteria[i] for i in np.argsort(-np.asarray(group_w))[:2]]              # A15
        out['frontier_pair'] = top2
        out['frontier'] = frontier(model, group_w, top2[0], top2[1], grid=frontier_grid)
        return out
    prim = smaa.run(model, smaa.weight_sampler_dirichlet(W), k=k, seed=seed)                  # A14
    boot = smaa.run(model, smaa.weight_sampler_bootstrap(W), k=k, seed=seed + 1)
    out['smaa'] = prim
    out['first_rank'] = dict(zip(cfg, np.round(prim['first_rank'], 4)))
    out['first_rank_bootstrap'] = dict(zip(cfg, np.round(boot['first_rank'], 4)))
    if scenario == 'S1':
        nf = smaa.run(m_full, smaa.weight_sampler_dirichlet(W), k=k, seed=seed + 2)
        out['first_rank_no_floor'] = dict(zip(m_full.configs, np.round(nf['first_rank'], 4)))
    if W_consistent is not None and len(W_consistent) >= 2:        # A3 sensitivity
        rc = smaa.run(model, smaa.weight_sampler_dirichlet(W_consistent), k=k, seed=seed + 4)
        out['first_rank_consistent_only'] = dict(zip(cfg, np.round(rc['first_rank'], 4)))
    out['variants'] = {}
    for name, vm in (variants or {}).items():
        if scenario == 'S1':
            vm, _ = secc_floor(vm)
        r = smaa.run(vm, smaa.weight_sampler_dirichlet(W), k=k, seed=seed + 3)
        out['variants'][name] = dict(zip(vm.configs, np.round(r['first_rank'], 4)))
    top2 = [model.criteria[i] for i in np.argsort(-np.asarray(group_w))[:2]]                  # A15
    out['frontier_pair'] = top2
    out['frontier'] = frontier(model, group_w, top2[0], top2[1], grid=frontier_grid)
    return out


def scenario_tests(records_by_criterion, criteria):
    """A7: exact within-expert permutation test per criterion, Holm-corrected.
    records_by_criterion: {criterion: [(expert, scenario, weight), ...]}."""
    res = {c: stats.perm_test_scenarios(records_by_criterion[c]) for c in criteria}
    adj = stats.holm([res[c][1] for c in criteria])
    return {c: {'stat': round(res[c][0], 6), 'p': round(res[c][1], 4), 'p_holm': round(float(a), 4), 'kind': res[c][2]}
            for c, a in zip(criteria, adj)}
