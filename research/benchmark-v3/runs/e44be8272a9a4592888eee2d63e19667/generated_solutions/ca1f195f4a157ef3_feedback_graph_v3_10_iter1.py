from collections import OrderedDict
from typing import Any, Dict, List, Optional

def lru_trace(capacity: int, operations: List[List[Any]]) -> Dict[str, Any]:
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    gets: List[Optional[int]] = []
    cache: OrderedDict[str, int] = OrderedDict()
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
            if capacity == 0:
                continue
            key, value = op[1], op[2]
            if key in cache:
                cache.pop(key)
            elif len(cache) >= capacity:
                cache.popitem(last=False)
            cache[key] = value
    return {"gets": gets, "keys": list(cache.keys())}
