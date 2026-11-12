def merge_records(records: list[dict]) -> list[dict]:
    merged = {}
    order = []
    for rec in records:
        rid = rec['id']
        if rid not in merged:
            merged[rid] = {'id': rid}
            order.append(rid)
        merged[rid].update(rec)
    return [merged[rid] for rid in order]
