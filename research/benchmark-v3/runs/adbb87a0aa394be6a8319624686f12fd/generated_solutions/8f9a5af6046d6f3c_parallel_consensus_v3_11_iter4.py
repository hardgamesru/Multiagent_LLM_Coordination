def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def validate_and_filter(intervals):
        res = []
        for s, e in intervals:
            if s > e:
                raise ValueError("Reversed interval")
            if s < e:
                res.append([s, e])
        return res

    b = validate_and_filter(base)
    c = validate_and_filter(cuts)
    if not b:
        return []
    b.sort(key=lambda x: x[0])
    c.sort(key=lambda x: x[0])

    # Merge base intervals
    merged_base = []
    for s, e in b:
        if not merged_base or s > merged_base[-1][1]:
            merged_base.append([s, e])
        else:
            merged_base[-1][1] = max(merged_base[-1][1], e)

    # Subtract cuts
    result = []
    cut_idx = 0
    n_cuts = len(c)
    for s, e in merged_base:
        cur = s
        while cur < e and cut_idx < n_cuts:
            cs, ce = c[cut_idx]
            if ce <= cur:
                cut_idx += 1
                continue
            if cs >= e:
                break
            if cs > cur:
                result.append([cur, min(cs, e)])
            cur = max(cur, ce)
            if cur >= e:
                break
            if cs < e:
                cut_idx += 1
        if cur < e:
            result.append([cur, e])

    # Merge touching intervals in result
    if not result:
        return []
    merged_result = [result[0][:]]
    for s, e in result[1:]:
        if s == merged_result[-1][1]:
            merged_result[-1][1] = e
        else:
            merged_result.append([s, e])
    return merged_result
