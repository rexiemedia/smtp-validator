from flask import Flask, request, jsonify
from app.auth import auth_bp, require_auth, require_role
from app.limiter import limiter, init_limiter
from app.parser import extract_fields
from app.quota import check_quota
from app.auth import require_auth, require_role
from app.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.secret_key = "your-secret"
app.register_blueprint(auth_bp)
init_limiter(app)

# User-specific quota
@limiter.limit("5/hour", key_func=lambda: request.user["sub"])
@app.route("/submit", methods=["POST"])
@require_auth
def submit():
    user_id = request.user["sub"]
    roles = request.user.get("https://your-app.com/roles", [])
    tier = "admin" if "admin" in roles else "pro" if "pro" in roles else "free"

    if not check_monthly_quota(user_id, tier):
        return jsonify({"error": "Monthly quota exceeded"}), 429

    data = request.json.get("data", "")
    result = extract_fields(data)
    return jsonify(result)

@app.route("/admin/reports", methods=["GET"])
@require_auth
@require_role("admin")
def view_reports():
    return jsonify({"status": "Admin access granted"})

# Admin-only route
@app.route("/admin/reports", methods=["GET"])
@require_auth
@require_role("admin")
def view_reports():
    return jsonify({"status": "Admin access granted"})
