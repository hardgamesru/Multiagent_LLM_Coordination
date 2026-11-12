def apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]:
    if not hunks:
        return list(lines)

    result = list(lines)
    offset = 0
    prev_end = -1

    for hunk in hunks:
        if not (isinstance(hunk, list) and len(hunk) == 3):
            raise ValueError("Invalid hunk format")
        start, old, new = hunk
        if not isinstance(start, int) or not isinstance(old, list) or not isinstance(new, list):
            raise ValueError("Invalid hunk types")

        if start < 0 or start + len(old) > len(lines):
            raise ValueError("Hunk out of bounds")
        if start < prev_end:
            raise ValueError("Overlapping hunks")

        orig_start = start
        orig_end = start + len(old)

        if lines[orig_start:orig_end] != old:
            raise ValueError("Old lines do not match")

        result[orig_start + offset : orig_end + offset] = new

        offset += len(new) - len(old)
        prev_end = orig_end

    return result
