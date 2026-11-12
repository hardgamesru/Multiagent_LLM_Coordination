import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if '\\' in pattern:
        raise ValueError("Trailing backslash is not allowed")
    
    # Создаем регулярное выражение из паттерна, заменяя * на .* и ? на .
    regex = re.compile(re.escape(pattern).replace(r'\*', '.*').replace(r'\?', '.'))
    
    return [word for word in words if regex.fullmatch(word)]
