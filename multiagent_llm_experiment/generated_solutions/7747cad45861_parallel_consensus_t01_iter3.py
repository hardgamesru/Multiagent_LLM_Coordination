def normalize_email(email: str) -> str:
    # Remove any surrounding white space from the email
    email = email.strip()
    
    # Split into local and domain parts using '@'
    parts = email.split('@')
    
    # Check that there is exactly one '@' symbol
    if len(parts) != 2:
        raise ValueError('Email must have exactly one "@".')
        
    # Extract local and domain parts
    local_part, domain_part = parts
    
    # Ensure neither the local nor domain part is empty
    if not local_part or not domain_part:
        raise ValueError('Local and domain parts cannot be empty.')
    
    # Convert the domain part to lowercase
    normalized_domain = domain_part.lower()
    
    # Verify that the domain contains at least one '.'
    if '.' not in normalized_domain:
        raise ValueError('Domain must contain a dot.')
    
    return f"{local_part}@{normalized_domain}"
