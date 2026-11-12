def evaluate_expression(text: str) -> int:
    s = text
    n = len(s)
    i = 0
    depth = 0

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
            raise ValueError
        return int(s[start:i])

    def parse_atom() -> int:
        nonlocal depth
        if consume('('):
            depth += 1
            if depth > 30:
                raise ValueError
            val = parse_expr()
            if not consume(')'):
                raise ValueError
            depth -= 1
            return val
        ch = peek()
        if ch == '+' or ch == '-':
            i_inc = 1
            i += i_inc
            val = parse_atom()
            return val if ch == '+' else -val
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

    if not s.strip():
        raise ValueError
    result = parse_expr()
    skip()
    if i != n:
        raise ValueError
    return result
