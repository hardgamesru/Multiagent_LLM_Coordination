def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    customer_set = set(d['id'] for d in customers)
    
    result = {}
    for order in orders:
        if order['customer'] not in customer_set:
            raise ValueError(f"Unknown customer: {order['customer']}")
        
        try:
            amount = int(order['amount'])
            if amount < 0:
                raise ValueError("Negative amount")
            
            result[order['customer']] = result.get(order['customer'], 0) + amount
        except KeyError:
            raise ValueError("Order must contain 'customer' and 'amount'")
    
    # Add missing customers with zero balance
    return [
        {'id': c['id'], 'total': result.get(c['id'], 0)}
        for c in customers
    ]
