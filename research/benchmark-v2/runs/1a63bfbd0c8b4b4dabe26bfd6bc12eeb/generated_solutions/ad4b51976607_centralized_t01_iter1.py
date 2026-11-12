def normalize_email(email: str) -> str:
    email = email.strip()
    if '@' not in email or email.count('@') > 1:
        raise ValueError
    local, domain = email.split('@')
    if not local or not local.isalpha() or not '.' in domain or not any(c.isalnum() for c in domain):
        raise ValueError
    return f"{local}@{domain.lower()}"
