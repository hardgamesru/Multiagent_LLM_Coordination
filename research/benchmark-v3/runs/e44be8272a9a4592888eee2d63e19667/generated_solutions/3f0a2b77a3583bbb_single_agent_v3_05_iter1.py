def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must be absolute")
    
    segments = path.split('/')
    normalized = []
    
    for seg in segments:
        # Skip empty segments caused by consecutive /
        if seg == '':
            continue
        
        # Handle current directory .
        if seg == '.':
            continue
            
        # Handle parent directory ..
        elif seg == '..':
            if normalized and normalized[-1] != '..':
                normalized.pop()
            else:
                normalized.append('..')
        else:
            normalized.append(seg)
    
    # If last segment is .. and no previous valid segment exists
    if len(normalized) > 0 and normalized[-1] == '..' and len(normalized) == 1:
        normalized.append('.')
    
    return '/' + '/'.join(normalized)
