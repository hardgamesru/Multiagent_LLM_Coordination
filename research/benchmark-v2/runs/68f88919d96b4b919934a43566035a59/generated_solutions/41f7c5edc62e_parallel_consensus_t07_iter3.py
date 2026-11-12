from collections import defaultdict, Counter
import re

def analyze_logs(lines: list[str]) -> dict:
    valid_count = 0
    level_counts = defaultdict(int)
    error_count = 0
    endpoint_counter = Counter()
    
    line_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (\S+) (\d{3})$')
    
    for line in lines:
        match = line_pattern.match(line)
        if not match:
            continue
        
        _, level, endpoint, status = match.groups()
        
        valid_count += 1
        level_counts[level] += 1
        if level == 'ERROR':
            error_count += 1
        endpoint_counter[endpoint] += 1
        
    most_common_endpoint = None
    if endpoint_counter:
        max_freq = max(endpoint_counter.values())
        candidates = [ep for ep, count in endpoint_counter.items() if count == max_freq]
        most_common_endpoint = min(candidates)
        
    return {
        'total': valid_count,
        'by_level': dict(level_counts),
        'errors': error_count,
        'most_common_endpoint': most_common_endpoint
    }
