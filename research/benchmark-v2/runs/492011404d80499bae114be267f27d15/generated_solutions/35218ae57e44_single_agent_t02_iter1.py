def parse_csv_line(line: str) -> list[str]:
    import csv
    from io import StringIO
    reader = csv.reader(StringIO(line), quotechar='"', doublequote=True, escapechar=None, strict=False)
    return next(reader)
