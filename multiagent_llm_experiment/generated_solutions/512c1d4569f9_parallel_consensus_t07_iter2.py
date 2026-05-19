from collections import Counter

def analyze_logs(lines):
    def parse_line(line):
        parts = line.split()
        try:
            _, timestamp, level, endpoint, status_code = parts[:5]
            # Validate date-time format, level, and status code
            year, month, day = map(int, timestamp.split('-'))
            hour, minute, second = map(int, parts[1].split(':'))
            if len(status_code) != 3 or not status_code.isdigit():
                return False
            return True
        except Exception:
            return False
    
    levels = ['INFO', 'WARNING', 'ERROR']
    valid_entries = []
    endpoints = []
    
    for line in lines:
        if parse_line(line):
            valid_entries.append(line)
            level = line.split()[2]
            endpoint = line.split()[3]
            endpoints.append(endpoint)
            
    result = {
        'total': len(valid_entries),
        'by_level': {level: sum(1 for entry in valid_entries if entry.split()[2] == level) for level in levels},
        'errors': sum(1 for entry in valid_entries if entry.split()[2] == 'ERROR'),
        'most_common_endpoint': None,
    }
    
    counter = Counter(endpoints)
    max_freq = max(counter.values(), default=0)
    most_common_endpoints = [k for k, v in counter.items() if v == max_freq]
    if most_common_endpoints:
        result['most_common_endpoint'] = min(most_common_endpoints)
        
    return result
