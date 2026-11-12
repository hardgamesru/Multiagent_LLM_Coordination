def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must be an absolute path")
    
    segments = path.split('/')
    result = []
    
    for seg in segments:
        # Skip empty segments caused by consecutive '/'
        if seg == '':
            continue
        
        # Handle ".." segment
        elif seg == '..':
            if result:
                result.pop()
            else:
                # Cannot go above root
                pass
        else:
            # Keep all other segments as is
            result.append(seg)
            
    return '/' + '/'.join(result)
