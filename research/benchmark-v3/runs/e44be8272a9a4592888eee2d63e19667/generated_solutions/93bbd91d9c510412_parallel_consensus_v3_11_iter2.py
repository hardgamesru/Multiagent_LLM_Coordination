def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals: list[list[int]]) -> list[list[int]]:
        res: list[list[int]] = []
        for s, e in intervals:
            if s > e:
                raise ValueError("Reversed interval")
            if s < e:
                res.append([s, e])
        if not res:
            return []
        res.sort(key=lambda x: (x[0], x[1]))
        merged: list[list[int]] = []
        cur_s, cur_e = res[0]
        for s, e in res[1:]:
            if s <= cur_e:
                if e > cur_e:
                    cur_e = e
            else:
                merged.append([cur_s, cur_e])
                cur_s, cur_e = s, e
        merged.append([cur_s, cur_e])
        return merged

    B = normalize(base)
    C = normalize(cuts)
    if not B or not C:
        return B.copy()

    result: list[list[int]] = []
    j = 0
    m = len(C)
    for b_s, b_e in B:
        cur = b_s
        while j < m and C[j][1] <= b_s:
            j += 1
        k = j
        while k < m and C[k][0] < b_e:
            c_s, c_e = C[k]
            if c_s > cur:
                result.append([cur, min(c_s, b_e)])
            cur = max(cur, c_e)
            if cur >= b_e:
                break
            k += 1
        if cur < b_e:
            result.append([cur, b_e])
        j = k

    if not result:
        return []

    final: list[list[int]] = []
    cur_s, cur_e = result[0]
    for s, e in result[1:]:
        if s <= cur_e:
            if e > cur_e:
                cur_e = e
        else:
            final.append([cur_s, cur_e])
            cur_s, cur_e = s, e
    final.append([cur_s, cur_e])
    return final
