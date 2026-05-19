def analyze_logs(lines):
    result = {"total": 0, "by_level": {}, "errors": 0, "most_common_endpoint": None}
    
    endpoints_counter = Counter()
    
    for line in lines:
        parts = line.split()
        
        if len(parts) != 4:
            continue
            
        timestamp, level, endpoint, status = parts
        
        # Check if level is one of expected values
        if level not in ["INFO", "WARNING", "ERROR"]:
            continue
            
        result["total"] += 1
        result["by_level"][level] = result["by_level"].get(level, 0) + 1
        
        if level == "ERROR":
            result["errors"] += 1
            
        endpoints_counter[endpoint] += 1
    
    if endpoints_counter:
        # Get the maximum frequency
        max_freq = max(endpoints_counter.values())
        # Filter by max frequency and get lexicographically smallest endpoint
        common_endpoints = [ep for ep, freq in endpoints_counter.items() if freq == max_freq]
        result["most_common_endpoint"] = min(common_endpoints)
    
    return result
