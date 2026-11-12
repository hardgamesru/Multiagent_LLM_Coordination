import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if '\\' in pattern[-1:]:
        raise ValueError("Trailing backslash")
    
    # Escape non-special characters except *, ?, \
    regex = re.escape(pattern)
    # Replace ? with single char match, * with zero-or-more chars
    regex = regex.replace('\\?', '.').replace('\\*', '.*')
    regex = regex.replace('?', '.').replace('*', '.*')
    
    return [word for word in words if re.fullmatch(regex, word)]
