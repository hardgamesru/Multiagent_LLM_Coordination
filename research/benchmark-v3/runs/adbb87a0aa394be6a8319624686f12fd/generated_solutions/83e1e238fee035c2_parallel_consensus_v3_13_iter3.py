import re

def evaluate_expression(text: str) -> int:
    def parse_atom(match):
        s = match.group(0)
        if s.startswith("+"):
            return parse_atom(s[1:])
        elif s.startswith("-"):
            return -parse_atom(s[1:])
        else:
            return int(s)
    
    def parse_term(match):
        parts = list(map(parse_atom, re.finditer(r"[\+\-\d]+", match.group(0))))
        result = parts[0]
        for p in parts[1:]:
            if isinstance(p, int):  
                result *= p
            else:
                result += p
        return result
    
    def parse_expr(match):
        parts = list(map(parse_term, re.finditer(r"\([\+\-\d\s\*]*\)|[+\-\d\s\*]+", match.group(0))))
        result = parts[0]
        for p in parts[1:]:
            if isinstance(p, int):
                result += p
            else:
                raise ValueError
        return result
    
    # Check empty string
    if len(text.strip()) == 0:
        raise ValueError
    
    # Validate expression structure
    try:
        parsed = re.match(r"^\s*[\+\-\d\(\)\*\s]+$", text)
        if not parsed:
            raise ValueError
    except TypeError:
        raise ValueError
    
    # Evaluate expression
    try:
        return parse_expr(re.match(r".+", text))
    except Exception:
        raise ValueError
