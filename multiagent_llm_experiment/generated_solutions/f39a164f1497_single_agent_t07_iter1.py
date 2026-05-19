def analyze_logs(lines):
    valid_pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) ([^ ]+) (\d+)$'
    
    by_level = Counter()
    endpoints = []
    errors = 0
    valid_count = 0
    
    for line in lines:
        match = re.match(valid_pattern, line)
        if match:
            _, level, endpoint, status_code = match.groups()
            
            # Count levels
            by_level[level] += 1
            
            # Collect endpoints
            endpoints.append(endpoint)
            
            # Increment error count if status code starts with 5xx
            if status_code.startswith('5'):
                errors += 1
                
            valid_count += 1
    
    # Find most common endpoint 
    endpoint_counter = Counter(endpoints)
    most_common_endpoint = min((endpoint for endpoint, freq in endpoint_counter.items() if freq == max(endpoint_counter.values())), default=None)
        
    return {
        "total": valid_count,
        "by_level": dict(by_level),
        "errors": errors,
        "most_common_endpoint": most_common_endpoint
    }
