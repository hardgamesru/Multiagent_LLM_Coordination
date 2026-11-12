from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    gets = []
    
    for op in operations:
        if op[0] == "put":
            # Удалить старый элемент, если уже заполнено
            if len(cache) >= capacity:
                cache.popitem(last=False)
            
            # Добавить новый элемент в начало
            cache[op[1]] = op[2]
        
        elif op[0] == "get":
            # Проверить наличие ключа и вернуть значение
            val = cache.get(op[1])
            if val is not None:
                # Обновить позицию ключа в кэше
                del cache[op[1]]
                cache[op[1]] = val
            
            # Запомнить результат операции
            gets.append(val)
    
    # Получить итоговый порядок ключей
    keys = list(cache.keys())
    
    return {
        "gets": gets,
        "keys": keys
    }
