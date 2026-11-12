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
            # Remove existing entry to prevent duplication
            cache.pop(key, None)
            
            # Check if adding would exceed capacity
            if len(cache) >= capacity:
                # Pop least recently used item if full
                cache.popitem(last=False)
                
            # Add new item
            cache[key] = op[2]
        else:  # op[0] == "get"
            value = cache.get(key)
            # If found, move to front of ordered cache
            if value is not None:
                del cache[key]
                cache[key] = value
            
            gets.append(value)
    
    # Return keys in order from least to most recent
    keys = list(cache.keys())
    
    return {
        "gets": gets,
        "keys": keys
    }
