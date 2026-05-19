def analyze_logs(lines):
    by_level = {}
    endpoints = []
    errors = 0
    
    for line in lines:
        parts = line.split()
        
        if len(parts) != 5:
            continue
            
        date, time, level, endpoint, status = parts
        
        # Check valid log levels
        if level not in ('INFO', 'WARNING', 'ERROR'):
            continue
            
        endpoints.append(endpoint)
        
        by_level[level] = by_level.get(level, 0) + 1
        
        if level == 'ERROR':
            errors += 1
                
    total = sum(by_level.values())
    
    # Find the most common endpoint 
    counter = Counter(endpoints)
    if counter:
        most_common_endpoint = sorted(counter.items(), key=lambda x: (-x[1], x[0]))[0][0]
    else:
        most_common_endpoint = None
        
    return {
        'total': total,
        'by_level': by_level,
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
