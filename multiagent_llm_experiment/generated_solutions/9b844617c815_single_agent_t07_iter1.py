from collections import Counter

def analyze_logs(lines):
    def is_valid(line):
        parts = line.split()
        return len(parts) == 4 and parts[2].startswith('/') and parts[3].isdigit() and len(parts[3]) == 3 
    
    valid_lines = [line for line in lines if is_valid(line)]
    by_level = Counter([line.split()[1] for line in valid_lines])
    endpoints = Counter([line.split()[2] for line in valid_lines])
    errors = sum(1 for line in valid_lines if "ERROR" in line)
    most_common_endpoint = min(endpoints, key=lambda x: (-endpoints[x], x)) if endpoints else None
    
    result = {
        'total': len(valid_lines),
        'by_level': dict(by_level),
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
    return result
