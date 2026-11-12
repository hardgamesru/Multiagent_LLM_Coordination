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

    def consume(ch):
        nonlocal i
        skip()
        if i < n and s[i] == ch:
            i += 1
            return True
        return False

    def parse_number():
        nonlocal i
        skip()
        start = i
        while i < n and s[i].isdigit():
            i += 1
        if start == i:
            raise ValueError
        return int(s[start:i])

    def parse_atom():
        if consume('('):
            val = parse_expr()
            if not consume(')'):
                raise ValueError
            return val
        if consume('+'):
            return parse_atom()
        if consume('-'):
            return -parse_atom()
        return parse_number()

    def parse_term():
        val = parse_atom()
        while True:
            if consume('*'):
                val *= parse_atom()
            else:
                break
        return val

    def parse_expr():
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
        raise ValueError
    return result
