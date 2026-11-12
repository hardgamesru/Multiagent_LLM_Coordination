def analyze_logs(lines: list[str]) -> dict:
    from collections import Counter
    import re
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|WARNING|ERROR) (/[^ ]+) (\d{3})$'
    logs = []
    errors = 0
    for line in lines:
        match = re.match(pattern, line)
        if match:
            level, endpoint, status = match.groups()
            logs.append((level, endpoint, int(status)))
        else:
            errors += 1
    counts_by_level = Counter(level for level, _, _ in logs)
    most_common_endpoint = None
    if logs:
        endpoints = [endpoint for _, endpoint, _ in logs]
        freq = Counter(endpoints)
        max_freq = max(freq.values())
        most_common_endpoints = [ep for ep, count in freq.items() if count == max_freq]
        most_common_endpoint = min(most_common_endpoints)
    return {
        'total': len(logs),
        'by_level': counts_by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
