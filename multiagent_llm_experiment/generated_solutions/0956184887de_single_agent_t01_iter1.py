def normalize_email(email: str) -> str:
    email = email.strip()
    
    if '@' not in email or email.count('@') > 1:
        raise ValueError('Invalid email format')
        
    local_part, domain_part = email.split('@', 1)
    
    if '.' not in domain_part or len(local_part) == 0 or len(domain_part) == 0:
        raise ValueError('Invalid email format')
        
    return f"{local_part}@{domain_part.lower()}"
