from collections import defaultdict

def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    
    for item in items:
        category = item.get('category', 'unknown')
        grouped[category].append(item)
    
    return dict(grouped)
