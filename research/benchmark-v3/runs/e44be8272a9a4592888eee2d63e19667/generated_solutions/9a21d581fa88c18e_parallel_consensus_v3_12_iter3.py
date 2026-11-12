def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    if len({c['id'] for c in customers}) != len(customers):
        raise ValueError("Duplicate customer IDs")
    
    result = {}
    
    for order in orders:
        customer_id = order.get('customer')
        
        # Check for unknown customer or negative amount
        if customer_id is None or order.get('amount') is None or \
           customer_id not in (c['id'] for c in customers) or \
           order['amount'] < 0:
            raise ValueError("Invalid order data")
            
        # Aggregate orders by customer ID
        result.setdefault(customer_id, 0)
        result[customer_id] += order['amount']
    
    # Add missing customers with zero balance
    return [
        {'id': c['id'], 'total': result.get(c['id'], 0)}
        for c in customers
    ]
