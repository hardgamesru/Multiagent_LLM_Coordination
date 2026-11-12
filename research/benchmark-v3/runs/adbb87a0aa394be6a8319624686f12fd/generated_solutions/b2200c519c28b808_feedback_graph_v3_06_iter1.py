def split_fields(text: str) -> list[str]:
    if text == "":
        return [""]
    fields = []
    current = []
    in_quote = None
    escape = False
    for i, c in enumerate(text):
        if escape:
            current.append(c)
            escape = False
        elif c == "\\":
            if i == len(text) - 1:
                raise ValueError("Dangling escape")
            escape = True
        elif in_quote:
            if c == in_quote:
                in_quote = None
            else:
                current.append(c)
        else:
            if c in ('"', "'"):
                in_quote = c
            elif c == ";":
                fields.append("".join(current))
                current = []
            else:
                current.append(c)
    if escape:
        raise ValueError("Dangling escape")
    if in_quote:
        raise ValueError("Unclosed quote")
    fields.append("".join(current))
    return fields
