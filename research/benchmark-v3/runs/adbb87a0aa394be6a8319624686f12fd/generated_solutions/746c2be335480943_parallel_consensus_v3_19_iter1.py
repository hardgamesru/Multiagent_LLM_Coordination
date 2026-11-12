import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    try:
        regex = re.compile(re.escape(pattern).replace('\\*', '.*').replace('\\?', '.'))
    except Exception as e:
        raise ValueError(f"Invalid escape sequence: {e}")
    
    return [word for word in words if regex.fullmatch(word)]
