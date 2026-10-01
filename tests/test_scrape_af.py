import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import scrape_af as af


class ParserTests(unittest.TestCase):
    def fixture(self, pid):
        return (ROOT / 'tests' / 'fixtures' / f'{pid}.txt').read_text()

    def test_mixed_attack_separates_launched_from_destroyed(self):
        r = af.parse(self.fixture(70754))
        self.assertEqual((r['uav'], r['msl'], r['down_total'], r['uav_down']), (284, 74, 320, 265))

    def test_two_missile_types_in_one_bullet_and_detection_before_defense(self):
        r = af.parse(self.fixture(71026))
        self.assertEqual((r['msl'], r['msl_min'], r['down_total'], r['uav_down']), (35, 35, 156, 154))

    def test_unknown_missile_types_are_not_zero(self):
        r = af.parse(self.fixture(78627))
        self.assertIsNone(r['msl'])
        self.assertFalse(r['msl_complete'])
        self.assertEqual((r['msl_min'], r['uav_down'], r['down_total']), (4, 124, 131))

    def test_ukrainian_numeric_suffix_is_not_confused_with_hits(self):
        r = af.parse(self.fixture(71299))
        self.assertEqual((r['uav'], r['uav_down']), (181, 163))

    def test_daytime_update_cannot_replace_morning_window(self):
        self.assertIsNone(af.parse('Протягом дня 12 вересня противник атакував 410 ударними БпЛА. ЗБИТО/ПОДАВЛЕНО 336 ударних БпЛА'))
        self.assertEqual(af.parse(self.fixture(77891))['uav'], 129)

    def test_header_total_and_slash_separated_missile_types(self):
        r = af.parse(self.fixture(73563))
        self.assertEqual((r['down_total'], r['uav_down'], r['msl_min']), (186, 145, 44))
        self.assertIsNone(r['msl'])

    def test_missing_uav_outcome_is_unknown_not_total(self):
        r = af.parse('ЗБИТО/ПОДАВЛЕНО 90 ЦІЛЕЙ. У ніч на 1 серпня атакував 100 ударними БпЛА та 5 крилатими ракетами. Повітряний напад відбивали.')
        self.assertIsNone(r['uav_down'])

    def test_missile_subtype_outcome_is_not_the_total_without_a_header(self):
        r = af.parse('У ніч на 1 серпня атакував 100 ударними БпЛА та 5 крилатими ракетами. За попередніми даними збито/подавлено 3 крилаті ракети та 80 ворожих БпЛА.')
        self.assertIsNone(r['down_total'])
        self.assertEqual(r['uav_down'], 80)

    def test_unknown_bullet_type_is_not_dropped_when_another_type_has_a_number(self):
        r = af.parse('У ніч на 1 серпня атакував:\n- 5 крилатими ракетами;\n- протирадіолокаційними ракетами;\n- 100 ударними БпЛА.\nПовітряний напад відбивали.')
        self.assertIsNone(r['msl'])
        self.assertEqual(r['msl_min'], 5)

    def test_singular_missile_and_genuine_zero(self):
        for phrase, expected in [('балістичною ракетою і ', 1), ('', 0)]:
            r = af.parse(f'У ніч на 1 серпня атакував {phrase}100 ударними БпЛА. Повітряний напад відбивали.')
            self.assertEqual(r['msl'], expected)

    def test_missile_counts_written_as_words(self):
        r = af.parse(self.fixture(78956))   # „двома протикорабельними ракетами”
        self.assertEqual((r['msl'], r['msl_min'], r['msl_complete']), (2, 2, True))
        r = af.parse(self.fixture(81294))   # „ракетою” + „двома балістичними ракетами”
        self.assertEqual((r['msl'], r['msl_min'], r['msl_complete']), (3, 3, True))

    def test_intercepted_missiles_raise_the_minimum_when_launch_count_is_missing(self):
        r = af.parse(self.fixture(79861))   # typy bez liczby; przechwycono 4 + 3
        self.assertIsNone(r['msl'])
        self.assertEqual(r['msl_min'], 7)
        r = af.parse('У ніч на 1 серпня атакував балістичними ракетами та 100 ударними БпЛА. Повітряний напад відбивали. Збито/подавлено 82 цілі: дві балістичні ракети та 80 ворожих БпЛА.')
        self.assertEqual((r['msl'], r['msl_min']), (None, 2))

    def test_intercept_total_is_not_added_to_its_own_breakdown(self):
        r = af.parse(self.fixture(70754))   # „55 ракет” = 1 + 54
        self.assertEqual((r['msl'], r['msl_min'], r['msl_complete']), (74, 74, True))

    def test_more_intercepted_than_launched_is_not_a_complete_count(self):
        r = af.parse('У ніч на 1 серпня атакував 2 крилатими ракетами та 100 ударними БпЛА. Повітряний напад відбивали. Збито/подавлено 5 крилатих ракет та 80 ворожих БпЛА.')
        self.assertEqual((r['msl'], r['msl_min'], r['msl_complete']), (None, 5, False))

    def test_latest_correction_wins_even_if_smaller(self):
        ps = [(12, '2026-09-01T06:00:00+00:00', 'У ніч на 1 вересня атакував 80 ударними БпЛА.'),
              (11, '2026-09-01T05:00:00+00:00', 'У ніч на 1 вересня атакував 90 ударними БпЛА.')]
        with patch.object(af, 'fetch', return_value=''), patch.object(af, 'posts', return_value=ps):
            r = af.scrape('2026-09-01', max_pages=1, sleep=0)
        self.assertEqual(r['2026-09-01']['uav'], 80)

    def test_report_date_uses_stated_night_and_kyiv_timezone(self):
        self.assertEqual(af.report_day('У ніч на 31 грудня', '2026-01-01T02:00:00+00:00'), '2025-12-31')
        self.assertEqual(af.report_day('без дати', '2026-08-31T22:30:00+00:00'), '2026-09-01')

    def test_committed_data_invariants(self):
        rows = json.loads((ROOT / 'data' / 'daily.json').read_text())
        self.assertEqual(len(rows), len({r['d'] for r in rows}))
        self.assertEqual(rows, sorted(rows, key=lambda r: r['d']))
        for r in rows:
            self.assertGreaterEqual(r['uav'], 0)
            if r['uav_down'] is not None: self.assertLessEqual(r['uav_down'], r['uav'])
            self.assertEqual(r['msl'] is not None, r['msl_complete'])
            if r['msl'] is not None: self.assertEqual(r['msl'], r['msl_min'])
            self.assertEqual(r['coverage'], 'morning')


if __name__ == '__main__':
    unittest.main()
