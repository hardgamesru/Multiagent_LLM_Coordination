def apply_patch_lines(lines, hunks):
    result = list(lines)
    offset = 0
    prev_end = 0
    for start, old, new in hunks:
        if not isinstance(start, int) or start < 0 or start + len(old) > len(lines):
            raise ValueError
        if start < prev_end:
            raise ValueError
        if lines[start:start+len(old)] != old:
            raise ValueError
        abs_start = start + offset
        result[abs_start:abs_start+len(old)] = new
        offset += len(new) - len(old)
        prev_end = start + len(old)
    return result
