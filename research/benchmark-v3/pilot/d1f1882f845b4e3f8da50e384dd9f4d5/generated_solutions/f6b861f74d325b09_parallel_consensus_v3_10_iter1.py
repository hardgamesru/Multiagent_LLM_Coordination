from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations[:1000]:
        if len(cache) == capacity and op[0] != "put":
            # Remove least recently used item when full and non-put operation
            cache.popitem(last=False)
        
        if op[0] == "put":
            # Update or add key with value, making it most recent
            cache[op[1]] = op[2]
        elif op[0] == "get":
            # Get value and mark as most recent
            value = cache.get(op[1])
            gets.append(value)
            if value is not None:
                del cache[op[1]]
                cache[op[1]] = value
    
    # Reverse order to get from least to most recent
    keys = list(reversed(list(cache.keys())))
    
    return {
        "gets": gets,
        "keys": keys
    }
