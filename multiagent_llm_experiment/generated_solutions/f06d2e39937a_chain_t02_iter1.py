def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    quoted = re.findall(r'(?:"([^"\\"]*(?:\\.[^"\\"]*)*)"|[^,]+)', line)
    return [re.sub(r'""', '"', x[0]) for x in quoted] if quoted else []
