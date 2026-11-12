from pyparsing import (
    Literal,
    OpAssoc,
    Combine,
    Group,
    ZeroOrMore,
    Forward,
    nums,
    oneOf,
)

def evaluate_expression(text: str) -> int:
    plus = Literal('+')
    minus = Literal('-')
    mult = Literal('*')
    lparen = Literal('(')
    rparen = Literal(')')
    
    atom = Combine(
        oneOf("+-")["optional_sign"] + 
        nums["number"]
    ).setParseAction(lambda t: int(t[0]))
    
    term = atom + ZeroOrMore(Group(oneOf("+-")) + atom)
    expr = lparen + Group(expr | term) + rparen | term
    
    expr.setParseAction(lambda t: eval(str(t)))
    
    try:
        result = expr.parseString(text)[0]
    except Exception:
        raise ValueError
        
    return result
