"""Exploratory carbon analyses (Stage 2 plan, section E). CARB was excluded from the Round 2 criteria set by
Stage 1 rule R2; nothing computed here enters a primary result.

E-C1  code_carbon_answer — the form answer (direction, 1-9 rating) as a ratio a, with a consistency flag.
E-C1  append_carbon      — a panellist's carbon weight from the extra Round 2 question, appended to the BWM weights.
E-C3  carbon_threshold   — the smallest carbon weight at which a scenario's first-ranked configuration changes."""
import numpy as np
from . import CRITERIA, CRITERIA_EXPLORATORY
from . import topsis


def carbon_ratio(direction, strength=None):
    """Code the Round 2 carbon question. direction: 'less' | 'equal' | 'more' (carbon compared with the panellist's
    most important criterion); strength: 2..9 when direction is not 'equal'.
    Returns a = (importance of best criterion) / (importance of carbon), in [1/9, 9]."""
    if direction == 'equal':
        return 1.0
    s = float(strength)
    if not 2 <= s <= 9:
        raise ValueError('strength must be 2..9 when direction is less or more')
    if direction == 'less':
        return s
    if direction == 'more':
        return 1.0 / s
    raise ValueError("direction must be 'less', 'equal' or 'more'")


FORM_DIRECTION = {'carbon intensity matters less': 'less', 'equally important': 'equal',
                  'carbon intensity matters more': 'more'}


def code_carbon_answer(direction_label, rating):
    """Code the Round 2 carbon question as fielded (round2-instrument-as-fielded.md, item (f)-(g); Stage 2 E-C1,
    revision of 7 Oct 2026). direction_label: the option text of (f); rating: the 1-9 value of (g), always shown.
    The direction decides. 'less'/'more' with rating 1, or 'equal' with rating > 1, gives a = 1 and is flagged.
    Returns (a, consistent: bool)."""
    d = FORM_DIRECTION.get(str(direction_label).strip().lower())
    if d is None:
        raise ValueError(f'unknown direction option: {direction_label!r}')
    if isinstance(rating, bool) or float(rating) != int(float(rating)):
        raise ValueError('rating must be an integer 1..9')
    r = int(float(rating))
    if not 1 <= r <= 9:
        raise ValueError('rating must be 1..9')
    if d == 'equal':
        return 1.0, r == 1
    if r == 1:
        return 1.0, False
    return carbon_ratio(d, r), True


def append_carbon(w, best_idx, a):
    """w: one panellist's primary weights over CRITERIA (sum 1); best_idx: the criterion they chose as best;
    a: carbon_ratio(...). Carbon weight = w[best] / a; the six weights are renormalised to sum 1.
    Returns a vector over CRITERIA_EXPLORATORY (CARB last)."""
    w = np.asarray(w, float)
    if len(w) != len(CRITERIA):
        raise ValueError('w must be over the primary criteria')
    if not (1 / 9 - 1e-12) <= a <= 9 + 1e-12:
        raise ValueError('a must lie in [1/9, 9]')
    v = np.append(w, w[best_idx] / a)
    return v / v.sum()


def carbon_threshold(model6, w5, t_grid=None, norm='vector'):
    """E-C3. model6: PerformanceModel over CRITERIA_EXPLORATORY (CARB = estimate medians). w5: primary group weights.
    For each carbon weight t, weights are (w5 * (1 - t), t). Returns the configuration ranked first at t = 0,
    the smallest t at which it changes (None if it never does within the grid), and the full path."""
    if list(model6.criteria) != CRITERIA_EXPLORATORY:
        raise ValueError('model6 must use CRITERIA_EXPLORATORY')
    t_grid = np.round(np.arange(0, 0.601, 0.01), 2) if t_grid is None else np.asarray(t_grid, float)
    X, ben, cfg = model6.X(), model6.benefit(), model6.configs
    w5 = np.asarray(w5, float) / np.sum(w5)
    tops = []
    for t in t_grid:
        c = topsis.closeness(X, np.append(w5 * (1 - t), t), ben, norm)
        tops.append(cfg[int(np.argmax(c))])
    change = next((float(t) for t, c in zip(t_grid, tops) if c != tops[0]), None)
    return {'first_at_zero': tops[0], 'threshold': change,
            'first_after_threshold': tops[list(t_grid).index(change)] if change is not None else None,
            'path': list(zip([float(t) for t in t_grid], tops))}
