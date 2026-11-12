from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations:
        if op[0] == "put":
            # Удалить старый элемент, если ключ уже есть
            cache.pop(op[1], None)
            
            # Добавить новый элемент или обновить существующий
            cache[op[1]] = op[2]
            
            # Очистить устаревшие элементы при переполнении
            if len(cache) > capacity:
                cache.popitem(last=False)
        
        elif op[0] == "get":
            # Получить значение или None при отсутствии ключа
            value = cache.get(op[1])
            gets.append(value)
    
    # Вернуть ключи в порядке от менее до наиболее недавних
    keys = list(cache.keys())
    
    return {
        "gets": gets,
        "keys": keys
    }
