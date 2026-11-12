from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = []
    seen_ids = set()
    
    # Группируем записи по id
    grouped = defaultdict(list)
    for rec in records:
        grouped[rec['id']].append(rec)
    
    # Объединяем поля, сохраняя последний вхождение каждого поля
    for group in grouped.values():
        merged = {}
        for rec in reversed(group):
            merged.update({k: v for k, v in rec.items() if k != 'id'})
        
        # Добавляем первую запись с этим id в результат
        if group[-1]['id'] not in seen_ids:
            result.append({'id': group[-1]['id'], **merged})
            seen_ids.add(group[-1]['id'])
            
    return result
