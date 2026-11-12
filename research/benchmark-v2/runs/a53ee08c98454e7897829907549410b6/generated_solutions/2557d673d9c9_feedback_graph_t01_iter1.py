def normalize_email(email: str) -> str:
    email = email.strip()
    if '@' not in email or email.count('@') > 1:
        raise ValueError
    local_part, domain = email.split('@')
    if not local_part or not domain or '.' not in domain:
        raise ValueError
    return f"{local_part}@{domain.lower()}"
