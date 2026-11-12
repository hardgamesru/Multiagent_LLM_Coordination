def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    seen = set()
    for c in customers:
        cid = c['id']
        if cid in seen:
            raise ValueError("Duplicate customer id")
        seen.add(cid)

    totals = {c['id']: 0 for c in customers}
    for o in orders:
        cust = o['customer']
        amt = o['amount']
        if amt < 0:
            raise ValueError("Negative amount")
        if cust not in totals:
            raise ValueError("Unknown customer in order")
        totals[cust] += amt

    return [{'id': c['id'], 'total': totals[c['id']]} for c in customers]
