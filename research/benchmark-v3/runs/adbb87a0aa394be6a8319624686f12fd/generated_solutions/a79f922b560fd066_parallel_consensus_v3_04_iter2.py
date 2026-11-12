from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = defaultdict(dict)
    
    for rec in records:
        rid = rec['id']
        # Update fields from current record, overwriting previous ones if present
        result[rid].update({k: v for k, v in rec.items() if k != 'id'})
    
    # Convert back to list of dictionaries preserving original appearance order
    return [{**r, 'id': k} for k, r in sorted(result.items(), key=lambda x: x[0])]
