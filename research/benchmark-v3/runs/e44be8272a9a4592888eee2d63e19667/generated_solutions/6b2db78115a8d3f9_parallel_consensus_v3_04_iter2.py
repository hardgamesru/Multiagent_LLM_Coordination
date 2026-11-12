from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    if not records:
        return []
    
    result = defaultdict(dict)
    seen_ids = set()
    
    for rec in records:
        rid = rec['id']
        
        # Skip duplicates based on first appearance order
        if rid not in seen_ids:
            seen_ids.add(rid)
            
            # Update fields from current record, overwriting previous ones
            for key, value in rec.items():
                result[rid][key] = value
                
    # Convert back to sorted list of dictionaries
    return [{'id': k, **v} for k, v in sorted(result.items())]
