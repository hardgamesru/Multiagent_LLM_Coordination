from collections import defaultdict, Counter
import re

def analyze_logs(lines: list[str]) -> dict:
    valid_count = 0
    by_level = defaultdict(int)
    endpoint_counter = Counter()
    
    for line in lines:
        parts = line.split()
        if len(parts) != 5:
            continue
        date_part, time_part, level, endpoint, status = parts
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date_part):
            continue
        if not re.fullmatch(r'\d{2}:\d{2}:\d{2}', time_part):
            continue
        if level not in ('INFO', 'WARNING', 'ERROR'):
            continue
        if not re.fullmatch(r'\d{3}', status):
            continue
        
        valid_count += 1
        by_level[level] += 1
        endpoint_counter[endpoint] += 1

    most_common_endpoint = None
    if endpoint_counter:
        max_freq = max(endpoint_counter.values())
        candidates = [ep for ep, cnt in endpoint_counter.items() if cnt == max_freq]
        most_common_endpoint = min(candidates)

    return {
        'total': valid_count,
        'by_level': dict(by_level),
        'errors': by_level.get('ERROR', 0),
        'most_common_endpoint': most_common_endpoint
    }
