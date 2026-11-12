def normalize_path(path: str) -> str:
    if not path.startswith('/') or len(path) == 0:
        raise ValueError('Invalid path')
    
    # Split into segments while skipping empty parts from double slashes
    segments = filter(None, path.split('/'))
    
    # Stack to track directory levels
    stack = []
    
    for seg in segments:
        if seg == '..':
            # Go up one level unless already at root
            if stack: stack.pop()
        elif seg != '.':
            # Add valid non-empty segments
            stack.append(seg)
            
    return '/' + '/'.join(stack)
