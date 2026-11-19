"""Tests for round2_analysis.py on SYNTHETIC responses (no real panel data is read)."""
import copy, json, os, sys, tempfile, unittest
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import round2_analysis as ra                                             # noqa: E402
from engine import CRITERIA                                              # noqa: E402
from engine.bwm import BWMResponse, evaluate                             # noqa: E402

MATRIX = os.path.join(HERE, '..', 'matrix', 'matrix-frozen-2026-10-19.json')
SHEET = os.path.join(HERE, '..', 'matrix', 'coding-sheet-coder1.xlsx')


def _scenario(w, break_a1=False):
    b, wo = int(np.argmax(w)), int(np.argmin(w))
    bo = np.clip(np.rint(w[b] / w), 1, 9); ow = np.clip(np.rint(w / w[wo]), 1, 9)
    bo[b] = 1; ow[wo] = 1; ow[b] = bo[wo]
    if break_a1:
        bo[b] = 5
    ev = evaluate(BWMResponse(b, wo, bo, ow))
    return {'valid': True, 'best': CRITERIA[b], 'worst': CRITERIA[wo],
            'bo': dict(zip(CRITERIA, bo.astype(int).tolist())), 'ow': dict(zip(CRITERIA, ow.astype(int).tolist())),
            'A1': {'passed': ev['attention_ok'], 'reasons': ev['attention_reasons']},
            'A3': {'consistent': ev['consistent'], 'rule': ev['threshold_rule'], 'recontact_criterion': None},
            'carbon': {'direction': 'Carbon intensity matters less', 'rating': 5, 'a': 5.0, 'consistent': True}}


def synthetic(n=6, fail=()):
    """n synthetic panellists; fail = {(code, scenario)} whose block-1 self-comparison is broken (A1 fails)."""
    rng = np.random.default_rng(1)
    centre = {'S1': [.15, .15, .15, .15, .40], 'S2': [.30, .25, .10, .25, .10], 'S3': [.15, .10, .35, .15, .25]}
    R = {}
    for i in range(n):
        code = f'R9{i}'
        R[code] = {'profile': {'A8_qualified': i % 2 == 0},
                   'scenarios': {s: _scenario(rng.dirichlet(np.array(c) * 40), (code, s) in fail) for s, c in centre.items()}}
    return {'_imported': 'synthetic', 'respondents': R}


class TestInputs(unittest.TestCase):
    def test_frozen_matrix_hash_checked(self):
        with open(MATRIX) as f:
            rec = json.load(f)
        ra.load_frozen_matrix(MATRIX)
        bad = copy.deepcopy(rec); bad['matrix']['C1']['TTDP'] = 5
        fd, p = tempfile.mkstemp(suffix='.json'); os.close(fd)
        with open(p, 'w') as f:
            json.dump(bad, f)
        with self.assertRaises(ra.AnalysisError):
            ra.load_frozen_matrix(p)
        os.remove(p)

    def test_enterprise_cells_read(self):
        e = ra.enterprise_cells(SHEET)
        self.assertEqual(set(e), {('C1', 'SECC'), ('C3', 'SECC'), ('C5', 'SECC'), ('C7', 'SECC'), ('C1', 'TCO')})


class TestAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, cls.variants = ra.build_models(ra.load_frozen_matrix(MATRIX), ra.enterprise_cells(SHEET))
        fail = {('R90', 'S2'), ('R91', 'S2'), ('R92', 'S3'), ('R93', 'S3')}
        cls.res = ra.analyse(synthetic(6, fail), cls.model, cls.variants, '2026-10-21', k=400)

    def test_smaa_only_with_five_valid(self):
        sc = self.res['scenarios']
        self.assertEqual((sc['S1']['valid_A1'], sc['S2']['valid_A1'], sc['S3']['valid_A1']), (6, 4, 4))
        self.assertTrue(sc['S1']['A14_run'])
        self.assertFalse(sc['S2']['A14_run'])
        self.assertIn('ranking_descriptive', sc['S2'])
        self.assertNotIn('first_rank', sc['S2']['ranking_descriptive'])
        self.assertEqual(self.res['P_as_specified_A14_scenarios'], ['S1'])

    def test_eo1_uses_all_choices_and_a1_subset(self):
        e = self.res['scenarios']['S2']['E-O1']
        self.assertEqual(len(e['panellists']), 6)
        self.assertEqual(len(e['a1_only_panellists']), 4)
        self.assertEqual(self.res['scenarios']['S2']['choice_counts']['n'], 6)
        self.assertIn('C2', e['uniform_reference']['first_rank'])
        self.assertNotIn('C2', self.res['scenarios']['S1']['E-O1']['main']['first_rank'])   # S1 security floor

    def test_carbon_weights_only_for_valid(self):
        c = self.res['scenarios']['S2']['E-C1']
        self.assertEqual(len(c['answers']), 6)
        self.assertEqual(len(c['carbon_weight_valid_bwm']), 4)

    def test_outputs_serialise(self):
        js = json.dumps(ra.clean(self.res))
        self.assertIn('P_exploratory_E-O1', js)
        self.assertIn('| S1 |', ra.report_md(ra.clean(self.res)))


if __name__ == '__main__':
    unittest.main()
