import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group()
        if s.startswith('-') or s.startswith('+'):
            return int(s)
        else:
            return int(s)
    
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
    while '(' in text:
        text = re.sub(r'(\()([^()]*)(\))', lambda m: f'{parse_term(re.findall(r"[+-]?\d+|[()+]", m.group(2)))}', text)
    
    # Evaluate remaining terms
    return parse_term(re.findall(r"[+-]?\d+", text))
