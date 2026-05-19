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
        # Check validity of log entry
        if (
            level in ["INFO", "WARNING", "ERROR"] 
            and status_code.isdigit() 
            and len(status_code) == 3
        ):
            valid_count += 1
            
            # Update levels count
            by_level[level] = by_level.get(level, 0) + 1
            
            # Count errors separately
            if level == "ERROR":
                errors += 1
                
            # Collect endpoints
            endpoints.append(endpoint)
    
    # Find most common endpoint
    if endpoints:
        counter = Counter(endpoints)
        max_freq = max(counter.values())
        candidates = [ep for ep, freq in counter.items() if freq == max_freq]
        most_common_endpoint = min(candidates)  # Lexicographically smallest
    else:
        most_common_endpoint = None
    
    return {
        'total': valid_count,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
