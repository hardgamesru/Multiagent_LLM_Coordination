import csv
from io import StringIO

def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    reader = csv.reader(StringIO(line), delimiter=',', quotechar='"', doublequote=True)
    return next(reader)
