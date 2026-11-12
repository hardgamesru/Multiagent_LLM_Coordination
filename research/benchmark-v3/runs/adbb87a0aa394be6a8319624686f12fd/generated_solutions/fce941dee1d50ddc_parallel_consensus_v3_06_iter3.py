import re

def split_fields(text: str) -> list[str]:
    def unquote_and_unescape(match):
        s = match.group()
        # Remove surrounding quotes if present
        if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
            s = s[1:-1]
        
        # Unescape backslashes
        return re.sub(r'\\.', lambda m: m.group(0)[1], s)
    
    # Split using semicolon as separator while preserving quoted segments
    parts = re.split(r';(?=(?:[^"\'\\]|"[^"]*' + 
                     r'|' + 
                     r"'[^']*'" +
                     r'|\\.)*[^"\'\\])?', text)
    
    # Process each part to handle escaping and quotes
    return [unquote_and_unescape(part) for part in parts]
