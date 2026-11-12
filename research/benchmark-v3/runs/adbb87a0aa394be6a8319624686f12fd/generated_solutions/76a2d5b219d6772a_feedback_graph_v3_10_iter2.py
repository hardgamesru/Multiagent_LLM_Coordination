from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations:
        if op[0] == "put":
            # Удалить старое значение, если есть место
            if len(cache) >= capacity:
                cache.popitem(last=True)
            
            # Добавить новое значение и сделать его самым свежим
            cache[op[1]] = op[2]
        
        elif op[0] == "get":
            # Проверить наличие ключа и обновить его позицию
            if op[1] in cache:
                value = cache.get(op[1])
                del cache[op[1]]
                cache[op[1]] = value
                gets.append(value)
            else:
                gets.append(None)
    
    # Получить финальные ключи в порядке LRU-MRU
    keys = list(cache.keys())
    
    return {
        "gets": gets,
        "keys": keys
    }
