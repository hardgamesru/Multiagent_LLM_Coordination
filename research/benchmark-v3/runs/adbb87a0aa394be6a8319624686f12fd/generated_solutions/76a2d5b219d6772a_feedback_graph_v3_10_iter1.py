from collections import OrderedDict

def lru_trace(capacity: int, operations: list[list]) -> dict:
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    
    cache = OrderedDict()
    result_gets = []
    
    def evict_least_recent():
        if cache:
            # Удалить наименее недавно использованный элемент
            k = next(iter(cache))
            del cache[k]
            
    for op in operations:
        if op[0] == "put":
            key, value = op[1], op[2]
            if len(cache) >= capacity:
                evict_least_recent()
            cache[key] = value  # Обновляем или добавляем ключ
        elif op[0] == "get":
            key = op[1]
            if key in cache:
                # Перемещаем ключ в начало (наиболее свежий)
                val = cache.pop(key)
                cache[key] = val
                result_gets.append(val)
            else:
                result_gets.append(None)
    
    # Возвращаем ключи в порядке от менее свежих к более свежим
    keys_list = list(reversed(list(cache.keys())))
    
    return {
        "gets": result_gets,
        "keys": keys_list
    }
