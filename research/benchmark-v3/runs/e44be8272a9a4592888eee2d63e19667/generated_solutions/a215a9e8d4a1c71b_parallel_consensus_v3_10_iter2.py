from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    result_gets = []
    current_keys = []

    def update_cache(key):
        # Remove from old position
        del cache[key]
        # Add as most recent
        cache[key] = None
        
    for op in operations:
        if len(op) != 3:
            continue
            
        cmd, k, v = op
        if cmd == "put":
            if k in cache:
                # Update existing entry
                update_cache(k)
                cache[k] = v
            else:
                # Full cache, evict least recent
                if len(cache) >= capacity:
                    least_recent = next(iter(cache))
                    del cache[least_recent]
                    
                # Insert new item
                cache[k] = v
                
            # Maintain order of keys
            current_keys.append(k)
            
        elif cmd == "get":
            if k in cache:
                # Get value and mark as most recent
                val = cache.pop(k)
                cache[k] = val
                result_gets.append(val)
            else:
                # Key not found
                result_gets.append(None)
    
    # Final keys ordered from least to most recent
    final_keys = list(reversed(list(cache.keys())))
    
    return {
        "gets": result_gets,
        "keys": final_keys
    }
