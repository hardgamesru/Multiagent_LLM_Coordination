from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations:
        if len(op) != 3 or op[0] not in ("put", "get"):
            continue
        
        key = op[1]
        if op[0] == "put":
            # Remove existing key if exists
            cache.pop(key, None)
            
            # Add new item and evict if full
            cache[key] = op[2]
            if len(cache) > capacity:
                cache.popitem(last=False)
                
        elif op[0] == "get":
            # Get value with side effect of moving key to front
            val = cache.get(key)
            gets.append(val)
            if val is not None:
                del cache[key]
                cache[key] = val
    
    # Final order from least to most recent
    keys = list(cache.keys())
    keys.reverse()
    
    return {"gets": gets, "keys": keys}
