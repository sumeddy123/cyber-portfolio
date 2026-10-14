import unittest
from app import create_app


class APITests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()
        self.event = dict(timestamp='2026-01-01T00:00:00Z', source_ip='192.0.2.1',
                          username='demo', outcome='failure')

    def test_health_and_headers(self):
        response = self.client.get('/health')
        self.assertEqual(response.json, {'status': 'ok'})
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')

    def test_valid_ipv4_and_ipv6(self):
        for ip in ('192.0.2.1', '2001:db8::1'):
            self.event['source_ip'] = ip
            self.assertEqual(self.client.post('/validate-event', json=self.event).status_code, 200)

    def test_invalid_fields(self):
        for key, value in [('timestamp', 'yesterday'), ('timestamp', '2026-01-01'),
                           ('source_ip', 'bad'), ('source_ip', 123), ('source_ip', True), ('username', ' '), ('outcome', 'unknown')]:
            event = dict(self.event, **{key: value})
            self.assertEqual(self.client.post('/validate-event', json=event).status_code, 400)

    def test_missing_and_wrong_shape(self):
        for item in ({}, [], None):
            self.assertEqual(self.client.post('/validate-event', data=__import__('json').dumps(item),
                                             content_type='application/json').status_code, 400)

    def test_malformed_json(self):
        self.assertEqual(self.client.post('/validate-event', data='{', content_type='application/json').status_code, 400)

    def test_content_type_and_size(self):
        self.assertEqual(self.client.post('/validate-event', data='hello').status_code, 415)
        self.assertEqual(self.client.post('/validate-event', json={'data': 'x' * 17000}).status_code, 413)

    def test_no_mutation_endpoint(self):
        self.assertEqual(self.client.delete('/health').status_code, 405)
        self.assertEqual(self.client.get('/missing').status_code, 404)


if __name__ == '__main__':
    unittest.main()
