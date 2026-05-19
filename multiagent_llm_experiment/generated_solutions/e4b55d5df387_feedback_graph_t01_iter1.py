def normalize_email(email: str) -> str:
    # Remove surrounding whitespaces
    email = email.strip()
    
    # Split into local and domain parts using '@'
    parts = email.split('@')
    
    if len(parts) != 2:
        raise ValueError('Email must have exactly one "@" symbol.')
        
    local_part, domain_part = parts
    
    # Check if either part is empty
    if not local_part or not domain_part:
        raise ValueError('Local and domain parts cannot be empty.')
    
    # Ensure domain has at least one dot
    if '.' not in domain_part:
        raise ValueError('Domain must contain at least one dot.')
    
    # Return normalized email with case-sensitive local part and lowercase domain
    return f"{local_part}@{domain_part.lower()}"
