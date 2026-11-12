def analyze_logs(lines: list[str]) -> dict:
    valid_counts = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    errors = 0
    endpoints = {}
    max_freq = 0
    most_common = None

    for line in lines:
        try:
            date, time, level, endpoint, status = line.split()
            _, _, status_code = status.rsplit('-', 2)
            if not (level in ('INFO', 'WARNING', 'ERROR') 
                    and status_code.isdigit() and len(status_code) == 3):
                continue
            valid_counts[level] += 1
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
            if endpoints[endpoint] > max_freq:
                max_freq = endpoints[endpoint]
                most_common = endpoint
            elif endpoints[endpoint] == max_freq:
                most_common = min(most_common, endpoint)
        except ValueError:
            errors += 1

    return {
        'total': len(lines) - errors,
        'by_level': valid_counts,
        'errors': errors,
        'most_common_endpoint': most_common
    }
