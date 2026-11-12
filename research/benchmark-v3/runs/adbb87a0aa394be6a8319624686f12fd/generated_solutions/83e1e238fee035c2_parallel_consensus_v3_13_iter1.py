import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group(0)
        if '+' in s or '-' in s:
            return int(s, 10)
        else:
            return int(s.strip('()'))
    
    def parse_term(tokens):
        result = None
        for token in tokens:
            if result is None:
                result = parse_atom(token)
            elif token == '*':
                result *= parse_atom(next(tokens))
        
        return result
    
    def parse_expr(tokens):
        result = None
        op = '+'
        
        for token in tokens:
            if token in ('+', '-'):
                op = token
            else:
                term_result = parse_term(iter([t for t in tokens if t != op]))
                
                if op == '+':
                    result = result + term_result if result else term_result
                else:
                    result = result - term_result if result else -term_result
        
        return result
    
    # Tokenize expression using regex, ignoring spaces
    tokens = list(map(parse_atom, re.finditer(r'[\d()+\-*]+', text)))
    
    return parse_expr(iter(tokens))
