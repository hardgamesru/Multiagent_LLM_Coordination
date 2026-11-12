def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for item in items:
        category = item.get('category', 'unknown')
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    return grouped
