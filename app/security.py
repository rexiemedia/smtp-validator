from functools import wraps
from flask import request, jsonify
import os

def require_api_key(f):
    """Decorator to enforce API key header validation."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        expected_key = os.getenv("API_KEY")

        if not expected_key:
            return jsonify({"error": "Server misconfiguration: API_KEY not set"}), 500

        if api_key != expected_key:
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)
    return decorated_function
