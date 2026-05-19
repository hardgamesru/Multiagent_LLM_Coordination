from collections import Counter

def analyze_logs(lines):
    valid_count = 0
    by_level = {}
    errors = 0
    endpoints = []
    
    for line in lines:
        parts = line.split()
        
        if len(parts) != 4:
            continue
            
        timestamp, level, endpoint, status_code = parts
        
        # Check if all components are present and valid
        if (
            len(timestamp) == 19 
            and level in {"INFO", "WARNING", "ERROR"} 
            and endpoint.startswith('/') 
            and status_code.isdigit() 
            and len(status_code) == 3
        ):
            valid_count += 1
            by_level[level] = by_level.get(level, 0) + 1
            
            if level == "ERROR":
                errors += 1
                
            endpoints.append(endpoint)
    
    result = {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': None
    }
    
    if endpoints:
        counter = Counter(endpoints)
        max_freq = max(counter.values())
        common_endpoints = [ep for ep, freq in counter.items() if freq == max_freq]
        result['most_common_endpoint'] = min(common_endpoints)
    
    return result
