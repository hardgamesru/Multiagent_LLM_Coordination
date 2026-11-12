def analyze_logs(lines: list[str]) -> dict:
    import re
    from collections import Counter
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ([A-Z]+) (/.*) (\d{3})$'
    by_level = {'INFO':0,'WARNING':0,'ERROR':0}
    errors = 0
    endpoints = []
    for line in lines:
        match = re.match(pattern,line)
        if match:
            level,status,endpoint = match.groups()
            by_level[level] += 1
            endpoints.append(endpoint)
        else:
            errors += 1
    most_common = Counter(endpoints).most_common()
    max_freq = most_common[0][1]
    most_common_endpoints = [endpoint for endpoint,freq in most_common if freq==max_freq]
    most_common_endpoint = min(most_common_endpoints) if most_common_endpoints else None
    return {'total':len(lines),'by_level':by_level,'errors':errors,'most_common_endpoint':most_common_endpoint}
