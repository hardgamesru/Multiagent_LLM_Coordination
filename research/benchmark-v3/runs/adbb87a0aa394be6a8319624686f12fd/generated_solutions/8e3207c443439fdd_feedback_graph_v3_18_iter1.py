def apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]:
    if not isinstance(lines, list) or not all(isinstance(l, str) for l in lines):
        raise ValueError("Invalid lines type")
    if not isinstance(hunks, list):
        raise ValueError("Invalid hunks type")

    result = list(lines)
    offset = 0
    prev_end = 0

    for h in hunks:
        if not (isinstance(h, list) and len(h) == 3):
            raise ValueError("Invalid hunk structure")
        start, old, new = h
        if not isinstance(start, int) or not isinstance(old, list) or not isinstance(new, list):
            raise ValueError("Invalid hunk types")
        if not all(isinstance(l, str) for l in old) or not all(isisinstance(l, str) for l in new):
            raise ValueError("Invalid old/new types")

        orig_start = start
        orig_end = start + len(old)

        if orig_start < 0 or orig_end > len(lines):
            raise ValueError("Hunk out of bounds")
        if lines[orig_start:orig_end] != old:
            raise ValueError("Old lines do not match")
        if orig_start < prev_end:
            raise ValueError("Hunks overlap or are out of order")

        current_start = orig_start + offset
        result[current_start:current_start + len(old)] = new
        offset += len(new) - len(old)
        prev_end = orig_end

    return result
