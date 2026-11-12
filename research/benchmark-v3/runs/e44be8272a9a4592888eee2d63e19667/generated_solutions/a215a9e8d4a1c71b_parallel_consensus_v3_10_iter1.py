from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity must be non-negative")
    
    cache = OrderedDict()
    gets_result = []
    
    for op in operations:
        if len(op) != 3 or op[0] not in ("put", "get"):
            continue
        
        key = op[1]
        if op[0] == "put":
            # Remove existing key if exists and add new one
            cache.pop(key, None)
            cache[key] = op[2]
            
            # If over capacity, evict least-recently used item
            if len(cache) > capacity:
                cache.popitem(last=False)
                
        elif op[0] == "get":
            # Get value and update order of access
            value = cache.get(key)
            if value is not None:
                del cache[key]
                cache[key] = value
            gets_result.append(value)
    
    # Return keys in reverse order (most recent first)
    return {
        "gets": gets_result,
        "keys": list(reversed(list(cache.keys())))
    }
