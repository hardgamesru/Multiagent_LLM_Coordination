def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    pattern = r'(?:"((?:[^"\\"]+|\\.)*)"|([^,]*))(?=(?:,|$))'
    fields = re.findall(pattern, line)
    result = []
    for field in fields:
        value = field[0] or field[1]
        value = value.strip('"').replace('""', '"')
        result.append(value)
    return result
