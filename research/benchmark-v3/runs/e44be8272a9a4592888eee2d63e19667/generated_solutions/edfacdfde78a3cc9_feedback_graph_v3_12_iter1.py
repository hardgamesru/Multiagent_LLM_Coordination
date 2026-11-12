def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    customer_set = set(d['id'] for d in customers)
    
    result = {}
    for order in orders:
        if order['customer'] not in customer_set:
            raise ValueError(f"Unknown customer '{order['customer']}'")
        
        if order['amount'] < 0:
            raise ValueError("Negative amount is not allowed")
            
        result[order['customer']] = result.get(order['customer'], 0) + order['amount']
    
    # Include zero-sum customers
    return [
        {'id': c['id'], 'total': result.get(c['id'], 0)}
        for c in customers
    ]
