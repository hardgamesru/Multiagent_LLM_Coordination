import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        value = match.group()
        if value.startswith('-') or value.startswith('+'):
            return int(value)
        else:
            return int(value, 10)
    
    def parse_term(tokens):
        result = None
        for token in tokens:
            if result is None:
                result = parse_atom(token)
            else:
                if token == '*':
                    result *= parse_atom(next(tokens))
                else:
                    raise ValueError("Invalid operator")
        
        return result
    
    def parse_expr(tokens):
        result = None
        op = '+'
        
        for token in tokens:
            if token == '(':
                # Handle nested expressions
                result = parse_expr(next(tokens))
            elif token == ')':
                break
            else:
                if op == '+':
                    result = result + parse_atom(token) if result else parse_atom(token)
                elif op == '-':
                    result = result - parse_atom(token) if result else -parse_atom(token)
                else:
                    raise ValueError("Invalid operation sequence")
            
            try:
                op = next(tokens)
            except StopIteration:
                pass
        
        return result
    
    # Tokenize expression removing spaces and handle nested expressions
    tokens = []
    for token in re.findall(r'\d+|\+|-|\(|\)', text):
        tokens.append(token)
    
    # Evaluate top-level expression
    try:
        return parse_expr(iter(tokens))
    except StopIteration:
        raise ValueError("Incomplete expression")
