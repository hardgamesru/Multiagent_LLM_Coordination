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
                raise ValueError("dangling escape")
            current.append(text[i])
            i += 1
            continue
        if in_quote:
            if ch == in_quote:
                in_quote = None
            else:
                current.append(ch)
            i += 1
            continue
        if ch in ('"', "'"):
            in_quote = ch
            i += 1
            continue
        if ch == ";":
            fields.append("".join(current))
            current = []
            i += 1
            continue
        current.append(ch)
        i += 1
    if in_quote:
        raise ValueError("unclosed quote")
    fields.append("".join(current))
    return fields
