def is_palindrome(text: str) -> bool:
    import re
    cleaned_text = re.sub(r'[\W_]+', '', text).lower()
    return cleaned_text == cleaned_text[::-1] if cleaned_text else False
