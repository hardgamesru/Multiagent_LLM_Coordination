from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    result = {"gets": [], "keys": []}
    
    for op in operations:
        if op[0] == "put":
            # Удалить старый элемент, если достигнута емкость
            if len(cache) >= capacity:
                cache.popitem(last=False)
            
            # Добавить новый элемент в начало очереди
            cache[op[1]] = op[2]
        
        elif op[0] == "get":
            # Проверить наличие ключа и обновить порядок доступа
            value = cache.get(op[1])
            if value is not None:
                del cache[op[1]]
                cache[op[1]] = value
                result["gets"].append(value)
            else:
                result["gets"].append(None)
    
    # Сохранить финальные ключи в порядке LRU-MRU
    result["keys"] = list(cache.keys())
    
    return result
