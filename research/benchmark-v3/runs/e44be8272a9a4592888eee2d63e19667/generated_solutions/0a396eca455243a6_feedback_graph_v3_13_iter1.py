def evaluate_expression(text: str) -> int:
    s = text
    n = len(s)
    pos = 0

    def skip():
        nonlocal pos
        while pos < n and s[pos].isspace():
            pos += 1

    def peek():
        skip()
        return s[pos] if pos < n else None

    def consume(ch: str):
        nonlocal pos
        skip()
        if pos < n and s[pos] == ch:
            pos += 1
            return True
        return False

    def parse_number() -> int:
        nonlocal pos
        skip()
        start = pos
        while pos < n and s[pos].isdigit():
            pos += 1
        if start == pos:
            raise ValueError
        return int(s[start:pos])

    def parse_atom() -> int:
        if consume('('):
            val = parse_expr()
            if not consume(')'):
                raise ValueError
            return val
        ch = peek()
        if ch == '+' or ch == '-':
            pos_inc = 1
            pos_local = pos + 1
            while pos_local < n and s[pos_local].isspace():
                pos_local += 1
            if pos_local < n and s[pos_local].isdigit():
                pos += pos_inc
                sign = 1 if ch == '+' else -1
                return sign * parse_number()
            else:
                pos += pos_inc
                return sign * parse_atom()
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
    if pos != n:
        raise ValueError
    return result
