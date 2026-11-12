import re

def split_fields(text: str) -> list[str]:
    def unescape(s):
        return s.replace('\\"', '"').replace('\\\\', '\\')
    
    # Regular expression for splitting with quoted fields
    pattern = r'"(?:\\.|[^"\\])*"' \
              '|\'(?:\\.|[^\'\\])*\'' \
              '|[^;]+'
    
    # Split the string using the regex pattern
    parts = re.findall(pattern, text)
    
    # Remove escaping characters from quoted parts
    result = []
    for part in parts:
        if len(part) >= 2 and part[0] == part[-1] and part[0] in ('"', "'"):
            result.append(unescape(part[1:-1]))
        else:
            result.append(part)
            
    return result
