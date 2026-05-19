def normalize_email(email: str) -> str:
    email = email.strip()
    local_part, domain = email.split('@', 1)
    
    if not local_part or '.' not in domain or ' ' in domain:
        raise ValueError("Invalid email format")
    
    return f"{local_part}@{domain.lower().rstrip()}".rstrip()
