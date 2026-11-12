def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    seen = set()
    for c in customers:
        cid = c['id']
        if cid in seen:
            raise ValueError("Duplicate customer id")
        seen.add(cid)

    totals = {cid: 0 for cid in seen}

    for o in orders:
        cust = o['customer']
        amt = o['amount']
        if amt < 0:
            raise ValueError("Negative amount")
        if cust not in totals:
            raise ValueError("Unknown customer in orders")
        totals[cust] += amt

    return [{'id': c['id'], 'total': totals[c['id']]} for c in customers]
