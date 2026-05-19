def normalize_email(email: str) -> str:
    # Remove leading and trailing white space
    email = email.strip()
    
    # Split into local and domain parts
    parts = email.split('@')
    
    # Check that there is exactly one '@' symbol
    if len(parts) != 2:
        raise ValueError('Email must have exactly one "@".')
        
    # Extract local and domain parts
    local_part, domain_part = parts
    
    # Ensure neither part is empty
    if not local_part or not domain_part:
        raise ValueError('Local and domain parts cannot be empty.')
    
    # Ensure domain has at least one '.'
    if '.' not in domain_part:
        raise ValueError('Domain must contain a dot.')
    
    # Normalize by making domain lowercase
    normalized_email = f"{local_part}@{domain_part.lower()}"
    
    return normalized_email
