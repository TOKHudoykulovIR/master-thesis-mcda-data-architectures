"""E-C1 coding of the Round 2 carbon question as fielded (Rating 1-9, no branching; Stage 2 revision of 7 Oct 2026)."""
import unittest
from engine.exploratory import code_carbon_answer


class TestCarbonFormCoding(unittest.TestCase):
    def test_consistent_answers(self):
        self.assertEqual(code_carbon_answer('Carbon intensity matters less', 7), (7.0, True))
        self.assertEqual(code_carbon_answer('Carbon intensity matters more', 4), (0.25, True))
        self.assertEqual(code_carbon_answer('Equally important', 1), (1.0, True))

    def test_inconsistent_answers_coded_equal_and_flagged(self):
        self.assertEqual(code_carbon_answer('Carbon intensity matters less', 1), (1.0, False))
        self.assertEqual(code_carbon_answer('Carbon intensity matters more', 1), (1.0, False))
        self.assertEqual(code_carbon_answer('Equally important', 6), (1.0, False))

    def test_label_tolerance_and_errors(self):
        self.assertEqual(code_carbon_answer('  carbon intensity matters LESS ', 9), (9.0, True))
        with self.assertRaises(ValueError):
            code_carbon_answer('Somewhat', 3)
        with self.assertRaises(ValueError):
            code_carbon_answer('Equally important', 0)
        for bad in (10, 7.5, True, '3.5'):
            with self.assertRaises(ValueError):
                code_carbon_answer('Carbon intensity matters less', bad)
        self.assertEqual(code_carbon_answer('Carbon intensity matters less', '7'), (7.0, True))
        self.assertEqual(code_carbon_answer('Carbon intensity matters less', 7.0), (7.0, True))


if __name__ == '__main__':
    unittest.main()
