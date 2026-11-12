import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    regex = re.compile(re.escape(pattern).replace("\\?", ".").replace("\\*", ".*"))
    return [word for word in words if regex.fullmatch(word)]
