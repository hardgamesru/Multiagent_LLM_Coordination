def split_fields(text: str) -> list[str]:
    if text == "":
        return [""]
    fields: list[str] = []
    current: list[str] = []
    i = 0
    n = len(text)
    quote: str | None = None
    while i < n:
        ch = text[i]
        if ch == "\\":
            i += 1
            if i >= n:
                raise ValueError("Dangling escape")
            current.append(text[i])
            i += 1
            continue
        if quote is None:
            if ch in ('"', "'"):
                quote = ch
                i += 1
                continue
            if ch == ";":
                fields.append("".join(current))
                current = []
                i += 1
                continue
            current.append(ch)
            i += 1
            continue
        # inside quotes
        if ch == quote:
            quote = None
            i += 1
            continue
        current.append(ch)
        i += 1
    if quote is not None:
        raise ValueError("Unclosed quote")
    fields.append("".join(current))
    return fields
