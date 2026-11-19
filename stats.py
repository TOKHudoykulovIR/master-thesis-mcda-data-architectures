"""Statistics for weights across scenarios and robustness (Stage 2 plan A6, A7, A11)."""
import itertools
import numpy as np
from scipy.stats import kendalltau


def perm_test_scenarios(records, n_mc=100_000, seed=0, exact_limit=2 ** 16):
    """A7. records: list of (expert_id, scenario, value) for ONE criterion.
    Statistic: variance of scenario means. Null: the criterion weight does not depend on the scenario.
    Permutation respects the design: each expert's values are permuted among that expert's OWN scenario
    labels (two ratings: swap; three ratings: all 3! = 6 orders; one rating: fixed).
    Exact enumeration when the number of assignments (product of m_i! over experts) <= exact_limit;
    otherwise Monte Carlo. With six experts rating three scenarios each: (3!)^6 = 46,656 assignments, exact.
    Returns (statistic, p_value, 'exact'|'monte carlo')."""
    by_exp = {}
    for e, s, v in records:
        by_exp.setdefault(e, []).append((s, float(v)))
    scen = sorted({s for _, s, _ in records})
    groups = list(by_exp.values())
    perms = [list(itertools.permutations(range(len(g)))) for g in groups]   # index 0 = identity

    def stat(choice):
        sums = dict.fromkeys(scen, 0.0); cnt = dict.fromkeys(scen, 0)
        for g, ps, k in zip(groups, perms, choice):
            for (s, _), j in zip(g, ps[k]):
                sums[s] += g[j][1]; cnt[s] += 1
        means = np.array([sums[s] / cnt[s] for s in scen if cnt[s] > 0])
        return float(means.var())

    obs = stat([0] * len(groups))
    total = int(np.prod([len(ps) for ps in perms]))
    if total <= exact_limit:
        allv = np.array([stat(ch) for ch in itertools.product(*[range(len(ps)) for ps in perms])])
        return obs, float(np.mean(allv >= obs - 1e-15)), 'exact'
    rng = np.random.default_rng(seed)
    ge = sum(stat([int(rng.integers(len(ps))) for ps in perms]) >= obs - 1e-15 for _ in range(n_mc))
    return obs, (ge + 1) / (n_mc + 1), 'monte carlo'


def holm(pvals):
    """Holm step-down adjusted p-values."""
    p = np.asarray(pvals, float); order = np.argsort(p); m = len(p)
    adj = np.empty(m); running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i]); adj[i] = min(1.0, running)
    return adj


def tau_b(scores_a, scores_b):
    """A11: Kendall's tau-b between two score vectors (higher = better)."""
    return float(kendalltau(scores_a, scores_b, variant='b').statistic)


def clr(W):
    L = np.log(np.clip(np.asarray(W, float), 1e-9, None))
    return L - L.mean(axis=1, keepdims=True)


def priority_profiles(W, k_range=(2, 3, 4), min_size=3, seed=0):
    """A6: k-means on clr-transformed weights; k by mean silhouette; clusters smaller than min_size are not allowed.
    Returns dict(k, labels, silhouette) or None when no admissible k exists."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    Z = clr(W); best = None
    for k in k_range:
        if len(Z) < k * min_size:
            continue
        lab = KMeans(n_clusters=k, n_init=50, random_state=seed).fit_predict(Z)
        if np.bincount(lab).min() < min_size:
            continue
        s = silhouette_score(Z, lab)
        if best is None or s > best['silhouette']:
            best = {'k': k, 'labels': lab, 'silhouette': float(s)}
    return best
