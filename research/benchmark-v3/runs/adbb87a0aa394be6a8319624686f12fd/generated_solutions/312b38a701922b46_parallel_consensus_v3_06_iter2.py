def split_fields(text: str) -> list[str]:
    if text == "":
        return [""]
    fields: list[str] = []
    current: list[str] = []
    quote: str | None = None
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\":
            i += 1
            if i >= n:
                raise ValueError("Dangling escape")
            current.append(text[i])
        elif quote:
            if ch == quote:
                quote = None
            else:
                current.append(ch)
        else:
            if ch in ('"', "'"):
                quote = ch
            elif ch == ";":
                fields.append("".join(current))
                current = []
            else:
                current.append(ch)
        i += 1
    if quote:
        raise ValueError("Unclosed quote")
    fields.append("".join(current))
    return fields
