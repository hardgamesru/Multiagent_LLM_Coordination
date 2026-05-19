def analyze_logs(lines):
    valid_entries = []
    for line in lines:
        match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+?) (\d+)$', line)
        if match:
            timestamp, level, endpoint, status_code = match.groups()
            if level in ('INFO', 'WARNING', 'ERROR'):
                valid_entries.append((level, endpoint))
    
    result = {
        'total': len(valid_entries),
        'by_level': Counter(level for level, _ in valid_entries),
        'errors': sum(1 for level, _ in valid_entries if level == 'ERROR')
    }
    
    endpoints_counter = Counter(endpoint for _, endpoint in valid_entries)
    if endpoints_counter:
        sorted_endpoints = sorted(endpoints_counter.items(), key=lambda x: (-x[1], x[0]))
        result['most_common_endpoint'] = sorted_endpoints[0][0]
    else:
        result['most_common_endpoint'] = None
        
    return result
