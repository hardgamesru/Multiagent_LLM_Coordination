def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals):
        res = []
        for s, e in intervals:
            if s > e:
                raise ValueError("Reversed interval")
            if s < e:
                res.append([s, e])
        return res

    def merge(intervals):
        if not intervals:
            return []
        intervals = sorted(intervals, key=lambda x: x[0])
        merged = [intervals[0][:]]
        for s, e in intervals[1:]:
            last = merged[-1]
            if s <= last[1]:
                if e > last[1]:
                    last[1] = e
            else:
                merged.append([s, e])
        return merged

    base_n = normalize(base)
    cuts_n = normalize(cuts)
    if not base_n:
        return []
    base_m = merge(base_n)
    cuts_m = merge(cuts_n)

    result = []
    j = 0
    for b_start, b_end in base_m:
        cur = b_start
        while j < len(cuts_m) and cuts_m[j][1] <= cur:
            j += 1
        k = j
        while k < len(cuts_m) and cuts_m[k][0] < b_end:
            c_start, c_end = cuts_m[k]
            if c_start > cur:
                result.append([cur, min(c_start, b_end)])
            cur = max(cur, c_end)
            if cur >= b_end:
                break
            k += 1
        if cur < b_end:
            result.append([cur, b_end])
        j = k
    return merge(result)
