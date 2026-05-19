def normalize_email(email: str) -> str:
    # Trim outer spaces
    email = email.strip()
    
    # Split into local and domain parts
    parts = email.split('@')
    
    # Validate exactly one '@' exists
    if len(parts) != 2:
        raise ValueError('Email must contain exactly one "@".')
        
    local_part, domain_part = parts
    
    # Check that both parts are non-empty
    if not local_part or not domain_part:
        raise ValueError('Local part and domain must be non-empty.')
    
    # Ensure domain has at least one dot
    if '.' not in domain_part:
        raise ValueError('Domain must contain at least one dot.')
    
    # Normalize by lowercasing only the domain part
    normalized_email = f"{local_part}@{domain_part.lower()}"
    
    return normalized_email
