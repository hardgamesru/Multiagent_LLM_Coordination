def parse_csv_line(line: str) -> list[str]:
    return next(csv.reader(StringIO(line), delimiter=','))
