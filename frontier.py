"""Priority frontier maps (Stage 2 plan A15)."""
import numpy as np
from .topsis import closeness


def frontier(model, group_w, a, b, grid=50):
    """Vary weights of criteria a and b over [0,1] (w_a + w_b <= 1); the others are rescaled proportionally to
    their group values to fill the remainder. Returns (wa_values, wb_values, winner index grid;
    -1 = infeasible, -2 = tie for first place — shown as a tie rather than resolved by index order)."""
    X, ben = model.X(), model.benefit()
    g = np.asarray(group_w, float)
    ia, ib = model.criteria.index(a), model.criteria.index(b)
    rest = [j for j in range(len(g)) if j not in (ia, ib)]
    rest_share = g[rest] / g[rest].sum() if g[rest].sum() > 0 else np.full(len(rest), 1 / len(rest))
    vals = np.linspace(0, 1, grid)
    out = np.full((grid, grid), -1, int)
    for i, wa in enumerate(vals):
        for j, wb in enumerate(vals):
            if wa + wb > 1 + 1e-12:
                continue
            w = np.zeros(len(g)); w[ia], w[ib] = wa, wb
            w[rest] = (1 - wa - wb) * rest_share
            if w.sum() <= 0:
                continue
            c = closeness(X, w, ben)
            top = np.flatnonzero(c >= c.max() - 1e-12)
            out[j, i] = int(top[0]) if len(top) == 1 else -2
    return vals, vals, out


def plot(vals_a, vals_b, grid, configs, a, b, path, title=''):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    palette = ['#4C78A8', '#F58518', '#54A24B', '#E45756', '#72B7B2', '#B279A2', '#9D755D']
    cmap = ListedColormap(['#BBBBBB', '#FFFFFF'] + palette[:len(configs)])
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    ax.imshow(grid + 2, origin='lower', extent=[0, 1, 0, 1], cmap=cmap, vmin=0, vmax=len(configs) + 1, aspect='auto')
    present = sorted({int(v) for v in np.unique(grid) if v >= 0})
    for v in present:
        ax.plot([], [], 's', color=palette[v], label=configs[v])
    if (grid == -2).any():
        ax.plot([], [], 's', color='#BBBBBB', label='tie')
    ax.legend(loc='upper right', fontsize=8, frameon=False)
    ax.set_xlabel(f'weight of {a}'); ax.set_ylabel(f'weight of {b}'); ax.set_title(title, fontsize=10)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
