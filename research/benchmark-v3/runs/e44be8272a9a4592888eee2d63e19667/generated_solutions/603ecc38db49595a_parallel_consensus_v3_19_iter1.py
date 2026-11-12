import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if '\\' in pattern:
        raise ValueError("Trailing backslash is not allowed")
    
    # Escape non-special characters except *, ?
    regex = re.escape(pattern)
    
    # Replace wildcards with appropriate regex patterns
    regex = regex.replace('\\*', '.*').replace('\\?', '.')
    regex = regex.replace('*', '.*').replace('?', '.')
    
    # Compile regex with case-sensitive flag
    compiled_pattern = re.compile(regex, re.VERBOSE | re.IGNORECASE)
    
    # Filter matching words
    return [word for word in words if compiled_pattern.fullmatch(word)]
