def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Path must start with '/'")
    
    # Разбиваем путь на компоненты, игнорируя пустые части из-за последовательных слешей
    parts = filter(None, path.split('/'))
    
    # Создаем стек для хранения нормализованных путей
    stack = []
    
    # Обрабатываем каждый сегмент пути
    for part in parts:
        if part == '..':
            # Переходим вверх по уровню, если возможно
            if stack:
                stack.pop()
        elif part != '.':
            # Добавляем остальные сегменты в стек
            stack.append(part)
    
    # Собираем результат, используя корневой символ '/'
    return '/' + '/'.join(stack)
