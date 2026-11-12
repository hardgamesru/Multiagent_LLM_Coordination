from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    result_gets = []
    
    for op in operations:
        if len(op) != 3 or op[0] not in ("put", "get"):
            continue
        
        key = op[1]
        if op[0] == "put":
            # Remove old entry if full and add new one
            if len(cache) >= capacity:
                cache.popitem(last=False)
            cache[key] = op[2]
        elif op[0] == "get":
            # Check if key exists and update order
            value = cache.get(key)
            if value is not None:
                del cache[key]
                cache[key] = value
            result_gets.append(value)
            
    # Reverse keys to maintain LRU order from least to most recent
    final_keys = list(reversed(list(cache.keys())))
    
    return {
        "gets": result_gets,
        "keys": final_keys
    }
