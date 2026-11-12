def analyze_logs(lines: list[str]) -> dict:
    import re
    valid_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|WARNING|ERROR) (/[^ ]+) (\d{3})$'
    by_level = {'INFO':0,'WARNING':0,'ERROR':0}
    errors = 0
    most_common_endpoint = None
    max_count = 0
    total = 0
    
    for line in lines:
        match = re.match(valid_pattern,line)
        if match:
            level,status_code,endpoint = match.groups()
            by_level[level] += 1
            total += 1
            
            if by_level[level] > max_count:
                max_count = by_level[level]
                most_common_endpoint = endpoint
        else:
            errors += 1
    
    if total == 0:
        most_common_endpoint = None
    elif max_count > 1:
        endpoints = [endpoint for endpoint,count in by_level.items() if count==max_count]
        most_common_endpoint = min(endpoints)
    
    return {'total':total,'by_level':by_level,'errors':errors,'most_common_endpoint':most_common_endpoint}
