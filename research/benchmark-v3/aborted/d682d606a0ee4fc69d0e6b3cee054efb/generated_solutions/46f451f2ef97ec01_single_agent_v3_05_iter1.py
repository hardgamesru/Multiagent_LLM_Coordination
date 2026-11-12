def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must be absolute")
    
    # Split path into components, skipping empty parts caused by double slashes
    components = [c for c in path.split('/') if c]
    
    normalized = []
    for comp in components:
        if comp == '..':
            # Go up one level unless already at root
            if len(normalized) > 0:
                normalized.pop()
        elif comp != '.':
            # Keep non-empty, non-current directory segments
            normalized.append(comp)
    
    # Join back with single slashes
    return '/' + '/'.join(normalized)
