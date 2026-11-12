def analyze_logs(lines: list[str]) -> dict:
    levels = {'INFO', 'WARNING', 'ERROR'}
    status_codes = set(str(i).zfill(3) for i in range(100, 600))
    result = {'total': 0, 'by_level': {}, 'errors': 0, 'most_common_endpoint': None}
    
    def parse_line(line):
        try:
            date_time, level, endpoint, status = line.split()
            _, year, month, day = date_time.split('-')
            _, hour, minute, second = date_time.split(':')
            if (level not in levels or 
                status not in status_codes or 
                len(endpoint) == 0 or 
                int(year) < 2000 or 
                int(month) > 12 or 
                int(day) > 31 or 
                int(hour) > 23 or 
                int(minute) > 59 or 
                int(second) > 59):
                raise ValueError
            return level, endpoint, status
        except:
            result['errors'] += 1
            return None, None, None
    
    for line in lines:
        level, endpoint, status = parse_line(line)
        if level is not None:
            result['total'] += 1
            result['by_level'][level] = result['by_level'].get(level, 0) + 1
            if result['most_common_endpoint'] is None or \
               result['most_common_endpoint'].count('/') != endpoint.count('/'):
                result['most_common_endpoint'] = endpoint
            elif result['most_common_endpoint'].split('/')[1:] == endpoint.split('/')[1:]:
                result['most_common_endpoint'] = min(result['most_common_endpoint'], endpoint)
    
    return result
