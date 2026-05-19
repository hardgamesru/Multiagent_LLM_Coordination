def normalize_email(email: str) -> str:
    email = email.strip()
    local_part, domain = email.rsplit('@', 1)
    if '@' in local_part or not local_part or '.' not in domain or domain.count('.') > 1:
        raise ValueError
    return f'{local_part}@{domain.lower()}'
