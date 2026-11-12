def apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]:
    result = list(lines)
    offset = 0
    prev_end = 0
    for start, old, new in hunks:
        if not isinstance(start, int) or start < 0 or start + len(old) > len(lines):
            raise ValueError
        if start < prev_end:
            raise ValueError
        orig_start = start
        orig_end = start + len(old)
        if lines[orig_start:orig_end] != old:
            raise ValueError
        res_start = orig_start + offset
        res_end = orig_end + offset
        result[res_start:res_end] = new
        offset += len(new) - len(old)
        prev_end = orig_end
    return result
