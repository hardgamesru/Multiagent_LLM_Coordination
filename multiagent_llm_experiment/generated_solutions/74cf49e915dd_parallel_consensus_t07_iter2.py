def analyze_logs(lines):
    result = {
        "total": 0,
        "by_level": {"INFO": 0, "WARNING": 0, "ERROR": 0},
        "errors": 0,
        "most_common_endpoint": None
    }
    
    endpoint_freqs = defaultdict(int)
    
    # Regular expression pattern for validating log entry format
    log_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|WARNING|ERROR) ([^ ]+) (\d+)$"
    
    for line in lines:
        match = re.match(log_pattern, line.strip())
        
        if match:
            _, level, endpoint, status_code = match.groups()
            
            # Increment total valid log count
            result["total"] += 1
            
            # Update log levels count
            result["by_level"][level] += 1
            
            # Track endpoint occurrences
            endpoint_freqs[endpoint] += 1
            
            # Check if this is an error-level log based on HTTP status code
            if int(status_code) >= 400:
                result["errors"] += 1
                
    # Find the most common endpoint
    if len(endpoint_freqs) > 0:
        max_freq = max(endpoint_freqs.values())
        candidates = [ep for ep, freq in endpoint_freqs.items() if freq == max_freq]
        result['most_common_endpoint'] = min(candidates)
        
    return result
