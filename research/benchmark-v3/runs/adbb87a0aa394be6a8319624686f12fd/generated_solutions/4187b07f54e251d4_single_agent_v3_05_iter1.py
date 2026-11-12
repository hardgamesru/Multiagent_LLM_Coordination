def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must start with '/'")
    
    # Split path into components, excluding empty parts caused by consecutive '/'
    components = filter(None, path.split('/'))
    
    normalized = []
    
    for comp in components:
        if comp == '.':
            continue
        elif comp == '..' and len(normalized) > 0:
            normalized.pop()
        else:
            normalized.append(comp)
            
    return '/' + '/'.join(normalized)
