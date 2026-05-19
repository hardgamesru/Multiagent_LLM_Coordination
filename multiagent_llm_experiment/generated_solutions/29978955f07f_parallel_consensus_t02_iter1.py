def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    pattern = r'(?:"((?:[^"]|"")*)"|([^,]+))'
    matches = re.findall(pattern, line)
    return [match[0].replace('""', '"') for match in matches if match[0]] + [match[1] for match in matches if match[1]]
