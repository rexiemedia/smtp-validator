# safe_extract.py
import re
import os

# If you can, prefer the email-validator package:
# pip install email-validator
try:
    from email_validator import validate_email as ev_validate, EmailNotValidError
    HAVE_EMAIL_VALIDATOR = True
except Exception:
    HAVE_EMAIL_VALIDATOR = False

MAX_INPUT_LEN = int(os.getenv("MAX_INPUT_LEN", 2000))  # cap input length to prevent abuse

# Safer regexes (no nested ambiguous quantifiers).
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', re.I)
PHONE_RE = re.compile(r'\+?\d(?:[ \-\(\)\.\d]{7,}\d)')  # anchored-ish: starts with digit (or +) then at least ~9 digits/sep
NAME_RE = re.compile(r'^[Nn]ame[:\-]?\s*(.+)$', re.MULTILINE)
COMPANY_RE = re.compile(r'^[Cc]ompany[:\-]?\s*(.+)$', re.MULTILINE)

def _safe_search(pattern, text):
    """Wrapper to run re.search on sliced text to avoid pathological length."""
    # operate on a limited window to avoid scanning absurdly long inputs
    window = text if len(text) <= MAX_INPUT_LEN else text[:MAX_INPUT_LEN]
    return pattern.search(window)

def extract_fields(text):
    """
    Extracts email, phone, name, company from `text` safely.
    - Caps input length (MAX_INPUT_LEN)
    - Uses safer regex patterns
    - Optionally validates email with email-validator if installed
    """
    if not isinstance(text, str):
        text = str(text or "")

    # quick defensive cap — return empty/partial if input is too large
    if len(text) > 10 * MAX_INPUT_LEN:
        # too large; return early or truncate — avoid heavy processing
        text = text[:MAX_INPUT_LEN]

    # Prefer a robust validator if available
    email_match = _safe_search(EMAIL_RE, text)
    email_val = email_match.group(0) if email_match else ''

    if HAVE_EMAIL_VALIDATOR and email_val:
        try:
            v = ev_validate(email_val)  # raises EmailNotValidError if invalid
            email_val = v["email"]  # normalized form
        except EmailNotValidError:
            email_val = ''  # treat as not found/invalid

    phone_match = _safe_search(PHONE_RE, text)
    name_match = _safe_search(NAME_RE, text)
    company_match = _safe_search(COMPANY_RE, text)

    return {
        "email": email_val,
        "phone": phone_match.group(0).strip() if phone_match else '',
        "name": name_match.group(1).strip() if name_match else '',
        "company": company_match.group(1).strip() if company_match else ''
    }
