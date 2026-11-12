def analyze_logs(lines: list[str]) -> dict:
    valid_count = errors = 0
    by_level = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    endpoints = {}
    
    for line in lines:
        try:
            date_str, level, endpoint, status = line.split(' ', 3)
            year, month, day = date_str.split('-')
            hour, minute, second = date_str.split(':')
            _, status_code = status.rsplit(' ', 1)
            
            if len(year) != 4 or len(month) != 2 or len(day) != 2 \
               or len(hour) != 2 or len(minute) != 2 or len(second) != 2 \
               or len(status_code) != 3 or not status_code.isdigit():
                continue
                
            valid_count += 1
            by_level[level] += 1
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
        
        except ValueError:
            errors += 1
    
    most_common_endpoint = None
    max_freq = 0
    freq_dict = sorted(endpoints.items())
    
    for endpoint, count in freq_dict:
        if count > max_freq:
            max_freq = count
            most_common_endpoint = endpoint
        elif count == max_freq:
            most_common_endpoint = min(most_common_endpoint, endpoint)
    
    return {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
