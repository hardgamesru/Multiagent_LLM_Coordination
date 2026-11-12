from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    if not records:
        return []
    
    result = defaultdict(dict)
    
    for rec in records:
        rid = rec['id']
        # Update existing fields or add new ones from current record
        result[rid].update({k: v for k, v in rec.items() if k != 'id'})
    
    # Convert back to list of dictionaries preserving original first appearance order
    return [{**r, **{'id': k}} for k, r in sorted(result.items())]
