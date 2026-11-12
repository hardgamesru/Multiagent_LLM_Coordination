def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError
    local_part, domain = parts
    if '@' in local_part or '.' in local_part:
        raise ValueError
    if '.' not in domain or domain.count('.') > 1:
        raise ValueError
    return f"{local_part}@{domain.lower()}"
