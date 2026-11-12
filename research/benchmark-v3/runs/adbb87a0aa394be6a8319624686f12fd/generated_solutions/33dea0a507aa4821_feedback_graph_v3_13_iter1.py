import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group(0)
        if s.startswith('+'):
            return int(s[1:])
        elif s.startswith('-'):
            return -int(s[1:])
        else:
            return int(s)
    
    def parse_term(tokens):
        result = None
        for token in tokens:
            if result is None:
                result = parse_atom(token)
            else:
                op = token
                next_value = parse_atom(next(tokens))
                if op == '*':
                    result *= next_value
                else:
                    result += next_value
        return result
    
    # Преобразуем строку в токены, игнорируя пробелы
    tokens = list(map(parse_atom, filter(None, re.split(r'(\d+|\+|\-|\*)', text))))
    
    # Вычисляем итоговое выражение слева направо
    return parse_term(tokens)
