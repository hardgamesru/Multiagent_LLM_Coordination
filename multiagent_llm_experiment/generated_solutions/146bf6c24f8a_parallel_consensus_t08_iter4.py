def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    result = {}
    for item in items:
        category = item.get('category', 'unknown')
        if category not in result:
            result[category] = []
        result[category].append(item)
    return result
