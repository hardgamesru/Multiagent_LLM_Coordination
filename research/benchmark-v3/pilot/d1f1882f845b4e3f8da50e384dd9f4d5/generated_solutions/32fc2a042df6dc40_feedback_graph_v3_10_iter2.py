from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    result_gets = []
    
    for op in operations:
        if op[0] == "put":
            # Удалить старый элемент, если уже есть место под новый
            if len(cache) >= capacity and capacity > 0:
                cache.popitem(last=False)
            
            # Добавить новый элемент в начало очереди
            cache[op[1]] = op[2]
        
        elif op[0] == "get":
            # Проверить наличие ключа и вернуть значение или None
            value = cache.get(op[1])
            if value is not None:
                # Обновить позицию ключа в очереди
                del cache[op[1]]
                cache[op[1]] = value
            
            result_gets.append(value)
    
    # Получить итоговый порядок ключей от менее до более свежих
    keys = list(cache.keys())
    
    return {
        "gets": result_gets,
        "keys": keys
    }
