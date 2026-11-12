import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if not pattern:
        return []
    
    # Создаем регулярное выражение, экранируя литералы и интерпретируя маски
    regex_pattern = re.escape(pattern)
    regex_pattern = regex_pattern.replace('\\*', '.*').replace('\\?', '.')
    
    # Проверяем соответствие каждого слова шаблону
    return [word for word in words if re.fullmatch(regex_pattern, word)]
