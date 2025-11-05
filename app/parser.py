import re

def extract_fields(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'(\+?\d[\d\s\-().]{7,}\d)', text)
    name = re.search(r'(?:Name[:\-]?\s*|^)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text)
    company = re.search(r'(?:Company[:\-]?\s*|^)([A-Z][\w\s&.,-]{2,})', text)

    return {
        "email": email.group(0) if email else '',
        "phone": phone.group(0).strip() if phone else '',
        "name": name.group(1).strip() if name else '',
        "company": company.group(1).strip() if company else ''
}
