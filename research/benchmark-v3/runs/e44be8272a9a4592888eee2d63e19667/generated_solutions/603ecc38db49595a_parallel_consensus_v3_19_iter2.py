import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if '\\' in pattern[-1:]:
        raise ValueError("Trailing backslash")
    
    # Escape non-special characters except *, ?
    regex = re.escape(pattern)
    # Replace * with .* and ? with .
    regex = regex.replace('\\*', '.*').replace('\\?', '.')
    
    # Compile regex with case-sensitive flag
    compiled_pattern = re.compile(regex, flags=re.VERBOSE | re.IGNORECASE)
    
    return [word for word in words if compiled_pattern.fullmatch(word)]
