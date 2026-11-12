def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals: list[list[int]]) -> list[list[int]]:
        res = []
        for s, e in intervals:
            if s >= e:
                raise ValueError("Invalid interval")
            res.append([s, e])
        if not res:
            return []
        res.sort(key=lambda x: x[0])
        merged = [res[0][:]]
        for s, e in res[1:]:
            if s <= merged[-1][1]:
                if e > merged[-1][1]:
                    merged[-1][1] = e
            else:
                merged.append([s, e])
        return merged

    base_n = normalize([iv[:] for iv in base])
    cuts_n = normalize([iv[:] for iv in cuts])

    result = []
    j = 0
    for b_start, b_end in base_n:
        cur = b_start
        while j < len(cuts_n) and cuts_n[j][1] <= cur:
            j += 1
        k = j
        while k < len(cuts_n) and cuts_n[k][0] < b_end:
            c_start, c_end = cuts_n[k]
            if c_start > cur:
                result.append([cur, min(c_start, b_end)])
            cur = max(cur, c_end)
            if cur >= b_end:
                break
            k += 1
        j = k
        if cur < b_end:
            result.append([cur, b_end])

    if not result:
        return []
    out = [result[0][:]]
    for s, e in result[1:]:
        if s <= out[-1][1]:
            if e > out[-1][1]:
                out[-1][1] = e
        else:
            out.append([s, e])
    return out
