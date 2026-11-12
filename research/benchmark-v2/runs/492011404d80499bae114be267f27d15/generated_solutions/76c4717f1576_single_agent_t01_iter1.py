def normalize_email(email: str) -> str:
    email = email.strip()
    if email.count('@') != 1:
        raise ValueError("Invalid email: must contain exactly one '@'")
    local, domain = email.split('@')
    if not local or not domain:
        raise ValueError("Invalid email: local and domain parts must be non-empty")
    if '.' not in domain:
        raise ValueError("Invalid email: domain must contain a dot")
    return local + '@' + domain.lower()
