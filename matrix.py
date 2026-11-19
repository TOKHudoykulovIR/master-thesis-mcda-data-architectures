"""Performance-matrix model with uncertainty (Stage 2 plan A9, A10a, A14; coding kit K7, K9, K11)."""
import numpy as np
from . import CRITERIA, CONFIGS, BENEFIT

PLATFORM_OF = {'C3': 'C1', 'C5': 'C1', 'C4': 'C2', 'C6': 'C2'}   # rows inherit their platform column (K11)
HUB, FED = ('C3', 'C4'), ('C5', 'C6')


class PerformanceModel:
    """base: dict config -> dict criterion -> float (deterministic value; CARB = median of its estimate).
    samplers: dict (config, criterion) -> f(rng, k) -> array (k,).
    carb_draws: optional array (N, len(configs)) of JOINT CARB draws (rows sampled together)."""

    def __init__(self, base, configs=CONFIGS, criteria=CRITERIA, samplers=None, carb_draws=None):
        self.configs, self.criteria = list(configs), list(criteria)
        self.base = {c: dict(base[c]) for c in self.configs}
        self.samplers = dict(samplers or {})
        self.carb_draws = None if carb_draws is None else np.asarray(carb_draws, float)
        self.notes = []

    # ---- views -------------------------------------------------------------------------
    def X(self):
        return np.array([[self.base[c][k] for k in self.criteria] for c in self.configs], float)

    def benefit(self):
        return np.array([BENEFIT[k] for k in self.criteria], bool)

    def subset(self, configs):
        keep = [c for c in self.configs if c in configs]
        m = PerformanceModel({c: self.base[c] for c in keep}, keep, self.criteria,
                             {key: f for key, f in self.samplers.items() if key[0] in keep})
        if self.carb_draws is not None:
            m.carb_draws = self.carb_draws[:, [self.configs.index(c) for c in keep]]
        m.notes = list(self.notes)
        return m

    def copy(self):
        return self.subset(self.configs)

    def sample(self, rng, k):
        """(k, m, n) matrices drawn from the model."""
        X = np.broadcast_to(self.X(), (k, len(self.configs), len(self.criteria))).copy()
        for (c, crit), f in self.samplers.items():
            X[:, self.configs.index(c), self.criteria.index(crit)] = f(rng, k)
        if self.carb_draws is not None and 'CARB' in self.criteria:
            idx = rng.integers(0, len(self.carb_draws), k)
            X[:, :, self.criteria.index('CARB')] = self.carb_draws[idx]
        return X

    # ---- construction helpers ----------------------------------------------------------
    def mark_insufficient(self, config, criterion):
        """A9: cell both coders marked insufficient -> midpoint 3, uniform over 1..5 in SMAA."""
        self.base[config][criterion] = 3.0
        self.samplers[(config, criterion)] = lambda rng, k: rng.uniform(1, 5, k)
        self.notes.append(f'{config}x{criterion}: insufficient -> 3, U[1,5]')

    def apply_tco_k11(self, tco_c1, tco_c2, directional=False):
        """K11: C1/C2 coded; C3-C6 inherit their platform; C7 = mean(C1, C2).
        Primary: symmetric U[-1,+1] shift, clipped to [1,5].
        Directional sensitivity: federated dearer by 0..2 classes, hub -1..+1, fabric dearer by 0..1 (lower score = dearer)."""
        vals = {'C1': tco_c1, 'C2': tco_c2}
        for c in self.configs:
            if c in ('C1', 'C2'):
                continue
            v = (tco_c1 + tco_c2) / 2 if c == 'C7' else vals[PLATFORM_OF[c]]
            self.base[c]['TCO'] = v
            if directional and c in FED:
                lo, hi = -2.0, 0.0
            elif directional and c == 'C7':
                lo, hi = -1.0, 0.0
            else:
                lo, hi = -1.0, 1.0
            self.samplers[(c, 'TCO')] = (lambda v, lo, hi: (lambda rng, k: np.clip(v + rng.uniform(lo, hi, k), 1, 5)))(v, lo, hi)
            if directional:   # deterministic runs use the midpoint of the directional shift
                self.base[c]['TCO'] = float(np.clip(v + (lo + hi) / 2, 1, 5))
        self.notes.append('TCO per K11' + (' (directional)' if directional else ''))

    def coder_disagreement(self, pairs):
        """A14 sensitivity: pairs = {(config, criterion): (score_coder1, score_coder2)} -> U[min, max]."""
        for (c, crit), (a, b) in pairs.items():
            lo, hi = min(a, b), max(a, b)
            if lo != hi:
                self.samplers[(c, crit)] = (lambda lo, hi: (lambda rng, k: rng.uniform(lo, hi, k)))(lo, hi)

    def set_value(self, config, criterion, value, note=''):
        self.base[config][criterion] = float(value)
        self.samplers.pop((config, criterion), None)
        if note:
            self.notes.append(note)


def secc_floor(model, floor=3.0):
    """A10a: configurations with SECC below the floor (on the deterministic, coded value) are excluded (S1 only)."""
    keep = [c for c in model.configs if model.base[c]['SECC'] >= floor]
    return model.subset(keep), [c for c in model.configs if c not in keep]


def variant_c6_blocked(model):
    """A14 / K9: C6 TTDP at level 1 (self-serve platform assumption removed)."""
    m = model.copy(); m.set_value('C6', 'TTDP', 1, 'K9: C6 TTDP=1'); return m


def variant_edition(model, enterprise_values):
    """A14 / K7: enterprise_values = {(config, criterion): value} for SECC (C1,C3,C5,C7) and TCO (C1).
    TCO rows are re-derived by K11 from the Enterprise C1 value."""
    m = model.copy()
    for (c, crit), v in enterprise_values.items():
        m.set_value(c, crit, v, f'K7 Enterprise: {c}x{crit}={v}')
    if ('C1', 'TCO') in enterprise_values:
        m.apply_tco_k11(m.base['C1']['TCO'], m.base['C2']['TCO'])
    return m


def variant_carb(model, carb_draws, note='CARB alternative estimate'):
    """A14: CARB replaced by an alternative joint estimate (e.g. carb R2_floor, the provisioning-floor
    model S7). Deterministic CARB values become the new medians; sampling uses the new joint draws."""
    m = model.copy()
    carb_draws = np.asarray(carb_draws, float)
    if carb_draws.shape[1] != len(model.configs):
        raise ValueError('carb_draws must have one column per configuration, in model order')
    m.carb_draws = carb_draws
    for i, c in enumerate(m.configs):
        m.base[c]['CARB'] = float(np.median(carb_draws[:, i]))
    m.notes.append(note)
    return m
