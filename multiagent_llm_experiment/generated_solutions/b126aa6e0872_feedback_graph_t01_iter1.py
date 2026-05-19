def is_palindrome(text: str) -> bool:
    cleaned = ''.join(char for char in text if char.isalnum()).lower()
    return cleaned == cleaned[::-1]
