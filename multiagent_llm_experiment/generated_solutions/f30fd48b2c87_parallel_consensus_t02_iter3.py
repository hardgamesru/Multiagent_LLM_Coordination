def parse_csv_line(line: str) -> list[str]:
    reader = csv.reader(StringIO(line), delimiter=',')
    return next(reader)
