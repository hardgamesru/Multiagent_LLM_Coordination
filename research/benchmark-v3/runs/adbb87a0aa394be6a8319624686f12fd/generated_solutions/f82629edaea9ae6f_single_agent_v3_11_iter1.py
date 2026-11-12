def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def normalize(intervals: list[list[int]]) -> list[list[int]]:
        res = []
        for s, e in intervals:
            if s > e:
                raise ValueError("Reversed interval")
            if s == e:
                continue
            res.append([s, e])
        return res

    def merge(intervals: list[list[int]]) -> list[list[int]]:
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

    b = normalize(base)
    c = normalize(cuts)
    b = merge(b)
    c = merge(c)

    result = []
    j = 0
    for bs, be in b:
        cur = bs
        while j < len(c) and c[j][1] <= bs:
            j += 1
        k = j
        while k < len(c) and c[k][0] < be:
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
    return merge(result)
