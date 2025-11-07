from flask import Flask, request, jsonify
from app.parser import extract_fields
from app.validator import validate_email
from app.sheets import append_to_google_sheet
from app.security import require_api_key  # <-- import decorator
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/submit', methods=['POST'])
@require_api_key
def submit():
    data = request.get_json(silent=True) or {}
    raw_text = data.get('data', '')

    fields = extract_fields(raw_text)
    smtp_config = {
        "host": os.getenv("SMTP_HOST", "smtp.example.com"),
        "port": int(os.getenv("SMTP_PORT", 587)),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASS", "")
    }

    validation = validate_email(
        email=fields.get("email", ""),
        host=smtp_config["host"],
        port=smtp_config["port"],
        user=smtp_config["user"],
        password=smtp_config["password"]
    )

    append_to_google_sheet([
        fields.get("email", ""),
        fields.get("name", ""),
        fields.get("company", ""),
        fields.get("phone", "")
    ])

    return jsonify({
        **fields,
        "validated": validation.get("validated", False),
        "error": validation.get("error", None)
    })
