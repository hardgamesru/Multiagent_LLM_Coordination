import re
from collections import Counter

def analyze_logs(lines: list[str]) -> dict:
    total = 0
    by_level = Counter()
    errors = 0
    endpoint_counter = Counter()
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (\S+) (\d{3})$')
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            errors += 1
            continue
        
        total += 1
        _, level, endpoint, status = match.groups()
        by_level[level] += 1
        endpoint_counter[endpoint] += 1
            
    most_common_endpoint = None
    if endpoint_counter:
        max_count = max(endpoint_counter.values())
        candidates = [ep for ep, cnt in endpoint_counter.items() if cnt == max_count]
        most_common_endpoint = min(candidates)
        
    return {
        'total': total,
        'by_level': dict(by_level),
        'errors': errors,
        'most_common_endpoint': most_common_endpoint
    }
