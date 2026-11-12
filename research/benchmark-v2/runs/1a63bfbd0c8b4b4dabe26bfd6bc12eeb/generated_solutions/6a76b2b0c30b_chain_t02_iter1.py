def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    pattern = r'(?:"((?:[^""]|"")*)"|([^,]+))'
    matches = re.findall(pattern, line)
    return [match[0].strip('"') if match[0] else match[1] for match in matches]
