def apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]:
    if not hunks:
        return list(lines)
    result = list(lines)
    offset = 0
    prev_end = -1
    for h in hunks:
        if not (isinstance(h, list) and len(h) == 3):
            raise ValueError
        start, old, new = h
        if not isinstance(start, int) or not isinstance(old, list) or not isinstance(new, list):
            raise ValueError
        if start < 0 or start + len(old) > len(lines):
            raise ValueError
        if lines[start:start+len(old)] != old:
            raise ValueError
        if start < prev_end:
            raise ValueError
        prev_end = start + len(old)
        result[offset + start:offset + start + len(old)] = new
        offset += len(new) - len(old)
    return result
