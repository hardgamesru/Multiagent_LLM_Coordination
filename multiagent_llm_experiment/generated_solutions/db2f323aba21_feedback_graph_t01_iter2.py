def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError('Invalid email format')
    local_part, domain = parts
    if '.' not in domain:
        raise ValueError('Domain must contain a dot')
    return f"{local_part}@{domain.lower()}"
