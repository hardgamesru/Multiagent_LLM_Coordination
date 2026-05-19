def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    import re
    pattern = r'(?:"([^"\\]*(?:\\.[^"\\]*)*)"|([^,]+))'
    matches = re.findall(pattern, line)
    def unescape_double_quotes(match): return match.group(1).replace('""', '"')
    return [unescape_double_quotes(match) if match[0] else match[1] for match in matches]
