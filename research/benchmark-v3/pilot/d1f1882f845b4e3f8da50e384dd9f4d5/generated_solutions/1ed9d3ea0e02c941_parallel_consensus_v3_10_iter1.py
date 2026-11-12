def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError
    from collections import OrderedDict
    cache = OrderedDict()
    gets = []
    for op in operations:
        if op[0] == "get":
            k = op[1]
            if k in cache:
                v = cache.pop(k)
                cache[k] = v
                gets.append(v)
            else:
                gets.append(None)
        elif op[0] == "put":
            k, v = op[1], op[2]
            if capacity == 0:
                continue
            if k in cache:
                cache.pop(k)
            elif len(cache) >= capacity:
                cache.popitem(last=False)
            cache[k] = v
    return {"gets": gets, "keys": list(cache.keys())}
