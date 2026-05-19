from collections import Counter

def analyze_logs(lines):
    by_level = {}
    endpoints = []
    errors = 0
    valid_count = 0

    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
        
        timestamp, level, endpoint, status_code = parts
    
        # Validate log structure
        try:
            int(status_code)
        except ValueError:
            continue
            
        if level not in ["INFO", "WARNING", "ERROR"]:
            continue
            
        valid_count += 1
        endpoints.append(endpoint)
        by_level[level] = by_level.get(level, 0) + 1
        
        if level == "ERROR":
            errors += 1

    counter = Counter(endpoints)
    most_common_endpoint = min(counter.items(), key=lambda x: (-x[1], x[0]), default=(None,))[0]

    return {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
