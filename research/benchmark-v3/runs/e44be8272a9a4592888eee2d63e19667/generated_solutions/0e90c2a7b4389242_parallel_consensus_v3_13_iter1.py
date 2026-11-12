import re

def evaluate_expression(text: str) -> int:
    def tokenize(expr):
        return list(filter(None, re.split(r'(\d+|\+|-|\*|\(|\))', expr)))
    
    def parse(tokens):
        def next_token():
            return tokens.pop(0)
        
        def parse_term():
            t = next_token()
            if t == '(':
                result = parse(tokens)
                expect(')')
                return result
            elif t.isdigit():
                return int(t)
            else:
                return -parse_term()
        
        def parse_expr():
            result = parse_term()
            
            while len(tokens) > 0:
                op = next_token()
                if op in ('+', '-'):
                    right = parse_term()
                    if op == '+':
                        result += right
                    else:
                        result -= right
            
            return result
        
        def expect(token):
            if len(tokens) == 0 or tokens[0] != token:
                raise ValueError(f"Expected '{token}'")
            else:
                next_token()
        
        tokens = tokenize(text)
        return parse_expr()
    
    try:
        return parse(list(text))
    except Exception as e:
        raise ValueError(str(e))
