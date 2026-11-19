"""Aggregation and consensus (Stage 2 plan A4–A5)."""
import numpy as np
from scipy.stats import rankdata


def geometric_mean(W):
    """A4 primary: geometric mean of individual weight vectors (rows), renormalised. Zero weights are floored at 1e-9."""
    W = np.clip(np.asarray(W, float), 1e-9, None)
    g = np.exp(np.log(W).mean(axis=0))
    return g / g.sum()


def arithmetic_mean(W):
    """A4 sensitivity."""
    W = np.asarray(W, float); a = W.mean(axis=0)
    return a / a.sum()


def kendalls_w(W):
    """A5: Kendall's coefficient of concordance over the panellists' criterion rankings (rows = raters),
    with the correction for ties. Higher weight = rank 1."""
    W = np.asarray(W, float)
    m, n = W.shape
    R = np.vstack([rankdata(-row, method='average') for row in W])
    Rj = R.sum(axis=0)
    S = ((Rj - Rj.mean()) ** 2).sum()
    T = 0.0
    for row in R:
        _, counts = np.unique(row, return_counts=True)
        T += (counts ** 3 - counts).sum()
    denom = m ** 2 * (n ** 3 - n) - m * T
    return float(12 * S / denom) if denom > 0 else float('nan')


def delphi_decision(w_by_scenario, threshold=0.5):
    """A5: {scenario: W} -> {scenario: 'terminate' | 'round 3'}."""
    return {s: ('terminate' if w >= threshold else 'round 3') for s, w in w_by_scenario.items()}


def stability(g_round2, g_round3):
    """A5: mean absolute change in group weight per criterion between rounds."""
    return float(np.mean(np.abs(np.asarray(g_round2) - np.asarray(g_round3))))
