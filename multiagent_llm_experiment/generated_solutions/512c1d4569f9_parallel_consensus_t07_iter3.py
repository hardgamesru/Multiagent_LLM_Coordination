from collections import Counter

def analyze_logs(lines):
    def parse_line(line):
        parts = line.split()
        try:
            timestamp, level, endpoint, status_code = parts[:4]
            # Validate date-time, level, endpoint, and status code format
            assert len(timestamp) == 19 and '-' in timestamp and ':' in timestamp
            assert level in ['INFO', 'WARNING', 'ERROR']
            assert '/' in endpoint
            int(status_code)
            return True, (level, endpoint)
        except Exception:
            return False, None
    
    valid_entries = []
    levels_counter = Counter()
    endpoints_counter = Counter()
    num_errors = 0
    
    for line in lines:
        is_valid, data = parse_line(line)
        if is_valid:
            level, endpoint = data
            valid_entries.append(data)
            levels_counter[level] += 1
            endpoints_counter[endpoint] += 1
            if level == 'ERROR':
                num_errors += 1
                
    total_valid = len(valid_entries)
    most_common_endpoint = min(endpoints_counter.items(), key=lambda x: (-x[1], x[0]), default=(None,))[0]
    
    result = {
        'total': total_valid,
        'by_level': dict(levels_counter),
        'errors': num_errors,
        'most_common_endpoint': most_common_endpoint
    }
    return result
