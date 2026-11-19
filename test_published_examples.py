"""Each method reproduces a numerical example published in the literature.
Run:  python -m unittest discover -s tests   (from the engine folder)"""
import unittest
import numpy as np
from engine.bwm import BWMResponse, linear_bwm, consistency_ratio, cr_threshold
from engine.topsis import closeness
from engine.promethee import net_flows


class TestBWMLinear(unittest.TestCase):
    """Rezaei (2016), Omega 64:126-130, linear model; car example (quality, price, comfort, safety, style),
    best = price, worst = style, BO = (2,1,4,3,8), OW = (4,8,4,2,1).
    Published (Rezaei, n.d., "BWM: Best Worst Method" slides, bestworstmethod.com, slide 25): xi_L = 0.061 and
    the weight vector 0.246, 0.431, 0.154, 0.123, 0.046, printed without labels; read in the criterion order of
    slide 24 (quality, price, comfort, safety, style).

    DISCREPANCY, documented rather than hidden: the engine reproduces xi_L and all five weight values, but
    returns comfort = 0.123 and safety = 0.154, i.e. the two values are transposed in the printed order. The printed
    assignment is infeasible for the published xi_L: with a_B,comfort = 4, |w_B - 4 w_comfort| =
    |0.431 - 4 x 0.154| = 0.185 > 0.061, violating the model's own constraint. The test therefore checks
    xi_L, the three unambiguous weights, the multiset of weights, and the constraint argument itself."""
    def test_car_example(self):
        r = BWMResponse(best=1, worst=4, bo=np.array([2, 1, 4, 3, 8]), ow=np.array([4, 8, 4, 2, 1]))
        w, xi = linear_bwm(r)
        self.assertAlmostEqual(xi, 0.061, delta=1e-3)
        np.testing.assert_allclose(w[[0, 1, 4]], [0.246, 0.431, 0.046], atol=1e-3)
        np.testing.assert_allclose(sorted(w), sorted([0.246, 0.431, 0.154, 0.123, 0.046]), atol=1e-3)
        self.assertGreater(abs(0.431 - 4 * 0.154), 0.061)           # printed comfort weight infeasible
        self.assertLessEqual(abs(w[1] - 4 * w[2]), xi + 1e-9)        # engine's comfort weight feasible
        self.assertAlmostEqual(w.sum(), 1.0, places=9)


class TestBWMConsistency(unittest.TestCase):
    """Liang, Brunelli & Rezaei (2020), Omega 96:102175: car example with BO=(1,2,4,3,8) over
    (price, quality, comfort, safety, style), OW=(8,4,4,2,1): CR_j = (0, 0, 0.14, 0.04, 0), CR = 0.14;
    Table 3 threshold for a_BW = 8, n = 5 is 0.2958 -> acceptable."""
    def test_car_example(self):
        r = BWMResponse(best=0, worst=4, bo=np.array([1, 2, 4, 3, 8]), ow=np.array([8, 4, 4, 2, 1]))
        cr, crj, worst_pair = consistency_ratio(r)
        np.testing.assert_allclose(crj, [0, 0, 8 / 56, 2 / 56, 0], atol=1e-12)
        self.assertAlmostEqual(cr, 0.14, delta=5e-3)
        self.assertEqual(worst_pair, 2)
        self.assertEqual(cr_threshold(8, 5), 0.2958)
        self.assertLess(cr, cr_threshold(8, 5))


class TestTOPSIS(unittest.TestCase):
    """Opricovic & Tzeng (2004), EJOR 156:445-455, numerical example, Table 3, TOPSIS with vector
    normalisation: f1 = (1, 2, 5) cost, f2 = (3000, 3750, 4500) benefit, equal weights ->
    C* = (0.762, 0.722, 0.238)."""
    def test_vector(self):
        X = np.array([[1, 3000], [2, 3750], [5, 4500]], float)
        c = closeness(X, [0.5, 0.5], [False, True], 'vector')
        np.testing.assert_allclose(np.round(c, 3), [0.762, 0.722, 0.238])

    def test_minmax_crosscheck(self):
        """Min-max variant (A12). Cross-checked against the pymcdm library's reference test for the
        same example (Kizielewicz et al. 2023, SoftwareX): (0.500, 0.617, 0.500)."""
        X = np.array([[1, 3000], [2, 3750], [5, 4500]], float)
        c = closeness(X, [0.5, 0.5], [False, True], 'minmax')
        np.testing.assert_allclose(np.round(c, 3), [0.500, 0.617, 0.500])


class TestPROMETHEE(unittest.TestCase):
    """Zhao, Peng & Li (2013), Procedia Computer Science 17:181-188, usual criterion:
    X = [[4,3,2],[3,2,4],[5,1,3]], w = (0.5, 0.3, 0.2), all benefit -> net flows (0.1, -0.3, 0.2).
    Also verified by hand in the engine README."""
    def test_usual(self):
        X = np.array([[4, 3, 2], [3, 2, 4], [5, 1, 3]], float)
        phi = net_flows(X, [0.5, 0.3, 0.2], [True, True, True], pref='usual')
        np.testing.assert_allclose(np.round(phi, 2), [0.1, -0.3, 0.2])


if __name__ == '__main__':
    unittest.main()
