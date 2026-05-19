def normalize_email(email: str) -> str:
    # Remove leading/trailing whitespace
    email = email.strip()
    
    # Split into local and domain parts using '@'
    parts = email.split('@')
    
    if len(parts) != 2 or not all(parts):
        raise ValueError('Invalid email format')
        
    local_part, domain_part = parts
    
    # Ensure there is at least one '.' in the domain
    if '.' not in domain_part:
        raise ValueError('Domain must contain a dot')
    
    # Convert domain to lowercase
    normalized_domain = domain_part.lower()
    
    return f"{local_part}@{normalized_domain}"
