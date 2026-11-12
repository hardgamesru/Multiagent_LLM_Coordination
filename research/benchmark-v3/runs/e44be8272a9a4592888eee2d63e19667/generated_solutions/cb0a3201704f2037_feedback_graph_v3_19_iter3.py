import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if not pattern:
        return [w for w in words if not w]
    
    # Создаем регулярное выражение из паттерна,
    # где '*' превращается в '*+' и '?' в '.'
    regex_pattern = re.escape(pattern)
    regex_pattern = regex_pattern.replace('\\*', '[^\\n]*').replace('\\?', '.')
    
    # Проверяем соответствие каждого слова шаблону
    return [word for word in words if re.fullmatch(regex_pattern, word)]
