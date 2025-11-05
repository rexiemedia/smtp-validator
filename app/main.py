from flask import Flask, request, jsonify
from app.parser import extract_fields
from app.validator import validate_email
from app.sheets import append_to_google_sheet
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    raw_text = request.json.get('data', '')
    fields = extract_fields(raw_text)

    smtp_config = {
        "host": os.getenv("SMTP_HOST", "smtp.example.com"),
        "port": int(os.getenv("SMTP_PORT", 587)),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASS", "")
    }

    validation = validate_email(
        email=fields["email"],
        host=smtp_config["host"],
        port=smtp_config["port"],
        user=smtp_config["user"],
        password=smtp_config["password"]
    )

    append_to_google_sheet([
        fields["email"],
        fields["name"],
        fields["company"],
        fields["phone"]
    ])

    return jsonify({
        **fields,
        "validated": validation["validated"],
        "error": validation["error"]
    })
