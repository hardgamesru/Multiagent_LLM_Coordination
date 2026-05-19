def group_by_category(items: List[Dict]) -> Dict[str, List[Dict]]:
    result = {}
    for item in items:
        category = item.get('category', 'unknown')
        result.setdefault(category, []).append(item)
    return result
