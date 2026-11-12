def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must be absolute")
    
    segments = path.split('/')
    result = []
    
    for seg in segments:
        # Skip empty segments caused by consecutive '/'
        if seg == '':
            continue
        
        # Handle ".." segment
        if seg == '..':
            if result:
                result.pop()
        else:
            # Keep all other segments as is
            result.append(seg)
            
    return '/' + '/'.join(result)
