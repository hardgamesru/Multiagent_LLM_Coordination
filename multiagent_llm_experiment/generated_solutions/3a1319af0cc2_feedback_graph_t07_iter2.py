def analyze_logs(lines):
    by_level = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errors = 0
    endpoints = []
    
    for line in lines:
        parts = line.split()
        
        if len(parts) != 5:
            continue
            
        timestamp, level, endpoint, status = parts[:4]
        
        # Validate fields
        if level not in ("INFO", "WARNING", "ERROR"):
            continue
            
        by_level[level] += 1
        endpoints.append(endpoint)
        
        if level == "ERROR":
            errors += 1
                
    total_valid = sum(by_level.values())
    
    if endpoints:
        endpoints_counter = Counter(endpoints)
        max_freq = max(endpoints_counter.values())
        common_endpoints = [ep for ep, freq in endpoints_counter.items() if freq == max_freq]
        most_common_endpoint = min(common_endpoints)
    else:
        most_common_endpoint = None
    
    return {
        "total": total_valid,
        "by_level": by_level,
        "errors": errors,
        "most_common_endpoint": most_common_endpoint
    }
