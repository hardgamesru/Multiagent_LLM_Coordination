from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    if not records:
        return []
    
    # Group records by id while preserving original order
    grouped = defaultdict(list)
    for rec in records:
        grouped[rec['id']].append(rec)
    
    result = []
    seen_ids = set()
    
    # Process each group of records with same id
    for recs in grouped.values():
        merged_rec = {}
        
        # Iterate through records in encounter order
        for rec in recs:
            # Update fields from latest record, skipping None values
            for key, value in rec.items():
                if value is not None:
                    merged_rec[key] = value
        
        # Add to output only if not already processed
        if recs[0]['id'] not in seen_ids:
            result.append(merged_rec)
            seen_ids.add(recs[0]['id'])
            
    return result
