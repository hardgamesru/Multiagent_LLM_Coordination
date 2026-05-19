def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or '.' not in parts[1]:
        raise ValueError('Invalid email format')
    local_part, domain_part = parts
    normalized_email = f"{local_part}@{domain_part.lower()}"
    if not local_part or not domain_part:
        raise ValueError('Local part or domain cannot be empty')
    return normalized_email
