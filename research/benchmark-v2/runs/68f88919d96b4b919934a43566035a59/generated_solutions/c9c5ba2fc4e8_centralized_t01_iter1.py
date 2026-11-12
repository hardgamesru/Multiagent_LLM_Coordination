def normalize_email(email: str) -> str:
    email = email.strip()
    if email.count('@') != 1:
        raise ValueError("Email must contain exactly one '@' symbol.")
    local_part, domain_part = email.split('@')
    if not local_part or not domain_part:
        raise ValueError("Local part and domain must be non-empty.")
    if '.' not in domain_part:
        raise ValueError("Domain must contain a dot.")
    return f"{local_part}@{domain_part.lower()}"
