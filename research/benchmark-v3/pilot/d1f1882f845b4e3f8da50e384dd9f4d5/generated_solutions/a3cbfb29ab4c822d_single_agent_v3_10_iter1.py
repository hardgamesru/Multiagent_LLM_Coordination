from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    cache = OrderedDict()
    gets = []
    for op in operations:
        if op[0] == "put":
            _, key, value = op
            if capacity == 0:
                continue
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
        elif op[0] == "get":
            _, key = op
            if key in cache:
                cache.move_to_end(key)
                gets.append(cache[key])
            else:
                gets.append(None)
    return {"gets": gets, "keys": list(cache.keys())}
