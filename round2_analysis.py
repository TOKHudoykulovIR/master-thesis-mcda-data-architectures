"""Delphi Round 2 — analysis on the imported responses (Stage 2 plan A1–A16, E-C1, E-O1; amendment 3).

Run ONLY after Round 2 has closed: the close date is a required argument and is written into the output. Running it
earlier would show results while the close date is still open (amendment 3, point 2).

What it does, per scenario:
  - A1–A5 on the BWM responses (pipeline.weights_stage): valid responses, consistency, group weights, Kendall's W
    (descriptive; no Round 3, amendment 3 point 4);
  - A10–A13 and A15 on the group weights, descriptively, if at least one valid response exists;
  - A14 (panel-fitted SMAA) only if the scenario has at least five valid responses (minimum for analysis);
  - E-O1 (ordinal SMAA) for every scenario, from every panellist's MOST and LEAST choices, with its sensitivity runs;
  - E-C1 carbon answers (all) and carbon weights (valid BWM responses only).
Across scenarios: A7 permutation tests, H1–H3 by direction, P1–P4 exploratory on E-O1 (and as specified on A14 where
it runs), A8 qualified subgroup (weights only).

Inputs: the import's round2-responses.json; the frozen matrix (its SHA-256 is checked); the coding sheet's Variant
sheet for the Enterprise edition cells (K7).

Usage (from this folder):
  python round2_analysis.py --responses imports/<date>/round2-responses.json --closed YYYY-MM-DD
  options: --out analysis/round2-analysis.json  --report analysis/round2-analysis-report.md  --plots analysis/
           --k 10000  --matrix ../matrix/matrix-frozen-2026-10-19.json  --sheet ../matrix/coding-sheet-coder1.xlsx"""
import argparse, datetime, hashlib, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'engine'))
from engine import CRITERIA, CONFIGS                                          # noqa: E402
from engine import pipeline, hypotheses, ordinal, exploratory                  # noqa: E402
from engine.matrix import PerformanceModel, variant_c6_blocked, variant_edition  # noqa: E402
from engine.frontier import plot                                               # noqa: E402
from engine.provenance import environment                                      # noqa: E402
from round2_import import load_responses                                       # noqa: E402

SCENARIOS = ['S1', 'S2', 'S3']
MIN_FOR_SMAA = 5


class AnalysisError(Exception):
    pass


# ---- inputs -------------------------------------------------------------------------------------------------
def load_frozen_matrix(path):
    with open(path, encoding='utf-8') as f:
        rec = json.load(f)
    canon = json.dumps(rec['matrix'], sort_keys=True, separators=(',', ':'))
    if hashlib.sha256(canon.encode()).hexdigest() != rec['sha256_of_canonical_json']:
        raise AnalysisError('frozen matrix does not match its recorded SHA-256')
    return rec


def enterprise_cells(sheet_path):
    """K7: the Enterprise-edition cells from the coding sheet's Variant sheet -> {(config, criterion): score}."""
    import openpyxl
    ws = openpyxl.load_workbook(sheet_path, data_only=True)['Variant']
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] and row[1] and row[3] and row[7] is not None:
            out[(str(row[1]).strip(), str(row[3]).strip())] = float(str(row[7]).strip())
    return out


def build_models(frozen, enterprise):
    """Primary model (A9, K11) and the A14 matrix variants (K9, K7, K11 directional)."""
    base = {c: {k: float(v) for k, v in frozen['matrix'][c].items()} for c in CONFIGS}
    model = PerformanceModel(base)
    model.apply_tco_k11(base['C1']['TCO'], base['C2']['TCO'])
    variants = {'K9 C6 TTDP=1': variant_c6_blocked(model),
                'K7 Enterprise edition': variant_edition(model, enterprise)}
    d = model.copy(); d.apply_tco_k11(base['C1']['TCO'], base['C2']['TCO'], directional=True)
    variants['K11 directional TCO'] = d
    return model, variants


# ---- per scenario -------------------------------------------------------------------------------------------
def _choices(data, scenario, a1_only=False):
    out = []
    for code, r in sorted(data['respondents'].items()):
        s = r['scenarios'].get(scenario)
        if not s or not s.get('valid') or (a1_only and not s['A1']['passed']):
            continue
        out.append((code, CRITERIA.index(s['best']), CRITERIA.index(s['worst'])))
    return out


def _carbon(data, scenario, experts, W):
    """E-C1: every carbon answer (descriptive); carbon weight only for valid BWM responses. The anchor is the
    MOST choice of the first submission (amendment 1, point 3; a correction never changes MOST)."""
    answers, weights = {}, {}
    for code, r in sorted(data['respondents'].items()):
        s = r['scenarios'].get(scenario) or {}
        if s.get('carbon'):
            answers[code] = {k: s['carbon'][k] for k in ('direction', 'rating', 'a', 'consistent')}
    for code, w in zip(experts, W):
        s = data['respondents'][code]['scenarios'][scenario]
        if s.get('carbon'):
            w6 = exploratory.append_carbon(w, CRITERIA.index(s['best']), s['carbon']['a'])
            weights[code] = float(w6[-1])
    return {'answers': answers, 'carbon_weight_valid_bwm': weights,
            'inconsistent_answers': sum(1 for a in answers.values() if not a['consistent'])}


def analyse_scenario(data, scenario, model, variants, k, seed, plots=None):
    responses = load_responses(data, scenario)
    n_a1 = sum(1 for code, _ in responses if data['respondents'][code]['scenarios'][scenario]['A1']['passed'])
    out = {'scenario': scenario, 'parsed_responses': len(responses), 'valid_A1': n_a1}
    ws = None
    if n_a1 >= 1:
        ws = pipeline.weights_stage(responses, CRITERIA)
        out['weights'] = {
            'experts': ws['experts'], 'individual': {e: dict(zip(CRITERIA, np.round(w, 4))) for e, w in zip(ws['experts'], ws['W'])},
            'group_geometric': dict(zip(CRITERIA, np.round(ws['group_geometric'], 4))),
            'group_arithmetic': dict(zip(CRITERIA, np.round(ws['group_arithmetic'], 4))),
            'group_consistent_only': (None if ws['group_consistent_only'] is None
                                      else dict(zip(CRITERIA, np.round(ws['group_consistent_only'], 4)))),
            'kendalls_W': round(ws['kendalls_w'], 4) if len(ws['experts']) >= 2 else None,
            'responses': ws['responses']}
        run_smaa = n_a1 >= MIN_FOR_SMAA
        r = pipeline.ranking_stage(model, ws['group_geometric'], ws['W'], scenario, variants if run_smaa else None,
                                   k=k, seed=seed, group_w_arith=ws['group_arithmetic'],
                                   W_consistent=ws['W_consistent'], run_smaa=run_smaa)
        va, vb, grid = r.pop('frontier')
        if plots:
            cfg = [c for c in CONFIGS if not (scenario == 'S1' and c in r.get('secc_floor_excluded', []))]
            plot(va, vb, grid, cfg, *r['frontier_pair'], os.path.join(plots, f'frontier_{scenario}.png'),
                 title=f'{scenario} — first-ranked configuration (group weights of {n_a1} valid responses)')
        out['A14_run'] = run_smaa
        if run_smaa:
            smaa = r.pop('smaa')
            out['A14_first_rank_array'] = (smaa['configs'], smaa['first_rank'])
        out['ranking_descriptive' if not run_smaa else 'ranking'] = r
    else:
        out['A14_run'] = False
    ch_all, ch_a1 = _choices(data, scenario), _choices(data, scenario, a1_only=True)
    out['choice_counts'] = ordinal.choice_counts(ch_all, CRITERIA)
    out['E-O1'] = ordinal.run_scenario(model, scenario, ch_all, ch_a1, variants, k=k, seed=ordinal.SEED)
    out['E-C1'] = _carbon(data, scenario, ws['experts'] if ws else [], ws['W'] if ws else [])
    out['_ws'] = ws
    return out


# ---- across scenarios ---------------------------------------------------------------------------------------
def analyse(data, model, variants, closed, k=10_000, seed=20261014, plots=None):
    res = {'WARNING': 'Round 2 analysis on real responses. Group weights are descriptive where fewer than five valid '
                      'responses exist; E-O1 is exploratory (Stage 2 plan, amendment 3).',
           'round2_closed': closed, 'environment': environment(),
           'imported': data.get('_imported'), 'corrections_applied': data.get('corrections_applied', []),
           'scenarios': {}}
    for s in SCENARIOS:
        res['scenarios'][s] = analyse_scenario(data, s, model, variants, k, seed, plots)
    records = {c: [] for c in CRITERIA}
    group = {}
    for s, r in res['scenarios'].items():
        ws = r.pop('_ws')
        if ws is None:
            continue
        group[s] = ws['group_geometric']
        for e, w in zip(ws['experts'], ws['W']):
            for j, c in enumerate(CRITERIA):
                records[c].append((e, s, w[j]))
    res['A7'] = pipeline.scenario_tests(records, CRITERIA) if all(records.values()) else None
    res['H'] = hypotheses.H(group, CRITERIA)
    eo1 = {s: (list(r['E-O1']['main']['first_rank']), np.array(list(r['E-O1']['main']['first_rank'].values())))
           for s, r in res['scenarios'].items()}
    res['P_exploratory_E-O1'] = hypotheses.P(eo1)
    a14 = {s: r.pop('A14_first_rank_array') for s, r in res['scenarios'].items() if 'A14_first_rank_array' in r}
    res['P_as_specified_A14'] = hypotheses.P(a14) if a14 else None
    res['P_as_specified_A14_scenarios'] = sorted(a14)
    qualified = [c for c, r in data['respondents'].items() if r['profile'].get('A8_qualified')]
    sub = {}
    for s in SCENARIOS:
        resp = [(c, b) for c, b in load_responses(data, s) if c in qualified]
        if any(data['respondents'][c]['scenarios'][s]['A1']['passed'] for c, _ in resp):
            w = pipeline.weights_stage(resp, CRITERIA)
            sub[s] = {'n': len(w['experts']), 'group_geometric': dict(zip(CRITERIA, np.round(w['group_geometric'], 4)))}
    res['A8_subgroup'] = {'members': sorted(qualified), 'weights': sub}
    return res


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.floating):
        return None if np.isnan(o) else float(o)
    if isinstance(o, float) and np.isnan(o):
        return None
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    return o


def report_md(res):
    L = ['# Round 2 — analysis report', '',
         f"Round 2 closed {res['round2_closed']}. Import of {res['imported']}. "
         f"Corrections applied: {len(res['corrections_applied'])}.", '',
         '| Scenario | Parsed | Valid (A1) | A14 run | Kendall\'s W | E-O1 panellists | E-O1 leader (first-rank) | Uniform reference leader |',
         '|---|---|---|---|---|---|---|---|']
    for s, r in res['scenarios'].items():
        fr = r['E-O1']['main']['first_rank']; top = max(fr, key=fr.get)
        u = r['E-O1']['uniform_reference']['first_rank']; utop = max(u, key=u.get)
        w = r.get('weights', {}).get('kendalls_W')
        L.append(f"| {s} | {r['parsed_responses']} | {r['valid_A1']} | {'yes' if r['A14_run'] else 'no'} | "
                 f"{'—' if w is None else w} | {len(r['E-O1']['panellists'])} | {top} ({fr[top]:.2f}) | {utop} ({u[utop]:.2f}) |")
    L += ['', '**H (direction of group weights, descriptive):** ' + json.dumps(clean(res['H']), ensure_ascii=False),
          '', '**P1–P4, exploratory examination on E-O1:** ' + json.dumps(clean(res['P_exploratory_E-O1']), ensure_ascii=False),
          '', '**P as specified (A14), scenarios:** ' + (', '.join(res['P_as_specified_A14_scenarios']) or 'none'),
          '', 'Full results: the JSON file. Group weights below five valid responses are descriptive only.']
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--responses', required=True)
    ap.add_argument('--closed', required=True, help='date Round 2 closed, YYYY-MM-DD')
    ap.add_argument('--matrix', default=os.path.join(HERE, '..', 'matrix', 'matrix-frozen-2026-10-19.json'))
    ap.add_argument('--sheet', default=os.path.join(HERE, '..', 'matrix', 'coding-sheet-coder1.xlsx'))
    ap.add_argument('--out', default=os.path.join(HERE, 'analysis', 'round2-analysis.json'))
    ap.add_argument('--report', default=os.path.join(HERE, 'analysis', 'round2-analysis-report.md'))
    ap.add_argument('--plots', default=os.path.join(HERE, 'analysis'))
    ap.add_argument('--k', type=int, default=10_000)
    a = ap.parse_args(argv)
    closed = datetime.date.fromisoformat(a.closed).isoformat()
    model, variants = build_models(load_frozen_matrix(a.matrix), enterprise_cells(a.sheet))
    with open(a.responses, encoding='utf-8') as f:
        data = json.load(f)
    os.makedirs(os.path.dirname(a.out), exist_ok=True); os.makedirs(a.plots, exist_ok=True)
    res = analyse(data, model, variants, closed, k=a.k, plots=a.plots)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(clean(res), f, indent=1, ensure_ascii=False)
    md = report_md(clean(res))
    with open(a.report, 'w', encoding='utf-8') as f:
        f.write(md)
    print(md)


if __name__ == '__main__':
    main()
