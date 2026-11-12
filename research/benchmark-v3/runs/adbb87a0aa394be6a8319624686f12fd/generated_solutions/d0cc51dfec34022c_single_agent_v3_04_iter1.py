from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = defaultdict(list)
    
    for rec in records:
        rid = rec['id']
        # Collect fields from each occurrence of the same ID
        result[rid].extend((k, v) for k, v in rec.items())
    
    # Reconstruct merged dictionaries preserving original order of first appearance
    return [
        dict(fields)  
        for _, fields in sorted(result.items())  
    ]
