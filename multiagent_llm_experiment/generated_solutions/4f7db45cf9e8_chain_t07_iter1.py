from collections import Counter

def analyze_logs(lines):
    valid_count = 0
    counts_by_level = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errors = 0
    endpoints = []
    
    for line in lines:
        parts = line.split()
        
        # Check basic structure validity
        if len(parts) != 4:
            continue
            
        timestamp, level, endpoint, status_code = parts
        
        # Validate level and status code
        if level not in ("INFO", "WARNING", "ERROR") or not status_code.isdigit() or len(status_code) != 3:
            continue
        
        valid_count += 1
        counts_by_level[level] += 1
        
        if level == "ERROR":
            errors += 1
            
        endpoints.append(endpoint)
    
    # Find most common endpoint
    counter = Counter(endpoints)
    if counter:
        most_common_endpoint = min(counter.items(), key=lambda x: (-x[1], x[0]))[0]
    else:
        most_common_endpoint = None
    
    result = {
        'total': valid_count,
        'by_level': counts_by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
    
    return result
