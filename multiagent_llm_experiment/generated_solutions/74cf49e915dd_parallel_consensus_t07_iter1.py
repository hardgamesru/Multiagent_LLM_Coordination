def analyze_logs(lines):
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (/[^ ]*) (\d+)$'
    
    # Initialize counters
    valid_count = 0
    levels = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errors = 0
    endpoints = []
    
    for line in lines:
        match = re.match(pattern, line)
        
        if match:
            _, level, endpoint, status_code = match.groups()
            
            # Update total valid count
            valid_count += 1
            
            # Increment appropriate level counter
            levels[level] += 1
            
            # Check for error based on HTTP status code
            if int(status_code) >= 400:
                errors += 1
                
            # Collect all valid endpoints
            endpoints.append(endpoint)
    
    # Determine most common endpoint 
    if len(endpoints) > 0:
        endpoint_counts = Counter(endpoints)
        max_freq = max(endpoint_counts.values())
        candidates = [e for e, f in endpoint_counts.items() if f == max_freq]
        most_common_endpoint = min(candidates)
    else:
        most_common_endpoint = None
    
    result = {
        'total': valid_count,
        'by_level': levels,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
    
    return result
