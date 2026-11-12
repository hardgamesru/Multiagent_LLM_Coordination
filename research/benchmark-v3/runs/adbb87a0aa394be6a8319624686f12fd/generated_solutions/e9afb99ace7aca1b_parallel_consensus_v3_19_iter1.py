import re

def wildcard_matches(pattern: str, words: list[str]) -> list[str]:
    if pattern.endswith('\\'):
        raise ValueError("Trailing backslash in pattern")

    regex_parts = ['^']
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '\\':
            i += 1
            if i >= len(pattern):
                raise ValueError("Trailing backslash in pattern")
            regex_parts.append(re.escape(pattern[i]))
        elif c == '?':
            regex_parts.append('.')
        elif c == '*':
            regex_parts.append('.*')
        else:
            regex_parts.append(re.escape(c))
        i += 1
    regex_parts.append('$')

    regex = ''.join(regex_parts)
    prog = re.compile(regex)

    return [w for w in words if prog.fullmatch(w) is not None]
