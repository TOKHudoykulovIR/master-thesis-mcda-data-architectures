"""PROMETHEE II (Brans & Vincke 1985) — Stage 2 plan A11."""
import numpy as np


def net_flows(X, w, benefit, pref='vshape', p=None):
    """Net outranking flows. pref: 'usual' (Type I) or 'vshape' (Type III, linear up to p).
    p: per-criterion preference threshold; default (A11) = range of that criterion across alternatives."""
    X = np.asarray(X, float); w = np.asarray(w, float); w = w / w.sum()
    m, n = X.shape
    sign = np.where(np.asarray(benefit, bool), 1.0, -1.0)
    D = (X[:, None, :] - X[None, :, :]) * sign          # d_j(a, b), positive = a better
    if pref == 'usual':
        P = (D > 0).astype(float)
    elif pref == 'vshape':
        if p is None:
            p = X.max(axis=0) - X.min(axis=0)
        p = np.where(np.asarray(p, float) == 0, np.inf, p)
        P = np.clip(D / p, 0, 1)
    else:
        raise ValueError(pref)
    Pi = (P * w).sum(axis=2)                             # aggregated preference pi(a, b)
    phi_plus = Pi.sum(axis=1) / (m - 1)
    phi_minus = Pi.sum(axis=0) / (m - 1)
    return phi_plus - phi_minus
