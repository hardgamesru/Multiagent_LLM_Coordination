import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group()
        if s.startswith('-') or s.startswith('+'):
            return int(s[1:], 10)
        else:
            return int(s, 10)
    
    def parse_term(tokens):
        result = next(tokens, None)
        while True:
            op = next(tokens, None)
            if op is None: break
            num = next(tokens, None)
            if num is None: raise ValueError
            if op == '*':
                result *= num
            elif op == '+':
                result += num
            elif op == '-':
                result -= num
        return result
    
    # Преобразование строки в токены
    tokens = iter(map(parse_atom, filter(None, re.split(r'(\d+|\+|-|\*)', text))))
    
    # Вычисление терминалов и термов
    try:
        return parse_term(tokens)
    except StopIteration:
        raise ValueError
