def analyze_logs(lines):
    valid_count = 0
    by_level = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    endpoints = []
    
    for line in lines:
        parts = line.split()
        
        if len(parts) != 4:
            continue
            
        timestamp, level, endpoint, status = parts
        
        # Validate log entry format
        if (
            level not in ["INFO", "WARNING", "ERROR"] 
            or not timestamp.replace("-", "").replace(":", "").isdigit() 
            or not status.isdigit()
        ):
            continue
            
        valid_count += 1
        by_level[level] += 1
        endpoints.append(endpoint)
    
    errors = by_level["ERROR"]
    endpoint_counter = Counter(endpoints)
    
    most_common_endpoint = min(
        endpoint_counter.items(), key=lambda x: (-x[1], x[0]), default=(None,)
    )[0]
    
    return {
        "total": valid_count,
        "by_level": by_level,
        "errors": errors,
        "most_common_endpoint": most_common_endpoint
    }
