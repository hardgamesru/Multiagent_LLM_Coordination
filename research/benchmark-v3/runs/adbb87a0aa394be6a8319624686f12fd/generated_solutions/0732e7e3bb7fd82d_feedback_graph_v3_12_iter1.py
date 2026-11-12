def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    seen = set()
    for c in customers:
        cid = c['id']
        if cid in seen:
            raise ValueError("duplicate customer id")
        seen.add(cid)

    totals = {c['id']: 0 for c in customers}
    customer_ids = set(totals)

    for o in orders:
        cust = o['customer']
        amt = o['amount']
        if cust not in customer_ids:
            raise ValueError("unknown customer in order")
        if not isinstance(amt, int) or amt < 0:
            raise ValueError("negative amount")
        totals[cust] += amt

    return [{'id': c['id'], 'total': totals[c['id']]} for c in customers]
