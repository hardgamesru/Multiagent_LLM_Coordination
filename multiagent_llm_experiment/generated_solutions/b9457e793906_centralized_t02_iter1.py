def parse_csv_line(line: str) -> list[str]:
    import csv
    reader = csv.reader([line])
    return next(reader)
