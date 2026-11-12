import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if '\\' in pattern[-1:]:
        raise ValueError("Trailing backslash")
    
    # Escape non-special characters except *, ?
    regex = re.escape(pattern)
    # Replace * with .*, ? with .
    regex = regex.replace('\\*', '.*').replace('\\?', '.')
    
    # Compile regex with case-sensitive flag
    compiled_pattern = re.compile(regex, flags=re.VERBOSE | re.IGNORECASE)
    
    # Filter matching words preserving original order
    return [word for word in words if compiled_pattern.fullmatch(word)]
