def window_minima(values: list[int], width: int) -> list[int]:
    n = len(values)
    if width < 1 or width > n:
        raise ValueError
    from collections import deque
    dq = deque()
    res = []
    for i, x in enumerate(values):
        while dq and values[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - width:
            dq.popleft()
        if i >= width - 1:
            res.append(values[dq[0]])
    return res
