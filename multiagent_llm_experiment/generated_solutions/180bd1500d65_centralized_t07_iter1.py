from collections import Counter

def analyze_logs(lines):
    valid_count = 0
    levels = Counter()
    endpoints = Counter()
    errors = 0

    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
            
        _, _, level, rest = parts
        endpoint_status = rest.rsplit(' ', 1)
        
        if len(endpoint_status) != 2:
            continue
            
        endpoint, status_code = endpoint_status
        
        if not (level in {"INFO", "WARNING", "ERROR"} 
                and status_code.isdigit() 
                and len(status_code) == 3):
            continue
            
        valid_count += 1
        levels[level] += 1
        endpoints[endpoint] += 1
        
        if level == "ERROR":
            errors += 1

    sorted_endpoints = sorted(endpoints.items(), key=lambda x: (-x[1], x[0]))
    most_common_endpoint = sorted_endpoints[0][0] if sorted_endpoints else None

    return {
        'total': valid_count,
        'by_level': dict(levels),
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
