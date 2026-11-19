"""Integration: the full scenario pipeline runs, is reproducible under a fixed seed, and keeps SMAA invariants."""
import unittest
import numpy as np
from engine import CRITERIA, CONFIGS
from engine.bwm import BWMResponse
from engine.matrix import PerformanceModel
from engine import pipeline


def _setup(seed=1):
    rng = np.random.default_rng(seed)
    base = {c: {'CARB': float(100 + 20 * i), 'TCO': 3.0, 'TTDP': float(rng.integers(1, 6)), 'AIRD': float(rng.integers(1, 6)),
                'PORT': float(rng.integers(1, 6)), 'SECC': float(rng.integers(3, 6))} for i, c in enumerate(CONFIGS)}
    m = PerformanceModel(base); m.apply_tco_k11(3.0, 3.0)
    resp = []
    for e in range(6):
        w = rng.dirichlet(np.ones(len(CRITERIA)) * 5); b, wo = int(np.argmax(w)), int(np.argmin(w))
        bo = np.clip(np.rint(w[b] / w), 1, 9); ow = np.clip(np.rint(w / w[wo]), 1, 9); bo[b] = 1; ow[wo] = 1; ow[b] = bo[wo]
        resp.append((f'E{e}', BWMResponse(b, wo, bo, ow)))
    return m, pipeline.weights_stage(resp, CRITERIA)


class TestPipeline(unittest.TestCase):
    def test_runs_and_reproducible(self):
        m, ws = _setup()
        r1 = pipeline.ranking_stage(m, ws['group_geometric'], ws['W'], 'S2', k=2000, seed=3, frontier_grid=10)
        r2 = pipeline.ranking_stage(m, ws['group_geometric'], ws['W'], 'S2', k=2000, seed=3, frontier_grid=10)
        self.assertEqual(r1['first_rank'], r2['first_rank'])
        acc = r1['smaa']['acceptability']
        np.testing.assert_allclose(acc.sum(axis=0), 1); np.testing.assert_allclose(acc.sum(axis=1), 1)
        self.assertEqual(sorted(r1['order_topsis']), sorted(CONFIGS))
        self.assertTrue(-1 <= r1['tau_b_topsis_promethee'] <= 1)

    def test_weights_stage_outputs(self):
        _, ws = _setup()
        self.assertAlmostEqual(ws['group_geometric'].sum(), 1)
        self.assertTrue(0 <= ws['kendalls_w'] <= 1)


if __name__ == '__main__':
    unittest.main()
