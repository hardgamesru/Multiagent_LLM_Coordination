def normalize_email(email: str) -> str:
    email = email.strip()
    if email.count('@') != 1:
        raise ValueError("Email must contain exactly one '@'")
    local, domain = email.split('@')
    if not local or not domain:
        raise ValueError("Local part and domain must be non-empty")
    if '.' not in domain:
        raise ValueError("Domain must contain a dot")
    return local + '@' + domain.lower()
