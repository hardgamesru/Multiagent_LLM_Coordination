def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    seen = set()
    for c in customers:
        cid = c['id']
        if cid in seen:
            raise ValueError('duplicate customer id')
        seen.add(cid)
    totals = {cid: 0 for cid in seen}
    for o in orders:
        cust = o['customer']
        amt = o['amount']
        if cust not in seen or amt < 0:
            raise ValueError('invalid order')
        totals[cust] += amt
    return [{'id': cid, 'total': totals[cid]} for cid in [c['id'] for c in customers]]
