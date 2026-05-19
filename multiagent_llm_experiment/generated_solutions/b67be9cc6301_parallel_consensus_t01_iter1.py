def normalize_email(email: str) -> str:
    # Remove surrounding whitespaces
    stripped = email.strip()
    
    if not stripped or "@" not in stripped:
        raise ValueError("Invalid email format")
        
    parts = stripped.split("@", maxsplit=1)
    
    if len(parts) != 2:
        raise ValueError("Email must have exactly one '@'")
    
    local_part, domain_part = parts
    
    if "." not in domain_part or not local_part or not domain_part:
        raise ValueError("Domain must contain a dot and both local part and domain must be non-empty")
    
    return f"{local_part}@{domain_part.lower()}"
