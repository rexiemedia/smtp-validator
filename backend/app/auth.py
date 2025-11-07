import requests
from jose import jwt
from flask import request, jsonify
from functools import wraps
from app.config import Config

AUTH0_DOMAIN = Config.AUTH0_DOMAIN
API_AUDIENCE = Config.AUTH0_AUDIENCE
ALGORITHMS = ["RS256"]
ROLE_NAMESPACE = "https://your-app.com/roles"  # Must match Auth0 claim namespace

def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()["keys"]

def verify_token(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = next((key for key in jwks if key["kid"] == unverified_header["kid"]), None)

    if not rsa_key:
        raise Exception("Unable to find appropriate key")

    return jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/"
    )

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"error": "Invalid Authorization header"}), 401

        token = parts[1]
        try:
            payload = verify_token(token)
            request.user = payload
        except Exception as e:
            return jsonify({"error": "Token verification failed", "details": str(e)}), 401

        return f(*args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = getattr(request, "user", {})
            roles = payload.get(ROLE_NAMESPACE, [])
            if role not in roles:
                return jsonify({"error": "Forbidden: missing required role"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
