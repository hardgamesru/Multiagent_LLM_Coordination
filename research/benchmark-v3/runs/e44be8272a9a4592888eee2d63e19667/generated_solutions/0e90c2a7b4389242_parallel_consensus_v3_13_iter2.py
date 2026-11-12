import re

def evaluate_expression(text: str) -> int:
    def tokenize(expr):
        # Tokenizes expression into numbers, operators, and brackets
        return list(filter(None, re.split(r'(\d+|\+|-|\*|\(|\) )', expr)))
    
    def parse(tokens):
        # Parses tokens using recursive descent parser
        def term():
            nonlocal pos
            result = factor()
            
            while pos < len(tokens) and tokens[pos] in ('+', '-'):
                op = tokens[pos]
                pos += 1
                right = factor()
                if op == '+':
                    result += right
                else:
                    result -= right
            
            return result
        
        def factor():
            nonlocal pos
            result = None
            
            if pos < len(tokens) and tokens[pos].isdigit():
                num = int(tokens[pos])
                pos += 1
                result = num
                
            elif pos < len(tokens) and tokens[pos] in ('(', '+'):
                # Handle negative terms
                if tokens[pos] == '(':
                    pos += 1
                    result = term()
                    if pos < len(tokens) and tokens[pos] == ')':
                        pos += 1
                else:
                    result = -factor()
            
            elif pos < len(tokens) and tokens[pos] == '*':
                pos += 1
                right = factor()
                result = result * right if result is not None else right
            
            return result
        
        pos = 0
        return term()
    
    try:
        tokens = tokenize(text)
        return parse(tokens)
    except IndexError:
        raise ValueError("Invalid expression")
