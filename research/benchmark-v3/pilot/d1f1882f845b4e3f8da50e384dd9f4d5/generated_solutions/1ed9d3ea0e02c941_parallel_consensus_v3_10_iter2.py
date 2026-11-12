def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    from collections import OrderedDict
    cache = OrderedDict()
    gets = []
    for op in operations:
        if op[0] == "get":
            key = op[1]
            if key in cache:
                value = cache.pop(key)
                cache[key] = value
                gets.append(value)
            else:
                gets.append(None)
        elif op[0] == "put":
            key, value = op[1], op[2]
            if capacity == 0:
                continue
            if key in cache:
                cache.pop(key)
            elif len(cache) >= capacity:
                cache.popitem(last=False)
            cache[key] = value
    return {"gets": gets, "keys": list(cache.keys())}
