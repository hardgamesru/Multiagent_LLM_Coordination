def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must be absolute")
    parts = path.split('/')
    stack = []
    for part in parts:
        if part == '' or part == '.':
            continue
        if part == '..':
            if stack:
                stack.pop()
            continue
        stack.append(part)
    return '/' + '/'.join(stack) if stack else '/'
