import re
from collections import defaultdict

def analyze_logs(lines: list[str]) -> dict:
    valid_count = 0
    by_level = defaultdict(int)
    errors = 0
    endpoint_counts = defaultdict(int)

    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (/[^\s]*) (\d{3})$')

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        _, level, endpoint, status = match.groups()
        if not (100 <= int(status) <= 999):
            continue

        valid_count += 1
        by_level[level] += 1
        if level == 'ERROR':
            errors += 1
        endpoint_counts[endpoint] += 1

    most_common_endpoint = None
    if endpoint_counts:
        max_count = max(endpoint_counts.values())
        candidates = [ep for ep, cnt in endpoint_counts.items() if cnt == max_count]
        most_common_endpoint = min(candidates)

    return {
        'total': valid_count,
        'by_level': dict(by_level),
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
