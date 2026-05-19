def is_palindrome(text: str) -> bool:
    import re
    normalized = re.sub(r"[^a-zA-Z0-9]", "", text).lower()
    return normalized == normalized[::-1]
