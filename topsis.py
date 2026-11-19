"""TOPSIS (Hwang & Yoon 1981) — Stage 2 plan A10, A12."""
import numpy as np


def normalise(X, benefit, method='vector'):
    X = np.asarray(X, float)
    if method == 'vector':
        return X / np.sqrt((X ** 2).sum(axis=0))
    if method == 'minmax':
        rng = X.max(axis=0) - X.min(axis=0)
        rng = np.where(rng == 0, 1.0, rng)
        N = (X - X.min(axis=0)) / rng
        # min-max makes every column benefit-oriented
        return np.where(np.asarray(benefit), N, 1 - N)
    raise ValueError(method)


def closeness(X, w, benefit, method='vector'):
    """Relative closeness C* per alternative (rows)."""
    benefit = np.asarray(benefit, bool)
    V = normalise(X, benefit, method) * np.asarray(w, float)
    if method == 'minmax':
        ideal, anti = V.max(axis=0), V.min(axis=0)
    else:
        ideal = np.where(benefit, V.max(axis=0), V.min(axis=0))
        anti = np.where(benefit, V.min(axis=0), V.max(axis=0))
    dp = np.sqrt(((V - ideal) ** 2).sum(axis=1))
    dm = np.sqrt(((V - anti) ** 2).sum(axis=1))
    tot = dp + dm
    return np.where(tot == 0, 0.5, dm / np.where(tot == 0, 1, tot))


def closeness_batch(Xs, Ws, benefit):
    """Vectorised vector-normalised TOPSIS for SMAA: Xs (k, m, n) or (m, n); Ws (k, n). Returns (k, m)."""
    Ws = np.asarray(Ws, float)
    Xs = np.broadcast_to(np.asarray(Xs, float), (Ws.shape[0],) + np.asarray(Xs).shape[-2:])
    benefit = np.asarray(benefit, bool)
    N = Xs / np.sqrt((Xs ** 2).sum(axis=1, keepdims=True))
    V = N * Ws[:, None, :]
    vmax, vmin = V.max(axis=1, keepdims=True), V.min(axis=1, keepdims=True)
    ideal = np.where(benefit, vmax, vmin); anti = np.where(benefit, vmin, vmax)
    dp = np.sqrt(((V - ideal) ** 2).sum(axis=2)); dm = np.sqrt(((V - anti) ** 2).sum(axis=2))
    tot = dp + dm
    return np.where(tot == 0, 0.5, dm / np.where(tot == 0, 1, tot))


def ranks(scores):
    """1 = best; ties get the same (minimum) rank."""
    s = np.asarray(scores)
    return np.array([1 + (s > v).sum() for v in s])
