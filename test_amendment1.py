"""Stage 2 amendment 1 (7 Oct 2026): A1 rejects best == worst and a_BW = 1 with other ratings above 1;
A3 uses threshold 0 at a_BW = 2 (Liang et al. 2020, note to Table 3)."""
import unittest
import numpy as np
from engine.bwm import BWMResponse, evaluate, attention_check


class TestAmendment1(unittest.TestCase):
    def test_best_equals_worst_fails_a1(self):
        ok, reasons = attention_check(BWMResponse(0, 0, np.ones(5), np.ones(5)))
        self.assertFalse(ok)
        self.assertIn('the same criterion was chosen as best and as worst', reasons)

    def test_abw1_all_ones_passes_with_equal_weights(self):
        e = evaluate(BWMResponse(0, 4, np.ones(5), np.ones(5)))
        self.assertTrue(e['attention_ok'])
        self.assertTrue(np.allclose(e['weights'], 0.2))
        self.assertTrue(e['consistent'])

    def test_abw1_with_other_ratings_fails_a1(self):
        ok, reasons = attention_check(BWMResponse(0, 4, np.array([1, 3, 1, 1, 1.]), np.ones(5)))
        self.assertFalse(ok)
        self.assertIn('best rated equal to worst, but not every criterion is rated 1', reasons)

    def test_abw2_cr_positive_is_not_consistent(self):
        e = evaluate(BWMResponse(0, 1, np.array([1, 2, 2, 2, 2.]), np.array([2, 1, 2, 2, 2.])))
        self.assertTrue(e['attention_ok'])
        self.assertEqual(e['threshold'], 0.0)
        self.assertGreater(e['CR'], 0)
        self.assertFalse(e['consistent'])

    def test_abw2_fully_consistent_is_consistent(self):
        # a_Bj * a_jW == 2 for every j
        e = evaluate(BWMResponse(0, 1, np.array([1, 2, 1, 2, 1.]), np.array([2, 1, 2, 1, 2.])))
        self.assertEqual(e['CR'], 0)
        self.assertTrue(e['consistent'])

    def test_abw1_rule_ignores_the_best_to_worst_pair(self):
        # bo[W] = 1, ow[B] = 2 (one-point disagreement, reconciled by A2), all others 1: passes A1
        ok, _ = attention_check(BWMResponse(0, 4, np.ones(5), np.array([2, 1, 1, 1, 1.])))
        self.assertTrue(ok)
        e = evaluate(BWMResponse(0, 4, np.ones(5), np.array([2, 1, 1, 1, 1.])))
        self.assertTrue(e['consistent'])

    def test_abw1_not_all_ones_not_consistent(self):
        e = evaluate(BWMResponse(0, 4, np.array([1, 3, 1, 1, 1.]), np.ones(5)))
        self.assertFalse(e['attention_ok'])
        self.assertFalse(e['consistent'])

    def test_table_rule_unchanged(self):
        e = evaluate(BWMResponse(0, 1, np.array([1, 8, 2, 4, 2.]), np.array([8, 1, 4, 2, 4.])))
        self.assertEqual(e['threshold_rule'], 'table')


if __name__ == '__main__':
    unittest.main()
