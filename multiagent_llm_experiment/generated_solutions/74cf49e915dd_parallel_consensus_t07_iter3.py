def analyze_logs(lines):
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+?) (\d+)$'
    
    valid_count = 0
    levels = Counter()
    statuses = []
    endpoints = []
    
    for line in lines:
        match = re.match(pattern, line)
        if match:
            timestamp, level, endpoint, status_code = match.groups()
            
            # Update counters
            valid_count += 1
            levels[level] += 1
            statuses.append(int(status_code))
            endpoints.append(endpoint)
    
    # Calculate error count based on HTTP status codes >= 400
    errors = sum(1 for s in statuses if s >= 400)
    
    # Find most common endpoint using Counter.most_common() which sorts first by frequency then lexicographically
    endpoint_counter = Counter(endpoints)
    most_common_endpoint = endpoint_counter.most_common(1)[0][0] if endpoint_counter else None
    
    result = {
        "total": valid_count,
        "by_level": dict(levels),
        "errors": errors,
        "most_common_endpoint": most_common_endpoint
    }
    
    return result
