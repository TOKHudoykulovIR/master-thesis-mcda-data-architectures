"""E-O1 — exploratory SMAA with ordinal weight information (Stage 2 plan, amendment 3, point 5).

A14 cannot run: no scenario has the five valid BWM responses it needs. E-O1 uses only each panellist's MOST and
LEAST choice per scenario. Each draw picks one panellist at random (equal probability), then a weight vector
uniformly from that panellist's region {w on the simplex : w[MOST] is the largest, w[LEAST] the smallest}; the
other three criteria are unordered. The draws are combined with the performance matrix through TOPSIS by
smaa.run, exactly as in A14 (same matrix uncertainty, same SECC floor in S1)."""
import numpy as np
from . import smaa
from .matrix import secc_floor

SEED = 20261019


def sample_region(rng, k, best, worst, n):
    """k weight vectors uniform on {w in simplex_n : w[best] = max, w[worst] = min}.
    A uniform simplex draw is sorted; the largest value goes to `best`, the smallest to `worst`, and the middle
    values to the other criteria in a random order. The region is the union of the (n-2)! order cones that put
    `best` first and `worst` last; all cones have equal volume, so this is exactly uniform on the region."""
    if best == worst:
        raise ValueError('MOST and LEAST must differ')
    u = np.sort(rng.dirichlet(np.ones(n), k), axis=1)                  # ascending
    W = np.empty((k, n))
    W[:, best], W[:, worst] = u[:, -1], u[:, 0]
    middle = [j for j in range(n) if j not in (best, worst)]
    perm = np.argsort(rng.random((k, n - 2)), axis=1)
    W[:, middle] = np.take_along_axis(u[:, 1:-1], perm, axis=1)
    return W


def usable_choices(choices):
    """choices: list of (panellist, best_index, worst_index). Drops MOST == LEAST (no ordinal information)."""
    keep = [(p, b, w) for p, b, w in choices if b is not None and w is not None and b != w]
    dropped = [p for p, b, w in choices if (p, b, w) not in keep]
    return keep, dropped


def weight_sampler_ordinal(choices, n):
    """Mixture over panellists with equal probability; uniform inside each panellist's region."""
    keep, _ = usable_choices(choices)
    if not keep:
        raise ValueError('no usable MOST/LEAST choice')
    bw = [(b, w) for _, b, w in keep]

    def f(rng, k):
        who = rng.integers(0, len(bw), k)
        W = np.empty((k, n))
        for i, (b, w) in enumerate(bw):
            sel = who == i
            if sel.any():
                W[sel] = sample_region(rng, int(sel.sum()), b, w, n)
        return W
    return f


def weight_sampler_uniform(n):
    """Reference run (iv): no preference information."""
    return lambda rng, k: rng.dirichlet(np.ones(n), k)


def choice_counts(choices, criteria):
    """Descriptive companion: how often each criterion was chosen as MOST and as LEAST."""
    most = {c: 0 for c in criteria}
    least = {c: 0 for c in criteria}
    for _, b, w in choices:
        if b is not None:
            most[criteria[b]] += 1
        if w is not None:
            least[criteria[w]] += 1
    return {'MOST': most, 'LEAST': least, 'n': len(choices)}


def _summary(res):
    cfg = res['configs']
    return {'first_rank': dict(zip(cfg, np.round(res['first_rank'], 4))),
            'acceptability': {c: np.round(res['acceptability'][i], 4).tolist() for i, c in enumerate(cfg)},
            'central_weights': {c: (None if np.isnan(res['central_weights'][i]).any()
                                    else np.round(res['central_weights'][i], 4).tolist()) for i, c in enumerate(cfg)},
            'confidence': {c: (None if np.isnan(res['confidence'][i]) else round(float(res['confidence'][i]), 4))
                           for i, c in enumerate(cfg)}}


def run_scenario(model, scenario, choices_all, choices_a1=None, variants=None, k=10_000, seed=SEED):
    """E-O1 for one scenario. choices_all: every panellist's (code, best, worst); choices_a1: only scenario responses
    that pass A1 (sensitivity i). variants: {name: PerformanceModel} for sensitivity iii.
    Returns a dict of summaries; `main` carries the full acceptability matrix."""
    n = len(model.criteria)
    keep, dropped = usable_choices(choices_all)
    floor = scenario == 'S1'
    m = secc_floor(model)[0] if floor else model
    out = {'scenario': scenario, 'panellists': [p for p, _, _ in keep], 'dropped_same_most_least': dropped,
           'secc_floor_excluded': secc_floor(model)[1] if floor else []}
    out['main'] = _summary(smaa.run(m, weight_sampler_ordinal(keep, n), k=k, seed=seed))
    if choices_a1 is not None:
        keep_a1, _ = usable_choices(choices_a1)
        out['a1_only_panellists'] = [p for p, _, _ in keep_a1]
        out['a1_only'] = (_summary(smaa.run(m, weight_sampler_ordinal(keep_a1, n), k=k, seed=seed + 1))
                          if keep_a1 else None)
    if floor:
        out['no_floor'] = _summary(smaa.run(model, weight_sampler_ordinal(keep, n), k=k, seed=seed + 2))
    out['variants'] = {}
    for name, vm in (variants or {}).items():
        vm = secc_floor(vm)[0] if floor else vm
        out['variants'][name] = _summary(smaa.run(vm, weight_sampler_ordinal(keep, n), k=k, seed=seed + 3))['first_rank']
    out['uniform_reference'] = _summary(smaa.run(m, weight_sampler_uniform(n), k=k, seed=seed + 4))
    return out
