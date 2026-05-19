def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    pattern = r'(?:"([^"\\]*(?:\\.[^"\\]*)*)"|[^,]+)(?=(?:,|$))'
    fields = re.findall(pattern, line)
    return [f.strip('"') for f in fields]
