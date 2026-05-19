def is_palindrome(text: str) -> bool:
    cleaned = ''.join(c for c in text if c.isalnum()).lower()
    return cleaned == cleaned[::-1]
