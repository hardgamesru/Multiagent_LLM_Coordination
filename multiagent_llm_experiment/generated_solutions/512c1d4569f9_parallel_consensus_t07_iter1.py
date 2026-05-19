from collections import Counter

def analyze_logs(lines):
    def parse_line(line):
        parts = line.split()
        try:
            # Validate date-time part, ensure it has exactly two spaces separating components
            if len(parts) != 4:
                return False
            
            timestamp, level, endpoint, status_code = parts
            if level not in ['INFO', 'WARNING', 'ERROR']:
                return False
            
            # Ensure status code is numeric and three digits long
            int(status_code)
            if len(status_code) != 3:
                return False
                
            return True
        
        except Exception:
            return False
    
    valid_lines = [line for line in lines if parse_line(line)]
    levels = []
    endpoints = []
    
    for line in valid_lines:
        _, level, endpoint, _ = line.split()
        levels.append(level)
        endpoints.append(endpoint)
    
    counter_levels = Counter(levels)
    counter_endpoints = Counter(endpoints)
    
    result = {
        'total': len(valid_lines),
        'by_level': dict(counter_levels),
        'errors': counter_levels.get('ERROR', 0),
        'most_common_endpoint': max(sorted(counter_endpoints.keys()), key=lambda x: (counter_endpoints[x], x)) if endpoints else None,
    }
    
    return result
