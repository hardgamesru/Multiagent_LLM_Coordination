def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals: list[list[int]]) -> list[tuple[int, int]]:
        res = []
        for s, e in intervals:
            if s > e:
                raise ValueError("Reversed interval")
            if s < e:
                res.append((s, e))
        return res

    def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if not intervals:
            return []
        intervals = sorted(intervals)
        merged = [intervals[0]]
        for s, e in intervals[1:]:
            ps, pe = merged[-1]
            if s <= pe:
                if e > pe:
                    merged[-1][1] = e
            else:
                merged.append([s, e])
        return merged

    b = merge([list(x) for x in normalize(base)])
    c = merge([list(x) for x in normalize(cuts)])

    result = []
    j = 0
    m = len(c)
    for bs, be in b:
        cur = bs
        while j < m and c[j][1] <= cur:
            j += 1
        k = j
        while k < m and c[k][0] < be:
            cs, ce = c[k]
            if cs > cur:
                result.append([cur, min(cs, be)])
            cur = max(cur, ce)
            if cur >= be:
                break
            k += 1
        if cur < be:
            result.append([cur, be])
        j = k

    if not result:
        return []

    final = [result[0]]
    for s, e in result[1:]:
        ps, pe = final[-1]
        if s <= pe:
            if e > pe:
                final[-1][1] = e
        else:
            final.append([s, e])
    return final
