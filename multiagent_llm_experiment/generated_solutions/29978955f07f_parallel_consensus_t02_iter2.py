def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    parts = re.findall(r'(?:"([^"]*"(""[^"]*)?"")|([^,]+))', line)
    return [part[0].replace('""', '"') for part in parts if part[0]]
