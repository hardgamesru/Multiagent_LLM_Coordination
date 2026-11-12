from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations:
        if op[0] == "put":
            key, value = op[1], op[2]
            
            # Удалить старый элемент, если есть
            if key in cache:
                del cache[key]
                
            # Добавить новый элемент или обновить существующий
            cache[key] = value
            
            # Убрать наименее используемый элемент при переполнении
            if len(cache) > capacity:
                cache.popitem(last=True)
        
        elif op[0] == "get":
            key = op[1]
            
            # Получить значение или None, переместить ключ в начало
            val = cache.get(key)
            if val is not None:
                gets.append(val)
                cache.move_to_end(key)
            else:
                gets.append(None)
    
    # Вернуть ключи в порядке от менее до наиболее недавних
    keys = list(cache.keys())
    keys.reverse()
    
    return {
        "gets": gets,
        "keys": keys
    }
