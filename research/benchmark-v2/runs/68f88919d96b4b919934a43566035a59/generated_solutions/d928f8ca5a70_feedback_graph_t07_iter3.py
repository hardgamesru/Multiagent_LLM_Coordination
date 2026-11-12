def analyze_logs(lines: list[str]) -> dict:
    from collections import Counter
    import re

    valid_count = 0
    level_counter = Counter()
    errors = 0
    endpoint_counter = Counter()

    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (\S+) (\d{3})$')

    for line in lines:
        m = pattern.match(line)
        if not m:
            errors += 1
            continue

        _, level, endpoint, status = m.groups()
        if not (100 <= int(status) <= 999):
            errors += 1
            continue

        valid_count += 1
        level_counter[level] += 1
        endpoint_counter[endpoint] += 1

    most_common_endpoint = None
    if endpoint_counter:
        max_freq = max(endpoint_counter.values())
        candidates = [ep for ep, cnt in endpoint_counter.items() if cnt == max_freq]
        most_common_endpoint = min(candidates)

    return {
        'total': valid_count,
        'by_level': dict(level_counter),
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
