def normalize_email(email: str) -> str:
    email = email.strip()
    if "@" not in email or email.count("@") != 1:
        raise ValueError("Invalid email format")
    local_part, domain_part = email.split('@')
    if not local_part or not domain_part or '.' not in domain_part:
        raise ValueError("Invalid email format")
    return f"{local_part}@{domain_part.lower()}"
