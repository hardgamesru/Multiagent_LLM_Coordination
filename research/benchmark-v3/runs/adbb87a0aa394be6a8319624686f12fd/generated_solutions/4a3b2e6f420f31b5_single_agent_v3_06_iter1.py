def split_fields(text: str) -> list[str]:
    if text == "":
        return [""]
    fields = []
    current = []
    in_quote = None
    escape = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if escape:
            current.append(c)
            escape = False
        elif c == "\\":
            escape = True
        elif in_quote:
            if c == in_quote:
                in_quote = None
            else:
                current.append(c)
        else:
            if c in "\"'":
                in_quote = c
            elif c == ";":
                fields.append("".join(current))
                current = []
            else:
                current.append(c)
        i += 1
    if escape:
        raise ValueError("Dangling escape")
    if in_quote:
        raise ValueError("Unclosed quote")
    fields.append("".join(current))
    return fields
