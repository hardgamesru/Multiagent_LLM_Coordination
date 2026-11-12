from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    result_gets = []
    
    for op in operations:
        if op[0] == "put":
            # Remove oldest item if cache is full
            if len(cache) >= capacity:
                cache.popitem(last=False)
            
            # Add new entry as most recent
            cache[op[1]] = op[2]
        
        elif op[0] == "get":
            # Get value and mark it as most recent
            value = cache.get(op[1])
            if value is not None:
                del cache[op[1]]
                cache[op[1]] = value
            
            result_gets.append(value)
    
    # Final order of keys from least to most recent
    keys = list(reversed(list(cache.keys())))
    
    return {
        "gets": result_gets,
        "keys": keys
    }
