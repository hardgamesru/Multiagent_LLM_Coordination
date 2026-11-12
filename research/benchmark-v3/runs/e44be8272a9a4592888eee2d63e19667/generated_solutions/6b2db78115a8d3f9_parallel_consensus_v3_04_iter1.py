from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = defaultdict(dict)
    
    for rec in records:
        rid = rec['id']
        # Update fields of current record, keeping last non-None value
        for k, v in rec.items():
            if k != 'id':
                result[rid][k] = v or result[rid].get(k)
    
    # Return sorted by first appearance of IDs
    return [r for _, r in sorted(result.items(), key=lambda x: x[0])]
