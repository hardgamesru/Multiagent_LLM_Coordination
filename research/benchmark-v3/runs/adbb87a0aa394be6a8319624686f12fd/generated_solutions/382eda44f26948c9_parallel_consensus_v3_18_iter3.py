def apply_patch_lines(lines, hunks):
    if not hunks:
        return list(lines)
    result = []
    prev_end = 0
    for h in hunks:
        if not (isinstance(h, (list, tuple)) and len(h) == 3):
            raise ValueError
        start, old, new = h
        if not isinstance(start, int) or not (0 <= start <= len(lines)):
            raise ValueError
        if not isinstance(old, list) or not isinstance(new, list):
            raise ValueError
        if start < prev_end:
            raise ValueError
        if start + len(old) > len(lines):
            raise ValueError
        if lines[start:start+len(old)] != old:
            raise ValueError
        result.extend(lines[prev_end:start])
        result.extend(new)
        prev_end = start + len(old)
    result.extend(lines[prev_end:])
    return result
