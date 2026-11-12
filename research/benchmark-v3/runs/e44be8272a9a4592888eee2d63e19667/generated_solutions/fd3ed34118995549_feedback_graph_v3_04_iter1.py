from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = defaultdict(dict)
    
    for rec in records:
        rid = rec['id']
        # Update fields of current record, overwriting previous values if present
        result[rid].update((k, v) for k, v in rec.items() if k != 'id')
    
    # Convert back to list of dictionaries preserving original appearance order
    return [result[r] for r in sorted(result.keys())]
