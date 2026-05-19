def normalize_email(email: str) -> str:
    email = email.strip()
    if email.count("@") != 1:
        raise ValueError("email must contain exactly one @")
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        raise ValueError("invalid email")
    return local + "@" + domain.lower()
