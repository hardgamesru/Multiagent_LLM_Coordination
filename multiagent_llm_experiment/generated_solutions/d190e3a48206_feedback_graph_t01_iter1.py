def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or '@@' in email:
        raise ValueError
    local_part, domain = parts
    if '.' not in domain or not local_part or not domain:
        raise ValueError
    return f"{local_part}@{domain.lower()}"
