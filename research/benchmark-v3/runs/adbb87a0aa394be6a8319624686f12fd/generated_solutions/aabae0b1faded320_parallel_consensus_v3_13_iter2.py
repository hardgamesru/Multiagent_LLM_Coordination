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

    def consume(ch):
        skip()
        nonlocal pos
        if pos < n and s[pos] == ch:
            pos += 1
            return True
        return False

    def parse_number():
        skip()
        nonlocal pos
        start = pos
        while pos < n and s[pos].isdigit():
            pos += 1
        if start == pos:
            raise ValueError
        return int(s[start:pos])

    def parse_atom():
        c = peek()
        if c == '+' or c == '-':
            op = c
            consume(c)
            val = parse_atom()
            return val if op == '+' else -val
        if c == '(':
            consume('(')
            val = parse_expr()
            if not consume(')'):
                raise ValueError
            return val
        return parse_number()

    def parse_term():
        val = parse_atom()
        while True:
            c = peek()
            if c == '*':
                consume('*')
                val *= parse_atom()
            else:
                break
        return val

    def parse_expr():
        val = parse_term()
        while True:
            c = peek()
            if c == '+' or c == '-':
                op = c
                consume(c)
                right = parse_term()
                val = val + right if op == '+' else val - right
            else:
                break
        return val

    result = parse_expr()
    if peek() is not None:
        raise ValueError
    return result
