def evaluate_expression(text: str) -> int:
    s = text
    n = len(s)
    i = 0

    def skip():
        nonlocal i
        while i < n and s[i].isspace():
            i += 1

    def peek():
        skip()
        return s[i] if i < n else None

    def consume(ch: str):
        nonlocal i
        skip()
        if i < n and s[i] == ch:
            i += 1
            return True
        return False

    def parse_number() -> int:
        nonlocal i
        skip()
        start = i
        while i < n and s[i].isdigit():
            i += 1
        if start == i:
            raise ValueError("Number expected")
        return int(s[start:i])

    def parse_atom() -> int:
        if consume('('):
            val = parse_expr()
            if not consume(')'):
                raise ValueError("Missing ')'")
            return val
        if consume('+'):
            return parse_atom()
        if consume('-'):
            return -parse_atom()
        return parse_number()

    def parse_term() -> int:
        val = parse_atom()
        while True:
            if consume('*'):
                val *= parse_atom()
            else:
                break
        return val

    def parse_expr() -> int:
        val = parse_term()
        while True:
            if consume('+'):
                val += parse_term()
            elif consume('-'):
                val -= parse_term()
            else:
                break
        return val

    result = parse_expr()
    skip()
    if i != n:
        raise ValueError("Trailing tokens")
    return result
