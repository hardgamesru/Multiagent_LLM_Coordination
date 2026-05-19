def group_by_category(items: List[Dict]) -> Dict[str, List[Dict]]:
    result = {}
    
    for item in items:
        category = item.get('category', 'unknown')
        
        if category not in result:
            result[category] = []
            
        result[category].append(item)
    
    return result
