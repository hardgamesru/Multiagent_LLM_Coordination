def analyze_logs(lines: list[str]) -> dict:
    from collections import Counter
    import re
    valid_count = 0
    level_counts = Counter()
    error_count = 0
    endpoint_counts = Counter()
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (/[^\s]*) (\d{3})$')
    for line in lines:
        match = pattern.match(line)
        if match:
            valid_count += 1
            _, level, endpoint, status = match.groups()
            level_counts[level] += 1
            if level == 'ERROR':
                error_count += 1
            endpoint_counts[endpoint] += 1
    most_common_endpoint = None
    if endpoint_counts:
        max_freq = max(endpoint_counts.values())
        candidates = [ep for ep, cnt in endpoint_counts.items() if cnt == max_freq]
        most_common_endpoint = min(candidates)
    return {
        'total': valid_count,
        'by_level': dict(level_counts),
        'errors': error_count,
        'most_common_endpoint': most_common_endpoint
    }
