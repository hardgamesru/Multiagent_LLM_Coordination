def normalize_email(email: str) -> str:
    if not isinstance(email, str):
        raise ValueError('Invalid email format')
    
    # Remove leading and trailing whitespaces
    email = email.strip()
    
    # Split into local and domain parts
    parts = email.split('@')
    
    # Check for exactly one '@'
    if len(parts) != 2:
        raise ValueError('Email must have exactly one "@" symbol')
        
    local_part, domain_part = parts
    
    # Validate that both parts are non-empty
    if not local_part or not domain_part:
        raise ValueError('Local part and domain cannot be empty')
        
    # Convert domain to lowercase
    normalized_domain = domain_part.lower()
    
    # Ensure there is at least one dot in the domain
    if '.' not in normalized_domain:
        raise ValueError('Domain must contain a dot')
        
    return f"{local_part}@{normalized_domain}"
