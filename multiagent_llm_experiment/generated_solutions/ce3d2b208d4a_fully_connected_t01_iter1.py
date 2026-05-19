def normalize_email(email: str) -> str:
    email = email.strip()
    parts = email.split('@')
    
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        raise ValueError
    
    local_part, domain = parts
    
    if '.' not in domain or ' ' in domain:
        raise ValueError
    
    return f"{local_part.strip()}@{domain.lower().strip()}"
