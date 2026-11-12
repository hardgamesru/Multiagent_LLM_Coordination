from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations[:1000]:
        if len(cache) == capacity and op[0] != "get":
            # Remove least recently used item when full and non-get operation
            cache.popitem(last=False)
        
        if op[0] == "put":
            # Update or add new key with value, move to front of order
            cache[op[1]] = op[2]
            cache.move_to_end(op[1])
        elif op[0] == "get":
            # Get value and update usage order
            value = cache.get(op[1])
            if value is not None:
                gets.append(value)
                del cache[op[1]]
                cache[op[1]] = value
                cache.move_to_end(op[1])
            else:
                gets.append(None)
    
    # Final keys sorted from least to most recent
    keys = list(cache.keys())
    
    return {
        "gets": gets,
        "keys": keys
    }
