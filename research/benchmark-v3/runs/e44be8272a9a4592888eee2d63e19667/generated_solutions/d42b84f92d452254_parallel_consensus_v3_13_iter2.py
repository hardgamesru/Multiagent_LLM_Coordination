def evaluate_expression(text: str) -> int:
    s = text
    n = len(s)
    i = 0
    depth = 0
    MAX_DEPTH = 30

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
        num = int(s[start:i])
        return num

    def parse_atom() -> int:
        nonlocal depth
        skip()
        ch = peek()
        if ch == '(':
            if depth >= MAX_DEPTH:
                raise ValueError
            depth += 1
            consume('(')
            val = parse_expr()
            if not consume(')'):
                raise ValueError
            depth -= 1
            return val
        if ch in '+-':
            sign = 1
            while peek() in '+-':
                if consume('-'):
                    sign = -sign
                else:
                    consume('+')
            val = parse_atom()
            return sign * val
        return parse_number()

    def parse_term() -> int:
        val = parse_atom()
        while True:
            skip()
            if i < n and s[i] == '*':
                i += 1
                rhs = parse_atom()
                val = val * rhs
            else:
                break
        return val

    def parse_expr() -> int:
        val = parse_term()
        while True:
            skip()
            if i < n and s[i] in '+-':
                op = s[i]
                i += 1
                rhs = parse_term()
                if op == '+':
                    val = val + rhs
                else:
                    val = val - rhs
            else:
                break
        return val

    skip()
    if i >= n:
        raise ValueError
    result = parse_expr()
    skip()
    if i != n:
        raise ValueError
    return result
