def analyze_logs(lines: list[str]) -> dict:
    from collections import defaultdict, Counter
    import re

    valid_count = 0
    by_level = defaultdict(int)
    endpoint_counter = Counter()
    errors = 0

    # Pattern: date time LEVEL ENDPOINT STATUS
    # LEVEL: INFO|WARNING|ERROR
    # STATUS: exactly 3 digits
    pattern = re.compile(
        r'^(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'(?P<level>INFO|WARNING|ERROR)\s+(?P<endpoint>\S+)\s+(?P<status>\d{3})$'
    )

    for line in lines:
        m = pattern.match(line)
        if not m:
            errors += 1
            continue

        level = m.group('level')
        endpoint = m.group('endpoint')

        valid_count += 1
        by_level[level] += 1
        endpoint_counter[endpoint] += 1

    if endpoint_counter:
        max_freq = max(endpoint_counter.values())
        candidates = [ep for ep, cnt in endpoint_counter.items() if cnt == max_freq]
        most_common_endpoint = min(candidates)
    else:
        most_common_endpoint = None

    return {
        'total': valid_count,
        'by_level': dict(by_level),
        'errors': errors,
        'most_common_endpoint': most_common_endpoint,
    }
