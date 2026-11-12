from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity must be non-negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations:
        if op[0] == "put":
            key, val = op[1], op[2]
            
            # Remove old entry if exists
            if key in cache:
                del cache[key]
                
            # Add new entry or update existing one
            cache[key] = val
            
            # Evict LRU item if capacity exceeded
            if len(cache) > capacity:
                cache.popitem(last=False)
        
        elif op[0] == "get":
            key = op[1]
            
            # Get value with side effect of making it most recent
            value = cache.get(key)
            gets.append(value)
    
    # Reverse order to get least-recent to most-recent
    keys = list(reversed(list(cache.keys())))
    
    return {"gets": gets, "keys": keys}
