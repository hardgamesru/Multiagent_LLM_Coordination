def analyze_logs(lines: list[str]) -> dict:
    valid_count = errors = 0
    by_level = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    endpoints = {}
    
    for line in lines:
        try:
            date, time, level, endpoint, status = line.split()
            year_month_day, hour_minute_second = date, time
            _, _, level = level.rpartition(':')
            _, endpoint = endpoint.rsplit(' ', 1)
            status_code = int(status)
            
            if level not in by_level or not(100 <= status_code < 600):
                continue
            valid_count += 1
            by_level[level] += 1
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
        
        except ValueError:
            errors += 1
    
    most_common_endpoint = None
    max_freq = 0
    for endpoint, freq in sorted(endpoints.items()):
        if freq > max_freq:
            max_freq = freq
            most_common_endpoint = endpoint
    
    return {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
