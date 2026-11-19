"""Auxiliary checks on the CARB estimate, reported in thesis Chapter 5 (§5.5.4, §5.5.6, §5.5.7).
Does not change the estimate. Runs carb_estimate.py in memory (outputs written to a temporary
directory, not over the frozen files) and reports:
  1. storage share of R2 per configuration (median of per-draw shares);
  2. daily work share A1 fixed at each end of its range: C1 median R2, C2/C1 ratio of medians, median order;
  3. functional units: per-draw full-ranking agreement R1 vs R2 and R3 vs R2; pairwise P(Ci < Cj) on R1/R2/R3.
Run from the carb folder:  python carb_checks.py"""
import itertools, os, tempfile, contextlib, io
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, 'carb_estimate.py')).read()
A1_LINE = 'W_TB_EQ_PER_DAY   = DATA_TB * U(0.2, 0.6)'
assert A1_LINE in SRC, 'A1 line changed in carb_estimate.py; update this check'


def run(src):
    ns = {'__name__': 'carb_check'}
    with tempfile.TemporaryDirectory() as d:
        old = os.getcwd(); os.chdir(d)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(src, 'carb_estimate.py', 'exec'), ns)
        finally:
            os.chdir(old)
    return ns


base = run(SRC)
D, W = base['draws'], base['W_TB_EQ_PER_DAY']
cfg = list(D)
print('1. Storage share of R2 (median of per-draw shares)')
for c in cfg:
    print(f'   {c}: {np.median(1 - D[c]["R2_compute"] / D[c]["R2"]):.2f}')

print('\n2. A1 fixed at the ends of its range')
for lo in (0.2, 0.6):
    ns = run(SRC.replace(A1_LINE, f'W_TB_EQ_PER_DAY   = DATA_TB * U({lo}, {lo + 1e-4})'))
    med = {c: float(np.median(ns['draws'][c]['R2'])) for c in cfg}
    print(f'   A1={lo:.0%}: C1 median {med["C1"]:.0f} g, C2/C1 ratio of medians {med["C2"] / med["C1"]:.2f}, '
          f'order {" < ".join(sorted(cfg, key=med.get))}')

print('\n3. Functional units')
X = {R: np.column_stack([D[c][R] for c in cfg]) for R in ('R1', 'R2', 'R3')}
rk = {R: np.argsort(np.argsort(v, 1), 1) for R, v in X.items()}
print(f'   full ranking equal, R1 vs R2: {np.mean((rk["R1"] == rk["R2"]).all(1)):.3f}; '
      f'R3 vs R2: {np.mean((rk["R3"] == rk["R2"]).all(1)):.3f}')
for i, j in itertools.combinations(range(len(cfg)), 2):
    p = [np.mean(X[R][:, i] < X[R][:, j]) for R in ('R1', 'R2', 'R3')]
    if abs(p[0] - p[1]) >= 0.01:
        print(f'   P({cfg[i]} < {cfg[j]}): R1 {p[0]:.3f}  R2 {p[1]:.3f}  R3 {p[2]:.3f}')
