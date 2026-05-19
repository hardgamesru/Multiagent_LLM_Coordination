def group_by_category(items):
    result = {}
    for item in items:
        category = item.get('category', '')
        if not category:
            category = 'unknown'
        result.setdefault(category, []).append(item)
    return result
