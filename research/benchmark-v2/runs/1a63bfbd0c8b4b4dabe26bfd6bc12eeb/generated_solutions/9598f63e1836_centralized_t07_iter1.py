def analyze_logs(lines: list[str]) -> dict:
    valid_count = 0
    by_level = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errors = 0
    endpoints = {}
    
    for line in lines:
        try:
            date_time, level, endpoint, status = line.split(" ", 3)
            year_month_day, hour_minute_second = date_time.split(" ")
            _, level = level.split(":", 1)
            _, status_code = status.rsplit(" ", 1)
            
            if not (level in ["INFO", "WARNING", "ERROR"]):
                raise ValueError
            if not (len(status_code) == 3 and status_code.isdigit()):
                raise ValueError
                
            valid_count += 1
            by_level[level] += 1
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
        
        except ValueError:
            errors += 1
    
    most_common_endpoint = None
    max_frequency = 0
    
    for endpoint, frequency in endpoints.items():
        if frequency > max_frequency:
            max_frequency = frequency
            most_common_endpoint = endpoint
        elif frequency == max_frequency:
            most_common_endpoint = min(most_common_endpoint, endpoint)
    
    return {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
