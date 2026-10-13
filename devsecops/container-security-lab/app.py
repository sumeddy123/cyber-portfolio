"""Small stateless API used to demonstrate CI and container controls."""
from datetime import datetime
from ipaddress import ip_address
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024

    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'none'; frame-ancestors 'none'"
        response.headers['Cache-Control'] = 'no-store'
        return response

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.name), error.code

    @app.get('/health')
    def health():
        return jsonify(status='ok')

    @app.post('/validate-event')
    def validate_event():
        if not request.is_json:
            return jsonify(error='Content-Type must be application/json'), 415
        item = request.get_json()
        if not isinstance(item, dict):
            return jsonify(error='Expected a JSON object'), 400
        try:
            timestamp = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
            if timestamp.tzinfo is None:
                raise ValueError('Timestamp needs a timezone')
            ip_address(item['source_ip'])
            if not isinstance(item['username'], str) or not 1 <= len(item['username'].strip()) <= 128:
                raise ValueError('Invalid username')
            if item['outcome'] not in ('success', 'failure'):
                raise ValueError('Invalid outcome')
        except (KeyError, TypeError, ValueError, AttributeError):
            return jsonify(error='Invalid event fields'), 400
        # Validation only: no persistence, authentication, or automatic response actions.
        return jsonify(valid=True), 200

    return app


app = create_app()
