import csv
from io import StringIO

def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    reader = csv.reader(StringIO(line), quotechar='"', doublequote=True, escapechar=None, strict=False)
    return next(reader)
