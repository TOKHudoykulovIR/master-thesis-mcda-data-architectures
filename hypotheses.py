"""Evaluation of H1–H3, P1–P4, R-a, R-b exactly as worded in the Stage 2 plan (A7, A16)."""
import numpy as np

MARGIN = 0.05   # A16: fewer than five percentage points -> indeterminate


def _set_vs_rest(configs, first_rank, claimed, against=None):
    fr = dict(zip(configs, first_rank))
    # a claimed configuration excluded by the S1 SECC floor has first-rank acceptability 0
    inside = max([fr[c] for c in claimed if c in fr], default=0.0)
    others = [c for c in (against or configs) if c not in claimed and c in fr]
    outside = max(fr[c] for c in others) if others else 0.0
    d = inside - outside
    verdict = 'supported' if d >= MARGIN else ('not supported' if d <= -MARGIN else 'indeterminate')
    return verdict, round(float(d), 4)


def H(group_w, criteria):
    """group_w: {scenario: vector}. Descriptive direction checks (tests are in stats.perm_test_scenarios).
    H3 as revised after Round 1: PORT weighs more in S3 than in S2 (the original H3 on CARB cannot be tested,
    since CARB was excluded from the weighting). If CARB is among the criteria (exploratory run), the
    original direction is reported as 'H3-carbon (exploratory)'."""
    top = {s: criteria[int(np.argmax(w))] for s, w in group_w.items()}
    port = {s: float(w[criteria.index('PORT')]) for s, w in group_w.items()}
    out = {'H1 (S1: SECC highest)': top.get('S1') == 'SECC',
           'H2 (S2: TTDP or AIRD highest)': top.get('S2') in ('TTDP', 'AIRD'),
           'H3 (S3: PORT above S2)': (port['S3'] > port['S2']) if {'S2', 'S3'} <= set(port) else None,
           'top criterion by scenario': top}
    if 'CARB' in criteria:
        carb = {s: float(w[criteria.index('CARB')]) for s, w in group_w.items()}
        out['H3-carbon (exploratory; S3: CARB above S1 and S2)'] = (
            carb['S3'] > max(carb['S1'], carb['S2'])) if {'S1', 'S2', 'S3'} <= set(carb) else None
    return out


def P(first_rank):
    """first_rank: {scenario: (configs, first-rank acceptability array)}."""
    out = {}
    if 'S1' in first_rank:
        out['P1 (S1: C1 or C3 highest)'] = _set_vs_rest(*first_rank['S1'], claimed=('C1', 'C3'))
    if 'S2' in first_rank:
        cfg, fr = first_rank['S2']; d = dict(zip(cfg, fr))
        s = d.get('C5', 0) + d.get('C6', 0)
        out['P2 (S2: C5+C6 below 10%)'] = ('supported' if s < 0.10 else 'not supported', round(float(s), 4))
    if 'S3' in first_rank:
        out['P3 (S3: C2, C4 or C6 highest)'] = _set_vs_rest(*first_rank['S3'], claimed=('C2', 'C4', 'C6'))
    per = {s: _set_vs_rest(cfg, fr, claimed=('C3', 'C4'), against=('C1', 'C2', 'C5', 'C6'))
           for s, (cfg, fr) in first_rank.items()}
    verdicts = [v for v, _ in per.values()]
    overall = 'supported' if 'supported' in verdicts else ('indeterminate' if 'indeterminate' in verdicts else 'not supported')
    out['P4 (hub beats every centralised and federated in >=1 scenario)'] = (overall, per)
    return out


def R_a(taus, threshold=0.7):
    return {s: (t >= threshold, round(t, 3)) for s, t in taus.items()}


def R_b(order_without_c7, order_with_c7):
    """Relative order of C1–C6 unchanged when C7 is added."""
    with_filtered = [c for c in order_with_c7 if c != 'C7']
    return with_filtered == list(order_without_c7)
