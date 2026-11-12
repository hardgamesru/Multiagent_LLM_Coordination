from collections import defaultdict

def merge_records(records: list[dict]) -> list[dict]:
    result = defaultdict(dict)
    
    for rec in records:
        rid = rec['id']
        # Обновляем поля текущего рекорда, перезаписывая предыдущие значения, если они есть
        result[rid].update((k, v) for k, v in rec.items() if k != 'id')
    
    # Преобразуем обратно в список словарей, сохраняя порядок первого появления ID
    return [{**r, 'id': k} for k, r in sorted(result.items(), key=lambda x: x[0])]
