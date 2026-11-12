import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    try:
        regex = re.compile(re.escape(pattern))
    except Exception as e:
        raise ValueError("Invalid escape sequence in pattern")
    
    return [word for word in words if regex.fullmatch(word)]
