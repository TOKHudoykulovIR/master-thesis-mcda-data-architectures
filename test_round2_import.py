"""Tests for round2_import.py on synthetic exports built from the real export header row (fixtures/export-headers.json).
No real response or identity is used. Run from this folder:  python -m unittest test_round2_import -v"""
import json, os, tempfile, unittest, datetime
import numpy as np
import openpyxl
import round2_import as ri

HERE = os.path.dirname(os.path.abspath(__file__))
HEADERS = json.load(open(os.path.join(HERE, 'fixtures', 'export-headers.json'), encoding='utf-8'))['headers']
KEY = {'panel': {'R91': {'version': 'A', 'emails': [], 'first_names': ['ann'], 'surnames': ['alphason']},
                 'R92': {'version': 'B', 'emails': ['bob.b@x.com'], 'first_names': ['bob'], 'surnames': ['betason']},
                 'R93': {'version': 'C', 'emails': [], 'first_names': ['gina', 'гіна'], 'surnames': ['gammason', 'гаммасон']}},
       'researcher': ['researcherov']}
CRIT = ri.OPTION_TEXT


CRIT_CODES = ['TTDP', 'AIRD', 'PORT', 'TCO', 'SECC']


def section(best, worst, bo, ow, carbon=('Carbon intensity matters less', 5)):
    return [CRIT[best], CRIT[worst], *bo, *ow, 'because', carbon[0], carbon[1]]


GOOD = section(4, 3, [3, 4, 5, 8, 1], [3, 2, 2, 1, 8])            # SECC best, TCO worst, a_BW 8 both ways
OTHER = section(0, 1, [1, 6, 2, 3, 4], [6, 1, 3, 2, 2])           # TTDP best, AIRD worst, a_BW 6


def row(i, name, email, sections, profile=('Lead or Principal Data Engineer', '5 to 10 years',
                                            'Yes, as the decision owner or co-owner'), when=(2026, 10, 5, 10, 0)):
    t = datetime.datetime(*when)
    r = [i, t, t, email, name, None, *profile]
    for s in sections:
        r += s
    assert len(r) == len(HEADERS)
    return r


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = []

    def tearDown(self):
        for p in self._tmp:
            os.remove(p)

    def write(self, rows, blank_after_first=False):
        fd, path = tempfile.mkstemp(suffix='.xlsx'); os.close(fd)
        wb = openpyxl.Workbook(); ws = wb.active
        ws.append(HEADERS)
        for k, r in enumerate(rows):
            ws.append(r)
            if blank_after_first and k == 0:
                ws.append([None] * len(HEADERS))
        wb.save(path)
        self._tmp.append(path)
        return path


class TestLayout(unittest.TestCase):
    def test_real_header_row_parses(self):
        lay = ri.parse_layout(HEADERS)
        self.assertEqual([s['best'] for s in lay['sections']], [9, 24, 39])
        self.assertEqual((lay['email'], lay['name']), (3, 4))

    def test_reordered_criteria_rejected(self):
        h = list(HEADERS); h[11], h[12] = h[12], h[11]
        with self.assertRaises(ri.ImportError_):
            ri.parse_layout(h)

    def test_missing_section_rejected(self):
        with self.assertRaises(ri.ImportError_):
            ri.parse_layout(HEADERS[:39])

    def test_unknown_metadata_language_falls_back_to_positions(self):
        h = list(HEADERS); h[3], h[4] = 'Ел. адреса', 'Прізвище'
        self.assertEqual((ri.parse_layout(h)['email'], ri.parse_layout(h)['name']), (3, 4))


class TestImport(Base):
    def test_versions_map_sections_to_scenarios(self):
        a = self.write([row(1, 'Ann Alphason', 'ann_alphason@x.com', [GOOD, OTHER, GOOD])])
        b = self.write([row(1, 'Bob Betason', 'bob.b@x.com', [OTHER, GOOD, GOOD])])
        data, rep = ri.import_versions({'A': a, 'B': b}, KEY)
        self.assertEqual(data['respondents']['R91']['scenarios']['S2']['best'], 'TTDP')   # A: section 2 = S2
        self.assertEqual(data['respondents']['R92']['scenarios']['S2']['best'], 'TTDP')   # B: section 1 = S2
        self.assertEqual(data['respondents']['R92']['scenarios']['S2']['position'], 1)
        self.assertTrue(all(s['A1']['passed'] for s in data['respondents']['R91']['scenarios'].values()))
        self.assertEqual(rep['problems'], [])
        self.assertEqual(len(data['_files']['A']['sha256']), 64)

    def test_surname_alone_does_not_match(self):
        c = self.write([row(1, 'Olga Gammason', 'olga@x.com', [GOOD] * 3)])
        data, rep = ri.import_versions({'C': c}, KEY)
        self.assertEqual(data['respondents'], {})
        self.assertEqual(len(rep['problems']), 1)

    def test_cyrillic_and_email_matching(self):
        c = self.write([row(1, 'Гіна Гаммасон', 'x@y.com', [GOOD] * 3)])
        b = self.write([row(1, 'B. B.', 'Bob.B@x.com', [GOOD] * 3)])
        data, _ = ri.import_versions({'C': c, 'B': b}, KEY)
        self.assertEqual(sorted(data['respondents']), ['R92', 'R93'])

    def test_researcher_excluded_conflict_reported(self):
        c = self.write([row(1, 'Res Researcherov', 'r@x.com', [GOOD] * 3),
                        row(2, 'Gina Gammason Researcherov', 'g@x.com', [GOOD] * 3),
                        row(3, 'Gina Gammason', 'g@x.com', [GOOD] * 3)])
        data, rep = ri.import_versions({'C': c}, KEY)
        self.assertEqual(sorted(data['respondents']), ['R93'])
        self.assertEqual(len(data['excluded_rows']), 2)
        self.assertTrue(any('both the researcher' in p for p in rep['problems']))

    def test_mislabelled_file_stops(self):
        b_as_a = self.write([row(1, 'Bob Betason', 'b@x.com', [OTHER, GOOD, GOOD])])
        with self.assertRaises(ri.ImportError_):
            ri.import_versions({'A': b_as_a}, KEY)
        data, _ = ri.import_versions({'A': b_as_a}, KEY, allow_version_mismatch=True)
        self.assertTrue(data['respondents']['R92']['wrong_version'])

    def test_single_wrong_link_flagged_and_order_seen_used(self):
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [GOOD] * 3),
                        row(2, 'Ann Alphason', 'a@x.com', [OTHER, GOOD, GOOD])])
        r = ri.import_versions({'C': c}, KEY)[0]['respondents']['R91']
        self.assertTrue(r['wrong_version'])
        self.assertEqual(r['scenarios']['S3']['best'], 'TTDP')                              # C: section 1 = S3

    def test_duplicate_rule_assigned_then_latest(self):
        a = self.write([row(1, 'Ann Alphason', 'a@x.com', [OTHER] * 3, when=(2026, 10, 5, 9, 0)),
                        row(2, 'Ann Alphason', 'a@x.com', [GOOD] * 3, when=(2026, 10, 6, 9, 0))])
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [GOOD] * 3),
                        row(2, 'Ann Alphason', 'a@x.com', [OTHER] * 3, when=(2026, 10, 7, 9, 0))])
        data, rep = ri.import_versions({'A': a, 'C': c}, KEY)
        r = data['respondents']['R91']
        self.assertEqual(r['version_answered'], 'A')                    # assigned version beats the later C row
        self.assertEqual(r['scenarios']['S1']['best'], 'SECC')          # latest A row kept
        self.assertEqual(sum('duplicate' in p for p in rep['problems']), 2)

    def test_a1_a3_and_carbon_flags(self):
        bad = section(2, 2, [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], ('Equally important', 4))
        abw2 = section(0, 1, [1, 2, 1, 1, 1], [2, 1, 1, 1, 1])
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [bad, abw2, GOOD])])
        r = ri.import_versions({'C': c}, KEY)[0]['respondents']['R93']['scenarios']
        self.assertFalse(r['S3']['A1']['passed'])
        self.assertEqual(r['S3']['carbon'], {'direction': 'Equally important', 'rating': 4, 'a': 1.0, 'consistent': False})
        self.assertTrue(r['S1']['A1']['passed'])
        self.assertFalse(r['S1']['A3']['consistent'])
        self.assertTrue(r['S1']['A3']['rule'].startswith('a_BW = 2'))

    def test_invalid_values_reported_without_echo(self):
        sec = list(GOOD); sec[0] = 'SECC – Security and compliance'            # en dash, not the option text
        sec2 = list(GOOD); sec2[0] = 'TTDP — Time-to-data-product;SECC — Security and compliance;'   # multi-select
        sec3 = list(GOOD); sec3[13] = 'Carbon intensity matters  more'; sec3[4] = 'inf'
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [sec, sec2, sec3])])
        data, rep = ri.import_versions({'C': c}, KEY)
        r = data['respondents']['R93']
        self.assertFalse(any(s['valid'] for s in r['scenarios'].values()))
        md = ri.report_md(data, rep)
        for leak in ('Security and compliance', 'Time-to-data-product', 'matters  more', 'inf'):
            self.assertNotIn(leak, md)
        self.assertIsNone(r['scenarios']['S2']['carbon'])          # C: section 3 = S2, carbon answer invalid
        self.assertIsNotNone(r['scenarios']['S3']['carbon'])       # carbon kept although the BWM part is invalid

    def test_profile_rules(self):
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [GOOD] * 3,
                            profile=('Other text', '5 to 10 years', 'Yes, as a contributor to the evaluation'))])
        p = ri.import_versions({'C': c}, KEY)[0]['respondents']['R93']['profile']
        self.assertTrue(p['role_other'])
        self.assertIsNone(p['A8_qualified'])                        # unexpected option -> unknown, not False
        self.assertTrue(p['A8_participation_only'])

    def test_sheet_row_numbers_survive_blank_rows(self):
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [GOOD] * 3),
                        row(2, 'Nobody Known', 'n@x.com', [GOOD] * 3)], blank_after_first=True)
        data, _ = ri.import_versions({'C': c}, KEY)
        self.assertIn('sheet row 4', data['excluded_rows'][0]['where'])

    def test_researcher_rows_numbered_when_included(self):
        c = self.write([row(1, 'Res Researcherov', 'r@x.com', [GOOD] * 3),
                        row(2, 'Res Researcherov', 'r@x.com', [OTHER] * 3)])
        data, _ = ri.import_versions({'C': c}, KEY, include_researcher=True)
        self.assertEqual(sorted(data['respondents']), ['TEST1', 'TEST2'])

    def test_section_order_check_from_researcher_row(self):
        marked = lambda names: [GOOD[:12] + [n] + GOOD[13:] for n in names]
        b_ok = self.write([row(1, 'Res Researcherov', 'r@x.com', marked(['High-growth start-up', 'Sustainability', 'S1'])),
                           row(2, 'Bob Betason', 'b@x.com', [GOOD] * 3)])
        data, _ = ri.import_versions({'B': b_ok}, KEY)
        self.assertEqual(data['_files']['B']['order_check'], 'passed')
        b_bad = self.write([row(1, 'Res Researcherov', 'r@x.com', marked(['Regulated finance', 'S2', 'S3'])),
                            row(2, 'Bob Betason', 'b@x.com', [GOOD] * 3)])
        with self.assertRaises(ri.ImportError_):
            ri.import_versions({'B': b_bad}, KEY)
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [GOOD] * 3)])
        self.assertNotIn('order_check', ri.import_versions({'C': c}, KEY)[0]['_files']['C'])

    def test_load_responses_round_trip(self):
        c = self.write([row(1, 'Gina Gammason', 'g@x.com', [GOOD, OTHER, GOOD])])
        data, _ = ri.import_versions({'C': c}, KEY)
        data = json.loads(json.dumps(data))                         # through JSON, as on disk
        (code, br), = ri.load_responses(data, 'S1')                 # C: section 2 = S1 = OTHER
        self.assertEqual((code, br.best, br.worst), ('R93', 0, 1))
        self.assertTrue(np.array_equal(br.bo, [1, 6, 2, 3, 4]))


class TestCorrections(Base):
    """Amendment 3, point 6: a panellist's own written correction of the comparison blocks."""
    def _data(self):
        broken = section(4, 0, [2, 4, 6, 5, 1], [5, 4, 2, 3, 1])     # SECC best, TTDP worst; LEAST not 1 in block 2
        b = self.write([row(1, 'Bob Betason', 'bob.b@x.com', [GOOD, OTHER, broken])])
        return ri.import_versions({'B': b}, KEY)[0]

    def test_applied_first_submission_kept_and_rechecked(self):
        data = self._data()
        s = data['respondents']['R92']['scenarios']['S1']             # third section of version B
        self.assertFalse(s['A1']['passed'])
        fix = {'code': 'R92', 'scenario': 'S1', 'source': 'message', 'recorded': '2026-10-19',
               'bo': dict(zip(CRIT_CODES, [6, 5, 3, 4, 1])), 'ow': dict(zip(CRIT_CODES, [1, 3, 5, 4, 6]))}
        ri.apply_corrections(data, [fix])
        s = data['respondents']['R92']['scenarios']['S1']
        self.assertTrue(s['A1']['passed'])
        self.assertEqual(s['first_submission']['bo']['TTDP'], 2)
        self.assertEqual(s['bo']['TTDP'], 6)
        self.assertEqual((s['best'], s['worst']), ('SECC', 'TTDP'))
        self.assertEqual(data['corrections_applied'][0]['code'], 'R92')
        self.assertIn('Corrections applied', ri.report_md(data, {'problems': []}))

    def test_correction_not_matching_most_least_rejected(self):
        data = self._data()
        fix = {'code': 'R92', 'scenario': 'S1', 'source': 'message', 'recorded': '2026-10-19',
               'bo': dict(zip(CRIT_CODES, [1, 5, 3, 4, 6])), 'ow': dict(zip(CRIT_CODES, [6, 3, 5, 4, 1]))}
        with self.assertRaises(ri.ImportError_):
            ri.apply_corrections(data, [fix])

    def test_unknown_response_rejected(self):
        data = self._data()
        with self.assertRaises(ri.ImportError_):
            ri.apply_corrections(data, [{'code': 'R99', 'scenario': 'S1', 'bo': {}, 'ow': {}, 'source': '', 'recorded': ''}])


if __name__ == '__main__':
    unittest.main()
