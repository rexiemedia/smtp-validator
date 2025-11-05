from app.parser import extract_fields

def test_extract_fields():
    text = "Name: Jane Doe\nCompany: Acme Inc.\nPhone: +1 555-123-4567\nEmail: jane@acme.com"
    result = extract_fields(text)
    assert result["email"] == "jane@acme.com"
    assert result["name"] == "Jane Doe"
    assert result["company"] == "Acme Inc."
    assert "+1 555-123-4567" in result["phone"]
