from collections import Counter

def analyze_logs(lines: list[str]) -> dict:
    valid_count = 0
    by_level = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errors = 0
    endpoint_counter = Counter()

    for line in lines:
        parts = line.split(maxsplit=4)
        if len(parts) != 5:
            continue
        date, time, level, endpoint, status = parts
        if level not in by_level:
            continue
        if not (len(status) == 3 and status.isdigit()):
            continue

        valid_count += 1
        by_level[level] += 1
        if level == "ERROR":
            errors += 1
        endpoint_counter[endpoint] += 1

    most_common_endpoint = None
    if endpoint_counter:
        max_freq = max(endpoint_counter.values())
        candidates = [ep for ep, cnt in endpoint_counter.items() if cnt == max_freq]
        most_common_endpoint = min(candidates)

    return {
        "total": valid_count,
        "by_level": by_level,
        "errors": errors,
        "most_common_endpoint": most_common_endpoint,
    }
