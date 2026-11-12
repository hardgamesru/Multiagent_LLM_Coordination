def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals: list[list[int]]) -> list[list[int]]:
        res = []
        for s, e in intervals:
            if s >= e:
                raise ValueError
            res.append([s, e])
        if not res:
            return []
        res.sort(key=lambda x: (x[0], x[1]))
        merged = [res[0][:]]
        for s, e in res[1:]:
            last = merged[-1]
            if s <= last[1]:
                if e > last[1]:
                    last[1] = e
            else:
                merged.append([s, e])
        return merged

    A = normalize(base)
    B = normalize(cuts)

    result = []
    j = 0
    for a_start, a_end in A:
        cur = a_start
        while j < len(B) and B[j][1] <= cur:
            j += 1
        k = j
        while k < len(B) and B[k][0] < a_end:
            b_start, b_end = B[k]
            if b_start > cur:
                result.append([cur, min(b_start, a_end)])
            cur = max(cur, b_end)
            if cur >= a_end:
                break
            k += 1
        if cur < a_end:
            result.append([cur, a_end])
        j = k

    if not result:
        return []

    merged = [result[0][:]]
    for s, e in result[1:]:
        last = merged[-1]
        if s <= last[1]:
            if e > last[1]:
                last[1] = e
        else:
            merged.append([s, e])

    return [iv for iv in merged if iv[0] < iv[1]]
