from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets_result = []
    
    for op in operations:
        if len(op) == 3 and op[0] == "put":
            # Put operation: update or add key with value
            key, val = op[1], op[2]
            
            if key in cache:
                del cache[key]
                
            cache[key] = val
            
            # Remove least recently used item if cache is full
            if len(cache) > capacity:
                cache.popitem(last=False)
        
        elif len(op) == 2 and op[0] == "get":
            # Get operation: retrieve value or None if missing
            key = op[1]
            
            if key in cache:
                # Move accessed key to front of ordered cache
                value = cache.pop(key)
                cache[key] = value
                
            else:
                value = None
                
            gets_result.append(value)
    
    # Final order from least to most recent access
    keys_list = list(cache.keys())
    
    return {
        "gets": gets_result,
        "keys": keys_list
    }
