import smtplib
from typing import Dict, Any

def validate_email(email: str, host: str, port: int, user: str, password: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "email": email,
        "validated": False,
        "error": None
    }
    try:
        server = smtplib.SMTP(host, port, timeout=10)
        server.starttls()
        server.login(user, password)
        code, _ = server.rcpt(email)
        result["validated"] = code in [250, 251]
        server.quit()
    except Exception as e:
        result["error"] = str(e)
    return result
