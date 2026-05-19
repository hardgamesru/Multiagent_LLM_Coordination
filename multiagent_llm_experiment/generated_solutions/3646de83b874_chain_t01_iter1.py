def normalize_email(email: str) -> str:
    # Remove surrounding white space
    email = email.strip()
    
    # Split into local and domain parts using '@'
    parts = email.split('@')
    
    # Check there is exactly one '@' symbol
    if len(parts) != 2:
        raise ValueError('Email must have exactly one "@".')
        
    # Extract local and domain parts
    local_part, domain_part = parts
    
    # Ensure both local and domain are non-empty
    if not local_part or not domain_part:
        raise ValueError('Local part and domain cannot be empty.')
    
    # Convert domain to lowercase
    normalized_domain = domain_part.lower()
    
    # Validate domain contains at least one '.'
    if '.' not in normalized_domain:
        raise ValueError('Domain must contain a dot.')
    
    return f"{local_part}@{normalized_domain}"
