import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        value = match.group()
        if value.startswith('-') or value.startswith('+'):
            return int(value)
        else:
            return int(value.lstrip('()'))
    
    def parse_term(tokens):
        result = None
        for token in tokens:
            if result is None:
                result = parse_atom(token)
            else:
                op = token[0]
                num = int(token[1:])
                if op == '+':
                    result += num
                elif op == '-':
                    result -= num
        
        return result
    
    # Remove spaces, handle nested expressions
    text = re.sub(r'\s+', '', text)
    tokens = re.findall(r'[\+\-\d\(\)]', text)
    
    # Evaluate innermost parentheses first
    while '(' in tokens:
        start = end = None
        for i, tok in enumerate(tokens):
            if tok == '(': start = i
            elif tok == ')': 
                end = i
                break
        
        # Extract subexpression, recursively evaluate it
        subexpr = ''.join(tokens[start+1:end])
        value = evaluate_expression(subexpr)
        # Replace with evaluated value
        tokens[start:end+1] = [str(value)]
    
    # Parse remaining terms
    return parse_term(tokens)
