"""Property and hand-calculation tests for components without a published numerical example."""
import unittest
import numpy as np
from scipy.stats import spearmanr
from engine.bwm import BWMResponse, linear_bwm, attention_check, reconcile, evaluate
from engine.aggregate import geometric_mean, kendalls_w
from engine.promethee import net_flows
from engine.smaa import dirichlet_mom, run as smaa_run, weight_sampler_dirichlet
from engine.matrix import PerformanceModel, secc_floor, variant_carb
from engine.stats import perm_test_scenarios, holm
from engine.frontier import frontier
# Generic six-criterion examples with one cost-type criterion (CARB) — the methods are criterion-agnostic.
CRITERIA = ['CARB', 'TTDP', 'AIRD', 'PORT', 'TCO', 'SECC']


class TestBWMProperties(unittest.TestCase):
    def test_fully_consistent_recovers_exact_weights(self):
        w_true = np.array([0.5, 0.25, 0.125, 0.0625, 0.0625])
        bo = w_true[0] / w_true; ow = w_true / w_true[4]
        w, xi = linear_bwm(BWMResponse(0, 4, bo, ow))
        np.testing.assert_allclose(w, w_true, atol=1e-9); self.assertLess(xi, 1e-9)

    def test_attention_and_reconcile(self):
        r = BWMResponse(0, 2, np.array([1, 3, 6]), np.array([5, 2, 1]))   # a_BW 6 vs 5: differs by 1
        ok, _ = attention_check(r); self.assertTrue(ok)
        self.assertEqual(reconcile(r).ow[0], 6)
        bad = BWMResponse(0, 2, np.array([2, 3, 6]), np.array([3, 2, 1]))
        ok, reasons = attention_check(bad); self.assertFalse(ok); self.assertEqual(len(reasons), 2)

    def test_evaluate_flags(self):
        e = evaluate(BWMResponse(0, 2, np.array([1, 3, 6]), np.array([6, 2, 1])))
        self.assertTrue(e['consistent']); self.assertAlmostEqual(e['weights'].sum(), 1)


class TestAggregation(unittest.TestCase):
    def test_geometric_mean_normalised(self):
        g = geometric_mean([[0.5, 0.3, 0.2], [0.2, 0.3, 0.5]])
        self.assertAlmostEqual(g.sum(), 1); self.assertAlmostEqual(g[0], g[2])

    def test_kendalls_w_bounds_and_two_rater_identity(self):
        self.assertAlmostEqual(kendalls_w([[.4, .3, .2, .1]] * 3), 1.0)
        rng = np.random.default_rng(1)
        for _ in range(20):   # for m = 2 raters, W = (rho_s + 1) / 2 (Siegel & Castellan)
            W = rng.dirichlet(np.ones(6), 2)
            rho = spearmanr(-W[0], -W[1]).statistic
            self.assertAlmostEqual(kendalls_w(W), (rho + 1) / 2, places=9)


class TestPROMETHEEVShape(unittest.TestCase):
    def test_vshape_hand_example(self):
        # two alternatives, one criterion, p = range = 2: difference 1 -> P = 0.5
        phi = net_flows(np.array([[3.0], [2.0], [1.0]]), [1.0], [True], pref='vshape')
        # pi(a1,a2)=0.5, pi(a1,a3)=1, pi(a2,a3)=0.5 -> phi = ((1.5)-(0))/2, (0.5-0.5)/2, (0-1.5)/2
        np.testing.assert_allclose(phi, [0.75, 0.0, -0.75])
        self.assertAlmostEqual(phi.sum(), 0)

    def test_cost_criterion_reverses(self):
        a = net_flows(np.array([[1.0], [2.0]]), [1], [True]); b = net_flows(np.array([[1.0], [2.0]]), [1], [False])
        np.testing.assert_allclose(a, -b)


class TestSMAA(unittest.TestCase):
    def test_dirichlet_mom_recovers_parameters(self):
        rng = np.random.default_rng(0); alpha = np.array([8., 4., 2., 6.])
        est = dirichlet_mom(rng.dirichlet(alpha, 200_000))
        np.testing.assert_allclose(est, alpha, rtol=0.03)

    def _model(self, X):
        base = {c: dict(zip(CRITERIA, row)) for c, row in zip(['A', 'B', 'C'], X)}
        return PerformanceModel(base, configs=['A', 'B', 'C'], criteria=CRITERIA)

    def test_dominance_gives_certainty(self):
        X = [[1, 5, 5, 5, 5, 5], [2, 3, 3, 3, 3, 3], [3, 1, 1, 1, 1, 1]]   # A dominates (CARB lower = better)
        res = smaa_run(self._model(X), weight_sampler_dirichlet(np.random.default_rng(0).dirichlet(np.ones(6), 20)), k=4000)
        self.assertEqual(res['first_rank'][0], 1.0); self.assertEqual(res['confidence'][0], 1.0)
        np.testing.assert_allclose(res['acceptability'].sum(axis=1), 1); np.testing.assert_allclose(res['acceptability'].sum(axis=0), 1)

    def test_secc_floor(self):
        X = [[1, 3, 3, 3, 3, 2], [1, 3, 3, 3, 3, 3], [1, 3, 3, 3, 3, 5]]
        m, excluded = secc_floor(self._model(X)); self.assertEqual(excluded, ['A']); self.assertEqual(m.configs, ['B', 'C'])

    def test_variant_carb_replaces_draws_not_original(self):
        X = [[1, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3]]
        base = self._model(X)
        alt = np.column_stack([np.full(100, 30.0), np.full(100, 20.0), np.arange(100, dtype=float)])
        v = variant_carb(base, alt)
        self.assertEqual([v.base[c]['CARB'] for c in v.configs], [30.0, 20.0, 49.5])
        self.assertEqual([base.base[c]['CARB'] for c in base.configs], [1.0, 2.0, 3.0])   # original untouched
        S = v.sample(np.random.default_rng(0), 50)
        np.testing.assert_array_equal(S[:, 0, 0], 30.0); np.testing.assert_array_equal(S[:, 1, 0], 20.0)
        with self.assertRaises(ValueError):
            variant_carb(base, alt[:, :2])


class TestStats(unittest.TestCase):
    def test_perm_exact_extremes(self):
        # 6 experts, criterion always higher in S1 than in S2 -> smallest attainable p = 2/64 (two-sided statistic)
        recs = [(e, 'S1', 0.5) for e in range(6)] + [(e, 'S2', 0.1) for e in range(6)]
        stat, p, kind = perm_test_scenarios(recs); self.assertEqual(kind, 'exact'); self.assertAlmostEqual(p, 2 / 64)
        recs = [(e, 'S1', 0.3) for e in range(6)] + [(e, 'S2', 0.3) for e in range(6)]
        self.assertAlmostEqual(perm_test_scenarios(recs)[1], 1.0)

    def test_holm(self):
        np.testing.assert_allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])


class TestFrontier(unittest.TestCase):
    def test_extremes(self):
        base = {'A': dict(zip(CRITERIA, [1, 5, 1, 1, 1, 1])), 'B': dict(zip(CRITERIA, [1, 1, 5, 1, 1, 1]))}
        m = PerformanceModel(base, configs=['A', 'B'], criteria=CRITERIA)
        _, _, g = frontier(m, np.full(6, 1 / 6), 'TTDP', 'AIRD', grid=11)
        self.assertEqual(g[0, 10], 0)    # all weight on TTDP -> A
        self.assertEqual(g[10, 0], 1)    # all weight on AIRD -> B
        self.assertEqual(g[10, 10], -1)  # infeasible corner
        self.assertEqual(g[0, 0], -2)    # all weight on criteria where A and B are equal -> tie


if __name__ == '__main__':
    unittest.main()
