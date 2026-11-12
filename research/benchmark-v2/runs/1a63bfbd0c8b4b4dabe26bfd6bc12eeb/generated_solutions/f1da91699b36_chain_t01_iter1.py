def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or any(not part for part in parts):
        raise ValueError
    local_part, domain = parts
    if '.' not in domain:
        raise ValueError
    return f"{local_part}@{domain.lower()}"
