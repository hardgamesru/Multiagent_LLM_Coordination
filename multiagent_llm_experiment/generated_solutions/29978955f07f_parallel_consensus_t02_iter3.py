def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    parts = re.findall(r'(?:"([^"]*"("""")[^"]*"")?"|([^,]+))', line)
    result = []
    for part in parts:
        value = part[0] or part[1]
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('""', '"')
        result.append(value)
    return result
