def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals: list[list[int]]) -> list[list[int]]:
        norm = []
        for s, e in intervals:
            if s > e:
                raise ValueError("Reversed interval")
            if s < e:
                norm.append([s, e])
        if not norm:
            return []
        norm.sort(key=lambda x: (x[0], x[1]))
        merged = [norm[0][:]]
        for s, e in norm[1:]:
            last = merged[-1]
            if s <= last[1]:
                if e > last[1]:
                    last[1] = e
            else:
                merged.append([s, e])
        return merged

    b = normalize(base)
    c = normalize(cuts)
    if not b or not c:
        return b[:]

    result = []
    j = 0
    m = len(c)
    for s, e in b:
        cur = s
        while j < m and c[j][1] <= cur:
            j += 1
        k = j
        while k < m and c[k][0] < e:
            cs, ce = c[k]
            if cs > cur:
                result.append([cur, min(cs, e)])
            cur = max(cur, ce)
            if cur >= e:
                break
            k += 1
        if cur < e:
            result.append([cur, e])
        j = k

    if not result:
        return []
    out = [result[0][:]]
    for s, e in result[1:]:
        last = out[-1]
        if s <= last[1]:
            if e > last[1]:
                last[1] = e
        else:
            out.append([s, e])
    return out
