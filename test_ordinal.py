"""Tests for E-O1, the exploratory ordinal SMAA (Stage 2 plan, amendment 3, point 5)."""
import os, sys, unittest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine import CRITERIA, CONFIGS                                    # noqa: E402
from engine.matrix import PerformanceModel                              # noqa: E402
from engine import ordinal                                              # noqa: E402

N = len(CRITERIA)


class TestRegionSampler(unittest.TestCase):
    def test_constraints_hold(self):
        rng = np.random.default_rng(1)
        W = ordinal.sample_region(rng, 20_000, best=4, worst=2, n=N)
        self.assertTrue(np.allclose(W.sum(axis=1), 1))
        self.assertTrue((W >= 0).all())
        self.assertTrue((W[:, 4] >= W.max(axis=1) - 1e-15).all())
        self.assertTrue((W[:, 2] <= W.min(axis=1) + 1e-15).all())

    def test_uniform_on_region_matches_rejection_sampling(self):
        """Means and pairwise order frequencies agree with rejection sampling from the uniform simplex."""
        rng = np.random.default_rng(2)
        W = ordinal.sample_region(rng, 200_000, best=0, worst=3, n=N)
        U = rng.dirichlet(np.ones(N), 2_000_000)
        R = U[(U.argmax(axis=1) == 0) & (U.argmin(axis=1) == 3)]
        self.assertGreater(len(R), 50_000)
        np.testing.assert_allclose(W.mean(axis=0), R.mean(axis=0), atol=0.003)
        np.testing.assert_allclose(W.std(axis=0), R.std(axis=0), atol=0.003)
        for a, b in [(1, 2), (1, 4), (2, 4)]:                         # middle criteria are unordered
            self.assertAlmostEqual((W[:, a] > W[:, b]).mean(), 0.5, delta=0.01)

    def test_analytic_means(self):
        """Uniform simplex, n = 5: E[max] = H_5 / 5, E[min] = 1 / 25."""
        rng = np.random.default_rng(3)
        W = ordinal.sample_region(rng, 400_000, best=1, worst=0, n=N)
        h5 = sum(1 / i for i in range(1, 6))
        self.assertAlmostEqual(W[:, 1].mean(), h5 / 5, delta=0.002)
        self.assertAlmostEqual(W[:, 0].mean(), 1 / 25, delta=0.001)

    def test_same_most_least_rejected(self):
        with self.assertRaises(ValueError):
            ordinal.sample_region(np.random.default_rng(0), 10, 2, 2, N)


class TestMixture(unittest.TestCase):
    def test_equal_share_per_panellist(self):
        choices = [('P1', 0, 4), ('P2', 4, 0), ('P3', 2, 1)]
        f = ordinal.weight_sampler_ordinal(choices, N)
        W = f(np.random.default_rng(4), 90_000)
        shares = [((W.argmax(1) == b) & (W.argmin(1) == w)).mean() for _, b, w in choices]
        for s in shares:
            self.assertAlmostEqual(s, 1 / 3, delta=0.01)

    def test_same_most_least_dropped(self):
        keep, dropped = ordinal.usable_choices([('P1', 0, 4), ('P2', 3, 3), ('P3', None, 1)])
        self.assertEqual([p for p, _, _ in keep], ['P1'])
        self.assertEqual(dropped, ['P2', 'P3'])

    def test_counts(self):
        c = ordinal.choice_counts([('P1', 4, 1), ('P2', 4, 2), ('P3', 0, 1)], CRITERIA)
        self.assertEqual(c['MOST']['SECC'], 2)
        self.assertEqual(c['LEAST']['AIRD'], 2)
        self.assertEqual(c['n'], 3)


def _model(rows):
    return PerformanceModel({c: dict(zip(CRITERIA, map(float, v))) for c, v in rows.items()}, configs=list(rows))


class TestRun(unittest.TestCase):
    def test_dominating_configuration_always_first(self):
        m = _model({'C1': [5, 5, 5, 5, 5], 'C2': [2, 3, 2, 3, 2], 'C3': [1, 2, 3, 2, 1]})
        r = ordinal.run_scenario(m, 'S2', [('P1', 0, 4), ('P2', 1, 2)], k=3_000)
        self.assertEqual(r['main']['first_rank']['C1'], 1.0)
        self.assertEqual(r['uniform_reference']['first_rank']['C1'], 1.0)

    def test_ordinal_information_moves_acceptability(self):
        """C1 is best on SECC, C2 on TTDP. A panel that puts SECC first gives C1 more first ranks than one
        that puts TTDP first."""
        m = _model({'C1': [1, 3, 3, 3, 5], 'C2': [5, 3, 3, 3, 1]})
        secc = ordinal.run_scenario(m, 'S2', [('P1', 4, 0)], k=5_000)['main']['first_rank']
        ttdp = ordinal.run_scenario(m, 'S2', [('P1', 0, 4)], k=5_000)['main']['first_rank']
        self.assertEqual(secc['C1'], 1.0)
        self.assertEqual(ttdp['C2'], 1.0)

    def test_secc_floor_in_s1(self):
        m = _model({'C1': [3, 3, 3, 3, 3], 'C2': [5, 5, 5, 5, 2], 'C3': [2, 2, 2, 2, 4]})
        r = ordinal.run_scenario(m, 'S1', [('P1', 0, 4)], k=2_000)
        self.assertEqual(r['secc_floor_excluded'], ['C2'])
        self.assertNotIn('C2', r['main']['first_rank'])
        self.assertIn('C2', r['no_floor']['first_rank'])

    def test_a1_sensitivity_and_determinism(self):
        m = _model({c: [1 + (i + j) % 5 for j in range(N)] for i, c in enumerate(CONFIGS)})
        ch = [('P1', 0, 4), ('P2', 2, 1), ('P3', 4, 3)]
        a = ordinal.run_scenario(m, 'S3', ch, choices_a1=ch[:2], k=2_000)
        b = ordinal.run_scenario(m, 'S3', ch, choices_a1=ch[:2], k=2_000)
        self.assertEqual(a['main'], b['main'])
        self.assertEqual(a['a1_only_panellists'], ['P1', 'P2'])
        for res in (a['main'], a['a1_only'], a['uniform_reference']):
            self.assertAlmostEqual(sum(res['first_rank'].values()), 1.0, places=6)


if __name__ == '__main__':
    unittest.main()
