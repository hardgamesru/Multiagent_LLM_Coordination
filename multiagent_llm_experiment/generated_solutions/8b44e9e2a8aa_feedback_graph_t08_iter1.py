def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    result = {}
    for item in items:
        category = item.get('category', 'unknown')
        result.setdefault(category, []).append(item)
    return result
