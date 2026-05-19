def parse_csv_line(line: str) -> list[str]:
    import re
    pattern = r'""|'  # escape double quote
    pattern += r'"((?:[^"\\"]*|\\.)*)"|'  # quoted field
    pattern += r'|([^,]+)'  # unquoted field
    result = re.findall(pattern, line)
    return [field.replace('""', '"') for field, _ in result if field]
