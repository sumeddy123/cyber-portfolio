from pathlib import Path
import tempfile
import unittest
from detector import summarize


class DetectorTests(unittest.TestCase):
    def test_ipv6_canonicalization_and_malformed_addresses(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'auth.log'
            path.write_text('Failed password for a from 2001:db8::1 port 22\n'
                            'Failed password for a from 2001:0db8::1 port 22\n'
                            'Failed password for a from 999.1.1.1 port 22\n'
                            'Accepted password for a from 192.0.2.1 port 22\n')
            result = summarize(path, 2)
            self.assertEqual(result['suspicious'], {'2001:db8::1': 2})
            self.assertEqual(result['invalid_addresses'], 1)
            self.assertEqual(result['failed_attempts'], 2)

    def test_empty_and_invalid_threshold(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'empty.log'
            path.touch()
            self.assertEqual(summarize(path)['counts'], {})
            with self.assertRaises(ValueError):
                summarize(path, 0)
