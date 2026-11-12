def normalize_path(path: str) -> str:
    if not path.startswith('/') or len(path) == 0:
        raise ValueError("Invalid absolute path")
    
    segments = path.split('/')
    result = []
    
    for seg in segments:
        # Skip empty segments caused by consecutive slashes
        if seg == '':
            continue
        
        # Handle current directory
        if seg == '.':
            continue
            
        # Handle parent directory
        if seg == '..':
            if result:
                result.pop()
            else:
                # Cannot go beyond root
                pass
        else:
            result.append(seg)
    
    return '/' + '/'.join(result)
