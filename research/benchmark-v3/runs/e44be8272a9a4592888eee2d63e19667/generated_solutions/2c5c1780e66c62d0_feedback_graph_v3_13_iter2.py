import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group(0)
        if '+' in s or '-' in s:
            return int(s, 10)
        else:
            return int(s)
    
    def parse_term(tokens):
        result = None
        for token in tokens:
            if result is None:
                result = parse_atom(token)
            else:
                if token == '*':
                    result *= parse_atom(next(tokens))
                elif token == '/':
                    divisor = parse_atom(next(tokens))
                    # Prevent division by zero
                    if divisor != 0:
                        result //= divisor
                    else:
                        raise ValueError
        return result
    
    def parse_expr(tokens):
        result = None
        op = '+'
        
        while tokens:
            if op == '+':
                result = parse_term(iter(tokens))
            elif op == '-':
                # Subtract negated term
                result -= parse_term(iter(tokens))
            
            try:
                # Get next operator or end of expression
                op = next(tokens)
            except StopIteration:
                break
        
        return result
    
    # Tokenize expression by removing spaces, handling nested expressions
    tokens = []
    for m in re.finditer(r'\d+|\+|-|\(|\)', text):
        tokens.append(m.group())
    
    # Evaluate expression using parsed tokens
    return parse_expr(iter(tokens))
