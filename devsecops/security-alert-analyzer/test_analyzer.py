from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from analyzer import analyze, load_events, main


def event(second, outcome='failure', ip='192.0.2.1', user='demo'):
    return dict(timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=second),
                source_ip=ip, username=user, outcome=outcome)


class AnalyzerTests(unittest.TestCase):
    def test_below_threshold_and_empty(self):
        self.assertEqual(analyze([])['alert_count'], 0)
        self.assertEqual(analyze([event(i) for i in range(4)])['alert_count'], 0)

    def test_exact_threshold_and_sorted_input(self):
        report = analyze([event(i) for i in reversed(range(5))])
        self.assertEqual(report['alert_count'], 1)
        self.assertEqual(report['alerts'][0]['failure_count'], 5)

    def test_inclusive_boundary(self):
        self.assertEqual(analyze([event(0), event(300)], 2)['alert_count'], 1)
        self.assertEqual(analyze([event(0), event(301)], 2)['alert_count'], 0)

    def test_ip_isolation(self):
        self.assertEqual(analyze([event(i, ip=f'192.0.2.{i}') for i in range(5)])['alert_count'], 0)

    def test_success_requires_same_account(self):
        events = [event(i) for i in range(5)]
        events += [event(5, 'success', user='other'), event(6, 'success'), event(7, 'success')]
        self.assertEqual([a['rule'] for a in analyze(events)['alerts']],
                         ['repeated_failed_logins', 'success_after_repeated_failures'])

    def test_expired_failures_do_not_correlate(self):
        self.assertEqual(analyze([event(i) for i in range(5)] + [event(400, 'success')])['alert_count'], 1)

    def test_cooldown(self):
        report = analyze([event(i) for i in range(20)], threshold=2, window_seconds=10)
        self.assertEqual([a['timestamp'] for a in report['alerts']],
                         [event(1)['timestamp'].isoformat(), event(11)['timestamp'].isoformat()])

    def test_invalid_config(self):
        for threshold, window in [(1, 300), (5, 0)]:
            with self.assertRaises(ValueError):
                analyze([], threshold, window)

    def test_sample_and_output(self):
        source = Path(__file__).with_name('sample_events.jsonl')
        report = analyze(load_events(source))
        self.assertEqual(report['alert_count'], 3)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'nested' / 'report.json'
            self.assertEqual(main([str(source), '--output', str(output)]), 0)
            self.assertTrue(output.exists())

    def test_bad_record_reports_line(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.jsonl'
            for line in ('not json', '{}', '[]', '{"timestamp":"2026-01-01T00:00:00Z","source_ip":123}', '{"timestamp":"2026-01-01"}'):
                path.write_text('\n' + line, encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'line 2'):
                    load_events(path)


if __name__ == '__main__':
    unittest.main()
