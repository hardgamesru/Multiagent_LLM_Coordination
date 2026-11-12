def analyze_logs(lines: list[str]) -> dict:
    valid_count = errors = 0
    by_level = {}
    endpoints = []
    
    for line in lines:
        try:
            date, time, level, endpoint, status = line.split(' ', 4)
            _, _, status_code = status.rsplit(' ', 2)
            if len(status_code) != 3 or not status_code.isdigit():
                continue
            valid_count += 1
            by_level.setdefault(level, 0)
            by_level[level] += 1
            endpoints.append(endpoint)
        except ValueError:
            errors += 1
    
    most_common_endpoint = None
    if endpoints:
        from collections import Counter
        freq = Counter(endpoints)
        max_freq = max(freq.values())
        most_common_endpoints = [ep for ep, count in freq.items() if count == max_freq]
        most_common_endpoint = min(most_common_endpoints)
    
    return {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
