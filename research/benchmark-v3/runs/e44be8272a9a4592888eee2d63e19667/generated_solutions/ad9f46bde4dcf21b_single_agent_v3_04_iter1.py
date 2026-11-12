from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = defaultdict(list)
    
    for rec in records:
        rid = rec['id']
        # Collect fields from each occurrence of the same id
        result[rid].append({k: v for k, v in rec.items() if k != 'id'})
    
    # Flatten and combine fields using last seen value
    merged = []
    for r in sorted(result.keys()):
        fields = {}
        for f in result[r]:
            fields.update(f)
        merged.append({'id': r, **fields})
    
    return merged
