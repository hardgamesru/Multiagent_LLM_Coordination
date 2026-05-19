def analyze_logs(lines: list[str]) -> dict:
    import re
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|WARNING|ERROR) (\S+) (\d{3})$")
    by_level = {}
    by_endpoint = {}
    total = 0
    errors = 0
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        level, endpoint, _status = match.groups()
        total += 1
        by_level[level] = by_level.get(level, 0) + 1
        by_endpoint[endpoint] = by_endpoint.get(endpoint, 0) + 1
        if level == "ERROR":
            errors += 1
    most_common_endpoint = None
    if by_endpoint:
        most_common_endpoint = sorted(by_endpoint.items(), key=lambda item: (-item[1], item[0]))[0][0]
    return {
        "total": total,
        "by_level": by_level,
        "errors": errors,
        "most_common_endpoint": most_common_endpoint,
    }
