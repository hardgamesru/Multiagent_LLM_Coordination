def apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]:
    if not isinstance(lines, list) or not all(isinstance(l, str) for l in lines):
        raise ValueError("lines must be a list of strings")
    if not isinstance(hunks, list):
        raise ValueError("hunks must be a list")

    result = list(lines)
    offset = 0
    prev_end = 0

    for hunk in hunks:
        if not (isinstance(hunk, list) and len(hunk) == 3):
            raise ValueError("Each hunk must be a list of [start, old, new]")
        start, old, new = hunk
        if not isinstance(start, int):
            raise ValueError("start must be an integer")
        if not isinstance(old, list) or not all(isinstance(l, str) for l in old):
            raise ValueError("old must be a list of strings")
        if not isinstance(new, list) or not all(isinstance(l, str) for l in new):
            raise ValueError("new must be a list of strings")

        if start < 0 or start > len(lines):
            raise ValueError("start out of bounds")
        if start + len(old) > len(lines):
            raise ValueError("old range out of bounds")
        if lines[start:start+len(old)] != old:
            raise ValueError("old lines do not match")
        if start < prev_end:
            raise ValueError("hunks overlap or are not in order")

        actual_start = start + offset
        result[actual_start:actual_start+len(old)] = new
        offset += len(new) - len(old)
        prev_end = start + len(old)

    return result
