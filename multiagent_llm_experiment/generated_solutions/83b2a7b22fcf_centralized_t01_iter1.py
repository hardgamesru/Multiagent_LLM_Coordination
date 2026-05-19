def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or not all(parts):
        raise ValueError('Invalid email format')
    local_part, domain_part = parts
    if '.' not in domain_part:
        raise ValueError('Domain is missing a dot')
    return f"{local_part}@{domain_part.lower()}"
