def group_by_category(items):
    result = defaultdict(list)
    
    for item in items:
        category = item.get('category', 'unknown')
        result[category].append(item)
        
    return dict(result)
