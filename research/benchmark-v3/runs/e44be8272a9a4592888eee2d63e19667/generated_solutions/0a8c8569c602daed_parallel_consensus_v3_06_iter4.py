def split_fields(text: str) -> list[str]:
    if text == "":
        return [""]
    fields: list[str] = []
    current: list[str] = []
    in_quote: str | None = None
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\":
            i += 1
            if i >= n:
                raise ValueError("Dangling escape")
            current.append(text[i])
        elif ch in ("'", '"'):
            if in_quote is None:
                in_quote = ch
            elif in_quote == ch:
                in_quote = None
            else:
                current.append(ch)
        elif ch == ";" and in_quote is None:
            fields.append("".join(current))
            current = []
        else:
            current.append(ch)
        i += 1
    if in_quote is not None:
        raise ValueError("Unclosed quote")
    fields.append("".join(current))
    return fields
