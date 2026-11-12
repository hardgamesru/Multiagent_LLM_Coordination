import re

def split_fields(text: str) -> list[str]:
    def unescape(s):
        return s.replace('\\"', '"').replace('\\\\', '\\')
    
    parts = []
    quoted = False
    current_part = ''
    
    for char in text:
        if quoted:
            # Inside quoted section, handle escaping and closing quote
            if char == '\\':
                current_part += '\\'
            elif char == '"' and (len(current_part) == 0 or current_part[-1] != '\\'):
                quoted = False
                current_part += '"'
            else:
                current_part += char
        else:
            # Outside quoted section, process normal characters
            if char == '"':
                quoted = True
                current_part += '"'
            elif char == ';':
                parts.append(unescape(current_part))
                current_part = ''
            else:
                current_part += char
    
    # Add last part if any
    if current_part:
        parts.append(unescape(current_part))
    
    # Handle empty string case
    if len(parts) == 0:
        return [""]
    
    return parts
