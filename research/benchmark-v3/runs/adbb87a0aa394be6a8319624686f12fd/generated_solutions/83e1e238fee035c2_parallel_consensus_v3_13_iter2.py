import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group()
        if '(' in s:
            return parse_expr(s)
        elif '+' in s or '-' in s:
            sign = '+' if s[0] == '+' else '-'
            num = int(s[1:])
            return num if sign == '+' else -num
        else:
            return int(s)
    
    def parse_term(match):
        parts = list(map(parse_atom, re.finditer(r'\+|\-|\d+|\(\d+\)', match.group())))
        result = None
        for p in parts:
            if result is None:
                result = p
            else:
                if isinstance(p, int):  
                    result *= p
                else:
                    result = eval(f'{result}{p}')
        return result
    
    def parse_expr(match):
        parts = list(map(parse_term, re.finditer(r'\+|\-|\d+|\(\d+\)', match.group())))
        result = None
        for p in parts:
            if result is None:
                result = p
            else:
                if isinstance(p, int):
                    result += p
                else:
                    result = eval(f'{result}{p}')
        return result
    
    # Check for empty string or invalid input
    if len(text.strip()) == 0 or (' ' in text and not text.startswith('(')):
        raise ValueError
    
    try:
        return parse_expr(re.match(r'.*', text))
    except Exception as e:
        raise ValueError from e
