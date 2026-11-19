"""Tests for the changes made after Delphi Round 1 (1 Oct 2026): five primary criteria, three scenarios per
panellist (A7 permutation over 3! orders within each panellist), revised H3, exploratory carbon analyses."""
import unittest
import numpy as np
from engine import CRITERIA, CRITERIA_EXPLORATORY, CONFIGS
from engine.stats import perm_test_scenarios
from engine.hypotheses import H
from engine.exploratory import carbon_ratio, append_carbon, carbon_threshold
from engine.matrix import PerformanceModel
from engine import topsis


class TestPermThreeScenarios(unittest.TestCase):
    def test_exact_minimum_p_with_three_labels(self):
        # 6 experts, identical strictly ordered triples: only the 3! global relabellings reach the observed
        # statistic, so p = 6 / 6^6 = 1/7776.
        recs = [(e, s, v) for e in range(6) for s, v in (('S1', .5), ('S2', .3), ('S3', .1))]
        stat, p, kind = perm_test_scenarios(recs)
        self.assertEqual(kind, 'exact'); self.assertAlmostEqual(p, 6 / 6 ** 6)

    def test_null_gives_one(self):
        recs = [(e, s, 0.2) for e in range(6) for s in ('S1', 'S2', 'S3')]
        self.assertAlmostEqual(perm_test_scenarios(recs)[1], 1.0)

    def test_two_label_case_unchanged(self):
        recs = [(e, 'S1', 0.5) for e in range(6)] + [(e, 'S2', 0.1) for e in range(6)]
        self.assertAlmostEqual(perm_test_scenarios(recs)[1], 2 / 64)

    def test_monte_carlo_when_large(self):
        recs = [(e, s, float(np.sin(e + i))) for e in range(8) for i, s in enumerate(('S1', 'S2', 'S3'))]
        stat, p, kind = perm_test_scenarios(recs, n_mc=2000)      # 6^8 > 65,536
        self.assertEqual(kind, 'monte carlo'); self.assertTrue(0 < p <= 1)


class TestH(unittest.TestCase):
    def test_h3_on_port_and_carbon_exploratory(self):
        g = {'S1': np.array([.1, .2, .2, .1, .4]), 'S2': np.array([.4, .3, .05, .15, .1]),
             'S3': np.array([.15, .1, .4, .15, .2])}
        r = H(g, CRITERIA)
        self.assertTrue(r['H1 (S1: SECC highest)']); self.assertTrue(r['H2 (S2: TTDP or AIRD highest)'])
        self.assertTrue(r['H3 (S3: PORT above S2)']); self.assertNotIn('H3-carbon (exploratory; S3: CARB above S1 and S2)', r)
        g6 = {s: np.append(w * .9, c) for (s, w), c in zip(g.items(), (.05, .02, .3))}
        self.assertTrue(H(g6, CRITERIA_EXPLORATORY)['H3-carbon (exploratory; S3: CARB above S1 and S2)'])


class TestExploratory(unittest.TestCase):
    def test_carbon_ratio_coding(self):
        self.assertEqual(carbon_ratio('equal'), 1.0); self.assertEqual(carbon_ratio('less', 4), 4.0)
        self.assertAlmostEqual(carbon_ratio('more', 3), 1 / 3)
        with self.assertRaises(ValueError): carbon_ratio('less', 1)
        with self.assertRaises(ValueError): carbon_ratio('sideways', 3)

    def test_append_carbon(self):
        w = np.array([.4, .2, .2, .1, .1])
        v = append_carbon(w, 0, 4.0)                      # carbon = 0.4 / 4 = 0.1 before renormalising
        np.testing.assert_allclose(v, np.append(w, .1) / 1.1); self.assertAlmostEqual(v.sum(), 1)
        self.assertAlmostEqual(v[-1] / v[0], 0.25)        # ratio to best criterion preserved
        self.assertGreater(append_carbon(w, 0, 1 / 3)[-1], append_carbon(w, 0, 1 / 3)[0])

    def test_threshold_zero_equals_primary_topsis(self):
        rng = np.random.default_rng(3)
        base = {c: {**{k: float(rng.integers(1, 6)) for k in CRITERIA}, 'CARB': float(100 + 40 * i)}
                for i, c in enumerate(CONFIGS)}
        m6 = PerformanceModel(base, criteria=CRITERIA_EXPLORATORY); m5 = PerformanceModel(base)
        w5 = np.array([.3, .2, .2, .15, .15])
        r = carbon_threshold(m6, w5)
        top5 = CONFIGS[int(np.argmax(topsis.closeness(m5.X(), w5, m5.benefit(), 'vector')))]
        self.assertEqual(r['first_at_zero'], top5)
        if r['threshold'] is not None:                  # the low-carbon configuration takes over eventually
            self.assertNotEqual(r['first_after_threshold'], top5)
        last = r['path'][-1][1]
        self.assertIn(last, CONFIGS)


if __name__ == '__main__':
    unittest.main()
