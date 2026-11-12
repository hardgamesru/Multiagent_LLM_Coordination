from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    current_keys = []
    
    for op in operations[:1000]:
        if len(cache) > capacity and capacity > 0:
            # Remove least recently used item when full
            cache.popitem(last=False)
        
        if op[0] == "put":
            # Update/insert key with new value and move it to front of order
            cache[op[1]] = op[2]
            current_keys.append(op[1])
        elif op[0] == "get":
            # Get value and update its position as most recent
            value = cache.get(op[1])
            if value is not None:
                gets.append(value)
                del cache[op[1]]
                cache[op[1]] = value
                current_keys.remove(op[1])
                current_keys.append(op[1])
            else:
                gets.append(None)
    
    # Return keys from least to most recent
    current_keys.reverse()
    return {
        "gets": gets,
        "keys": current_keys
    }
