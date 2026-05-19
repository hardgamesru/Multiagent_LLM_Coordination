def analyze_logs(lines):
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (\S+) (\d+)$'
    valid_entries = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            valid_entries.append(match.groups())
            
    levels = [entry[1] for entry in valid_entries]
    count_by_level = Counter(levels)
    
    total_valid = len(valid_entries)
    
    num_errors = sum(1 for lvl in levels if lvl == 'ERROR')
    
    endpoints = [entry[2] for entry in valid_entries]
    endpoint_counter = Counter(endpoints)
    most_common_endpoint = min(endpoint_counter.items(), key=lambda x: (-x[1], x[0]), default=(None,))[0]
    
    return {
        "total": total_valid,
        "by_level": dict(count_by_level),
        "errors": num_errors,
        "most_common_endpoint": most_common_endpoint
    }
