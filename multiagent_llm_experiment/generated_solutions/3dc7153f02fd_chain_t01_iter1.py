def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Invalid email format")
    local_part, domain = parts
    if '.' not in domain or domain.count('.') > 1:
        raise ValueError("Invalid domain format")
    return f"{local_part}@{domain.lower()}"
