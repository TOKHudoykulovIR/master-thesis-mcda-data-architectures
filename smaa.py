"""SMAA-2 with TOPSIS (Lahdelma & Salminen 2001) — Stage 2 plan A14."""
import numpy as np
from .topsis import closeness_batch


def dirichlet_mom(W):
    """Method-of-moments Dirichlet fit to weight vectors (rows). alpha = mean * s, where the precision s is
    estimated per criterion as m(1-m)/var - 1 and averaged over criteria (Ronning 1989)."""
    W = np.asarray(W, float)
    m, v = W.mean(axis=0), W.var(axis=0, ddof=1)
    ok = v > 0
    s_j = m[ok] * (1 - m[ok]) / v[ok] - 1
    s_j = s_j[s_j > 0]
    s = float(np.mean(s_j)) if len(s_j) else 1e3     # no spread -> nearly degenerate at the mean
    return m * s


def weight_sampler_dirichlet(W):
    alpha = dirichlet_mom(W)
    return lambda rng, k: rng.dirichlet(alpha, k)


def weight_sampler_bootstrap(W):
    """A14 sensitivity: resample observed individual vectors."""
    W = np.asarray(W, float)
    return lambda rng, k: W[rng.integers(0, len(W), k)]


def _rank_matrix(scores, rng):
    """scores (k, m) -> ranks (k, m), 1 = best, ties broken at random."""
    noise = rng.uniform(0, 1e-12, scores.shape)
    order = np.argsort(-(scores + noise), axis=1)
    ranks = np.empty_like(order)
    k, m = scores.shape
    ranks[np.arange(k)[:, None], order] = np.arange(1, m + 1)
    return ranks


def run(model, weight_sampler, k=10_000, seed=0, chunk=2_000):
    """Returns dict: acceptability (m x m, [config, rank-1]), central_weights (m x n, NaN if never first),
    confidence (m,), plus draws for reuse."""
    rng = np.random.default_rng(seed)
    benefit = model.benefit()
    m, n = len(model.configs), len(model.criteria)
    counts = np.zeros((m, m)); wsum = np.zeros((m, n)); first = np.zeros(m)
    done = 0
    while done < k:
        kk = min(chunk, k - done)
        Ws = weight_sampler(rng, kk)
        Xs = model.sample(rng, kk)
        R = _rank_matrix(closeness_batch(Xs, Ws, benefit), rng)
        for r in range(1, m + 1):
            counts[:, r - 1] += (R == r).sum(axis=0)
        win = (R == 1)
        wsum += win.T.astype(float) @ Ws
        first += win.sum(axis=0)
        done += kk
    acc = counts / k
    central = np.where(first[:, None] > 0, wsum / np.maximum(first, 1)[:, None], np.nan)
    conf = np.full(m, np.nan)
    for i in range(m):
        if first[i] == 0:
            continue
        Ws = np.broadcast_to(central[i], (k, n))
        Xs = model.sample(rng, k)
        R = _rank_matrix(closeness_batch(Xs, Ws, benefit), rng)
        conf[i] = (R[:, i] == 1).mean()
    return {'configs': model.configs, 'acceptability': acc, 'first_rank': acc[:, 0],
            'central_weights': central, 'confidence': conf}
