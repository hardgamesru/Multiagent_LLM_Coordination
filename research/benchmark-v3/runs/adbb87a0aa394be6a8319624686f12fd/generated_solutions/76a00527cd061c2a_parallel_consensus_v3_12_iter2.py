def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    seen = set()
    for c in customers:
        cid = c.get('id')
        if not isinstance(cid, str) or cid in seen:
            raise ValueError
        seen.add(cid)

    totals = {cid: 0 for cid in seen}
    for o in orders:
        cust = o.get('customer')
        amt = o.get('amount')
        if not isinstance(cust, str) or not isinstance(amt, int) or amt < 0:
            raise ValueError
        if cust not in totals:
            raise ValueError
        totals[cust] += amt

    return [{'id': cid, 'total': totals[cid]} for cid in [c['id'] for c in customers]]
