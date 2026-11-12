def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must be absolute")
    
    # Преобразуем путь в список сегментов
    segments = path.split('/')
    
    # Создаем пустой стек для хранения нормализованных сегментов
    stack = []
    
    # Обрабатываем каждый сегмент
    for seg in segments:
        # Пропускаем пустые сегменты (результат split())
        if not seg:
            continue
        
        # Для ".." перемещаемся вверх, но не выше корня
        if seg == '..':
            if len(stack) > 0:
                stack.pop()
        else:
            # Добавляем остальные сегменты в стек
            stack.append(seg)
    
    # Собираем нормализованный путь обратно в строку
    return '/' + '/'.join(stack)
