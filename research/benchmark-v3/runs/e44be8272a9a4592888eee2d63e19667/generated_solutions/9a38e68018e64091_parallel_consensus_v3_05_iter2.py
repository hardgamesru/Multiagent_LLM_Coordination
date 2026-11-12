def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must start with '/'")
    
    # Split path into components, skipping empty parts caused by consecutive '/'
    components = filter(None, path.split('/'))
    
    # Stack to track directory levels
    stack = []
    
    for comp in components:
        if comp == '..':
            # Move up one level unless already at root
            if stack:
                stack.pop()
        elif comp != '.':
            # Add valid component to stack
            stack.append(comp)
            
    # Join components back together with single slashes
    return '/' + '/'.join(stack)
