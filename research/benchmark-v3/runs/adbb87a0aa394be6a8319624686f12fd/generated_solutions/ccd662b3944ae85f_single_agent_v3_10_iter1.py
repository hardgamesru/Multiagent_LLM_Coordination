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
                
            # Add new entry, evicting least-recent if full
            cache[key] = val
            if len(cache) > capacity:
                cache.popitem(last=False)
        
        elif op[0] == "get":
            key = op[1]
            
            # Get value with side effect of making it most recent
            value = cache.get(key)
            if value is not None:
                gets.append(value)
                cache.move_to_end(key)
            else:
                gets.append(None)
    
    # Keys ordered from least to most recent
    keys = list(cache.keys())
    
    return {"gets": gets, "keys": keys}
