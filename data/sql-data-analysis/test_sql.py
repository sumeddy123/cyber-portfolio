import sqlite3
import unittest
from analyze import ROOT, report


class SQLTests(unittest.TestCase):
    def test_join_preserves_inactive_user(self):
        self.assertIn({'username': 'riley', 'total_events': 0, 'failures': 0}, report()['account_summary'])

    def test_threshold_and_aggregation(self):
        self.assertEqual(report()['repeated_failures'], [{'source_ip': '192.0.2.10', 'failures': 3}])
        self.assertEqual(report(4)['repeated_failures'], [])
        with self.assertRaises(ValueError):
            report(0)

    def test_foreign_key_and_outcome_constraints(self):
        with sqlite3.connect(':memory:') as db:
            db.executescript((ROOT / 'schema.sql').read_text())
            db.execute("INSERT INTO users VALUES (1, 'alex')")
            for user, outcome in [(99, 'failure'), (1, 'unknown')]:
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute('INSERT INTO login_events VALUES (1, ?, ?, ?, ?)',
                               (user, '192.0.2.1', '2026-01-01T00:00:00Z', outcome))
